from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from gpd.adapters.runtime_catalog import get_hook_payload_policy
from gpd.hooks.install_context import SelfOwnedInstallContext
from gpd.hooks.payload_policy import resolve_hook_payload_policy, resolve_hook_surface_runtime


def test_resolve_hook_surface_runtime_prefers_self_owned_install_for_supported_surface(tmp_path: Path) -> None:
    hook_file = tmp_path / ".claude" / "hooks" / "statusline.py"
    self_install = SelfOwnedInstallContext(
        config_dir=tmp_path / ".claude",
        runtime="claude-code",
        install_scope="local",
    )

    with (
        patch("gpd.hooks.payload_policy.hook_layout.detect_self_owned_install", return_value=self_install),
        patch("gpd.hooks.payload_policy.detect_active_runtime_with_gpd_install", return_value="gemini"),
    ):
        runtime = resolve_hook_surface_runtime(hook_file=hook_file, cwd=tmp_path / "workspace", surface="statusline")

    assert runtime == "claude-code"


def test_resolve_hook_surface_runtime_ignores_self_owned_install_when_surface_is_unsupported(tmp_path: Path) -> None:
    hook_file = tmp_path / ".codex" / "hooks" / "statusline.py"
    self_install = SelfOwnedInstallContext(
        config_dir=tmp_path / ".codex",
        runtime="codex",
        install_scope="local",
    )

    with (
        patch("gpd.hooks.payload_policy.hook_layout.detect_self_owned_install", return_value=self_install),
        patch("gpd.hooks.payload_policy.detect_active_runtime_with_gpd_install", return_value="gemini"),
    ):
        runtime = resolve_hook_surface_runtime(hook_file=hook_file, cwd=tmp_path / "workspace", surface="statusline")

    assert runtime == "gemini"


def test_resolve_hook_payload_policy_uses_surface_runtime_resolution(tmp_path: Path) -> None:
    hook_file = tmp_path / ".codex" / "hooks" / "notify.py"

    with patch("gpd.hooks.payload_policy.resolve_hook_surface_runtime", return_value="codex") as mock_runtime:
        policy = resolve_hook_payload_policy(hook_file=hook_file, cwd=tmp_path / "workspace", surface="notify")

    mock_runtime.assert_called_once_with(hook_file=hook_file, cwd=tmp_path / "workspace", surface="notify")
    assert policy == get_hook_payload_policy("codex")
