"""Regression tests for verification scaffold and workflow surface alignment."""

from __future__ import annotations

from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "src" / "gpd" / "specs" / "templates"
WORKFLOWS_DIR = Path(__file__).resolve().parents[2] / "src" / "gpd" / "specs" / "workflows"


def _read(relative_path: str) -> str:
    return (Path(__file__).resolve().parents[2] / relative_path).read_text(encoding="utf-8")


def test_verification_scaffolds_surface_closed_comparison_kind_enum_without_blank_placeholder() -> None:
    research_verification = _read("src/gpd/specs/templates/research-verification.md")
    verify_workflow = _read("src/gpd/specs/workflows/verify-work.md")

    expected_enum = "comparison_kind: [benchmark | prior_work | experiment | cross_method | baseline | other]"
    omit_instruction = "omit both `comparison_kind` and `comparison_reference_id` instead of leaving blank placeholders"

    assert expected_enum in research_verification
    assert expected_enum in verify_workflow
    assert "comparison_kind: [benchmark | prior_work | experiment | cross_method | baseline | other | \"\"]" not in research_verification
    assert "comparison_kind: [benchmark | prior_work | experiment | cross_method | baseline | other | \"\"]" not in verify_workflow
    assert omit_instruction in research_verification
    assert omit_instruction in verify_workflow


def test_verification_report_strict_pass_guidance_includes_reference_coverage_rules() -> None:
    verification_report = _read("src/gpd/specs/templates/verification-report.md")

    assert "status: passed` is strict" in verification_report
    assert "every claim, deliverable, and acceptance_test entry in `contract_results` is `passed`" in verification_report
    assert "every reference entry is `completed`" in verification_report
    assert "every `must_surface` reference has all `required_actions` recorded in `completed_actions`" in verification_report
    assert "suggested_contract_checks" in verification_report
    assert "status: passed" in verification_report


def test_verification_guidance_surfaces_the_same_canonical_suggestion_contract() -> None:
    research_verification = _read("src/gpd/specs/templates/research-verification.md")
    verify_workflow = _read("src/gpd/specs/workflows/verify-work.md")

    expected_suggestion = "suggested_contract_checks"
    decisive_gap_text = "required_actions including `compare` is still incomplete"

    assert expected_suggestion in research_verification
    assert expected_suggestion in verify_workflow
    assert decisive_gap_text in research_verification
    assert decisive_gap_text in verify_workflow
    assert "same canonical schema surface" in research_verification
    assert "frontmatter contract compatible with `@{GPD_INSTALL_DIR}/templates/verification-report.md`" in verify_workflow
