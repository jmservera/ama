<!-- markdownlint-disable-file -->
# RPI Changes: Issue #189 Simulator Run Owner, Time Limit, and Budget Alert Controls

## Metadata

* Task ID: 189-simulator-controls-2142
* Related plan: .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: All planned `src/core` governance, controller status, regression test, documentation, static typing, lint, format, and unit test tasks completed and verified with `sensor_stream.py` untouched.

## Execution Summary

Delivered the locally verifiable simulator run-control invariants for Issue #189 ("Run has an owner, a time limit and a budget alert") across `run_governance.py`, `run_plan.py`, `test_simulator_run_budget_controls.py`, and `src/core/README.md`. Every simulator `RunPlan`, `RunGovernance`, `RunMeter`, and `RunController` instance now rejects placeholder owners/alert names (including `"TBC"` and `"pending"`), validates JSON-safe GBP fields and ungoverned `planned_cost_gbp`, enforces `max_seconds` via `check_time_limit()` and `admit()`, freezes elapsed and clamped remaining runtime upon halt or idempotent operator stop, and exposes a unified `RunController.status()` snapshot across `idle`, `running`, and `stopped` states without altering `sensor_stream.py` provenance digests or `_body(plan)` estimate records.

## Completed Work

### RunGovernance placeholder hardening, deadline check, and frozen RunMeter runtime

* Related phase or task: `P01`, `P01-T01`
* Files: `src/core/src/zava_forward/core/synthetic/run_governance.py`
* What changed and why: Added `governed_text()` wrapping `accountable_text()` to reject `"tbc"` and `"pending"` without modifying `sensor_stream.py`; added `ended` timestamp tracking, `check_time_limit()`, `_ensure_running()` (`RUN_STOPPED` vs `halt_reason`), and idempotent `stop()` on `RunMeter`; enriched `RunMeter.summary()` with frozen `elapsed_seconds`, clamped `remaining_seconds >= 0.0`, and paired `budget_alert_gbp`/`alert_gbp` keys.
* Completion evidence: `run_governance.py` edits passing strict `mypy`, `ruff`, and `GovernanceValidation` + `BudgetMeter` unit tests.
* Validation: Passed (`python3 -m mypy`, `python3 -m ruff check .`, `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*simulator*.py' -v`).

### Fail-closed RunPlan GBP validation and unified RunController lifecycle status

* Related phase or task: `P01`, `P01-T02`
* Files: `src/core/src/zava_forward/core/synthetic/run_plan.py`
* What changed and why: Enforced `governed_text()` on `RunPlan.owner` and `RunPlan.alert_reference`; enforced `isinstance(..., str)` GBP checks and `planned_cost_gbp == 0` when GBP alert/cap are omitted inside `RunPlan.governance()`; validated `plan` fail-closed in `RunController.__init__()` with canonical `idle` `budget_alert_gbp`; widened `RunController.admit()` to `Decimal | int | str`; added `RunController.check_time_limit()` for both USD-only and GBP-metered runs; froze `_stopped_at` idempotently on the `"running"` -> `"stopped"` transition; and unified `RunController.status()` across `idle`, `running`, and `stopped` states.
* Completion evidence: `run_plan.py` edits passing strict `mypy`, `ruff`, `RunPlanWiring`, `test_run_plan.py`, and `src/api/tests/test_iot_stream.py`.
* Validation: Passed.

### Focused simulator governance unit tests and core README update

* Related phase or task: `P02`, `P02-T01`, `P02-T02`
* Files: `src/core/tests/test_simulator_run_budget_controls.py`, `src/core/README.md`
* What changed and why: Expanded `test_simulator_run_budget_controls.py` (21 total tests, 0 removals) to cover `"TBC"`/`"pending"` refusal, ungoverned/malformed `planned_cost_gbp` refusal, fail-closed `RunController` construction, canonical `idle` `budget_alert_gbp`, unified `status()` across `idle`/`running`/`stopped`, idempotent `stop()` and `RUN_STOPPED`/`RUN_NOT_RUNNING` error codes, `Decimal` admission, `check_time_limit()` with and without a GBP meter, frozen `elapsed_seconds` and clamped `remaining_seconds == 0.0`, and CLI error exits; documented the updated surface in `src/core/README.md`.
* Completion evidence: All 21 simulator tests, 42 sibling `test_run_plan.py` + `test_sensor_stream.py` tests, 2 `test_dependency_rule.py` tests, and 37 `src/api` `test_iot_stream.py` tests passed; `git diff` on `sensor_stream.py` confirmed empty.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

None required; implementation matched the finalized plan (`PC-001` and `PC-002` included).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` (316 files, `strict = true`) | Passed | `Success: no issues found in 316 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (263 formatted files) | Passed | `263 files already formatted` |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*simulator*.py' -v` | `src/core/tests/test_simulator_run_budget_controls.py` | Passed | `Ran 21 tests in 0.015s — OK` (`PYTHONPATH=src` binds to this worktree's `src/core/src` rather than the shared host's `~/.local` editable install at `/home/azureuser/source/ama/src/core/src`) |
| `PYTHONPATH=src python3 -m unittest tests/test_run_plan.py tests/test_sensor_stream.py tests/test_dependency_rule.py -v` | `src/core` sibling & dependency contracts | Passed | `42 + 2 = 44 tests — OK`; `sensor_stream.py` diff verified empty |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_iot_stream.py -q` | `src/api` `RunController` caller compatibility | Passed | `Ran 37 tests in 11.262s — OK` |
| Complete local gate (`tools/rpi-checks.py --all`) & hosted CI | Repository-wide | Skipped | Focused validation tier applies to scoped offline `src/core` unit slice; caller explicitly prohibited `git push` |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]` and `complete`)
* Completed-work evidence and handoff prose: current
* Validation, blockers, remaining work, and follow-up items: current
* Review readiness: ready for `rpi-review`

## Blockers

* None.

## Remaining Work

* None within declared full-plan scope.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md, `## Follow-Up Items`
* Live Azure `Microsoft.Consumption/budgets` alert firing and subscription headroom verification (#146, #189): outside local `src/core` scope; owned by project owner during an approved live Azure IoT Hub exercise.

## Return-to-Caller State

* Implementation execution status: Complete (Full plan)
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: `mypy` (316 files), `ruff check`, `ruff format --check`, simulator unit tests (21 passed), sibling `run_plan`/`sensor_stream`/`dependency_rule` tests (44 passed), and `src/api` `test_iot_stream` (37 passed)
* Blockers: none
* Current plan and detail updates: none
* Planning and critique state: implementation-ready (`PC-001` and `PC-002` applied and verified)
* Follow-up items: live Azure budget alert verification (#146, #189)
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: parent confirmed automatic RPI Agent
