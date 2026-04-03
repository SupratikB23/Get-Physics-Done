from __future__ import annotations

from pathlib import Path

from gpd.core.proof_review import (
    manuscript_has_theorem_bearing_language,
    manuscript_proof_review_manifest_path,
    phase_proof_review_manifest_path,
    resolve_manuscript_proof_review_status,
    resolve_phase_proof_review_status,
)
from tests.manuscript_test_support import CANONICAL_MANUSCRIPT_STEM, write_proof_review_package


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
    manuscript_path = write_proof_review_package(tmp_path, theorem_bearing=False, review_report=False).manuscript_path

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
    manuscript_path = write_proof_review_package(tmp_path, theorem_bearing=True, review_report=False, proof_redteam_status=None).manuscript_path

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "missing_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"


def test_manuscript_theorem_language_scan_follows_nested_section_files(tmp_path: Path) -> None:
    manuscript_path = write_proof_review_package(tmp_path, theorem_bearing=False, review_report=False).manuscript_path
    manuscript_path.write_text(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\\input{sections/results}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    section_path = tmp_path / "paper" / "sections" / "results.tex"
    section_path.parent.mkdir(parents=True, exist_ok=True)
    section_path.write_text(
        "\\begin{theorem}For every r_0 > 0, the orbit intersects the target annulus.\\end{theorem}\n"
        "\\begin{proof}Nested section proof.\\end{proof}\n",
        encoding="utf-8",
    )

    assert manuscript_path.name == f"{CANONICAL_MANUSCRIPT_STEM}.tex"
    assert manuscript_has_theorem_bearing_language(tmp_path, manuscript_path) is True


def test_manuscript_proof_review_rejects_nonpassing_proof_redteam_artifact(tmp_path: Path) -> None:
    manuscript_path = write_proof_review_package(tmp_path, theorem_bearing=True, review_report=True, proof_redteam_status="gaps_found").manuscript_path

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "open_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"


def test_manuscript_proof_review_rejects_mismatched_proof_redteam_snapshot(tmp_path: Path) -> None:
    manuscript_path = write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=True,
        proof_redteam_status="passed",
        proof_redteam_sha256="a" * 64,
    ).manuscript_path

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "invalid_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert "manuscript_sha256" in status.detail


def test_manuscript_proof_review_rejects_incomplete_proof_redteam_body(tmp_path: Path) -> None:
    package = write_proof_review_package(tmp_path, theorem_bearing=True, review_report=True, proof_redteam_status="passed")
    manuscript_path = package.manuscript_path
    (tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md").write_text(
        (
            "---\n"
            "status: passed\n"
            "reviewer: gpd-check-proof\n"
            "claim_ids:\n"
            "  - CLM-001\n"
            "proof_artifact_paths:\n"
            "  - paper/curvature_flow_bounds.tex\n"
            "manuscript_path: paper/curvature_flow_bounds.tex\n"
            f"manuscript_sha256: {package.manuscript_sha256}\n"
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
    manuscript_path = write_proof_review_package(tmp_path, theorem_bearing=True, review_report=True, proof_redteam_status="passed").manuscript_path

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert status.state == "fresh"
    assert status.can_rely_on_prior_review is True
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"
    assert manuscript_proof_review_manifest_path(manuscript_path).exists()


def test_manuscript_proof_review_uses_latest_matching_round_specific_proof_redteam(tmp_path: Path) -> None:
    manuscript_path = write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=True,
        proof_redteam_status="passed",
        round_number=1,
    ).manuscript_path
    write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=False,
        proof_redteam_status=None,
        round_number=2,
    )

    status = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert status.state == "missing_required_artifact"
    assert status.can_rely_on_prior_review is False
    assert status.anchor_artifact == tmp_path / "GPD" / "review" / "PROOF-REDTEAM-R2.md"


def test_manuscript_proof_review_rejects_invalid_latest_round_anchor_without_falling_back(tmp_path: Path) -> None:
    manuscript_path = write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=True,
        proof_redteam_status="passed",
        round_number=1,
    ).manuscript_path
    write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=True,
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
    manuscript_path = write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=True,
        proof_redteam_status="passed",
        round_number=1,
    ).manuscript_path
    write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=True,
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
    manuscript_path = write_proof_review_package(tmp_path, theorem_bearing=True, review_report=True, proof_redteam_status="passed").manuscript_path
    bibliography_path = tmp_path / "paper" / "references.bib"

    fresh = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert fresh.state == "fresh"

    bibliography_path.write_text("@article{demo,title={Updated Demo}}\n", encoding="utf-8")

    stale = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert stale.state == "stale"
    assert stale.can_rely_on_prior_review is False
    assert bibliography_path in stale.changed_files


def test_manuscript_proof_review_turns_stale_after_proof_redteam_edit(tmp_path: Path) -> None:
    manuscript_path = write_proof_review_package(tmp_path, theorem_bearing=True, review_report=True, proof_redteam_status="passed").manuscript_path
    proof_redteam_path = tmp_path / "GPD" / "review" / "PROOF-REDTEAM.md"

    fresh = resolve_manuscript_proof_review_status(tmp_path, manuscript_path, persist_manifest=True)

    assert fresh.state == "fresh"

    proof_redteam_path.write_text(proof_redteam_path.read_text(encoding="utf-8") + "\n<!-- drift -->\n", encoding="utf-8")

    stale = resolve_manuscript_proof_review_status(tmp_path, manuscript_path)

    assert stale.state == "stale"
    assert stale.can_rely_on_prior_review is False
    assert proof_redteam_path in stale.changed_files


def test_manuscript_proof_review_turns_stale_after_external_proof_artifact_edit(tmp_path: Path) -> None:
    manuscript_path = write_proof_review_package(
        tmp_path,
        theorem_bearing=True,
        review_report=True,
        proof_redteam_status="passed",
        proof_artifact_relpath="proofs/external-proof.tex",
    ).manuscript_path
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
