"""Tests for the shared installed runtime CLI bridge."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from gpd.adapters import get_adapter
from gpd.core.constants import ENV_GPD_ACTIVE_RUNTIME, ENV_GPD_DISABLE_CHECKOUT_REEXEC
from gpd.runtime_cli import main


def _mark_complete_install(config_dir: Path, *, runtime: str, install_scope: str = "local") -> None:
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "get-physics-done").mkdir(parents=True, exist_ok=True)
    (config_dir / "gpd-file-manifest.json").write_text(
        json.dumps({"runtime": runtime, "install_scope": install_scope}),
        encoding="utf-8",
    )


def _run_runtime_cli_with_recording(
    monkeypatch,
    *,
    cwd: Path,
    argv: list[str],
) -> tuple[int, dict[str, object]]:
    observed: dict[str, object] = {}
    adapter = get_adapter("codex")

    def record_missing_install_artifacts(target_dir: Path) -> tuple[str, ...]:
        observed["config_dir"] = target_dir
        return ()

    def fake_entrypoint() -> int:
        observed["argv"] = list(sys.argv)
        observed["runtime"] = os.environ.get(ENV_GPD_ACTIVE_RUNTIME)
        observed["disable_reexec"] = os.environ.get(ENV_GPD_DISABLE_CHECKOUT_REEXEC)
        return 0

    monkeypatch.chdir(cwd)
    monkeypatch.delenv(ENV_GPD_ACTIVE_RUNTIME, raising=False)
    monkeypatch.delenv(ENV_GPD_DISABLE_CHECKOUT_REEXEC, raising=False)
    monkeypatch.setattr(adapter, "missing_install_artifacts", record_missing_install_artifacts)
    monkeypatch.setattr("gpd.runtime_cli.get_adapter", lambda runtime: adapter)
    monkeypatch.setattr("gpd.runtime_cli._prepend_checkout_src", lambda: None)
    monkeypatch.setattr("gpd.cli.entrypoint", fake_entrypoint)

    return main(argv), observed


def test_runtime_cli_fails_cleanly_for_incomplete_install(tmp_path: Path, capsys) -> None:
    config_dir = tmp_path / ".codex"
    config_dir.mkdir()

    exit_code = main(
        [
            "--runtime",
            "codex",
            "--config-dir",
            str(config_dir),
            "--install-scope",
            "local",
            "state",
            "load",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 127
    assert "GPD runtime install incomplete for Codex" in captured.err
    assert "`gpd-file-manifest.json`" in captured.err
    assert "`get-physics-done`" in captured.err
    assert "npx -y get-physics-done --codex --local" in captured.err


def test_runtime_cli_dispatches_with_runtime_pin(monkeypatch, tmp_path: Path) -> None:
    config_dir = tmp_path / ".codex"
    _mark_complete_install(config_dir, runtime="codex")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("gpd.version.checkout_root", lambda start=None: None)

    observed: dict[str, object] = {}

    def fake_entrypoint() -> int:
        observed["argv"] = list(sys.argv)
        observed["runtime"] = os.environ.get(ENV_GPD_ACTIVE_RUNTIME)
        observed["disable_reexec"] = os.environ.get(ENV_GPD_DISABLE_CHECKOUT_REEXEC)
        return 0

    monkeypatch.setattr("gpd.cli.entrypoint", fake_entrypoint)

    exit_code = main(
        [
            "--runtime",
            "codex",
            "--config-dir",
            "./.codex",
            "--install-scope",
            "local",
            "state",
            "load",
        ]
    )

    assert exit_code == 0
    assert observed["argv"] == ["gpd", "state", "load"]
    assert observed["runtime"] == "codex"
    assert observed["disable_reexec"] == "1"


def test_runtime_cli_resolves_local_config_dir_from_ancestor_workspace(monkeypatch, tmp_path: Path) -> None:
    config_dir = tmp_path / ".codex"
    _mark_complete_install(config_dir, runtime="codex")
    nested_cwd = tmp_path / "research" / "notes"
    nested_cwd.mkdir(parents=True)
    monkeypatch.chdir(nested_cwd)
    monkeypatch.setattr("gpd.version.checkout_root", lambda start=None: None)

    observed: dict[str, object] = {}

    def fake_entrypoint() -> int:
        observed["argv"] = list(sys.argv)
        observed["runtime"] = os.environ.get(ENV_GPD_ACTIVE_RUNTIME)
        return 0

    monkeypatch.setattr("gpd.cli.entrypoint", fake_entrypoint)

    exit_code = main(
        [
            "--runtime",
            "codex",
            "--config-dir",
            "./.codex",
            "--install-scope",
            "local",
            "state",
            "load",
        ]
    )

    assert exit_code == 0
    assert observed["argv"] == ["gpd", "state", "load"]
    assert observed["runtime"] == "codex"


def test_runtime_cli_ignores_unrelated_nested_runtime_dirs_when_resolving_ancestor_local_install(
    monkeypatch,
    tmp_path: Path,
) -> None:
    config_dir = tmp_path / ".codex"
    _mark_complete_install(config_dir, runtime="codex")
    _mark_complete_install(tmp_path / "research" / ".claude", runtime="claude-code")
    _mark_complete_install(tmp_path / "research" / "notes" / ".gemini", runtime="gemini")
    nested_cwd = tmp_path / "research" / "notes" / "drafts"
    nested_cwd.mkdir(parents=True)

    exit_code, observed = _run_runtime_cli_with_recording(
        monkeypatch,
        cwd=nested_cwd,
        argv=[
            "--runtime",
            "codex",
            "--config-dir",
            "./.codex",
            "--install-scope",
            "local",
            "state",
            "load",
        ],
    )

    assert exit_code == 0
    assert observed["config_dir"] == config_dir
    assert observed["argv"] == ["gpd", "state", "load"]
    assert observed["runtime"] == "codex"
    assert observed["disable_reexec"] == "1"


def test_runtime_cli_ignores_global_scope_candidates_when_resolving_ancestor_local_install(
    monkeypatch,
    tmp_path: Path,
) -> None:
    config_dir = tmp_path / ".codex"
    _mark_complete_install(config_dir, runtime="codex")
    global_dir = tmp_path / "home" / ".codex"
    _mark_complete_install(global_dir, runtime="codex", install_scope="global")
    nested_cwd = tmp_path / "research" / "notes"
    nested_cwd.mkdir(parents=True)
    monkeypatch.setenv("CODEX_CONFIG_DIR", str(global_dir))

    exit_code, observed = _run_runtime_cli_with_recording(
        monkeypatch,
        cwd=nested_cwd,
        argv=[
            "--runtime",
            "codex",
            "--config-dir",
            "./.codex",
            "--install-scope",
            "local",
            "state",
            "load",
        ],
    )

    assert exit_code == 0
    assert observed["config_dir"] == config_dir
    assert observed["argv"] == ["gpd", "state", "load"]
    assert observed["runtime"] == "codex"
    assert observed["disable_reexec"] == "1"
