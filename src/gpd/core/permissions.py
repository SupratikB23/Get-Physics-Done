"""Runtime permission helpers.

Generates launch wrappers and status reports for runtime-specific
permission configurations.  The ``runtime_permissions`` config key
controls whether GPD asks the host runtime to operate in a more
permissive mode (fewer tool-permission prompts).

This is a *runtime integration layer* — it does not modify any upstream
CLI source code.  It generates configuration artifacts (wrapper scripts,
config entries) that the user opts into.
"""

from __future__ import annotations

import logging
import os
import platform
import stat
from pathlib import Path

from gpd.core.config import RuntimePermissions

logger = logging.getLogger(__name__)

__all__ = [
    "PermissionsStatusResult",
    "permissions_status",
    "generate_launch_wrapper",
]

# Name of the generated wrapper script (without extension).
_CLAUDE_WRAPPER_NAME = "claude-gpd"
_WRAPPER_DIR_NAME = "bin"


def _gpd_home() -> Path:
    """Return ``~/.gpd``, creating it if needed."""
    home = Path.home() / ".gpd"
    home.mkdir(parents=True, exist_ok=True)
    return home


def _wrapper_dir() -> Path:
    d = _gpd_home() / _WRAPPER_DIR_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def _wrapper_path() -> Path:
    name = _CLAUDE_WRAPPER_NAME
    if platform.system() == "Windows":
        name += ".cmd"
    return _wrapper_dir() / name


# ---- Status report --------------------------------------------------------


class PermissionsStatusResult:
    """Plain object returned by ``permissions_status``."""

    def __init__(
        self,
        *,
        runtime: str,
        mode: str,
        effective: str,
        wrapper_path: str | None = None,
        message: str = "",
    ) -> None:
        self.runtime = runtime
        self.mode = mode
        self.effective = effective
        self.wrapper_path = wrapper_path
        self.message = message

    def to_dict(self) -> dict[str, object]:
        d: dict[str, object] = {
            "runtime": self.runtime,
            "mode": self.mode,
            "effective": self.effective,
            "message": self.message,
        }
        if self.wrapper_path:
            d["wrapper_path"] = self.wrapper_path
        return d


def _detect_active_runtime() -> str:
    """Return the active GPD runtime name, or ``unknown``."""
    return os.environ.get("GPD_ACTIVE_RUNTIME", "unknown")


def permissions_status(mode: RuntimePermissions) -> PermissionsStatusResult:
    """Build a status report for the current runtime and permission mode."""
    runtime = _detect_active_runtime()

    if runtime == "claude-code":
        return _claude_status(mode)
    if runtime == "codex":
        return _codex_status(mode)
    if runtime == "gemini":
        return _gemini_status(mode)
    if runtime == "opencode":
        return _opencode_status(mode)

    return PermissionsStatusResult(
        runtime=runtime,
        mode=mode.value,
        effective="unknown",
        message=f"Runtime {runtime!r} is not recognized. Permission presets are not available.",
    )


def _claude_status(mode: RuntimePermissions) -> PermissionsStatusResult:
    wrapper = _wrapper_path()
    wrapper_exists = wrapper.is_file()

    if mode == RuntimePermissions.PERMISSIVE:
        if wrapper_exists:
            return PermissionsStatusResult(
                runtime="claude-code",
                mode="permissive",
                effective="permissive" if _launched_with_skip() else "default (wrapper not used)",
                wrapper_path=str(wrapper),
                message=(
                    f"Launch wrapper exists at {wrapper}.\n"
                    "Exit this session and re-launch with:\n"
                    f"  {wrapper}\n"
                    "to run Claude Code with --dangerously-skip-permissions."
                )
                if not _launched_with_skip()
                else "Running with --dangerously-skip-permissions via launch wrapper.",
            )
        return PermissionsStatusResult(
            runtime="claude-code",
            mode="permissive",
            effective="default (wrapper not generated)",
            message=(
                "Permissive mode is configured but no launch wrapper found.\n"
                "Run `gpd permissions generate-wrapper` to create it, then\n"
                "re-launch Claude Code with the wrapper."
            ),
        )

    return PermissionsStatusResult(
        runtime="claude-code",
        mode="default",
        effective="default",
        message="Claude Code is running with standard permission prompts.",
    )


def _launched_with_skip() -> bool:
    """Heuristic: check if the current process tree includes the skip flag.

    This is best-effort — the flag is a CLI launch argument and there is
    no reliable runtime API to query it.
    """
    # If someone used our wrapper, they set this env var.
    return os.environ.get("GPD_CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS") == "1"


def _codex_status(mode: RuntimePermissions) -> PermissionsStatusResult:
    return PermissionsStatusResult(
        runtime="codex",
        mode=mode.value,
        effective="permissive (sandbox)",
        message=(
            "Codex runs agents in a workspace-write sandbox by default.\n"
            "No additional configuration is needed for permissive mode."
        ),
    )


def _gemini_status(mode: RuntimePermissions) -> PermissionsStatusResult:
    return PermissionsStatusResult(
        runtime="gemini",
        mode=mode.value,
        effective="partial",
        message=(
            "Gemini CLI auto-approves a limited set of GPD shell commands.\n"
            "Full permissive mode is not available for Gemini at this time."
        ),
    )


def _opencode_status(mode: RuntimePermissions) -> PermissionsStatusResult:
    return PermissionsStatusResult(
        runtime="opencode",
        mode=mode.value,
        effective="partial (permission grants)",
        message=(
            "OpenCode uses directory-level permission grants for GPD paths.\n"
            "Full permissive mode is not available for OpenCode at this time."
        ),
    )


# ---- Launch wrapper generation --------------------------------------------


def generate_launch_wrapper() -> Path:
    """Write a shell wrapper that launches Claude Code with --dangerously-skip-permissions.

    Returns the path to the generated wrapper.
    """
    wrapper = _wrapper_path()
    system = platform.system()

    if system == "Windows":
        content = (
            "@echo off\n"
            "REM Generated by GPD — launches Claude Code in permissive mode.\n"
            "set GPD_CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS=1\n"
            'claude --dangerously-skip-permissions %*\n'
        )
    else:
        content = (
            "#!/usr/bin/env sh\n"
            "# Generated by GPD — launches Claude Code in permissive mode.\n"
            "# This passes --dangerously-skip-permissions to skip all tool\n"
            "# permission prompts.  Use with care.\n"
            "export GPD_CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS=1\n"
            'exec claude --dangerously-skip-permissions "$@"\n'
        )

    wrapper.write_text(content, encoding="utf-8")
    if system != "Windows":
        wrapper.chmod(wrapper.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    logger.info("Generated launch wrapper at %s", wrapper)
    return wrapper


def remove_launch_wrapper() -> bool:
    """Remove the generated launch wrapper if it exists."""
    wrapper = _wrapper_path()
    if wrapper.is_file():
        wrapper.unlink()
        return True
    return False
