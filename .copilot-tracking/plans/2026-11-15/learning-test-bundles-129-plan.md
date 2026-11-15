<!-- markdownlint-disable-file -->
# RPI Plan: Journey Learning-Test Bundles and Role-Screen Scenario Verification (Issue #129)

## Task Metadata

* Task ID: issue-129-learning-test-bundles-0023
* Task slug: learning-test-bundles-129
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/learning-test-bundles-129-plan-critique.md

## Executive Summary

This plan completes the code-testable learning-test bundle contracts and specialist role-screen scenario verification for Issue #129 (`Refs #129`) on `feat/ux-129-learning-test-bundles-0023`. It enriches `zava_forward.core.learning_test_bundles.Bundle` and `compare_bundle` with additive, backward-compatible PRD and UX-protocol metadata (`title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, and `stop_rule`), closes the fifth-bundle (`funding-evidence`) and resident-effort-shift coverage gaps in `src/core/tests/test_learning_test_bundles.py`, and adds `src/api/tests/test_learning_test_bundle_scenarios.py` to execute constructed two-arm comparisons alongside real Node-VM renders of `role-screens.js` and `aftercare.js` (backed by `AftercareService`) across all five candidate bundles while preserving the protocol's screen-wiring and run-storage governance gate.

### User Decisions and Requirements Highlights

* Complete `plan`, `plan-critique`, `implement`, and `review` for Issue #129 on `feat/ux-129-learning-test-bundles-0023`, implement learning-test bundle and role-screen scenario verification in `src/core/tests/` and `src/api/tests/`, run focused tests plus `ruff` and `mypy`, and leave one clean frozen local commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
* Keep Opportunities `O10` and `O18` to `O20` out of scope, label saved minutes as `capacity` until Finance validates them, and keep human/resident approval, Atlas-owner mapping confirmation, DPO retention, and live usability-study boundaries explicit (`Refs #129`, never `Closes #129`).

### What You May Not Know

* `docs/reference/research/ux/journey-learning-test-bundles.md` (lines 102-103) explicitly prohibits wiring `learning_test_bundles.py` to a runtime screen or storing run records until Atlas-owner confirmation and the DPO representative-data retention decision clear. Scenario verification in `src/api/tests/` therefore tests the real rendered specialist role screens (`role-screens.js` and `aftercare.js`) against `learning_test_bundles` without adding an unratified bundle-runner route or UI table.
* In `src/api/pyproject.toml`, `zava_forward.core.*` is configured with `follow_imports = "skip"` under `mypy --strict`; any helper in `src/api/tests/` calling `zava_forward.core` functions must carry explicit return and parameter type annotations to avoid `no-any-return` failures.

### Unresolved Decisions or Blockers

* None for this slice. Human governance prerequisites (Atlas-owner mapping confirmation including `O16`, DPO retention decision, live facilitator runs, and Finance cashable-benefit validation) remain explicitly tracked as open follow-up gates under `Refs #129`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Continue from `.copilot-tracking/research/2026-11-15/learning-test-bundles-129-research.md` and complete the full automatic RPI loop (`plan`, `plan-critique`, `implement`, `review`) for Issue #129 on `feat/ux-129-learning-test-bundles-0023` (user prompt, 2026-11-15).
* Implement learning-test bundle and role-screen scenario verification in `src/core/tests/` and `src/api/tests/` covering all five candidate bundles (including Bundle 5 / `handover-aftercare` accessible handover and aftercare, `funding-evidence` fifth-item parity, non-AI comparators, six-component net-effort rules, and stop rules) (user prompt, 2026-11-15; `.copilot-tracking/reviews/2026-11-14/129-learning-bundles-1848-review.md`).
* Preserve `docs/reference/research/ux/journey-learning-test-bundles.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` (Decisions 1-5), and `docs/prds/zava-forward-retrofit-programme-demonstrator.md` ("Candidate journey learning tests"): exclude `O10` and `O18`-`O20`, require explicit single-owner `o16_counted_under` reconciliation for `O16`, require `representative_data_retained is False`, and keep saved minutes labelled as `capacity` until Finance validates them.
* Run focused unit tests plus `ruff` and `mypy`, write `.copilot-tracking/changes/` and `.copilot-tracking/reviews/` artifacts, and commit locally with `Refs #129` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (user prompt, 2026-11-15).

## Goals

* Make every PRD and UX-protocol bundle attribute (`title`, `atlas_ids`, `linked_requirements`, `comparator`, `zero_measures`, `learning_question`, `beyond_effort_measures`, and `stop_rule`) deterministic and code-testable in `zava_forward.core.learning_test_bundles` without breaking existing positional callers or the `learning-bundle-constructed-input-v1` stdin CLI contract.
* Prove full five-bundle parity, resident-effort-transfer non-saving (`NFR-009`), per-measure target-zero stop-rule activation, and cross-bundle `O16` single-counting reconciliation in `src/core/tests/test_learning_test_bundles.py`.
* Prove constructed two-arm bundle-to-role-screen scenario alignment across all five bundles in `src/api/tests/test_learning_test_bundle_scenarios.py` by rendering the real `role-screens.js` and `aftercare.js` views in Node VM alongside `AftercareService` and `learning_test_bundles`, while verifying that no unapproved bundle-runner screen or run-storage endpoint is exposed.

## Scope and Non-Goals

### In Scope

* Additive protocol metadata fields on `Bundle` and `compare_bundle` in `src/core/src/zava_forward/core/learning_test_bundles.py` and concise documentation synchronization in `src/core/README.md`.
* Expanded five-bundle unit tests in `src/core/tests/test_learning_test_bundles.py`.
* New specialist role-screen and aftercare bundle scenario verification test module `src/api/tests/test_learning_test_bundle_scenarios.py`.
* Focused validation (`ruff check`, `ruff format --check`, `mypy`, and targeted `unittest` runs across `src/core` and `src/api`, including existing role-screen conformance, accessibility baseline, content standard, and UX traceability guardrails).

### Non-Goals

* Opportunities `O10`, `O18`, `O19`, and `O20` (explicitly excluded by ADR 0003 Decision 4).
* Adding an interactive bundle-runner screen in `role-screens.js`, adding `/api/...` routes in `server.py`, or persisting experiment run records before Atlas-owner confirmation and DPO retention approval.
* Claiming live human usability execution, Atlas-owner mapping ratification, DPO approval, Finance cashable savings, or `Closes #129`.
* Pushing commits to `origin` or opening/updating a pull request.

## Functional Requirements

* FR-1: `zava_forward.core.learning_test_bundles.Bundle` and `BUNDLES` shall expose canonical `title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, and `stop_rule` values matching `docs/reference/research/ux/journey-learning-test-bundles.md` and `docs/prds/zava-forward-retrofit-programme-demonstrator.md` for all five bundles (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`), and `compare_bundle` shall include `bundle_title`, `atlas_ids`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, and `stop_rule` in its returned report dictionary while preserving all existing keys, `render_report` formatting, and `learning-bundle-constructed-input-v1` validation.
  * Observable acceptance criteria: AC-1, AC-2.
* FR-2: `src/core/tests/test_learning_test_bundles.py` shall verify all five bundles' non-AI comparators, canonical protocol metadata, `O10`/`O18`-`O20` exclusion, resident-effort shift non-saving (`NFR-009`), target-zero breach detection across all six zero measures across the five bundles, and five-bundle constructed campaign execution with `reconcile_o16`.
  * Observable acceptance criteria: AC-2, AC-3.
* FR-3: `src/api/tests/test_learning_test_bundle_scenarios.py` shall verify constructed two-arm scenarios for all five bundles (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`) against real Node-VM renders of `src/api/src/zava_forward/api/web/role-screens.js` and `src/api/src/zava_forward/api/web/aftercare.js` (including real `AftercareService` handover/financial closure with open concern state), asserting both clean comparator/workflow comparisons and stop-rule triggers for plain-language boundary violations, plus absence of unapproved bundle-runner screens or stored run routes.
  * Observable acceptance criteria: AC-4, AC-5.

## Non-Functional Requirements

* NFR-1: Static quality, strict typing, and focused validation discipline (owner decision D4 / #1294).
  * Objective threshold or evaluation condition: Zero errors from `ruff check .`, `ruff format --check .`, and `mypy` in both `src/core` and `src/api`, and 100% pass across targeted unit and conformance tests.
  * Operating condition or verification approach, if needed: Run commands from `src/core` and `src/api` with repository-documented `PYTHONPATH` and isolated temporary directories (`ZF_DATA` untouched).
  * Observable acceptance criteria: AC-6.
* NFR-2: Governance and tracking-hygiene preservation.
  * Objective threshold or evaluation condition: Zero `.copilot-tracking/` references in production source, code comments, docstrings, or commit messages; `representative_data_retained` enforced as `False`; saved minutes framed strictly as `capacity`; commit message uses `Refs #129` and required `Co-authored-by` trailer with zero remote push.
  * Observable acceptance criteria: AC-5, AC-7.

## Acceptance Criteria

* AC-1: Each entry in `learning_test_bundles.BUNDLES` carries backward-compatible fields `(key, atlas_ids, comparator, zero_measures, title, linked_requirements, learning_question, beyond_effort_measures, stop_rule)` matching the PRD and `docs/reference/research/ux/journey-learning-test-bundles.md`, and `src/core/README.md` accurately reflects the helper contract.
* AC-2: Existing `learning-bundle-constructed-input-v1` stdin CLI invocations, refusal cases, and `render_report` stop-first outputs remain 100% backward-compatible.
* AC-3: `src/core/tests/test_learning_test_bundles.py` passes assertions covering all five bundles (including `funding-evidence`), non-AI comparator wording, every target-zero measure breach, resident-effort transfer non-saving (`NFR-009`), and five-bundle `reconcile_o16` consistency.
* AC-4: `src/api/tests/test_learning_test_bundle_scenarios.py` renders real `role-screens.js` (`resident-choice`, `resident-service-issues`, `programme-queue`, `procurement-packages`, `contractor-job-pack`, `technical-queue`, `quality-queue`, `finance-funding`, `finance-invoices`) and `aftercare.js` (`receiptView`, `evaluatorView` over `AftercareService`) in Node VM and proves each of the five bundles' plain-language stop-rule boundaries, non-colour text cues, AI-unavailable manual continuity, and constructed two-arm `run_report` scoring.
* AC-5: Automated tests explicitly verify that `O10` and `O18`-`O20` remain excluded and that no unapproved learning-bundle screen (`registerRoleScreen`) or stored run endpoint exists while Atlas-owner confirmation and DPO retention remain open.
* AC-6: `ruff check .`, `ruff format --check .`, `mypy`, and targeted `unittest` suites pass in `src/core` and `src/api`.
* AC-7: Implementation records and repository-local privacy-safe noreply `user.email` (`8036360+jmservera@users.noreply.github.com`) are configured in `P03-T02` before Review freeze, enabling `rpi-review` to write its read-only review log and the automatic RPI parent to commit all workspace changes and dated `.copilot-tracking/` artifacts cleanly on `feat/ux-129-learning-test-bundles-0023` with `Refs #129`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and no push.

## Test Ownership, Change Bounds, and Validation Lock

* Applicable test ownership:
  * `src/core/tests/test_learning_test_bundles.py` owns pure unit, metadata, NFR-009 effort-accounting, O16 reconciliation, and stdin CLI regression coverage for `zava_forward.core.learning_test_bundles`.
  * `src/api/tests/test_learning_test_bundle_scenarios.py` owns cross-layer scenario verification linking `zava_forward.core.learning_test_bundles` to rendered `role-screens.js`, `aftercare.js`, `AftercareService`, and API/screen governance boundaries.
* Exact file/test removals: `none`.
* Maximum file/test additions:
  * Production files added: `0` (in-place additive update to `src/core/src/zava_forward/core/learning_test_bundles.py` and `src/core/README.md` only; `role-screens.js` and `aftercare.js` unchanged).
  * Test files added: `1` (`src/api/tests/test_learning_test_bundle_scenarios.py`), plus up to `4` focused test methods added in `src/core/tests/test_learning_test_bundles.py` and up to `7` focused test methods in `src/api/tests/test_learning_test_bundle_scenarios.py`.
* Canonical vs generated targets:
  * Canonical edited/created targets: `src/core/src/zava_forward/core/learning_test_bundles.py`, `src/core/README.md`, `src/core/tests/test_learning_test_bundles.py`, `src/api/tests/test_learning_test_bundle_scenarios.py`.
  * Generated targets: `none`.
* Semantic vs regression coverage:
  * Semantic coverage: PRD/protocol metadata alignment across all 5 bundles, NFR-009 resident-effort transfer non-saving, per-bundle stop-rule firing, and rendered specialist role-screen + aftercare stop-rule boundary verification across Bundles 1-5.
  * Regression coverage: Existing 22 CLI/scorer unit tests in `test_learning_test_bundles.py` plus existing API/UI guardrail tests (`test_role_screens.py`, `test_role_screens_conformance.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_aftercare_screen.py`).
* Validation tier and basis:
  * **Focused tier** (owner decision D4 / #1294): small bounded core metadata + unit/scenario test slice with no infrastructure, deployment, SQL schema, Dockerfile, workflow, dependency-manifest, or security-control change. Hosted CI is unobserved locally because the caller instructed not to push.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md                                                                     |
| Phase details                    | .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md                                                          |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/learning-test-bundles-129-plan-critique.md (`Complete`, `Pass`, 0 findings)                   |
| Relevant research                | .copilot-tracking/research/2026-11-15/learning-test-bundles-129-research.md (`Planning Readiness: Ready`, `C1`-`C12`)                    |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md is created by implementation as its evidence record            |
| Planning execution and readiness | Ready for implementation after passing single final-candidate `rpi-plan-critique`                                                        |
| Continuation context             | Confirmed automatic RPI Agent parent continues to `Implement` and `Review` after critique gates pass                                     |

## Sources

* `.copilot-tracking/research/2026-11-15/learning-test-bundles-129-research.md`: Cycle 1 three-wave synthesis (`C1`-`C12`) and selected convergence Option 1.
* `docs/reference/research/ux/journey-learning-test-bundles.md`: Canonical five-bundle table, comparators, NFR-009 six-component effort rules, per-bundle learning questions and beyond-effort measures, stop rules, and screen/storage gate.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Candidate journey learning tests table and linked requirements (`FR-008`, `FR-014`, `FR-019`, `FR-042`, `FR-043`, `FR-045`, `FR-048`, `FR-049`, `AC-011`, `AC-013`, `AC-050`, `AC-051`, `AC-062` to `AC-065`, `GOAL-004`, `NFR-009`).
* `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`: Decisions 1-5 governing deterministic state, server-side authority/closure rules, bounded assistants, non-AI comparators, `O10`/`O18`-`O20` exclusion, and capacity-until-Finance-validates framing.
* `src/core/src/zava_forward/core/learning_test_bundles.py` and `src/core/tests/test_learning_test_bundles.py`: Current core scorer, CLI validator, and 4-bundle AC1 test baseline.
* `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/aftercare.js`, and `src/api/tests/test_aftercare_screen.py`: Specialist role-screen and aftercare contracts and Node-VM test harness patterns.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Protocol Metadata Enrichment and Five-Bundle Unit Coverage

* Intent: Enrich `Bundle` and `compare_bundle` in `zava_forward.core.learning_test_bundles` with full PRD/protocol metadata and prove complete five-bundle parity, NFR-009 effort rules, target-zero stop firing, and O16 reconciliation in `src/core/tests/test_learning_test_bundles.py`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add backward-compatible protocol metadata to `learning_test_bundles.py` and update `src/core/README.md`

* Requirement and evidence: FR-1, AC-1, AC-2 (`C1`, `C2`, `C4`).
* Expected result: `Bundle` exposes `title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, and `stop_rule` with safe defaults preserving 4-argument positional construction; `BUNDLES` populates all five bundles verbatim from the protocol and PRD; `compare_bundle` surfaces the read-only metadata fields without changing `zero_measures`, `render_report`, or `_validate_input`; `src/core/README.md` documents the enriched report metadata.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Expand `src/core/tests/test_learning_test_bundles.py` for full five-bundle, NFR-009, and target-zero parity

* Requirement and evidence: FR-2, AC-2, AC-3, AC-5 (`C1`, `C4`, `C5`, `C12`).
* Expected result: `test_learning_test_bundles.py` verifies all five bundles (including `funding-evidence`), canonical titles/Atlas IDs/linked requirements/questions/beyond-effort measures/stop rules, resident-effort transfer non-saving, every target-zero measure breach across all five bundles, and a reconciled five-bundle constructed campaign (`reconcile_o16`).
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Specialist Role-Screen and Aftercare Bundle Scenario Verification

* Intent: Add `src/api/tests/test_learning_test_bundle_scenarios.py` verifying constructed two-arm scenarios for all five bundles against real Node-VM renders of `role-screens.js` and `aftercare.js` (with `AftercareService`), plus protocol screen/storage governance invariants.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Create `src/api/tests/test_learning_test_bundle_scenarios.py` covering Bundles 1-5 and governance boundaries

* Requirement and evidence: FR-3, NFR-1, AC-4, AC-5 (`C1`, `C3`, `C6`, `C7`, `C8`, `C9`, `C10`, `C11`).
* Expected result: Typed (`mypy --strict` clean) `unittest` suite rendering `role-screens.js` and `aftercare.js` in Node VM with constructed two-arm cases scored through `learning_test_bundles.run_report` and `reconcile_o16` across `story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare` (including `AftercareService` open concern surviving handover and financial closure), and `funding-evidence`, plus static verification that no unapproved bundle-runner screen or stored run route is wired.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Validation, Implementation Reconciliation, and Commit Readiness

* Intent: Execute focused `ruff`, `mypy`, and `unittest` checks across `src/core` and `src/api`, reconcile `.copilot-tracking/changes/` and plan/detail markers before Review freeze, and configure repository-local privacy-safe Git author identity so the automatic RPI parent can commit the frozen reviewed branch on `feat/ux-129-learning-test-bundles-0023` without pushing.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run focused linters, strict typechecks, and unit/guardrail test suites in `src/core` and `src/api`

* Requirement and evidence: NFR-1, NFR-2, AC-6 (`C10`, `C11`).
* Expected result: `ruff check .`, `ruff format --check .`, `mypy`, and targeted `unittest` suites in `src/core` and `src/api` pass with zero errors and zero `.copilot-tracking/` leakage in non-tracking files.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Reconcile RPI implementation records and configure local noreply commit readiness

* Requirement and evidence: NFR-2, AC-7 (repository Branch and Pull Request Workflow instructions; caller prompt).
* Expected result: `.copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md`, plan markers, and phase details are reconciled before `rpi-review` freeze, and repository-local `git config --local user.email` is set to the authenticated GitHub noreply email (`8036360+jmservera@users.noreply.github.com`) so post-Review closeout commits cleanly on `feat/ux-129-learning-test-bundles-0023` with `Refs #129` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md

## Dependencies

* Node.js runtime (`node`) available on `PATH`: required by `src/api/tests/` Node-VM screen rendering tests (`test_aftercare_screen.py`, `test_technical_quality_screens.py`, `test_learning_test_bundle_scenarios.py`).
* Local editable/installed `src/core` and `src/api` packages plus `ruff` and `mypy` in the Python environment: verified via `src/core/pyproject.toml` and `src/api/pyproject.toml`.
* Open external human dependencies (not resolved in code): Atlas-owner confirmation of bundle-to-opportunity mapping (`O16` overlap), DPO representative-data retention decision, live participant bundle runs, and Finance benefit validation.

## Critique Disposition

Single final-candidate `rpi-plan-critique` completed at `.copilot-tracking/reviews/plans/2026-11-15/learning-test-bundles-129-plan-critique.md` (`Execution status: Complete`, `Verdict: Pass`, `0` Critical/High/Medium/Low `PC-xxx` findings).

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| 2026-11-15 pass (`none`) | Accepted (`Pass`) | Zero actionable defects; noted `roleScreensView()` stage-map routing and `Contractor` role scope for `contractor-job-pack` in `P02-T01`, with human Atlas-owner, DPO, live-run, and Finance gates retained as explicit follow-ups under `Refs #129` |

## Follow-Up Items

* Atlas-owner confirmation of bundle-to-opportunity mapping, including whether `O16` belongs to both `change-impact` and `funding-evidence` or one owning bundle (`docs/reference/research/ux/journey-learning-test-bundles.md`, human owner gate).
* DPO decision on representative-data retention before any run retains representative data or stores run records (`docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, DPO gate).
* Facilitator-run live bundle experiments (#129 / #155) and Finance validation before saved capacity minutes can be treated as cash, headcount, or realised benefit.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md
* Ready phase or task: Full plan complete (`P01`, `P02`, `P03`); ready for `rpi-review`
* Remaining provisional question or blocker: None
