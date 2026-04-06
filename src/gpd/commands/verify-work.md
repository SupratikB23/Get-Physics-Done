---
name: gpd:verify-work
description: Verify research results through physics consistency checks
argument-hint: "[phase] [--dimensional] [--limits] [--convergence] [--regression] [--all]"
context_mode: project-required
requires:
  files: ["GPD/ROADMAP.md"]
review-contract:
  review_mode: review
  schema_version: 1
  required_outputs:
    - "GPD/phases/XX-name/XX-VERIFICATION.md"
  required_evidence:
    - roadmap
    - phase summaries
    - artifact files
  blocking_conditions:
    - missing project state
    - missing roadmap
    - missing phase artifacts
    - degraded review integrity
  preflight_checks:
    - command_context
    - project_state
    - roadmap
    - phase_lookup
    - phase_artifacts
    - phase_summaries
    - phase_proof_review
  required_state: phase_executed
allowed-tools:
  - file_read
  - shell
  - find_files
  - search_files
  - file_edit
  - file_write
  - task
  - mcp__gpd_verification__get_bundle_checklist
  - mcp__gpd_verification__suggest_contract_checks
  - mcp__gpd_verification__run_contract_check
---

<!-- Tool names and @ includes are platform-specific. The installer translates paths for your runtime. -->
<!-- Allowed-tools are runtime-specific. Other platforms may use different tool interfaces. -->

<objective>
Verify research results through systematic physics checks with persistent state.

Purpose: Confirm that derivations are correct, numerical results are trustworthy, and physical conclusions are sound. One check at a time, plain text responses, no interrogation. When issues are found, automatically diagnose, classify severity, and prepare for resolution.

Output: `GPD/phases/XX-name/XX-VERIFICATION.md` tracking all check results. This workflow is only valid once the phase has reached the `phase_executed` state. If issues are found, return diagnosed gaps with severity classification and verified fix plans ready for `gpd:execute-phase`.

Physics verification is fundamentally different from software testing. A software test has a binary pass/fail; a physics check has degrees of agreement, expected approximation errors, and regime-dependent validity. The verification framework accounts for this.
</objective>

<execution_context>
@{GPD_INSTALL_DIR}/workflows/verify-work.md
@{GPD_INSTALL_DIR}/references/verification/core/verification-core.md
@{GPD_INSTALL_DIR}/templates/verification-report.md
@{GPD_INSTALL_DIR}/templates/contract-results-schema.md
</execution_context>

<context>
Phase: $ARGUMENTS (optional)
- If provided: Verify specific phase (e.g., "4")
- If not provided: Check for active sessions or prompt for phase

@GPD/STATE.md
@GPD/ROADMAP.md
</context>

<process>
**CRITICAL: First, read the full workflow file using the file_read tool:**
Read the file at {GPD_INSTALL_DIR}/workflows/verify-work.md — this contains the complete step-by-step instructions. Do NOT improvise. Follow the workflow file exactly.

Execute the workflow end-to-end and preserve its session, diagnosis, fix-planning, and routing gates.
The workflow file owns the detailed check taxonomy; this wrapper only bootstraps the canonical verification surfaces and delegates the physics checks.

## Severity Classification

- **CRITICAL** — Result is wrong (dimensional error, symmetry violation, sign error). Blocks all downstream work.
- **MAJOR** — Result may be wrong (failed limiting case, numerical non-convergence). Must be resolved before conclusions are drawn.
- **MINOR** — Result is probably correct but incompletely validated (missing one limiting case, no error bars on a qualitative plot). Should be resolved before publication.
- **NOTE** — Observation for the record (e.g., "convergence is slow but adequate", "agrees with Smith et al. to 3 significant figures").

**For deeper focused analysis**, use the dedicated commands: `gpd:dimensional-analysis` (unit consistency), `gpd:limiting-cases` (known limit recovery), or `gpd:numerical-convergence` (convergence testing).
  </process>
