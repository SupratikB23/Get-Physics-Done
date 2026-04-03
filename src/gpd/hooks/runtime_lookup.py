"""Shared runtime-lookup decisions for hook surfaces."""

from __future__ import annotations

from pathlib import Path

import gpd.hooks.install_context as hook_layout
from gpd.hooks.runtime_detect import ALL_RUNTIMES, SCOPE_LOCAL, detect_runtime_install_target


def _workspace_has_local_runtime_install(workspace_dir: str) -> bool:
    """Return whether any runtime has a local install anchored at *workspace_dir*."""
    resolved_workspace = Path(workspace_dir).expanduser().resolve(strict=False)
    for runtime in ALL_RUNTIMES:
        install_target = detect_runtime_install_target(runtime, cwd=resolved_workspace)
        if install_target is not None and install_target.install_scope == SCOPE_LOCAL:
            return True
    return False


def resolve_runtime_lookup_dir(
    *,
    workspace_dir: str,
    project_root: str,
    explicit_project_dir: bool,
) -> str:
    """Return the cwd hook surfaces should use for runtime-owned lookups."""
    if explicit_project_dir:
        return workspace_dir if _workspace_has_local_runtime_install(workspace_dir) else project_root

    lookup = hook_layout.resolve_hook_lookup_context(cwd=workspace_dir)
    return str(lookup.lookup_cwd) if lookup.lookup_cwd is not None else workspace_dir
