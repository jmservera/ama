<!-- markdownlint-disable-file -->
# RPI Changes: Cost, Scale and Run Controls for the Simulator (Issue #189)

## Metadata

* Task ID: `simulator-run-controls-189`
* Related plan: .copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete (full plan `P01`, `P02`, `P03`)
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`
* All remaining active-plan markers: None
* Status basis: All planned source and test tasks (`P01` through `P03`) are implemented, reconciled, and validated across `src/core` and `src/api` regression checks with zero touches to excluded files.

## Execution Summary

Completed full-plan delivery (`P01` through `P03`) for Issue #189 simulator run controls (`owner`, bounded `time_limit_minutes` / `max_duration_seconds`, and linked `BudgetAlertContract` runtime + Bicep verification) across `sensor_stream.py`, `run_governance.py`, `run_plan.py`, and `test_simulator_run_controls_189.py`.

## Completed Work

### Owner Validation and Stream Pacer Envelope Preflight (`P01`, `P01-T01`)

* Related markers: `P01`, `P01-T01`
* Files: `src/core/src/zava_forward/core/synthetic/sensor_stream.py`
* What changed and why: Expanded `_PLACEHOLDERS` in `sensor_stream.py` to reject anonymous, unattended, guest, unowned, system, automated, bot, and null/nil strings alongside template/placeholder strings; rejected ASCII control characters and strings without any alphanumeric character in `accountable_text`; extracted `RunBudget._preflight_envelope()` and `RunBudget.preflight()`; enforced `budget._preflight_envelope()` in `Pacer.__init__()`; enforced `INVALID_RUN_RATE` on invalid `max_per_second` in `Pacer.admit_send()`; and enforced `INVALID_RUN_LIMIT` on invalid rate mutations in `Pacer.set_max_per_second()`.
* Completion evidence: Blank, placeholder, punctuation-only, control-character, and anonymous owners fail closed across `accountable_text`, `RunBudget`, and `Pacer`, while short valid alphanumeric identifiers (`"o"`, `"r"`) and `HubPublisher.run(..., pacer=...)` `INVALID_RUN_RATE` behavior remain intact.
* Validation: Passed `test_simulator_run_controls_189.py`, `test_sensor_stream.py`, `src/api/tests/test_iot_stream.py`, `src/api/tests/test_live_control.py`, `ruff`, and strict `mypy`.

### Bounded Duration Resolution and Linked Budget-Alert Contracts (`P01`, `P01-T02`)

* Related markers: `P01`, `P01-T02`
* Files: `src/core/src/zava_forward/core/synthetic/run_governance.py`
* What changed and why: Added `MIN_TIME_LIMIT_SECONDS`, `MAX_TIME_LIMIT_SECONDS`, `MAX_TIME_LIMIT_MINUTES`, and `resolve_duration_seconds()` (`1.0..3600.0` seconds / `<= 60.0` minutes with `TIME_LIMIT_REQUIRED` and `TIME_LIMIT_MISMATCH`); introduced frozen `BudgetAlertContract` (binding `threshold_percent`, `threshold_type`, `alert_rule_reference`, `alert_owner_reference`, and optional USD/GBP caps) and `SimulatorRunControls` (`validate()` and `preflight()`); and added `RunGovernance.from_minutes()`, `time_limit_minutes`, and `max_duration_seconds`.
* Completion evidence: Missing, non-finite, `bool`, out-of-range, or conflicting durations and unlinked/anonymous/invalid budget alerts raise deterministic `StreamError` codes before execution begins.
* Validation: Passed `test_simulator_run_controls_189.py`, `test_simulator_run_budget_controls.py`, `ruff`, and strict `mypy`.

### RunPlan, RunController, and CLI Run-Control Wiring (`P02`, `P02-T01`)

* Related markers: `P02`, `P02-T01`
* Files: `src/core/src/zava_forward/core/synthetic/run_plan.py`
* What changed and why: Added defaulted `alert_owner` and `alert_threshold_type` fields on `RunPlan` (omitted when default in `_body(plan)` to preserve legacy `estimate.json` SHA-256 digests while cryptographically binding explicit values), `RunPlan.from_controls()`, `max_duration_seconds`, `time_limit_minutes`, `budget_alert_contract()`, and `preflight_controls()` enforced inside `RunPlan.validate()`; added `RunController.preflight()` and enriched `RunController.status()` with `max_duration_seconds`, `time_limit_minutes`, and `budget_alert`; and added `--time-limit-minutes` and `--alert-owner` to `run_plan.main()` with `StreamError` exit-code `2` handling.
* Completion evidence: Every `RunPlan`, `RunController`, and CLI `run_plan.main` path enforces owner, bounded duration, and linked budget-alert preflight while keeping legacy estimate digests compatible.
* Validation: Passed `test_run_plan.py`, `test_simulator_run_budget_controls.py`, `test_simulator_run_controls_189.py`, `ruff`, and strict `mypy`.

### Bicep Run-Control Alignment Extractor and Verifier (`P02`, `P02-T02`)

* Related markers: `P02`, `P02-T02`
* Files: `src/core/src/zava_forward/core/synthetic/run_plan.py`
* What changed and why: Added `BicepNotificationContract`, `BicepRunControlContract`, and `verify_bicep_run_controls(infra_dir, controls=...)` verifying `infra/governance.bicep` (`owner` in `requiredTags`), `infra/main.bicep` (`ownerTag` in `allTags` passed to `iotHub`, required `alertEmail`, and `budget-${prefix}`), `infra/modules/iothub.bicep` (`ResourceId`-scoped `budget-${name}` with enabled `actual80` and `forecast100` routed to `alertEmail`), and `infra/live-simulator-job.bicep` (`replicaTimeout <= 3600`, `replicaRetryLimit == 0`, `--once`, `approvalReference`, read-only `/certs/control.json`), plus runtime `SimulatorRunControls` threshold/type alignment.
* Completion evidence: `verify_bicep_run_controls()` validates real `infra/` templates and fails closed with `StreamError("BICEP_CONTRACT_MISMATCH")` on tampered Bicep fixtures or unaligned runtime alert thresholds.
* Validation: Passed `test_simulator_run_controls_189.py` (including ARM compilation via `az bicep build`), `ruff`, and strict `mypy`.

### Focused Runtime and Bicep Contract Test Suite (`P03`, `P03-T01`)

* Related markers: `P03`, `P03-T01`
* Files: `src/core/tests/test_simulator_run_controls_189.py`
* What changed and why: Added 11 focused unit and contract test methods across `OwnerEnforcementTests`, `BoundedDurationTests`, `BudgetAlertPreflightAndRuntimeTests`, and `BicepRunControlContractTests` covering positive and negative cases for named owners, minute/second bounded durations, deadline halts (`RUN_DEADLINE`), budget threshold alerts and pre-cap halts (`RUN_BUDGET_HALT`), tampered estimate rejection (`ESTIMATE_MISMATCH`), Bicep contract drift (`BICEP_CONTRACT_MISMATCH`), and compiled ARM JSON verification.
* Completion evidence: All 11 new test methods and all existing `src/core` and `src/api` simulator/governance suites pass with zero touches to `server.py`, `test_role_endpoint_inventory.py`, `README.md`, or `infra/*.bicep`.
* Validation: Passed focused and full `src/core` unit tests, cross-package `src/api` simulator/content tests, `ruff check`, `ruff format --check`, `mypy`, and `tools/rename-zava-tests.py`.

## Implementation-Time Plan and Detail Updates

### Preserve `HubPublisher.run` Supplied-Pacer `INVALID_RUN_RATE` Contract (`P01-T01`)

* Affected area and marker: `P01-T01` in `.copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md` (`In Scope`, `Phase Checklist`) and `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md` (`P01`, `P01-T01`).
* What changed and why: Split `RunBudget._preflight_envelope()` (owner/cost/alert accountability, `max_seconds` bounds, and message/quota bounds) from `max_per_second` checking so `Pacer.__init__()` enforces `budget._preflight_envelope()` at construction while `Pacer.admit_send()` enforces `0 < self.max_per_second <= 100` (`StreamError("INVALID_RUN_RATE")`) before admitting any frame and `Pacer.set_max_per_second()` enforces `StreamError("INVALID_RUN_LIMIT")`.
* Triggering evidence and user decision: Cross-package regression run of `src/api/tests/test_iot_stream.py` (`PublisherTests.test_invalid_supplied_pacer_limits_refuse_before_client_creation`) showed `HubPublisher.run` callers construct `Pacer(replace(budget, max_per_second=rate))` and assert `HubPublisher.run` raises `INVALID_RUN_RATE` prior to IoT Hub client creation. Preserving that contract while failing closed in `Pacer.admit_send()` needed no new user decision.
* Reconciliation performed: Updated `plan.md` (`In Scope`, `P01-T01`, and `## Follow-Up Items` to mirror the deferred sibling-PR API surfacing item) and `phase-details.md` (`Phase Index`, `P01`, `P01-T01`).
* Planning and critique state: Immediately relevant current-state update preserving approved intent and `PC-001`–`PC-003` dispositions; no new critique required.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_simulator_run_controls_189.py" -q` | `src/core` (#189 suite) | Passed | 11 tests passed (`OK`) including ARM JSON compilation check |
| `PYTHONPATH="$(pwd)/src:$(pwd)/tests" python3 -m unittest tests/test_simulator_run_controls_189.py tests/test_sensor_stream.py tests/test_run_plan.py tests/test_simulator_run_budget_controls.py tests/test_dependency_rule.py -q` | `src/core` simulator & architecture boundary suites | Passed | 76 tests passed (`OK`) |
| Full `src/core` unit suite (`unittest discover -s tests -q` + isolated venv checks for `test_device_registry_azure.py`, `test_learning_test_bundles.py`, `test_stock_fabric.py`, `test_discovery_assistant_demo.py`) | `src/core` (3,563 tests) | Passed | All `src/core` unit tests verified passing (`test_device_registry_azure.py` 39 passed in Azure SDK venv; `test_discovery_assistant_demo.py` 14 passed in isolated editable venv) |
| `PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests:tests python3 -m unittest tests/test_iot_stream.py tests/test_live_control.py tests/test_content_standard.py -q` | `src/api` cross-package callers & content standard | Passed | 122 tests passed (`OK`) |
| `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` | `src/core` lint, format, strict typing | Passed | Ruff: all checks passed, 289 files formatted; Mypy: 0 issues in 342 source files |
| `python3 tools/rename-zava-tests.py` | Repository naming regression gate | Passed | 25 tests passed (`OK`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` checked `[x]` in `plan.md`; `Completed` in `phase-details.md`)
* Completed-work evidence and handoff prose: Reconciled across `plan.md` and `changes.md`
* Validation, blockers, remaining work, and follow-up items: Reconciled and mirrored between `plan.md` and `changes.md`
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* None

## Remaining Work

* None in active plan scope (`P01`–`P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md, `## Follow-Up Items`
* Live Azure `Microsoft.Consumption/budgets` notification firing verification in the `ama` resource group: outside immediate offline `src/core` scope; tracked under Issue #146 and Issue #189 hosted deployment checks.
* Surface `time_limit_minutes` and `budget_alert` summary fields in FastAPI admin live-control endpoints: deferred out of immediate scope per stack-isolation constraint prohibiting edits to `server.py` and `test_role_endpoint_inventory.py` until #1641 merges.

## Return-to-Caller State

* Implementation execution status: Complete (full plan `P01`–`P03`)
* Declared scope and markers: Full plan (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` completed; none remaining)
* Validation coverage: Focused + full `src/core` unit tests, cross-package `src/api` IoT/live-control/content-standard tests, `ruff check`, `ruff format --check`, strict `mypy`, and `tools/rename-zava-tests.py` all passed
* Blockers: None
* Current plan and detail updates: 1 immediately relevant current-state update on `P01-T01` (`Pacer` envelope preflight + `admit_send` `INVALID_RUN_RATE` compatibility) reconciled in `plan.md` and `phase-details.md`
* Planning and critique state: Ready (`PC-001`, `PC-002`, `PC-003` resolved; no material divergence)
* Follow-up items: 2 distinct out-of-scope follow-up items mirrored in `plan.md`
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent confirmed automatic RPI Agent
