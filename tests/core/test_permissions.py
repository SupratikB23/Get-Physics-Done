"""Tests for runtime permission helpers and CLI commands."""

from __future__ import annotations

import json
import platform
import stat
from pathlib import Path

import pytest
from typer.testing import CliRunner

from gpd.cli import app
from gpd.core.config import GPDProjectConfig, RuntimePermissions, load_config
from gpd.core.permissions import (
    generate_launch_wrapper,
    permissions_status,
    remove_launch_wrapper,
)

runner = CliRunner()


# ---- Config model ---------------------------------------------------------


class TestRuntimePermissionsConfig:
    def test_default_is_default(self) -> None:
        config = GPDProjectConfig()
        assert config.runtime_permissions == RuntimePermissions.DEFAULT

    def test_accepts_permissive(self) -> None:
        config = GPDProjectConfig(runtime_permissions="permissive")
        assert config.runtime_permissions == RuntimePermissions.PERMISSIVE

    def test_rejects_invalid(self) -> None:
        with pytest.raises(ValueError):
            GPDProjectConfig(runtime_permissions="invalid")

    def test_roundtrip_through_config_file(self, tmp_path: Path) -> None:
        gpd_dir = tmp_path / ".gpd"
        gpd_dir.mkdir()
        config_path = gpd_dir / "config.json"
        config_path.write_text(
            json.dumps({"runtime_permissions": "permissive"}),
            encoding="utf-8",
        )
        config = load_config(tmp_path)
        assert config.runtime_permissions == RuntimePermissions.PERMISSIVE

    def test_default_when_missing_from_file(self, tmp_path: Path) -> None:
        gpd_dir = tmp_path / ".gpd"
        gpd_dir.mkdir()
        config_path = gpd_dir / "config.json"
        config_path.write_text(json.dumps({"autonomy": "yolo"}), encoding="utf-8")
        config = load_config(tmp_path)
        assert config.runtime_permissions == RuntimePermissions.DEFAULT


# ---- Status reporting -----------------------------------------------------


class TestPermissionsStatus:
    def test_claude_default_mode(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "claude-code")
        result = permissions_status(RuntimePermissions.DEFAULT)
        assert result.runtime == "claude-code"
        assert result.mode == "default"

    def test_claude_permissive_no_wrapper(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "claude-code")
        result = permissions_status(RuntimePermissions.PERMISSIVE)
        assert result.runtime == "claude-code"
        assert result.mode == "permissive"
        assert "wrapper" in result.message.lower()

    def test_codex_always_permissive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "codex")
        result = permissions_status(RuntimePermissions.DEFAULT)
        assert result.effective == "permissive (sandbox)"

    def test_gemini_partial(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "gemini")
        result = permissions_status(RuntimePermissions.PERMISSIVE)
        assert result.effective == "partial"

    def test_opencode_partial(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "opencode")
        result = permissions_status(RuntimePermissions.PERMISSIVE)
        assert "permission grants" in result.effective

    def test_unknown_runtime(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "unknown-runtime")
        result = permissions_status(RuntimePermissions.DEFAULT)
        assert result.effective == "unknown"

    def test_claude_permissive_with_skip_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "claude-code")
        monkeypatch.setenv("GPD_CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS", "1")
        # Create the wrapper so the status sees it
        generate_launch_wrapper()
        try:
            result = permissions_status(RuntimePermissions.PERMISSIVE)
            assert result.effective == "permissive"
        finally:
            remove_launch_wrapper()


# ---- Launch wrapper -------------------------------------------------------


class TestLaunchWrapper:
    def test_generates_executable_wrapper(self) -> None:
        wrapper = generate_launch_wrapper()
        try:
            assert wrapper.is_file()
            content = wrapper.read_text()
            assert "claude" in content
            assert "--dangerously-skip-permissions" in content
            assert "GPD_CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS" in content
            if platform.system() != "Windows":
                assert wrapper.stat().st_mode & stat.S_IXUSR
        finally:
            remove_launch_wrapper()

    def test_remove_wrapper(self) -> None:
        generate_launch_wrapper()
        assert remove_launch_wrapper() is True
        assert remove_launch_wrapper() is False  # already gone

    def test_wrapper_is_idempotent(self) -> None:
        w1 = generate_launch_wrapper()
        w2 = generate_launch_wrapper()
        try:
            assert w1 == w2
            assert w1.is_file()
        finally:
            remove_launch_wrapper()


# ---- CLI commands ---------------------------------------------------------


class TestPermissionsCLI:
    def _setup_project(self, tmp_path: Path) -> Path:
        gpd_dir = tmp_path / ".gpd"
        gpd_dir.mkdir()
        (gpd_dir / "config.json").write_text("{}", encoding="utf-8")
        return tmp_path

    def test_status_command(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cwd = self._setup_project(tmp_path)
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "claude-code")
        result = runner.invoke(app, ["--raw", "--cwd", str(cwd), "permissions", "status"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["runtime"] == "claude-code"
        assert payload["mode"] == "default"

    def test_enable_permissive_command(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cwd = self._setup_project(tmp_path)
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "claude-code")
        result = runner.invoke(app, ["--raw", "--cwd", str(cwd), "permissions", "enable-permissive"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["updated"] is True
        assert payload["mode"] == "permissive"
        assert "wrapper_path" in payload

        # Verify config was updated
        config = load_config(cwd)
        assert config.runtime_permissions == RuntimePermissions.PERMISSIVE

        # Verify wrapper was generated
        wrapper = Path(payload["wrapper_path"])
        assert wrapper.is_file()
        assert "--dangerously-skip-permissions" in wrapper.read_text()

        # Cleanup
        remove_launch_wrapper()

    def test_disable_permissive_command(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cwd = self._setup_project(tmp_path)
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "claude-code")

        # Enable first
        runner.invoke(app, ["--raw", "--cwd", str(cwd), "permissions", "enable-permissive"])

        # Now disable
        result = runner.invoke(app, ["--raw", "--cwd", str(cwd), "permissions", "disable-permissive"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["updated"] is True
        assert payload["mode"] == "default"

        # Verify config reverted
        config = load_config(cwd)
        assert config.runtime_permissions == RuntimePermissions.DEFAULT

    def test_generate_wrapper_command(self, tmp_path: Path) -> None:
        result = runner.invoke(app, ["--raw", "permissions", "generate-wrapper"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["generated"] is True
        assert "claude-gpd" in payload["wrapper_path"]

        # Cleanup
        remove_launch_wrapper()

    def test_enable_permissive_codex_no_wrapper(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cwd = self._setup_project(tmp_path)
        monkeypatch.setenv("GPD_ACTIVE_RUNTIME", "codex")
        result = runner.invoke(app, ["--raw", "--cwd", str(cwd), "permissions", "enable-permissive"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["effective"] == "permissive (sandbox)"
        assert "wrapper_path" not in payload or payload.get("wrapper_path") is None


# ---- Autonomy vs permissions independence ---------------------------------


class TestAutonomyPermissionsIndependence:
    """Verify that autonomy and runtime_permissions are truly independent."""

    def test_yolo_with_default_permissions(self) -> None:
        config = GPDProjectConfig(autonomy="yolo", runtime_permissions="default")
        assert config.autonomy.value == "yolo"
        assert config.runtime_permissions.value == "default"

    def test_supervised_with_permissive(self) -> None:
        config = GPDProjectConfig(autonomy="supervised", runtime_permissions="permissive")
        assert config.autonomy.value == "supervised"
        assert config.runtime_permissions.value == "permissive"

    def test_balanced_with_permissive(self) -> None:
        config = GPDProjectConfig(autonomy="balanced", runtime_permissions="permissive")
        assert config.autonomy.value == "balanced"
        assert config.runtime_permissions.value == "permissive"


# ---- Config get/set integration ------------------------------------------


class TestConfigGetSetIntegration:
    def test_config_get_runtime_permissions(self, tmp_path: Path) -> None:
        gpd_dir = tmp_path / ".gpd"
        gpd_dir.mkdir()
        (gpd_dir / "config.json").write_text(
            json.dumps({"runtime_permissions": "permissive"}),
            encoding="utf-8",
        )
        result = runner.invoke(app, ["--raw", "--cwd", str(tmp_path), "config", "get", "runtime_permissions"])
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["value"] == "permissive"
        assert payload["found"] is True

    def test_config_set_runtime_permissions(self, tmp_path: Path) -> None:
        gpd_dir = tmp_path / ".gpd"
        gpd_dir.mkdir()
        (gpd_dir / "config.json").write_text("{}", encoding="utf-8")
        result = runner.invoke(
            app,
            ["--raw", "--cwd", str(tmp_path), "config", "set", "runtime_permissions", "permissive"],
        )
        assert result.exit_code == 0, result.output
        payload = json.loads(result.output)
        assert payload["value"] == "permissive"
        assert payload["updated"] is True

    def test_config_set_runtime_permissions_invalid(self, tmp_path: Path) -> None:
        gpd_dir = tmp_path / ".gpd"
        gpd_dir.mkdir()
        (gpd_dir / "config.json").write_text("{}", encoding="utf-8")
        result = runner.invoke(
            app,
            ["--raw", "--cwd", str(tmp_path), "config", "set", "runtime_permissions", "invalid"],
        )
        assert result.exit_code != 0
