from __future__ import annotations

from copy import deepcopy

import pytest

from gpd.core.resume_surface import (
    RESUME_COMPATIBILITY_ALIAS_KEYS,
    build_resume_compat_surface,
    canonicalize_resume_public_payload,
)


def test_build_resume_compat_surface_returns_none_without_compat_aliases() -> None:
    payload = {
        "active_resume_kind": "bounded_segment",
        "active_resume_origin": "compat.current_execution",
        "active_resume_pointer": "GPD/phases/03/.continue-here.md",
    }

    assert build_resume_compat_surface(payload) is None


def test_build_resume_compat_surface_extracts_top_level_legacy_fields() -> None:
    payload = {
        "current_execution": {"resume_file": "GPD/phases/03/.continue-here.md"},
        "active_execution_segment": {"segment_id": "seg-1"},
        "current_execution_resume_file": "GPD/phases/03/.continue-here.md",
        "execution_resume_file": "GPD/phases/03/.continue-here.md",
        "execution_resume_file_source": "current_execution",
        "missing_session_resume_file": "GPD/phases/03/alternate.md",
        "recorded_session_resume_file": "GPD/phases/03/alternate.md",
        "resume_mode": "bounded_segment",
        "segment_candidates": [{"source": "current_execution"}],
        "session_resume_file": "GPD/phases/03/alternate.md",
    }

    compat = build_resume_compat_surface(payload)

    assert compat is not None
    assert set(compat) == set(RESUME_COMPATIBILITY_ALIAS_KEYS)
    assert compat["current_execution"] == {"resume_file": "GPD/phases/03/.continue-here.md"}
    assert compat["active_execution_segment"] == {"segment_id": "seg-1"}
    assert compat["execution_resume_file"] == "GPD/phases/03/.continue-here.md"
    assert compat["execution_resume_file_source"] == "current_execution"
    assert compat["missing_session_resume_file"] == "GPD/phases/03/alternate.md"
    assert compat["recorded_session_resume_file"] == "GPD/phases/03/alternate.md"
    assert compat["resume_mode"] == "bounded_segment"
    assert compat["segment_candidates"] == [{"source": "current_execution"}]
    assert compat["session_resume_file"] == "GPD/phases/03/alternate.md"


@pytest.mark.parametrize(
    "wrapper_key",
    ["compat_resume_surface", "legacy_resume_surface", "compatibility_resume_surface"],
)
def test_build_resume_compat_surface_extracts_wrapper_aliases(wrapper_key: str) -> None:
    payload = {
        wrapper_key: {
            "execution_resume_file": "GPD/phases/04/.continue-here.md",
            "execution_resume_file_source": "session_resume_file",
            "resume_mode": "continuity_handoff",
            "segment_candidates": [{"source": "session_resume_file", "status": "handoff"}],
            "session_resume_file": "GPD/phases/04/.continue-here.md",
        }
    }

    compat = build_resume_compat_surface(payload)

    assert compat is not None
    assert compat["execution_resume_file"] == "GPD/phases/04/.continue-here.md"
    assert compat["execution_resume_file_source"] == "session_resume_file"
    assert compat["resume_mode"] == "continuity_handoff"
    assert compat["segment_candidates"] == [{"source": "session_resume_file", "status": "handoff"}]
    assert compat["session_resume_file"] == "GPD/phases/04/.continue-here.md"


def test_build_resume_compat_surface_merges_sources_with_explicit_precedence() -> None:
    payload_one = {
        "compat_resume_surface": {
            "execution_resume_file": "GPD/phases/01/.continue-here.md",
            "session_resume_file": "GPD/phases/01/legacy.md",
        },
    }
    payload_two = {
        "compatibility_resume_surface": {
            "session_resume_file": "GPD/phases/02/legacy.md",
            "execution_resume_file_source": "session_resume_file",
        }
    }
    payload_three = {
        "legacy_resume_surface": {
            "recorded_session_resume_file": "GPD/phases/03/legacy.md",
            "session_resume_file": "GPD/phases/03/legacy.md",
        },
        "execution_resume_file": "GPD/phases/03/.continue-here.md",
        "resume_mode": "continuity_handoff",
    }

    compat = build_resume_compat_surface(payload_one, payload_two, payload_three)

    assert compat is not None
    assert compat["execution_resume_file"] == "GPD/phases/03/.continue-here.md"
    assert compat["execution_resume_file_source"] == "session_resume_file"
    assert compat["resume_mode"] == "continuity_handoff"
    assert compat["recorded_session_resume_file"] == "GPD/phases/03/legacy.md"
    assert compat["session_resume_file"] == "GPD/phases/03/legacy.md"


def test_canonicalize_resume_public_payload_removes_legacy_top_level_aliases_and_preserves_canonical_fields() -> None:
    payload = {
        "active_resume_kind": "bounded_segment",
        "active_resume_origin": "compat.current_execution",
        "active_resume_pointer": "GPD/phases/03/.continue-here.md",
        "execution_resumable": True,
        "execution_resume_file": "GPD/phases/03/.continue-here.md",
        "execution_resume_file_source": "current_execution",
        "resume_mode": "bounded_segment",
        "segment_candidates": [{"source": "current_execution"}],
        "session_resume_file": "GPD/phases/03/legacy.md",
        "compat_resume_surface": {
            "session_resume_file": "GPD/phases/03/legacy.md",
            "resume_mode": "bounded_segment",
        },
    }

    canonical = canonicalize_resume_public_payload(payload)

    assert canonical["active_resume_kind"] == "bounded_segment"
    assert canonical["active_resume_origin"] == "compat.current_execution"
    assert canonical["active_resume_pointer"] == "GPD/phases/03/.continue-here.md"
    assert canonical["execution_resumable"] is True
    assert "execution_resume_file" not in canonical
    assert "execution_resume_file_source" not in canonical
    assert "resume_mode" not in canonical
    assert "segment_candidates" not in canonical
    assert "session_resume_file" not in canonical
    assert canonical["compat_resume_surface"]["execution_resume_file"] == "GPD/phases/03/.continue-here.md"
    assert canonical["compat_resume_surface"]["execution_resume_file_source"] == "current_execution"
    assert canonical["compat_resume_surface"]["resume_mode"] == "bounded_segment"
    assert canonical["compat_resume_surface"]["segment_candidates"] == [{"source": "current_execution"}]
    assert canonical["compat_resume_surface"]["session_resume_file"] == "GPD/phases/03/legacy.md"
    assert canonical["compat_resume_surface"]["recorded_session_resume_file"] is None
    assert canonical["compat_resume_surface"]["missing_session_resume_file"] is None


def test_canonicalize_resume_public_payload_is_idempotent_on_already_canonical_payload() -> None:
    payload = {
        "active_resume_kind": "continuity_handoff",
        "active_resume_origin": "continuation.handoff",
        "active_resume_pointer": "GPD/phases/04/.continue-here.md",
        "has_continuity_handoff": True,
        "compat_resume_surface": {
            "execution_resume_file": "GPD/phases/04/.continue-here.md",
            "execution_resume_file_source": "session_resume_file",
            "resume_mode": "continuity_handoff",
            "session_resume_file": "GPD/phases/04/.continue-here.md",
        },
    }

    once = canonicalize_resume_public_payload(payload)
    twice = canonicalize_resume_public_payload(deepcopy(once))

    assert once == twice
    assert once["active_resume_kind"] == "continuity_handoff"
    assert once["active_resume_origin"] == "continuation.handoff"
    assert once["active_resume_pointer"] == "GPD/phases/04/.continue-here.md"
    assert "resume_mode" not in once
    assert "execution_resume_file" not in once
    assert "execution_resume_file_source" not in once
    assert once["compat_resume_surface"]["execution_resume_file"] == "GPD/phases/04/.continue-here.md"
    assert once["compat_resume_surface"]["execution_resume_file_source"] == "session_resume_file"
    assert once["compat_resume_surface"]["resume_mode"] == "continuity_handoff"
    assert once["compat_resume_surface"]["session_resume_file"] == "GPD/phases/04/.continue-here.md"
    assert once["compat_resume_surface"]["segment_candidates"] is None
    assert once["compat_resume_surface"]["recorded_session_resume_file"] is None
