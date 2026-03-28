from __future__ import annotations

from gpd.core.workflow_presets import get_workflow_preset, list_workflow_presets, resolve_workflow_preset_readiness


def test_workflow_preset_inventory_is_stable_and_non_persisted() -> None:
    presets = list_workflow_presets()

    assert [preset.id for preset in presets] == [
        "core-research",
        "theory",
        "numerics",
        "publication-manuscript",
        "full-research",
    ]
    assert get_workflow_preset("publication-manuscript") is not None
    assert get_workflow_preset("missing") is None
    assert all("model_cost_posture" in preset.recommended_config for preset in presets)


def test_publication_and_full_presets_are_the_only_verified_tooling_presets() -> None:
    presets = {preset.id: preset for preset in list_workflow_presets()}

    assert presets["publication-manuscript"].required_checks == ("LaTeX Toolchain",)
    assert presets["full-research"].required_checks == ("LaTeX Toolchain",)
    assert presets["theory"].required_checks == ()
    assert presets["numerics"].required_checks == ()


def test_workflow_preset_readiness_degrades_only_publication_family_without_latex() -> None:
    readiness = resolve_workflow_preset_readiness(base_ready=True, latex_available=False)
    statuses = {preset["id"]: preset["status"] for preset in readiness["presets"]}

    assert readiness["ready"] == 3
    assert readiness["degraded"] == 2
    assert readiness["blocked"] == 0
    assert statuses["core-research"] == "ready"
    assert statuses["theory"] == "ready"
    assert statuses["numerics"] == "ready"
    assert statuses["publication-manuscript"] == "degraded"
    assert statuses["full-research"] == "degraded"


def test_workflow_preset_readiness_blocks_everything_when_base_runtime_is_not_ready() -> None:
    readiness = resolve_workflow_preset_readiness(base_ready=False, latex_available=True)

    assert readiness["ready"] == 0
    assert readiness["degraded"] == 0
    assert readiness["blocked"] == 5
    assert all(preset["status"] == "blocked" for preset in readiness["presets"])
