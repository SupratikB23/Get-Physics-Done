from __future__ import annotations

import json
from pathlib import Path

from gpd.core.proof_review import (
    manuscript_proof_review_manifest_path,
    phase_proof_review_manifest_path,
    resolve_manuscript_proof_review_status,
    resolve_phase_proof_review_status,
)
from gpd.core.reproducibility import compute_sha256


def _write_proof_bearing_manuscript_review_artifacts(
    project_root: Path,
    *,
    proof_redteam_status: str | None,
    proof_redteam_reviewer: str = "gpd-check-proof",
    proof_redteam_sha256: str | None = None,
    round_number: int = 1,
    proof_artifact_path: str = "paper/main.tex",
) -> Path:
    manuscript_path = project_root / "paper" / "main.tex"
    manuscript_path.parent.mkdir(parents=True, exist_ok=True)
    manuscript_path.write_text(
        "\\documentclass{article}\n\\begin{document}\nProof.\n\\end{document}\n",
        encoding="utf-8",
    )

    proof_artifact = project_root / proof_artifact_path
    proof_artifact.parent.mkdir(parents=True, exist_ok=True)
    if proof_artifact != manuscript_path:
        proof_artifact.write_text(
            "\\documentclass{article}\n\\begin{document}\nExternal proof.\n\\end{document}\n",
            encoding="utf-8",
        )
    proof_redteam_artifact_paths = f"  - {proof_artifact_path}\n"
    if proof_artifact_path != "paper/main.tex":
        proof_redteam_artifact_paths += "  - paper/main.tex\n"

    review_dir = project_root / "GPD" / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    manuscript_sha256 = compute_sha256(manuscript_path)
    round_suffix = "" if round_number <= 1 else f"-R{round_number}"
    (review_dir / f"CLAIMS{round_suffix}.json").write_text(
        json.dumps(
            {
                "version": 1,
                "manuscript_path": "paper/main.tex",
                "manuscript_sha256": manuscript_sha256,
                "claims": [
                    {
                        "claim_id": "CLM-001",
                        "claim_type": "main_result",
                        "text": "For every r_0 > 0, the orbit intersects the target annulus.",
                        "artifact_path": proof_artifact_path,
                        "section": "Main Result",
                        "theorem_assumptions": ["chi > 0"],
                        "theorem_parameters": ["r_0"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (review_dir / f"STAGE-math{round_suffix}.json").write_text(
        json.dumps(
            {
                "version": 1,
                "round": round_number,
                "stage_id": "math",
                "stage_kind": "math",
                "manuscript_path": "paper/main.tex",
                "manuscript_sha256": manuscript_sha256,
                "claims_reviewed": ["CLM-001"],
                "summary": "math review",
                "strengths": ["checked proof"],
                "findings": [],
                "proof_audits": [
                    {
                        "claim_id": "CLM-001",
                        "theorem_assumptions_checked": ["chi > 0"],
                        "theorem_parameters_checked": ["r_0"],
                        "proof_locations": [f"{proof_artifact_path}:1"],
                        "uncovered_assumptions": [],
                        "uncovered_parameters": [],
                        "coverage_gaps": [],
                        "alignment_status": "aligned",
                        "notes": "Complete coverage.",
                    }
                ],
                "confidence": "high",
                "recommendation_ceiling": "minor_revision",
            }
        ),
        encoding="utf-8",
    )
    if proof_redteam_status is not None:
        (review_dir / f"PROOF-REDTEAM{round_suffix}.md").write_text(
            (
                "---\n"
                f"status: {proof_redteam_status}\n"
                f"reviewer: {proof_redteam_reviewer}\n"
                "claim_ids:\n"
                "  - CLM-001\n"
                "proof_artifact_paths:\n"
                f"{proof_redteam_artifact_paths}"
                "manuscript_path: paper/main.tex\n"
                f"manuscript_sha256: {proof_redteam_sha256 or manuscript_sha256}\n"
                f"round: {round_number}\n"
                "---\n\n"
                "# Proof Redteam\n"
                "## Proof Inventory\n"
                "- Exact claim / theorem text: For every r_0 > 0, the orbit intersects the target annulus.\n"
                "- Claim / theorem target: Annulus intersection for every target radius.\n"
                "- Named parameters:\n"
                "  - `r_0`: target radius\n"
                "- Hypotheses:\n"
                "  - `H1`: chi > 0\n"
                "- Quantifier / domain obligations:\n"
                "  - for every r_0 > 0\n"
                "- Conclusion clauses:\n"
                "  - annulus intersection holds\n"
                "## Coverage Ledger\n"
                "### Named-Parameter Coverage\n"
                "| Parameter | Role / Domain | Proof Location | Status | Notes |\n"
                "| --- | --- | --- | --- | --- |\n"
                f"| `r_0` | target radius | {proof_artifact_path}:1 | covered | Carried through the argument. |\n"
                "### Hypothesis Coverage\n"
                "| Hypothesis | Proof Location | Status | Notes |\n"
                "| --- | --- | --- | --- |\n"
                f"| `H1` | {proof_artifact_path}:1 | covered | Used in the positivity step. |\n"
                "### Quantifier / Domain Coverage\n"
                "| Obligation | Proof Location | Status | Notes |\n"
                "| --- | --- | --- | --- |\n"
                f"| `for every r_0 > 0` | {proof_artifact_path}:1 | covered | No specialization introduced. |\n"
                "### Conclusion-Clause Coverage\n"
                "| Clause | Proof Location | Status | Notes |\n"
                "| --- | --- | --- | --- |\n"
                f"| annulus intersection holds | {proof_artifact_path}:1 | covered | Final sentence states it. |\n"
                "## Adversarial Probe\n"
                "- Probe type: dropped-parameter test\n"
                "- Result: The proof still references r_0, so the theorem remains global in the target radius.\n"
                "## Verdict\n"
                "- Scope status: `matched`\n"
                "- Quantifier status: `matched`\n"
                "- Counterexample status: `none_found`\n"
                "- Blocking gaps:\n"
                "  - None.\n"
                "## Required Follow-Up\n"
                "- None.\n"
            ),
            encoding="utf-8",
        )
    return manuscript_path


def test_phase_proof_review_bootstraps_manifest_and_turns_stale_after_edit(tmp_path: Path) -> None:
    phase_dir = tmp_path / "GPD" / "phases" / "01-proofs"
    phase_dir.mkdir(parents=True)
    summary_path = phase_dir / "01-SUMMARY.md"
    summary_path.write_text("# Summary\n", encoding="utf-8")
    verification_path = phase_dir / "01-VERIFICATION.md"
    verification_path.write_text("# Verification\n", encoding="utf-8")

    fresh = resolve_phase_proof_review_status(tmp_path, phase_dir, persist_manifest=True)

    assert fresh.state == "fresh"
    assert fresh.manifest_bootstrapped is True
    assert phase_proof_review_manifest_path(verification_path).exists()

    summary_path.write_text("# Summary\n\nUpdated theorem proof.\n", encoding="utf-8")

    stale = resolve_phase_proof_review_status(tmp_path, phase_dir)

    assert stale.state == "stale"
    assert stale.can_rely_on_prior_review is False
    assert summary_path in stale.changed_files


def test_manuscript_proof_review_bootstraps_manifest_and_turns_stale_after_edit(tmp_path: Path) -> None:
    manuscript_path = tmp_path / "paper" / "main.tex"
    manuscript_path.parent.mkdir(parents=True)
    manuscript_path.write_text(
        "\\documentclass{article}\n\\begin{document}\nProof.\n\\end{document}\n",
        encoding="utf-8",
    )

    review_dir = tmp_path / "GPD" / "review"
    review_dir.mkdir(parents=True)
    (review_dir / "CLAIMS.json").write_text(
        json.dumps(
            {
                "version": 1,
                "manuscript_path": "paper/main.tex",
                "manuscript_sha256": compute_sha256(manuscript_path),
                "claims": [
                    {
                        "claim_id": "CLM-001",
                        "claim_type": "main_result",
                        "text": "The manuscript makes a test claim.",
                        "artifact_path": "paper/main.tex",
                        "section": "Main Result",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (review_dir / "STAGE-math.json").write_text(
        json.dumps(
            {
                "version": 1,
                "round": 1,
                "stage_id": "math",
                "stage_kind": "math",
                "manuscript_path": "paper/main.tex",
                "manuscript_sha256": compute_sha256(manuscript_path),
                "claims_reviewed": ["CLM-001"],
                "summary": "math review",
                "strengths": ["checked proof"],
                "findings": [],
                "confidence": "high",
                "recommendation_ceiling": "minor_revision",
            }
        ),
        encoding="utf-8",
    )

    fresh = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert fresh.state == "fresh"
    assert fresh.manifest_bootstrapped is True
    assert manuscript_proof_review_manifest_path(manuscript_path).exists()

    manuscript_path.write_text(
        "\\documentclass{article}\n\\begin{document}\nRevised proof.\n\\end{document}\n",
        encoding="utf-8",
    )

    stale = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert stale.state == "stale"
    assert stale.can_rely_on_prior_review is False
    assert manuscript_path in stale.changed_files


def test_manuscript_proof_review_requires_proof_redteam_artifact_for_proof_bearing_manuscript(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(tmp_path, proof_redteam_status=None)

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "missing_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"


def test_manuscript_proof_review_rejects_nonpassing_proof_redteam_artifact(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(tmp_path, proof_redteam_status="gaps_found")

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "open_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"


def test_manuscript_proof_review_rejects_mismatched_proof_redteam_snapshot(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status="passed",
        proof_redteam_sha256="a" * 64,
    )

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "invalid_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert "manuscript_sha256" in status.detail


def test_manuscript_proof_review_rejects_incomplete_proof_redteam_body(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(tmp_path, proof_redteam_status="passed")
    (tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md").write_text(
        (
            "---\n"
            "status: passed\n"
            "reviewer: gpd-check-proof\n"
            "claim_ids:\n"
            "  - CLM-001\n"
            "proof_artifact_paths:\n"
            "  - paper/main.tex\n"
            "manuscript_path: paper/main.tex\n"
            f"manuscript_sha256: {compute_sha256(manuscript_path)}\n"
            "round: 1\n"
            "---\n\n"
            "# Proof Redteam\n"
        ),
        encoding="utf-8",
    )

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "invalid_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert "missing required sections" in status.detail


def test_manuscript_proof_review_anchors_to_passed_proof_redteam_artifact(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(tmp_path, proof_redteam_status="passed")

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert status.state == "fresh"
    assert status.can_rely_on_prior_review is True
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"
    assert manuscript_proof_review_manifest_path(manuscript_path).exists()


def test_manuscript_proof_review_uses_latest_matching_round_specific_proof_redteam(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status="passed",
        round_number=1,
    )
    _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status=None,
        round_number=2,
    )

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "missing_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM-R2.md"


def test_manuscript_proof_review_rejects_invalid_latest_round_anchor_without_falling_back(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status="passed",
        round_number=1,
    )
    _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status="passed",
        round_number=2,
    )
    (tmp_path / "GPD" / "review" / "CLAIMS-R2.json").write_text("{}", encoding="utf-8")

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "invalid_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "STAGE-math-R2.json"
    assert "STAGE-math-R2.json" in status.detail


def test_manuscript_proof_review_rejects_unreadable_latest_stage_math_without_falling_back(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status="passed",
        round_number=1,
    )
    _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status="passed",
        round_number=2,
    )
    (tmp_path / "GPD" / "review" / "STAGE-math-R2.json").write_text("{not json", encoding="utf-8")

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "invalid_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "STAGE-math-R2.json"
    assert "STAGE-math-R2.json" in status.detail


def test_manuscript_proof_review_turns_stale_after_bibliography_edit(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(tmp_path, proof_redteam_status="passed")
    bibliography_path = tmp_path / "paper" / "references.bib"

    fresh = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert fresh.state == "fresh"

    bibliography_path.write_text("@article{demo,title={Updated Demo}}\n", encoding="utf-8")

    stale = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert stale.state == "stale"
    assert stale.can_rely_on_prior_review is False
    assert bibliography_path in stale.changed_files


def test_manuscript_proof_review_turns_stale_after_proof_redteam_edit(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(tmp_path, proof_redteam_status="passed")
    proof_redteam_path = tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"

    fresh = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert fresh.state == "fresh"

    proof_redteam_path.write_text(proof_redteam_path.read_text(encoding="utf-8") + "\n<!-- drift -->\n", encoding="utf-8")

    stale = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert stale.state == "stale"
    assert stale.can_rely_on_prior_review is False
    assert proof_redteam_path in stale.changed_files


def test_manuscript_proof_review_turns_stale_after_external_proof_artifact_edit(tmp_path: Path) -> None:
    manuscript_path = _write_proof_bearing_manuscript_review_artifacts(
        tmp_path,
        proof_redteam_status="passed",
        proof_artifact_path="proofs/external-proof.tex",
    )
    external_proof_path = tmp_path / "proofs" / "external-proof.tex"

    fresh = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert fresh.state == "fresh"
    assert external_proof_path in fresh.watched_files

    external_proof_path.write_text(
        "\\documentclass{article}\n\\begin{document}\nRevised external proof.\n\\end{document}\n",
        encoding="utf-8",
    )

    stale = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert stale.state == "stale"
    assert stale.can_rely_on_prior_review is False
    assert external_proof_path in stale.changed_files
