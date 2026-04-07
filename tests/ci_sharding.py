from __future__ import annotations

import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

CI_TOTAL_SHARDS = 12

# Observed GitHub Actions timings on 2026-04-07 showed that these files are the
# real bottlenecks, not just the largest by collected test count. Split them
# inside the file and bias their weight upward so the planner isolates them.
CI_HOT_TEST_FILE_SPLITS = {
    "test_runtime_cli.py": 4,
    "test_cli_integration.py": 2,
    "test_update_workflow.py": 2,
    "core/test_cli.py": 2,
    "core/test_contract_validation.py": 2,
}

CI_HOT_TEST_FILE_WEIGHT_MULTIPLIERS = {
    "test_runtime_cli.py": 6.0,
    "test_cli_integration.py": 3.0,
    "test_update_workflow.py": 2.0,
    "core/test_cli.py": 1.5,
    "core/test_contract_validation.py": 1.4,
    "hooks/test_runtime_detect.py": 1.5,
    "hooks/test_statusline.py": 1.5,
}


@dataclass(frozen=True)
class CIShardSpec:
    slug: str
    shard_index: int
    shard_total: int


@dataclass(frozen=True)
class CIWorkUnit:
    label: str
    targets: tuple[str, ...]
    weight: float


def ci_shard_specs() -> tuple[CIShardSpec, ...]:
    return tuple(
        CIShardSpec(
            slug=f"shard-{shard_index}",
            shard_index=shard_index,
            shard_total=CI_TOTAL_SHARDS,
        )
        for shard_index in range(1, CI_TOTAL_SHARDS + 1)
    )


def all_test_relpaths(*, tests_root: Path) -> tuple[str, ...]:
    return tuple(path.relative_to(tests_root).as_posix() for path in sorted(tests_root.rglob("test_*.py")))


def collected_test_inventory(*, repo_root: Path | None = None) -> dict[str, tuple[str, ...]]:
    root = Path.cwd() if repo_root is None else repo_root
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "--collect-only",
            "-q",
            "-n",
            "0",
        ],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )

    inventory: dict[str, list[str]] = {}
    for line in proc.stdout.splitlines():
        if "::" not in line:
            continue
        path_text = line.split("::", 1)[0]
        if path_text.startswith("tests/"):
            path_text = path_text[len("tests/") :]
        inventory.setdefault(path_text, []).append(line)
    return {rel_path: tuple(nodeids) for rel_path, nodeids in sorted(inventory.items())}


def collected_test_counts_by_file(*, repo_root: Path | None = None) -> dict[str, int]:
    return {
        rel_path: len(nodeids)
        for rel_path, nodeids in collected_test_inventory(repo_root=repo_root).items()
    }


def _split_nodeids_round_robin(nodeids: tuple[str, ...], *, parts: int) -> tuple[tuple[str, ...], ...]:
    if parts < 1:
        raise ValueError("parts must be positive")
    buckets: list[list[str]] = [[] for _ in range(parts)]
    for index, nodeid in enumerate(nodeids):
        buckets[index % parts].append(nodeid)
    return tuple(tuple(bucket) for bucket in buckets if bucket)


def _file_weight(rel_path: str, *, test_count: int) -> float:
    return test_count * CI_HOT_TEST_FILE_WEIGHT_MULTIPLIERS.get(rel_path, 1.0)


def build_ci_work_units(
    inventory: Mapping[str, tuple[str, ...]],
) -> tuple[CIWorkUnit, ...]:
    work_units: list[CIWorkUnit] = []

    for rel_path, nodeids in inventory.items():
        split_parts = CI_HOT_TEST_FILE_SPLITS.get(rel_path, 1)
        split_groups = _split_nodeids_round_robin(nodeids, parts=split_parts)
        total_weight = _file_weight(rel_path, test_count=len(nodeids))
        scale = total_weight / len(nodeids)

        if len(split_groups) == 1:
            work_units.append(
                CIWorkUnit(
                    label=rel_path,
                    targets=(f"tests/{rel_path}",),
                    weight=total_weight,
                )
            )
            continue

        for group_index, group in enumerate(split_groups, start=1):
            work_units.append(
                CIWorkUnit(
                    label=f"{rel_path} [{group_index}/{len(split_groups)}]",
                    targets=group,
                    weight=len(group) * scale,
                )
            )

    return tuple(sorted(work_units, key=lambda unit: (-unit.weight, unit.label)))


def plan_ci_shards_from_work_units(
    work_units: tuple[CIWorkUnit, ...],
    *,
    shard_total: int = CI_TOTAL_SHARDS,
) -> tuple[tuple[str, ...], ...]:
    if shard_total < 1:
        raise ValueError("shard_total must be positive")

    shard_targets: list[list[str]] = [[] for _ in range(shard_total)]
    shard_weights = [0.0] * shard_total

    for unit in work_units:
        shard_index = min(
            range(shard_total),
            key=lambda index: (shard_weights[index], len(shard_targets[index]), index),
        )
        shard_targets[shard_index].extend(unit.targets)
        shard_weights[shard_index] += unit.weight

    return tuple(tuple(targets) for targets in shard_targets)


def plan_ci_shards(*, repo_root: Path | None = None) -> tuple[tuple[str, ...], ...]:
    inventory = collected_test_inventory(repo_root=repo_root)
    work_units = build_ci_work_units(inventory)
    return plan_ci_shards_from_work_units(work_units)


def expand_ci_targets_to_nodeids(
    targets: tuple[str, ...],
    *,
    inventory: Mapping[str, tuple[str, ...]],
) -> tuple[str, ...]:
    expanded: list[str] = []
    for target in targets:
        if "::" in target:
            expanded.append(target)
            continue
        rel_path = target[len("tests/") :] if target.startswith("tests/") else target
        expanded.extend(inventory[rel_path])
    return tuple(expanded)


def select_ci_shard_targets(
    *,
    shard_index: int,
    shard_total: int,
    repo_root: Path | None = None,
) -> tuple[str, ...]:
    if shard_total != CI_TOTAL_SHARDS:
        raise ValueError(f"shard_total must equal {CI_TOTAL_SHARDS}")
    if shard_index < 1 or shard_index > shard_total:
        raise ValueError("shard_index must be within shard_total")
    planned_shards = plan_ci_shards(repo_root=repo_root)
    return planned_shards[shard_index - 1]


def write_ci_shard_targets_file(
    *,
    target_file: Path,
    shard_index: int,
    shard_total: int,
    repo_root: Path | None = None,
) -> tuple[str, ...]:
    targets = select_ci_shard_targets(
        shard_index=shard_index,
        shard_total=shard_total,
        repo_root=repo_root,
    )
    target_file.write_text("\n".join(targets) + "\n", encoding="utf-8")
    return targets
