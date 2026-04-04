from __future__ import annotations

import json
from pathlib import Path

from gpd.contracts import ProjectContractParseResult, ResearchContract
from gpd.core import context as context_module

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "stage0"


def _load_contract_fixture() -> ResearchContract:
    payload = json.loads((FIXTURES_DIR / "project_contract.json").read_text(encoding="utf-8"))
    return ResearchContract.model_validate(payload)


def test_canonicalize_project_contract_surfaces_recoverable_salvage_findings(monkeypatch) -> None:
    contract = _load_contract_fixture()

    recovered_contract = contract.model_copy(
        update={
            "references": [
                reference.model_copy(update={"aliases": ["benchmark-anchor"]})
                if reference.id == contract.references[0].id
                else reference
                for reference in contract.references
            ]
        }
    )

    monkeypatch.setattr(
        context_module,
        "parse_project_contract_data_salvage",
        lambda payload: ProjectContractParseResult(
            contract=recovered_contract,
            recoverable_errors=["references.0.aliases must be a list, not str"],
        ),
    )

    canonical, warnings = context_module._canonicalize_project_contract(
        contract,
        active_references=[reference.model_dump(mode="json") for reference in contract.references],
        effective_reference_intake=contract.context_intake.model_dump(mode="json"),
    )

    assert canonical is not None
    assert canonical.references[0].aliases == ["benchmark-anchor"]
    assert any("canonical project_contract merge required salvage" in warning for warning in warnings)
