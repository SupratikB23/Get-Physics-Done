"""Focused regression coverage for beginner onboarding docs."""

from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _assert_fragments(content: str, fragments: tuple[str, ...]) -> None:
    for fragment in fragments:
        assert fragment in content


@pytest.mark.parametrize(
    ("doc_name", "fragments"),
    [
        (
            "claude-code.md",
            (
                "/gpd:help",
                "/gpd:start",
                "/gpd:tour",
                "/gpd:new-project --minimal",
                "/gpd:map-research",
                "/gpd:resume-work",
            ),
        ),
        (
            "codex.md",
            (
                "$gpd-help",
                "$gpd-start",
                "$gpd-tour",
                "$gpd-new-project --minimal",
                "$gpd-map-research",
                "$gpd-resume-work",
            ),
        ),
        (
            "gemini-cli.md",
            (
                "/gpd:help",
                "/gpd:start",
                "/gpd:tour",
                "/gpd:new-project --minimal",
                "/gpd:map-research",
                "/gpd:resume-work",
            ),
        ),
        (
            "opencode.md",
            (
                "/gpd-help",
                "/gpd-start",
                "/gpd-tour",
                "/gpd-new-project --minimal",
                "/gpd-resume-work",
                "/gpd-map-research",
            ),
        ),
    ],
)
def test_runtime_quickstarts_surface_the_beginner_next_steps(
    doc_name: str, fragments: tuple[str, ...]
) -> None:
    content = _read(f"docs/{doc_name}")
    _assert_fragments(content, fragments)


@pytest.mark.parametrize(
    "doc_name",
    ["macos.md", "windows.md", "linux.md"],
)
def test_os_quickstarts_link_runtime_guides_and_post_install_help(doc_name: str) -> None:
    content = _read(f"docs/{doc_name}")

    _assert_fragments(
        content,
        (
            "Confirm success",
            "gpd --help",
            "Not sure which path fits this folder",
            "Want a guided overview",
            "Start a new project",
            "Map an existing folder",
            "Reopen work from your normal terminal",
        ),
    )

    for guide in ("claude-code.md", "codex.md", "gemini-cli.md", "opencode.md"):
        assert f"./{guide}" in content


def test_shared_onboarding_readme_surfaces_help_start_and_tour() -> None:
    content = _read("README.md")

    _assert_fragments(
        content,
        (
            "`help`",
            "`start`",
            "`tour`",
            "/gpd:help",
            "/gpd:start",
            "/gpd:tour",
            "Guided first-run triage",
            "guided walkthrough",
        ),
    )
    assert content.index("`help`") < content.index("`start`")
    assert content.index("`start`") < content.index("`tour`")
