<!-- markdownlint-disable-file -->
# RPI Changes: Issue #135 Data Steward and Digital Operator Exception Queue

## Metadata

* Task ID: issue-135-2330
* Related plan: .copilot-tracking/plans/2026-11-14/exception-queue-135-2330-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: All planned phases (`P01`, `P02`, `P03`) completed and validated cleanly under the Focused validation tier.

## Execution Summary

Completed all planned phases (`P01`, `P02`, `P03`) for Issue #135 across `src/core` (`exception_queue.py`, `exception_feeds.py`, `exception_register.py`, and core unit tests) and `src/api` (`web/app.js` `#/exceptions` view, `test_exception_register.py` register/SQL/JSON/HTTP tests, and new `test_exception_queue_ui.py` Node-VM UI contract tests). All static checks (`mypy`, `ruff check .`, `ruff format --check .`) and focused unittest suites (`29` tests in `src/core`, `231` tests across 15 suites in `src/api`) pass cleanly without touching `workbench_browser_check.py`, `scenario-manifest.json`, `workbench.py`, `role-screens.js`, or `sqlstore.py`.

## Completed Work

### Core Exception Queue, Feeds, and Store Register Contract Enrichment

* Related phase or task: `P01` (`P01-T01`, `P01-T02`, `P01-T03`)
* Files: `src/core/src/zava_forward/core/exception_queue.py`, `src/core/src/zava_forward/core/exception_feeds.py`, `src/core/src/zava_forward/core/exception_register.py`, `src/core/tests/test_exception_queue.py`, `src/core/tests/test_exception_feeds.py`
* What changed and why: Added `resolution_owner` on conflict items, `failure_category` on failure items, deterministic `correlation_id` and `recovery_context` across all items, timestamped multi-entry `audit_trail` on recovery actions, plain-language `next_steps` and `record_detected_outage` on `outage_banner`, `correlation_id` extraction (`correlation_id`, `envelope.correlation_id`, `envelope.request_id`, `envelope.meter_id`, and import batch/refusal `correlation_id`) and sourceless `stranded_task` fallback `ref` (`f"task:{case_id}:{task}"`) in `exception_feeds.py`, and read-only rejected `import_batches` / `import_exceptions.rejected_batches` projection, idempotent `deepcopy`-based `_with_recoveries` full `audit_trail` reconstruction, `viewer_roles` + `allowed_kinds` in `access`, and `actual_hold`-aware continuity/service outage projection (supporting both string and mapping `incident_owner`) across `ok` and `roles_not_named` banners in `exception_register.py`.
* Completion evidence: `mypy` (316 files, 0 issues), `ruff check .`, `ruff format --check .`, and 29 core unit tests passed.
* Validation: Passed (`mypy`, `ruff check`, `ruff format --check`, `tests/test_exception_queue.py`, `tests/test_exception_feeds.py`).

### Interactive Employee Workbench Exception Queue View and End-to-End API/UI Tests

* Related phase or task: `P02` (`P02-T01`, `P02-T02`) and `P03` (`P03-T01`)
* Files: `src/api/src/zava_forward/api/web/app.js`, `src/api/tests/test_exception_register.py`, `src/api/tests/test_exception_queue_ui.py`
* What changed and why: Activated `redesign-existing-projects` and `web-design-guidelines` (with current rules fetched), added `body.key` deduplication in `mutationKey`, routed `#/exceptions` in `route()` with matching `routeStatusLabel`, added plain-ASCII `#/exceptions` secondary entry links in `handoffWaitingView` and `importView`, and implemented `exceptionsView` + accessible helpers in `web/app.js` rendering honest outage banners + `next_steps`, scoped operator access (`viewer_roles`, `allowed_kinds`, category `scope`), dual-value conflicts (`<caption>` + `<th scope="col">` table with `source`, `recorded_at`, `version`, and `resolution_owner`), owned failures (`failure_category`, `correlation_id`, `recovery_context`), preserved `Unknown` eligibility and `original_source`, and controlled `POST /api/exceptions/recovery` forms (`"Keep on hold"` / `"Record check by named owner"` + required reason) with full `audit_trail` display and owner-named `403` / `roles_not_named` / `502` guidance. Extended `test_exception_register.py` across `Register`, `SqlStore`/`Store` restart parity, and HTTP endpoints, and added `test_exception_queue_ui.py` running the shipped `app.js` view in Node VM.
* Completion evidence: `mypy` (284 files, 0 issues), `ruff check .`, `ruff format --check .`, and 231 tests across 15 `src/api` suites (including lexical copy guard `test_content_standard.py`, `test_design_system.py`, `test_role_screens.py`, `test_exception_register_screen.py`, `test_exception_register.py`, and `test_exception_queue_ui.py`) passed.
* Validation: Passed (`mypy`, `ruff check`, `ruff format --check`, and 15 focused `unittest` suites).

## Implementation-Time Plan and Detail Updates

* Minor resilience refinement in `src/core/src/zava_forward/core/exception_register.py` (`_apply_detected_outages`): `ContinuityMixin.suspend(...)` stores `incident_owner` as a stripped string (for example `"Pam Lead"`), whereas raw fixture entries may use a mapping; handled both string and mapping `incident_owner` cleanly without changing any planned API shape.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python -m mypy` | `src/core` | Passed | `Success: no issues found in 316 source files` |
| `python -m ruff check . && python -m ruff format --check .` | `src/core` | Passed | `All checks passed!`, `263 files already formatted` |
| Focused core unit tests (`test_exception_queue`, `test_exception_feeds`) | `src/core/tests` | Passed | `Ran 29 tests in 0.006s — OK` |
| `python -m mypy` | `src/api` | Passed | `Success: no issues found in 284 source files` |
| `python -m ruff check . && python -m ruff format --check .` | `src/api` | Passed | `All checks passed!`, `200 files already formatted` |
| Focused API, UI, WCAG, copy-standard, and design-system suites (15 suites) | `src/api/tests` | Passed | `Ran 231 tests in 115.091s — OK (skipped=4)` across `test_exception_register`, `test_exception_queue_ui`, `test_exception_register_screen`, `test_data_operator_screen`, `test_data_steward_screen_wcag`, `test_role_screens`, `test_role_endpoint_inventory`, `test_handoff_waiting_view`, `test_case_journey`, `test_epic149_role_workbench_heading_hierarchy`, `test_content_standard`, `test_design_system`, `test_app_js_notices_content`, `test_static_assets`, `test_workspace_scripts` |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`..`T03`, `P02`, `P02-T01`..`T02`, `P03`, `P03-T01` all `[x]`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled
* Review readiness: Ready (`P01`–`P03` implemented and validated; ready for `rpi-review`)

## Blockers

* none

## Remaining Work

* Execute one-pass `rpi-review` (including refreshed Web Interface Guidelines audit of changed `web/app.js` lines) and create clean local commit with `Refs #135` without pushing.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/exception-queue-135-2330-plan.md, `## Follow-Up Items`
* Connect standalone importer process rejected-batch storage directly to the shared database without manual refusal-ledger transfer once importer storage topology is unified (owner: data engineering / programme support).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused tier complete (`mypy`, `ruff check`, `ruff format --check`, 29 core tests, 231 API/UI/WCAG/copy-standard tests)
* Blockers: none
* Current plan and detail updates: string/mapping `incident_owner` handling recorded above
* Planning and critique state: Ready (`PC-001`..`PC-006` resolved)
* Follow-up items: standalone importer rejected-batch storage unification
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent confirmed automatic RPI Agent
