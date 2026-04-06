from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import yaml

from tests.conftest import (
    _FAST_SUITE_ENV_VAR,
    FAST_SUITE_EXCLUDES,
    _explicit_collection_requested,
    _full_suite_requested,
    full_suite_ignore_args,
)


def _read(relpath: str) -> str:
    return (Path(__file__).resolve().parent / relpath).read_text(encoding="utf-8")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _workflow_data() -> dict[str, object]:
    return yaml.safe_load((_repo_root() / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8"))


def _workflow_job_steps(workflow: dict[str, object], job_name: str) -> list[dict[str, object]]:
    jobs = workflow["jobs"]
    assert isinstance(jobs, dict)
    job = jobs[job_name]
    assert isinstance(job, dict)
    steps = job["steps"]
    assert isinstance(steps, list)
    assert all(isinstance(step, dict) for step in steps)
    return steps


def test_fast_suite_policy_is_centralized_in_root_conftest() -> None:
    root_conftest = _read("conftest.py")
    core_conftest = _read("core/conftest.py")

    assert "FAST_SUITE_EXCLUDES" in root_conftest
    assert "--full-suite" in root_conftest
    assert _FAST_SUITE_ENV_VAR in root_conftest
    assert "collect_ignore" not in core_conftest


def test_full_suite_toggle_accepts_cli_or_env() -> None:
    assert _full_suite_requested(cli_flag=True, env_value=None) is True
    assert _full_suite_requested(cli_flag=False, env_value="1") is True
    assert _full_suite_requested(cli_flag=False, env_value="true") is True
    assert _full_suite_requested(cli_flag=False, env_value="yes") is True
    assert _full_suite_requested(cli_flag=False, env_value=None) is False
    assert _full_suite_requested(cli_flag=False, env_value="0") is False


def test_fast_suite_policy_keeps_heavyweight_skips_explicit() -> None:
    expected = {
        "test_bootstrap_installer.py",
        "test_install_lifecycle.py",
        "test_runtime_cli.py",
        "hooks/test_notify.py",
        "mcp/test_verification_contract_server_regressions.py",
        "core/test_cli.py",
        "core/test_state.py",
    }

    assert expected <= FAST_SUITE_EXCLUDES


def test_fast_suite_policy_keeps_boundary_regressions_in_default_path() -> None:
    required = {
        "core/test_contract_validation_smoke.py",
        "core/test_executor_prompt_contract_visibility.py",
        "core/test_frontmatter_smoke.py",
        "core/test_plan_contract_prompt_visibility_regressions.py",
        "test_project_contract_boundary_regressions.py",
        "test_runtime_abstraction_boundaries.py",
        "core/test_contract_schema_prompt_parity.py",
        "core/test_verification_contract_evidence.py",
        "mcp/test_tool_contract_visibility.py",
        "core/test_verifier_prompt_contract_visibility.py",
        "core/test_verification_surface_alignment_regressions.py",
    }

    assert required.isdisjoint(FAST_SUITE_EXCLUDES)


def test_ci_and_test_readme_document_explicit_fast_and_full_suite_commands() -> None:
    repo_root = _repo_root()
    workflow = _workflow_data()
    tests_readme = (repo_root / "tests" / "README.md").read_text(encoding="utf-8")
    pytest_steps = _workflow_job_steps(workflow, "pytest")
    step_names = [str(step.get("name", "")) for step in pytest_steps]
    run_steps = {str(step.get("name", "")): str(step.get("run", "")) for step in pytest_steps if "run" in step}

    assert "Set up Node.js" in step_names
    assert step_names.index("Set up Node.js") < step_names.index("Install dependencies")
    assert run_steps["Run fast test suite"] == "uv run pytest tests/ -q -n auto --dist=loadscope"
    assert "from tests.conftest import full_suite_ignore_args" in run_steps["Run complementary heavy suite"]
    assert "uv run pytest tests/ -q -n auto --dist=loadscope $HEAVY_SUITE_IGNORE_ARGS" in run_steps[
        "Run complementary heavy suite"
    ]
    assert "--full-suite" not in run_steps["Run complementary heavy suite"]
    assert "preferred parallel fast path" in tests_readme
    assert "parallel flags now live at the call site instead of repo config" in tests_readme
    assert "GitHub Actions workflow runs both fast and full suites explicitly" in tests_readme
    assert full_suite_ignore_args() == tuple(f"--ignore=tests/{rel_path}" for rel_path in sorted(FAST_SUITE_EXCLUDES))


def test_explicit_collection_is_not_treated_as_fast_suite_blacklisting() -> None:
    collection_path = Path(__file__).resolve().parent / "core" / "test_state.py"
    config = SimpleNamespace(
        invocation_params=SimpleNamespace(args=[str(collection_path)]),
    )

    assert _explicit_collection_requested(collection_path.resolve(strict=False), config) is True
