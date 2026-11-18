<!-- markdownlint-disable-file -->
# RPI Changes: Issue 83 Unaccepted Handoff Visibility and SLA Escalation (BG-010)

## Metadata

* Task ID: 83-handoff-escalation
* Related plan: .copilot-tracking/plans/2026-11-15/83-handoff-escalation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/83-handoff-escalation-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: None
* Status basis: All planned phases and tasks (`P01`..`P03`) completed and verified against Focused-tier static and unit test checks across `src/core` and `src/api`.

## Execution Summary

Delivered `BG-010` deterministic handoff acceptance SLA evaluation, enriched case and shared work-queue projections, shared/role handoff queues (`unowned_handoffs`, `unaccepted_handoffs`, `escalated_handoffs`), manager-controlled overdue escalation sweeps (`escalate_overdue_handoffs`), HTTP API endpoints (`GET /api/handoffs/unowned`, `GET /api/handoffs/escalated`, `POST /api/handoffs/escalate-overdue`), and focused unit test suites across `src/core` and `src/api` without modifying `src/api/src/zava_forward/api/web/role-screens.js`.

## Completed Work

### P01: Core BG-010 Handoff SLA Evaluation, Projections, Queues, and Overdue Sweep

* `P01-T01` (`src/core/src/zava_forward/core/workflows.py`): Implemented `approved_handoff_policy`, `approved_handoff_limit_hours`, `handoff_sla`, enriched `handoff_view`, policy-aware 13-key `handoff_ageing` with exact-second breach comparison, `unowned_handoffs`, `escalated_handoffs`, updated `pending_handoffs` and `unaccepted_handoffs`, and added manager-controlled `escalate_overdue_handoffs` keeping sender accountability unchanged.
* `P01-T02` (`taskqueues.py`, `store.py`, `sqlstore.py`, `exception_register.py`, `progress.py`): Wired `effective_due_at` into `overdue_tasks`, added `BG-010` escalation metadata and guidance to `taskqueues.context`, passed dataset `as_of`, `handoff_policy`, and `staff` across `Store`, `ExceptionRegister`, and `progress`, added `handoff_policy` to `SqlStore.DOCS`, bumped `MEMBERSHIP_REVISION` to `4`, and refreshed SQLite queue memberships on `handoff_policy` changes.

### P02: HTTP API Handoff Queue and Escalation Sweep Routes

* `P02-T01` (`src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`): Added shared `_parse_max_age_hours` validator, registered `/api/handoffs/unowned` and `/api/handoffs/escalated` in `get_kind`, implemented `GET /api/handoffs/unowned`, `GET /api/handoffs/escalated`, and `POST /api/handoffs/escalate-overdue` (checking `MANAGER_ROLES` before body parsing), and registered all three routes in the 9-role endpoint inventory without touching `web/role-screens.js`.

### P03: Focused Unit Tests and Static/Runtime Verification

* `P03-T01` (`src/core/tests/test_handoff_escalation_83.py`, `src/api/tests/test_handoff_escalation_api_83.py`): Authored dual-store (`Store` and `SqlStore`) core unit tests and loopback HTTP API tests covering routine/urgent `BG-010` SLA evaluation, `OD-09` unapproved null preservation, exact-second boundary timing, `detail["handoff"]` and `work["handoff"]` projections, `overdue`/`unowned` parity, `unowned_handoffs` / `unaccepted_handoffs` / `escalated_handoffs` role visibility and redaction (`NOTE_HELD`), `ExceptionRegister` stranded-task routing, and `escalate_overdue_handoffs` sweep idempotency and audit ledger integrity.
* `P03-T02`: Executed Focused-tier `ruff check`, `ruff format --check`, `mypy`, and full `unittest discover` suites across `src/core` (3,490 tests) and `src/api` (3,534 tests) with zero errors, and verified `web/role-screens.js` has zero diff lines.

## Implementation-Time Plan and Detail Updates

None. Implementation matched the post-critique plan and phase details directly; local test-harness adjustments in `test_handoff_escalation_83.py` and `test_handoff_escalation_api_83.py` used `change_provenance.controlled` when stamping synthetic historical `offered_at` timestamps on `SqlStore`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` | `src/core`, `src/api` | Passed | All checks passed in both projects |
| `ruff format --check .` | `src/core` (282 files), `src/api` (197 files) | Passed | All files already formatted |
| `mypy src tests` | `src/core` (335 files), `src/api` (222 files) | Passed | Success: no issues found in 557 total checked files |
| Targeted handoff/queue/CSV/inventory unit tests | `src/core` (77 tests), `src/api` (71 tests, 4 skipped) | Passed | `OK` across `test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`, `test_handoff_lifecycle.py`, `test_handoff_api.py`, `test_unaccepted_handoff_csv_api.py`, `test_handoff_waiting_view.py`, `test_taskqueues.py`, `test_sqlqueues.py`, `test_exception_feeds.py`, `test_role_endpoint_inventory.py`, `test_list_export_inventory.py` |
| Full `unittest discover -s tests -q` | `src/core` | Passed | `Ran 3490 tests in 1246.782s — OK (skipped=419)` |
| Full `unittest discover -s tests -q` | `src/api` | Passed | `Ran 3534 tests in 1935.483s — OK (skipped=635)` |
| `git diff --name-only -- src/api/src/zava_forward/api/web/role-screens.js` | `web/role-screens.js` guard | Passed | `0` modified files |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan markers)
* Review readiness: Ready

## Blockers

* None

## Remaining Work

* None in active plan scope

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/83-handoff-escalation-plan.md, `## Follow-Up Items`
* Owner sign-off of live operational escalation timings (`OD-09`) and human usability/accessibility journey validation (`NFR-008`, `NFR-009`) remain programme-level items outside Issue #83's software capability slice; if a live `ZF_DATA` deployment activates `handoff_policy` globally, relax `approved_limit_hours === null` in `web/app.js` `waitingRows` in a web-scoped change.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`..`P03`, all checked `[x]`)
* Validation coverage: Focused tier complete (`ruff check`, `ruff format --check`, `mypy`, and full `unittest discover` in `src/core` and `src/api`)
* Blockers: None
* Current plan and detail updates: Plan checklist reconciled (`P01`..`P03` checked `[x]`)
* Planning and critique state: Ready (`PC-001`..`PC-005` resolved)
* Follow-up items: Recorded above
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
