"""Focused regressions for skill-routing quality."""

from __future__ import annotations

from unittest.mock import patch

from gpd.registry import SkillDef


def _skill(name: str, *, category: str, registry_name: str) -> SkillDef:
    return SkillDef(
        name=name,
        description=name,
        content=name,
        category=category,
        path=f"/tmp/{name}.md",
        source_kind="command",
        registry_name=registry_name,
    )


def test_route_skill_does_not_route_generic_project_planning_to_new_project() -> None:
    from gpd.mcp.servers.skills_server import route_skill

    with patch(
        "gpd.mcp.servers.skills_server._load_skill_index",
        return_value=[
            _skill("gpd-help", category="help", registry_name="help"),
            _skill("gpd-new-project", category="project", registry_name="new-project"),
        ],
    ):
        result = route_skill("overview of project planning")

    assert result["suggestion"] == "gpd-help"
    assert result["confidence"] <= 0.1


def test_route_skill_still_matches_real_new_project_lifecycle_intent() -> None:
    from gpd.mcp.servers.skills_server import route_skill

    with patch(
        "gpd.mcp.servers.skills_server._load_skill_index",
        return_value=[
            _skill("gpd-help", category="help", registry_name="help"),
            _skill("gpd-new-project", category="project", registry_name="new-project"),
        ],
    ):
        result = route_skill("create a new project workspace")

    assert result["suggestion"] == "gpd-new-project"
    assert result["confidence"] > 0.1
