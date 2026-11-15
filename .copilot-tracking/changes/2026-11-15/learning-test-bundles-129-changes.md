<!-- markdownlint-disable-file -->
# RPI Changes: Journey Learning-Test Bundles and Role-Screen Scenario Verification (Issue #129)

## Metadata

* Task ID: issue-129-learning-test-bundles-0023
* Related plan: .copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P03, P03-T01, P03-T02
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks (`P01` through `P03-T02`) completed, validated across `src/core` and `src/api` linters, strict `mypy`, and targeted `unittest` suites, and reconciled for `rpi-review`.

## Execution Summary

Delivered backward-compatible PRD and UX-protocol metadata across all five candidate learning-test bundles in `zava_forward.core.learning_test_bundles`, expanded core unit tests in `src/core/tests/test_learning_test_bundles.py` to cover all five bundles, NFR-009 resident-effort transfer rules, every target-zero breach, and five-bundle `O16` reconciliation, and added cross-layer Node-VM specialist role-screen and aftercare scenario verification in `src/api/tests/test_learning_test_bundle_scenarios.py` while keeping `O10`/`O18`-`O20` excluded and preserving the Atlas-owner and DPO screen/storage governance gates.

## Completed Work

### Core Protocol Metadata Enrichment (`P01`, `P01-T01`)

* Files changed: `src/core/src/zava_forward/core/learning_test_bundles.py`, `src/core/README.md`
* Summary: Added defaulted immutable fields (`title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, `stop_rule`) to `Bundle` so positional 4-argument construction remains backward-compatible, populated all five `BUNDLES` entries verbatim from `docs/reference/research/ux/journey-learning-test-bundles.md` and `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and surfaced read-only metadata keys (`bundle_title`, `atlas_ids`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, `stop_rule`) in `compare_bundle` without altering `render_report` or `learning-bundle-constructed-input-v1` stdin CLI validation. Updated `src/core/README.md` to document the enriched bundle and report metadata.

### Complete Five-Bundle and NFR-009 Core Unit Coverage (`P01`, `P01-T02`)

* Files changed: `src/core/tests/test_learning_test_bundles.py`
* Summary: Extended `test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure` to cover all five bundle keys including `funding-evidence`, and added four focused unit tests (`test_protocol_metadata_matches_prd_and_learning_questions`, `test_shifting_staff_minutes_to_resident_effort_is_not_a_saving`, `test_every_zero_measure_across_all_five_bundles_triggers_stop_rule`, and `test_five_bundle_campaign_reconciles_single_o16_owner`) increasing module test count from 22 to 26.

### Specialist Role-Screen and Aftercare Scenario Verification (`P02`, `P02-T01`)

* Files created: `src/api/tests/test_learning_test_bundle_scenarios.py`
* Summary: Implemented six `mypy --strict`-clean scenario and governance tests executing real Node-VM renders of `src/api/src/zava_forward/api/web/role-screens.js` (`resident-choice`, `resident-service-issues`, `programme-queue`, `procurement-packages`, `contractor-job-pack`, `technical-queue`, `quality-queue`, `finance-funding`, `finance-invoices`, wired with the real `workSummary` helper from `app.js`) and `src/api/src/zava_forward/api/web/aftercare.js` (`formView`, `receiptView`, `concernView`, `evaluatorView` over a real temporary `AftercareService` store) paired with constructed two-arm `learning_test_bundles.run_report` and `reconcile_o16` comparisons across `story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare` (including open aftercare concern surviving recorded handover and financial closures), and `funding-evidence`. Verified `OUT_OF_SCOPE` (`O10`, `O18`-`O20`) exclusion and confirmed that no unapproved learning-bundle screen or `/api/...` run-storage route is exposed while Atlas-owner and DPO gates remain open.

### Focused Validation, Tracking Reconciliation, and Commit Author Readiness (`P03`, `P03-T01`, `P03-T02`)

* Files updated: `.copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md`, `.copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md`, `.copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md`, `.copilot-tracking/rpi-sessions/2026-11-15/learning-test-bundles-129-state.json`
* Summary: Executed `ruff check .`, `ruff format --check .`, `mypy`, and targeted `unittest` suites across `src/core` and `src/api`, verified live Markdown links and zero `.copilot-tracking/` strings in modified source/README files, resolved authenticated GitHub noreply identity via `gh api user` (`8036360+jmservera@users.noreply.github.com`), configured repository-local `git config --local user.email`, and reconciled all plan and phase-detail markers ahead of read-only `rpi-review`.

## Implementation-Time Plan and Detail Updates

### Lifecycle Boundary Clarification on `P03-T02` and `AC-7`

* Classification: Immediately relevant current-state update preserving approved user intent.
* Affected markers: `AC-7`, `P03`, `P03-T02` in `.copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md` and `.copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md`.
* What changed and why: Clarified `P03-T02` so implementation-owned reconciliation (`learning-test-bundles-129-changes.md`, plan/detail markers, and repository-local `git config --local user.email "8036360+jmservera@users.noreply.github.com"`) completes cleanly inside `Implement`, while `rpi-review` writes `.copilot-tracking/reviews/logs/2026-11-15/learning-test-bundles-129-review.md` under its strict read-only rule on planning/changes records and the automatic RPI parent performs the single frozen local commit immediately after `Review` -> `Follow-up` state persistence.
* Triggering evidence and user decision: `rpi-review` constraint prohibiting mutation of `plan.md`, `phase-details.md`, or `changes.md` during Review; aligns stage responsibilities with user direction to write `.copilot-tracking/changes/` and `.copilot-tracking/reviews/` and leave one clean local commit without pushing.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` | Passed | `264 files already formatted` |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 317 source files` |
| `python3 -m unittest discover -s tests -p 'test_learning_test_bundles.py' -v` | `src/core/tests` | Passed | `Ran 26 tests in 3.121s - OK` |
| `python3 -m unittest tests/test_atlas_screen_trace.py -v` | `src/core/tests` | Passed | `Ran 17 tests in 0.097s - OK` |
| `python3 -m unittest tests/test_live_doc_links.py -v` | `src/core/tests` | Passed | `Ran 2 tests in 0.975s - OK` |
| `python3 -m ruff check .` | `src/api` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/api` | Passed | `202 files already formatted` |
| `python3 -m mypy` | `src/api` | Passed | `Success: no issues found in 286 source files` |
| `python3 -m unittest discover -s tests -p 'test_learning_test_bundle_scenarios.py' -v` | `src/api/tests` | Passed | `Ran 6 tests in 0.390s - OK` |
| Guardrail regression suite (`test_role_screens.py`, `test_role_screens_conformance.py`, `test_role_screens_connected_journey.py`, `test_technical_quality_screens.py`, `test_aftercare_screen.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_learning_test_bundle_scenarios.py`) | `src/api/tests` | Passed | `Ran 118 tests in 5.049s - OK` |
| Tracking-hygiene grep for `.copilot-tracking` in touched `src/` files | `src/core`, `src/api` | Passed | Zero matches in `learning_test_bundles.py`, `src/core/README.md`, `test_learning_test_bundles.py`, and `test_learning_test_bundle_scenarios.py` |
| Hosted CI workflows | Remote GitHub Actions | Skipped | User explicitly instructed not to push (`do NOT push`); focused local validation completed per D4 / #1294 |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all `[x]` / `Complete`).
* Completed-work evidence and handoff prose: Reconciled with exact files, tests, and implementation-time `P03-T02` lifecycle clarification.
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan tasks, `3` external human-gated follow-up items preserved).
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None in active plan scope (`rpi-review` log generation and parent post-Review frozen local commit follow next in the automatic RPI loop).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md, `## Follow-Up Items`
* Atlas-owner confirmation of bundle-to-opportunity mapping including `O16` overlap (`docs/reference/research/ux/journey-learning-test-bundles.md`, human owner gate).
* DPO decision on representative-data retention before any run retains representative data or stores run records (`docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, DPO gate).
* Facilitator-run live bundle experiments (#129 / #155) and Finance validation before saved capacity minutes can be treated as cash, headcount, or realised benefit.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P03, P03-T01, P03-T02; remaining: none
* Validation coverage: Passed across `src/core` (`ruff`, `mypy`, 45 targeted tests) and `src/api` (`ruff`, `mypy`, 118 targeted scenario and guardrail tests); hosted CI skipped because push is prohibited by user direction
* Blockers: None
* Current plan and detail updates: Clarified `P03-T02` / `AC-7` boundary so implementation reconciliation and local noreply Git email configuration complete before read-only `rpi-review` and post-Review parent commit
* Planning and critique state: Ready (`Complete`, `Pass` in `.copilot-tracking/reviews/plans/2026-11-15/learning-test-bundles-129-plan-critique.md`)
* Follow-up items: 3 human-gated follow-up items preserved in plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent for confirmed automatic RPI Agent
