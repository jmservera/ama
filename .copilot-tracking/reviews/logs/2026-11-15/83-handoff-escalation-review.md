<!-- markdownlint-disable-file -->
# Review: Issue 83 Unaccepted Handoff Visibility and SLA Escalation (BG-010)

## Scope and Evidence

* Task ID: 83-handoff-escalation
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Requirements `FR-1`..`FR-4` and `NFR-1`..`NFR-2`, acceptance criteria on Issue #83 (`Unaccepted handoffs are visible and escalated within approved times (BG-010)`), post-critique dispositions `PC-001`..`PC-005`, `src/core` and `src/api` source and test diffs, `web/role-screens.js` zero-diff guard, and Focused-tier validation results.
* Plan: .copilot-tracking/plans/2026-11-15/83-handoff-escalation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/83-handoff-escalation-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/83-handoff-escalation-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/83-handoff-escalation-research.md; direct read-only inspection of `src/core` and `src/api` implementation and unit test files; Focused-tier `ruff`, `mypy`, and `unittest` execution outputs.

## Opening Review State

* Interpreted review goal: Verify once, from canonical artifacts, code diffs, and Focused-tier validation evidence, whether Issue #83's `BG-010` unaccepted handoff visibility and SLA escalation slice satisfies all planned requirements, critique dispositions, safety/redaction invariants, and non-regression guards.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready — research, post-critique plan, phase details, plan critique, reconciled changes record, source/test files, and Focused-tier validation results are complete and reconciled.
* Acceptance basis: Plan `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, Issue #83 `BG-010` acceptance criterion, caller guard requirements 1..5, and resolved critique items `PC-001`..`PC-005`.
* First comparison boundary: Reconcile plan checklist markers (`P01`..`P03`) and `PC-001`..`PC-005` critique dispositions against `workflows.py`, `taskqueues.py`, `store.py`, `sqlstore.py`, `exception_register.py`, `progress.py`, and `server.py` before assessing test coverage and residual follow-up routing.
* Active read-only boundaries: Read-only across source, test, research, plan, details, critique, and changes files; write access restricted to `.copilot-tracking/reviews/logs/2026-11-15/83-handoff-escalation-review.md` (and parent RPI session state on phase handoff).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass review on `2026-11-15` across full plan scope (`P01`, `P02`, `P03`), reconciling `.copilot-tracking/plans/2026-11-15/83-handoff-escalation-plan.md`, `.copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/83-handoff-escalation-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/83-handoff-escalation-changes.md`, the 8 modified `src/core` and `src/api` files, the 2 new unit test suites, and Focused-tier `ruff`, `mypy`, and `unittest` outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `### P01: Core BG-010 Handoff SLA Evaluation, Projections, Queues, and Overdue Sweep` | Reconciled | Plan markers `[x]`, phase details, changes evidence, and `src/core` / `progress.py` diffs match across all helper, projection, queue, `SqlStore`, and `ExceptionRegister` targets. |
| `P02` (`P02-T01`) | `### P02: HTTP API Handoff Queue and Escalation Sweep Routes` | Reconciled | Plan markers `[x]`, `server.py` GET/POST routes, `get_kind` registration, and `test_role_endpoint_inventory.py` entries match without touching `web/role-screens.js`. |
| `P03` (`P03-T01`, `P03-T02`) | `### P03: Focused Unit Tests and Static/Runtime Verification` | Reconciled | Plan markers `[x]`, test suites (`test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`), and full Focused-tier validation record (`3,490` core tests + `3,534` API tests + `ruff` + `mypy`) match. |
| `## Follow-Up Items` | `## Follow-Up Items` | Reconciled | Both pre-declared follow-ups (`OD-09` operational sign-off and `web/app.js` `waitingRows` alignment when live `ZF_DATA` enables global `handoff_policy`) remain outside active `Pxx` scope and are mirrored in the changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/workflows.py` | Added `approved_handoff_policy`, `approved_handoff_limit_hours`, `handoff_sla`, enriched `handoff_view`, exact-second policy-aware 13-key `handoff_ageing`, `unowned_handoffs`, `escalated_handoffs`, updated `pending_handoffs` / `unaccepted_handoffs`, and added manager-gated `escalate_overdue_handoffs` keeping sender accountability unchanged. | Verified directly in `workflows.py` diff and unit test assertions on routine/urgent windows, `OD-09` null fallback, boundary seconds, role visibility, redaction, and idempotent sweep provenance. | Passed (`ruff`, `mypy`, `3,490` `src/core` unit tests) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/taskqueues.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/exception_register.py`, `src/api/src/zava_forward/api/progress.py` | Wired `effective_due_at` into `overdue_tasks`, enriched `work["handoff"]` and `work["next_action"]`, passed `as_of`, `handoff_policy`, and `staff` into `handoff_view` / `handoff_ageing`, added `handoff_policy` to `SqlStore.DOCS` + `_queue_fingerprint` + `save()`, and bumped `MEMBERSHIP_REVISION = 4`. | Verified directly in diffs and dual-store (`Store` and `SqlStore`) parity + `ExceptionRegister` stranded-task routing tests. | Passed (`ruff`, `mypy`, `3,490` `src/core` + `3,534` `src/api` unit tests) | Reconciled |
| `P02-T01` | `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py` | Added `_parse_max_age_hours`, registered `/api/handoffs/unowned` and `/api/handoffs/escalated` in `get_kind`, implemented `GET /api/handoffs/unowned`, `GET /api/handoffs/escalated`, and `POST /api/handoffs/escalate-overdue` (`MANAGER_ROLES` checked before body parsing), and added all three endpoints to the 9-role endpoint inventory. | Verified in `server.py` and `test_role_endpoint_inventory.py` diffs plus HTTP tests for `200`/`400`/`403`, CSV compatibility, and canary redaction. | Passed (`ruff`, `mypy`, `3,534` `src/api` unit tests) | Reconciled |
| `P03-T01` | `src/core/tests/test_handoff_escalation_83.py`, `src/api/tests/test_handoff_escalation_api_83.py` | Added focused unit test suites covering `BG-010` routine/urgent SLA limits, `OD-09` unapproved preservation, exact-second boundary behavior, `Store`/`SqlStore` parity, shared role queues, `NOTE_HELD` redaction, `ExceptionRegister`, HTTP endpoints, and sweep idempotency/audit integrity. | Both files created within locked test-addition ceiling (2 new files, 0 removed). | Passed (`11` new core tests + `4` new API tests all passing) | Reconciled |
| `P03-T02` | `src/core`, `src/api`, `src/api/src/zava_forward/api/web/role-screens.js` | Executed Focused-tier static analysis, formatting, type-checking, and full test discovery across `src/core` and `src/api`, and verified zero modifications to `web/role-screens.js`. | Recorded in changes Validation Record and verified from command exit status `0` and `0` diff count on `web/role-screens.js`. | Passed (`ruff check`, `ruff format --check`, `mypy`, `7,024` total tests run, `0` failures) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None (local test-helper adjustment only in `P03-T01`) | Used `change_provenance.controlled` + `_save_workflow` in `_offer_aged` test helpers so synthetic historical `offered_at` timestamps persist through `SqlStore` touch tracking and provenance checks. | Triggered by `SqlStore.save()` touch-set verification during `P03-T02`; no user decision or plan change required. | Recorded in `.copilot-tracking/changes/2026-11-15/83-handoff-escalation-changes.md` under `## Implementation-Time Plan and Detail Updates`; active plan and phase details required no structural revision. | Not needed (`PC-001`..`PC-005` and plan readiness unchanged) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five findings (`PC-001` exact-second breach comparison, `PC-002` `SqlStore` `staff` and `handoff_policy` refresh, `PC-003` manager role check before body validation on `POST /api/handoffs/escalate-overdue`, `PC-004` explicit test-inventory additions/removals lock, and `PC-005` `web/app.js` `waitingRows` follow-up boundary) were applied in the plan and verified in the delivered code and tests.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No material revision occurred; phases executed sequentially (`P01` -> `P02` -> `P03`) with no premature resumption.
* Justification assessment: Supported by code diffs and passing Focused-tier validation.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Operational sign-off of live routine and urgent `BG-010` handoff acceptance limits (`OD-09`) and human usability/accessibility journey validation (`NFR-008`, `NFR-009`) | Operational policy thresholds and human governance/usability sign-offs cannot be invented by engineering code (`docs/reference/regulatory/README.md`). | Named programme owner (`Retrofit Programme Manager`) to ratify `handoff_policy` values and human journey sign-off before closing programme-wide governance gates. | Open outside active software scope; routed as distinct governance follow-up. |
| Relax `row.approved_limit_hours === null` in `src/api/src/zava_forward/api/web/app.js` `waitingRows` when a live `ZF_DATA` deployment activates `handoff_policy` globally | Changing `web/app.js` falls under web-bundle scope and current waiting-view regression contracts when `OD-09` is unratified in the default synthetic seed. | Future web-scoped slice once `OD-09` policy values are enabled in live demo datasets. | Open outside active backend/API scope; routed as distinct web follow-up. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material defects, decision gaps, or evidence gaps were identified within the assessed Issue #83 `BG-010` software boundary (`P01`..`P03`).

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | None | No `rpi-implement`, `rpi-plan`, or `rpi-research` remediation required for active scope | Active `P01`..`P03` scope is conformant |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Distinct web follow-up (outside active `P01`..`P03` scope): Update `waitingRows` in `src/api/src/zava_forward/api/web/app.js` when a deployment enables an approved `handoff_policy` in `ZF_DATA` globally so policy-backed limits display without suppressing the unratified `OD-09` badge behavior tested by `test_handoff_waiting_view.py`.
* Distinct governance follow-up (outside active `P01`..`P03` scope): Obtain named programme-owner sign-off on operational `BG-010` routine/urgent acceptance hours (`OD-09`) and human journey validation (`NFR-008`, `NFR-009`).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all completed and verified)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `ruff check .` | `src/core`, `src/api` | Passed | `All checks passed!` across both projects |
| `ruff format --check .` | `src/core` (282 files), `src/api` (197 files) | Passed | All 479 Python files formatted cleanly |
| `mypy src tests` | `src/core` (335 files), `src/api` (222 files) | Passed | `Success: no issues found` across all 557 checked files |
| `python -m unittest discover -s tests -q` | `src/core` | Passed | `Ran 3490 tests in 1246.782s — OK (skipped=419)`, including `test_handoff_escalation_83.py` (`Store` + `SqlStore`) and 60,000-case queue benchmarks |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest discover -s tests -q` | `src/api` | Passed | `Ran 3534 tests in 1935.483s — OK (skipped=635)`, including `test_handoff_escalation_api_83.py`, `test_handoff_api.py`, `test_unaccepted_handoff_csv_api.py`, `test_handoff_waiting_view.py`, `test_role_endpoint_inventory.py`, and `test_list_export_inventory.py` |
| `git diff --name-only -- src/api/src/zava_forward/api/web/role-screens.js` | `web/role-screens.js` baseline guard | Passed | `0` modified lines; role-screen WCAG counted guards preserved untouched |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned requirement (`FR-1`..`FR-4`, `NFR-1`, `NFR-2`), caller guard requirement (`1`..`5`), post-critique disposition (`PC-001`..`PC-005`), and Issue #83's `BG-010` acceptance criterion (`Unaccepted handoffs are visible and escalated within approved times (BG-010)`) is implemented, reconciled across tracking artifacts, and proven by passing Focused-tier static checks and 7,024 unit tests with zero defects and zero edits to `web/role-screens.js`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up items (`## Follow-Up Items`) | Optional later web slice (`web/app.js` `waitingRows` when global `handoff_policy` is enabled) and programme-owner `OD-09` operational timing ratification |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`ruff check`, `ruff format --check`, `mypy`, `3,490` `src/core` tests, `3,534` `src/api` tests, and `0` `web/role-screens.js` diff lines)
* Blockers: None

