"""Shared resume-surface normalization helpers.

The canonical public resume surface keeps modern continuation fields at the
top level and groups legacy raw aliases under ``compat_resume_surface``. This
module centralizes that projection so ``init_resume()``, CLI raw output, and
other public surfaces do not each reinvent compatibility handling. The compat
schema inventory lives here as the single source of truth for alias names and
wrapper aliases.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

__all__ = [
    "RESUME_COMPATIBILITY_ALIAS_FIELDS",
    "RESUME_COMPATIBILITY_SCHEMA",
    "RESUME_COMPATIBILITY_WRAPPER_ALIASES",
    "RESUME_COMPATIBILITY_ALIAS_KEYS",
    "build_resume_compat_surface",
    "canonicalize_resume_public_payload",
]


RESUME_COMPATIBILITY_ALIAS_FIELDS: tuple[str, ...] = (
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

RESUME_COMPATIBILITY_WRAPPER_ALIASES: tuple[str, ...] = (
    "compat_resume_surface",
    "legacy_resume_surface",
    "compatibility_resume_surface",
)

RESUME_COMPATIBILITY_SCHEMA: dict[str, tuple[str, ...] | str] = {
    "surface_key": "compat_resume_surface",
    "alias_fields": RESUME_COMPATIBILITY_ALIAS_FIELDS,
    "wrapper_aliases": RESUME_COMPATIBILITY_WRAPPER_ALIASES,
}

# Backward-compatible alias for callers that still import the older constant name.
RESUME_COMPATIBILITY_ALIAS_KEYS: tuple[str, ...] = RESUME_COMPATIBILITY_ALIAS_FIELDS


def build_resume_compat_surface(
    *sources: Mapping[str, object] | None,
    fields: Sequence[str] = RESUME_COMPATIBILITY_ALIAS_FIELDS,
) -> dict[str, object] | None:
    """Return the nested compatibility resume block for one payload."""
    compat: dict[str, object] = dict.fromkeys(fields)
    found_alias_data = False

    for source in sources:
        if not isinstance(source, Mapping):
            continue
        for key in RESUME_COMPATIBILITY_WRAPPER_ALIASES:
            value = source.get(key)
            if isinstance(value, Mapping):
                nested_alias_data = False
                for field in fields:
                    if field in value:
                        compat[field] = value.get(field)
                        nested_alias_data = True
                if nested_alias_data:
                    found_alias_data = True
                    break
        if any(key in source for key in fields):
            found_alias_data = True
            break

    for key in fields:
        for source in sources:
            if not isinstance(source, Mapping) or key not in source:
                continue
            compat[key] = source.get(key)
            break

    return compat if found_alias_data else None


def canonicalize_resume_public_payload(
    payload: Mapping[str, object],
    *,
    compat_fields: Sequence[str] = RESUME_COMPATIBILITY_ALIAS_FIELDS,
) -> dict[str, object]:
    """Group legacy resume aliases under ``compat_resume_surface`` only."""
    canonical = dict(payload)
    compat = build_resume_compat_surface(canonical, fields=compat_fields)

    for key in RESUME_COMPATIBILITY_ALIAS_FIELDS:
        canonical.pop(key, None)
    for key in RESUME_COMPATIBILITY_WRAPPER_ALIASES:
        canonical.pop(key, None)

    if compat is not None:
        canonical["compat_resume_surface"] = compat
    else:
        canonical.pop("compat_resume_surface", None)

    return canonical
