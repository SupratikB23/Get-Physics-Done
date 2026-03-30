"""Shared resume-surface normalization helpers.

The canonical public resume surface keeps modern continuation fields at the
top level and groups legacy raw aliases under ``compat_resume_surface``. This
module centralizes that projection so ``init_resume()``, CLI raw output, and
other public surfaces do not each reinvent compatibility handling.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

__all__ = [
    "RESUME_COMPATIBILITY_ALIAS_KEYS",
    "RESUME_COMPAT_SURFACE_FIELDS",
    "RESUME_EXECUTION_RUNTIME_ALIAS_KEYS",
    "build_resume_compat_surface",
    "canonicalize_resume_public_payload",
]


RESUME_COMPATIBILITY_ALIAS_KEYS: tuple[str, ...] = (
    "active_execution_segment",
    "current_execution",
    "current_execution_resume_file",
    "execution_resume_file",
    "execution_resume_file_source",
    "missing_session_resume_file",
    "recorded_session_resume_file",
    "resume_mode",
    "segment_candidates",
    "session_resume_file",
)

RESUME_COMPAT_SURFACE_FIELDS: tuple[str, ...] = (
    *RESUME_COMPATIBILITY_ALIAS_KEYS,
    "execution_resumable",
    "execution_paused_at",
    "execution_review_pending",
    "execution_pre_fanout_review_pending",
    "execution_skeptical_requestioning_required",
    "execution_downstream_locked",
    "execution_blocked",
    "has_interrupted_agent",
    "interrupted_agent_id",
    "has_live_execution",
)

RESUME_EXECUTION_RUNTIME_ALIAS_KEYS: tuple[str, ...] = (
    "current_execution",
    "current_execution_resume_file",
    "session_resume_file",
    "recorded_session_resume_file",
    "missing_session_resume_file",
    "execution_resume_file",
    "execution_resume_file_source",
)

_COMPAT_SURFACE_ALIASES: tuple[str, ...] = (
    "compat_resume_surface",
    "legacy_resume_surface",
    "compatibility_resume_surface",
)


def build_resume_compat_surface(
    *sources: Mapping[str, object] | None,
    fields: Sequence[str] = RESUME_COMPATIBILITY_ALIAS_KEYS,
) -> dict[str, object] | None:
    """Return the nested compatibility resume block for one payload."""
    compat: dict[str, object] = {}

    for source in sources:
        if not isinstance(source, Mapping):
            continue
        for key in _COMPAT_SURFACE_ALIASES:
            value = source.get(key)
            if isinstance(value, Mapping):
                compat = dict(value)
                break
        if compat:
            break

    for key in fields:
        if key in compat:
            continue
        for source in sources:
            if not isinstance(source, Mapping) or key not in source:
                continue
            value = source.get(key)
            if value is not None:
                compat[key] = value
            break

    return compat or None


def canonicalize_resume_public_payload(
    payload: Mapping[str, object],
    *extra_sources: Mapping[str, object] | None,
    compat_fields: Sequence[str] = RESUME_COMPAT_SURFACE_FIELDS,
) -> dict[str, object]:
    """Group legacy resume aliases under ``compat_resume_surface`` only."""
    canonical = dict(payload)
    compat = build_resume_compat_surface(canonical, *extra_sources, fields=compat_fields)

    for key in RESUME_COMPATIBILITY_ALIAS_KEYS:
        canonical.pop(key, None)
    for key in _COMPAT_SURFACE_ALIASES[1:]:
        canonical.pop(key, None)

    if compat is not None:
        canonical["compat_resume_surface"] = compat
    else:
        canonical.pop("compat_resume_surface", None)

    return canonical
