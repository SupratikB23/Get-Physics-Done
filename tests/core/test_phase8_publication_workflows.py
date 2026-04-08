from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = REPO_ROOT / "src/gpd/specs/workflows"


def test_write_paper_balanced_mode_keeps_outline_as_working_draft_and_threads_mode_context() -> None:
    workflow = (WORKFLOWS_DIR / "write-paper.md").read_text(encoding="utf-8")

    assert "Do not force a routine outline-approval pause in balanced mode." in workflow
    assert (
        "If `autonomy=supervised`, present the outline for approval before proceeding. "
        "If `autonomy=balanced`, treat the outline as a working draft"
    ) in workflow
    assert "Present outline for approval before proceeding." not in workflow
    assert "<autonomy_mode>{AUTONOMY}</autonomy_mode>" in workflow
    assert "<research_mode>{RESEARCH_MODE}</research_mode>" in workflow
    assert workflow.count("<autonomy_mode>{AUTONOMY}</autonomy_mode>") >= 3
    assert workflow.count("<research_mode>{RESEARCH_MODE}</research_mode>") >= 3
    assert "Treat the emitted `.tex` file as the success artifact gate for each section." in workflow
    assert "Treat `${PAPER_DIR}/CITATION-AUDIT.md` and the refreshed `${PAPER_DIR}/BIBLIOGRAPHY-AUDIT.json` as the bibliography success gate." in workflow
    assert "Confirm `${PAPER_DIR}/BIBLIOGRAPHY-AUDIT.json` exists after the refresh before proceeding to reproducibility or strict review." in workflow


def test_respond_to_referees_balanced_mode_does_not_force_parse_confirmation() -> None:
    workflow = (WORKFLOWS_DIR / "respond-to-referees.md").read_text(encoding="utf-8")

    assert "research_mode" in workflow
    assert "RESEARCH_MODE=$(echo \"$INIT\" | gpd json get .research_mode --default balanced)" in workflow
    assert (
        "Present the parsed structure. Ask for explicit user confirmation only in supervised mode or when the report source is ambiguous; "
        "balanced mode should treat the parse as working context"
    ) in workflow
    assert "Present the parsed structure for user confirmation:" not in workflow
    assert "<autonomy_mode>{AUTONOMY}</autonomy_mode>" in workflow
    assert "<research_mode>{RESEARCH_MODE}</research_mode>" in workflow
    assert "Treat `GPD/AUTHOR-RESPONSE{round_suffix}.md` and `GPD/review/REFEREE_RESPONSE{round_suffix}.md` as the response success gate." in workflow
    assert "Confirm the refreshed JSON artifact exists before treating the round as complete." in workflow


def test_peer_review_stage_six_requires_report_artifacts_and_threads_mode_context() -> None:
    workflow = (WORKFLOWS_DIR / "peer-review.md").read_text(encoding="utf-8")

    assert "Parse JSON for: `project_exists`, `state_exists`, `commit_docs`, `autonomy`, `research_mode`" in workflow
    assert "RESEARCH_MODE=$(echo \"$INIT\" | gpd json get .research_mode --default balanced)" in workflow
    assert "<autonomy_mode>{AUTONOMY}</autonomy_mode>" in workflow
    assert "<research_mode>{RESEARCH_MODE}</research_mode>" in workflow
    assert "Treat the referee report files as required final-stage artifacts." in workflow
    assert "Also confirm `GPD/REFEREE-REPORT{round_suffix}.md` and `GPD/REFEREE-REPORT{round_suffix}.tex` exist before treating the final recommendation as complete." in workflow
    assert "GPD/REFEREE-REPORT{round_suffix}.md" in workflow
    assert "GPD/REFEREE-REPORT{round_suffix}.tex" in workflow
