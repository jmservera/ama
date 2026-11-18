<!-- markdownlint-disable-file -->
# RPI Changes: Hazard and Safeguarding Clock and Named Owner Projection (Issue #76)

## Metadata

* Task ID: issue-76
* Related plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`, `P04`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`), `P04` (`P04-T01`)
* All remaining active-plan markers: None
* Status basis: Full plan (`P01`–`P04`) implemented and verified under the focused validation tier (`ruff check`, `ruff format --check`, `mypy`, and full `unittest` suites across `src/core` and `src/api`).

## Execution Summary

Delivered the remaining unchecked acceptance criterion on Issue #76 (`Hazard and safeguarding items show a clock and named owner`) across role-based task queues, `My cases today`, the shared `All open cases` work queue, and case cards without modifying `src/api/src/zava_forward/api/web/role-screens.js` or relaxing any accessibility, content-standard, privacy, or referral-ownership guard.

## Completed Work

### Shared Safety Clock and Accountable-Owner Projection (`P01-T01`)

* Updated `src/core/src/zava_forward/core/taskqueues.py`:
  * Bumped `MEMBERSHIP_REVISION = 4` so reopening pre-change SQLite/MSSQL databases refreshes `queue_blocked` and `queue_overdue` flags automatically when `meta.key='queue_context'` changes.
  * Added `SAFEGUARDING_ITEM_KEYS`, `UNRECORDED_OWNER_TOKENS`, `raw_safeguarding_items`, `is_safeguarding_item`, `is_open_safety_item`, `has_open_safety`, `has_open_safeguarding`, and `project_safety_clock_and_owner`.
  * Projected statutory/operational clocks (`clock_status`, `clock_remaining_hours`, `clock_deadline_utc`, `clock_label`, `clock_window_hours`, `clock_basis`) for emergency/urgent/significant/routine hazards (Awaab's Law 24h emergency / 7d investigation / 14d work-start reference windows and recorded deadlines) and safeguarding items (24h emergency/urgent and 48h referral response clocks), failing closed with `clock_status="fail_closed_missing_timestamp"` whenever awareness/deadline timestamps are missing, unparseable, or future-dated relative to `as_of`.
  * Enforced receipt-is-not-acceptance (`accepted_by -> destination only if accepted_at -> sender -> follow_up -> owner -> named_owner -> accountable_owner`) and non-blank named accountable/escalation ownership (`named_owner`, `accountable_owner`, `owner_role`, `owner_id`, `escalation_owner`, `unassigned`), keeping legacy `owner == "Unknown"` on queue clock dicts when unallocated for backward compatibility.
  * Extended `overdue_tasks` with standalone safeguarding recorded service deadlines and extended `context(..., staff=None)` to emit enriched `hazard_clocks`, `safeguarding_clocks`, and `safety_items`.
* Updated `src/core/src/zava_forward/core/workflows.py`:
  * Added `"Safeguarding"` to `HAZARD_CATEGORIES`, enriched `hazard_view(...)` via `_apply_safety_enrichment`, added `safeguarding_view(...)`, and wired `case`, `as_of`, and `staff` through `hazard_states(...)`.

### Store, SqlStore, Insights, Ranking, and Privacy-Redaction Parity (`P01-T02`)

* Updated `src/core/src/zava_forward/core/store.py`, `sqlstore.py`, `insights.py`, `ranking.py`, and `projection.py`:
  * Wired `insights.has_hazard`, `ranking._hazard`, and `SqlStore._row(c)` `hazard` column to `taskqueues.has_open_safety(c)` while ignoring passive note-only canary `safeguarding={"note": "..."}` containers.
  * Added `safeguarding=taskqueues.has_open_safeguarding(c)` on `Store.summary` and aligned `Store._work_context` (`staff=staff_list`), `Store.counts`, `Store.focus`, `Store.gate_reasons`, `Store.status_line`, and `Store.require_safety_clear`.
  * Projected normalized standalone safeguarding items into `d["safeguarding_items"]` and appended copies (`standalone_safeguarding=True`, scalar `owner` backfilled from `named_owner` when unallocated) into `d["hazards"]` so unmodified `web/role-screens.js` renders standalone safeguarding cases on `#/screens?screen=safety-lead` and `hazard-triage` with zero `"Mismatch"` or `"Owner: Unknown"`.
  * Extended `projection.hold_notes` to redact `"source"`, `"job"`, `"summary"`, and `"reason"` alongside `NOTE_KEYS` on both `hazards` and `safeguarding_items` for non-reason staff while preserving contractor default-deny withholding (`PR-002`) and keeping clock and named-owner fields intact for authorized staff.

### Self-Contained Queue Row and Case Card Rendering (`P02-T01`)

* Updated `src/api/src/zava_forward/api/web/app.js` without modifying `src/api/src/zava_forward/api/web/role-screens.js`:
  * Kept `workSummary(work)` completely self-contained between `function workSummary(` and `function workSteps(` so `test_role_screens.py`'s isolated Node VM slice executes without external dependencies, rendering clock labels, remaining/overdue hours or fail-closed timestamp notices, named accountable owners (with role and ID when present), and `[Unassigned item; escalation owner: ...]` notices.
  * Added `"Safeguarding"` to `HAZ_CATEGORIES`, updated `caseView` `openHaz` to check both `c.hazards` and `c.safeguarding_items`, and added `describeClockAndOwner` + `<p class="safety-clock-owner">` and read-only `ul.list.safeguarding-items` in `safetyPanel(...)` while keeping `<dl class="safety-facts">` at exact 4 `<dt>` rows without `"Unknown"` and zero banned `CopyAudit` terms.

### Focused Core & API/UI Unit Tests and Component Documentation (`P03-T01`, `P03-T02`)

* Created `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` (3 focused test methods covering clock windows, running/overdue/completed/fail-closed states, receipt-is-not-acceptance, unallocated escalation owners, JSON vs SQLite parity, `MEMBERSHIP_REVISION=4` stale-DB rebuild, note-only canary safety, non-reason redaction, and contractor withholding).
* Created `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py` (2 focused test methods covering live HTTP `/api/cases` queue endpoints, `/api/cases/{id}` role-scoped projections, unmodified `role-screens.js` VM rendering, and `safetyPanel` DOM rendering).
* Updated `src/core/README.md` and `src/api/README.md` (`ms.date: 2026-11-15`).

### Focused-Tier Validation and Guard Verification (`P04-T01`)

* Verified `ruff check .`, `ruff format --check .`, strict `mypy`, and full `unittest discover -s tests -q` across both `src/core` and `src/api`, plus `git diff --name-status` confirming `src/api/src/zava_forward/api/web/role-screens.js` is untouched, 0 test files removed, and 2 focused test files added.

## Implementation-Time Plan and Detail Updates

* Local judgment only (no plan/scope changes): aligned test timestamps in `test_hazard_safeguarding_clock_owner_76.py` and `test_hazard_safeguarding_clock_owner_api_76.py` with `taskqueues.instant("2026-10-16")` midnight UTC (`2026-10-16T00:00:00Z`) and `SqlStore` `meta.key='queue_context'`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` & `ruff format --check .` | `src/core` (282 formatted files) | Passed | 0 lint errors, 0 formatting diffs |
| `mypy` (`strict = true`) | `src/core` (335 source files) | Passed | `Success: no issues found in 335 source files` |
| `python -m unittest discover -s tests -q` | `src/core` (all core tests incl. `test_hazard_safeguarding_clock_owner_76.py`) | Passed | 3,482 tests passed (3,443 + 39 `test_device_registry_azure.py` with `iothub` extra installed; 0 failures, 0 errors) |
| `ruff check .` & `ruff format --check .` | `src/api` (197 formatted files) | Passed | 0 lint errors, 0 formatting diffs |
| `mypy` (`strict = true`) | `src/api` (281 source files) | Passed | `Success: no issues found in 281 source files` |
| `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` | `src/api` (all API/UI/a11y/baseline tests incl. `test_hazard_safeguarding_clock_owner_api_76.py`) | Passed | `Ran 3534 tests in 2053.333s — OK (skipped=635)` (0 failures, 0 errors; counted baseline guards `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_role_screens.py`, `test_safety_panel_ux.py`, and `test_content_standard.py` all green) |
| Diff boundary check (`git status --short`) | Repository worktree | Passed | `src/api/src/zava_forward/api/web/role-screens.js` unmodified; 0 test files removed; 2 focused test files added |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`–`P04` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md, `## Follow-Up Items`
* None

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`), `P04` (`P04-T01`); remaining none
* Validation coverage: Focused tier complete (`ruff check`, `ruff format --check`, strict `mypy`, and full `unittest` suites across `src/core` and `src/api`, all passing)
* Blockers: None
* Current plan and detail updates: None beyond completion markers
* Planning and critique state: Complete (`PC-001`..`PC-005` resolved)
* Follow-up items: None
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
