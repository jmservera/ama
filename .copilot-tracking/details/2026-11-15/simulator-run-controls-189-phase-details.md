<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #189 Simulator Run Controls

## Metadata

* Task ID: issue-189-simulator-run-controls
* Task slug: simulator-run-controls-189
* Related plan: .copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md (`C1`–`C10`), `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (FR-050, AC-066), `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` (Decision 6)

## Phase Index

| Phase ID | Name                                                                               | Status    | Detail sections          |
|----------|------------------------------------------------------------------------------------|-----------|--------------------------|
| P01      | Harden Owner Validation, Stream Budget Preflight, and Core Run-Control Contracts   | Completed | P01, P01-T01, P01-T02    |
| P02      | Wire Run-Control Contracts and Bicep Alignment Verifier into `run_plan.py`         | Completed | P02, P02-T01, P02-T02    |
| P03      | Focused Unit & Bicep Contract Tests and Validation                                 | Completed | P03, P03-T01             |

## Test Ownership, Canonical Targets, and Budget Lock

* Canonical production targets (max 3 files modified, 0 removed):
  * `src/core/src/zava_forward/core/synthetic/sensor_stream.py`
  * `src/core/src/zava_forward/core/synthetic/run_governance.py`
  * `src/core/src/zava_forward/core/synthetic/run_plan.py`
* Canonical test additions (exact 1 new file, 0 existing test removals):
  * `src/core/tests/test_simulator_run_controls_189.py` (semantic unit + Bicep contract alignment + negative/tampered Bicep tests)
* Regression test suites run unchanged:
  * `src/core/tests/test_sensor_stream.py`, `src/core/tests/test_run_plan.py`, `src/core/tests/test_simulator_run_budget_controls.py`, `src/core/tests/test_dependency_rule.py`, and `src/api/tests/test_live_control.py`
* Strictly excluded targets (0 touches):
  * `server.py`, `test_role_endpoint_inventory.py`, all `README.md` files, and `infra/*.bicep`

<!-- rpi:phase id=P01 -->
## P01: Harden Owner Validation, Stream Budget Preflight, and Core Run-Control Contracts

### Context

Research (`C1`, `C2`, `C8`) showed that `accountable_text` (`sensor_stream.py`) and `governed_text` (`run_governance.py`) reject template placeholders (`<name>`, `tbd`, `tbc`, `pending`, `none`, `unknown`, `nobody`, `unassigned`, `n/a`, `na`, `todo`), but still accept `"anonymous"`, `"anon"`, `"guest"`, `"unattended"`, `"unowned"`, `"null"`, `"nil"`, `"system"`, `"auto"`, `"automated"`, `"bot"`, control characters, and punctuation-only strings (`"---"`). Furthermore, `Pacer.__init__` does not invoke `RunBudget` preflight validation, and `run_governance.py` lacks `time_limit_minutes` resolution and a structured `BudgetAlertContract` / `SimulatorRunControls` preflight object.

### Intent

Make every core stream and governance primitive fail closed when an owner is blank/anonymous/non-identifier, when duration is missing or outside `1..3600` seconds (`<= 60` minutes), or when a linked budget alert contract is absent or invalid.

### Boundaries

* Included: `src/core/src/zava_forward/core/synthetic/sensor_stream.py` and `src/core/src/zava_forward/core/synthetic/run_governance.py`.
* Excluded: Changing `Replay` frame wire bytes or breaking short alphanumeric fixture identifiers (`"o"`, `"r"`, `"owner"`).

### Likely Targets

* `src/core/src/zava_forward/core/synthetic/sensor_stream.py`: `accountable_text`, `RunBudget._preflight_envelope`, `RunBudget.preflight`, `RunBudget.validate`, `Pacer.__init__`, `Pacer.admit_send`, `Pacer.set_max_per_second`.
* `src/core/src/zava_forward/core/synthetic/run_governance.py`: `MIN_TIME_LIMIT_SECONDS`, `MAX_TIME_LIMIT_MINUTES`, `resolve_duration_seconds`, `BudgetAlertContract`, `SimulatorRunControls`, `RunGovernance`.

### Dependencies

* None.

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_sensor_stream.py src/core/tests/test_simulator_run_budget_controls.py -q` passes.
* `mypy` and `ruff` pass on `src/core`.

### Completion Evidence

* Anonymous/blank/punctuation-only owners and unvalidated `RunBudget` instances fail closed in `RunBudget.preflight()` and `Pacer.__init__()`.
* `BudgetAlertContract` and `SimulatorRunControls` validate named owner, bounded `time_limit_minutes` / `max_duration_seconds`, and linked threshold + rule + owner references.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `accountable_text` and enforce `RunBudget` preflight in `Pacer`

#### Context

`sensor_stream.accountable_text` (`C1`) is the shared root validator for `RunBudget`, `RunGovernance`, `RunPlan`, and `src/api/live_control.py` (`C8`). `Pacer(budget)` previously trusted `budget.owner`, `budget.max_seconds`, and `budget.max_per_second` without running `RunBudget` validation, while `HubPublisher.run(..., pacer=...)` in `src/api/iot_stream.py` validates supplied pacer send rates and raises `INVALID_RUN_RATE`.

#### Intent

Reject anonymous, unattended, bot/system, null, control-character, and punctuation-only identifiers in `accountable_text`; enforce owner/cost/alert accountability and bounded duration/message envelope preflight in `Pacer.__init__()`; and fail closed on invalid send rates in both `Pacer.admit_send()` (`INVALID_RUN_RATE`) and `Pacer.set_max_per_second()` (`INVALID_RUN_LIMIT`).

#### Boundaries

* Included: Expand `_PLACEHOLDERS` in `sensor_stream.py` with the unified disallowed set (`"tbd"`, `"tbc"`, `"todo"`, `"pending"`, `"n/a"`, `"na"`, `"none"`, `"null"`, `"nil"`, `"unknown"`, `"nobody"`, `"unassigned"`, `"unowned"`, `"anonymous"`, `"anon"`, `"guest"`, `"unattended"`, `"system"`, `"auto"`, `"automated"`, `"bot"`); enforce no ASCII control chars and `any(ch.isalnum() for ch in text)`; add `RunBudget._preflight_envelope()` and `RunBudget.preflight()` raising existing `StreamError` codes (`RUN_OWNER_COST_ALERT_REQUIRED`, `INVALID_RUN_LIMIT`, `RUN_MESSAGE_LIMIT`); call `budget._preflight_envelope()` in `Pacer.__init__()`; enforce `type(self.max_per_second) in (int, float) and math.isfinite(self.max_per_second) and 0 < self.max_per_second <= 100` in `Pacer.admit_send()` (`StreamError("INVALID_RUN_RATE")`, preserving `HubPublisher.run` caller contract in `src/api/tests/test_iot_stream.py`); and enforce `type(rate) in (int, float) and math.isfinite(rate) and 0 < rate <= 100` in `Pacer.set_max_per_second()` (`StreamError("INVALID_RUN_LIMIT")`).
* Excluded: Rejecting 1-character alphanumeric strings (`"o"`, `"r"`) relied upon by `test_live_control.py`.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/sensor_stream.py`: owner/alert identifier check and `RunBudget`/`Pacer` preflight enforcement.

#### Dependencies

* None.

#### Validation Expectations

* `Pacer(RunBudget(owner="anonymous", cost_reference="c", alert_reference="a"))` raises `StreamError("RUN_OWNER_COST_ALERT_REQUIRED")`.
* `Pacer(RunBudget(owner="owner", cost_reference="cost", alert_reference="alert", max_seconds=7200))` raises `StreamError("INVALID_RUN_LIMIT")`.
* Existing `test_sensor_stream.py` and `src/api/tests/test_live_control.py` pass unchanged.

#### Completion Evidence

* Updated `sensor_stream.py` passing `mypy --strict`, `ruff`, `test_sensor_stream.py`, and `test_live_control.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `resolve_duration_seconds`, `BudgetAlertContract`, and `SimulatorRunControls` to `run_governance.py`

#### Context

`run_governance.py` (`C2`) defines `MAX_TIME_LIMIT_SECONDS = 3600.0`, `governed_text`, `RunGovernance`, and `RunMeter`, but lacks minute-based bounded duration conversion/validation (`time_limit_minutes` vs `max_duration_seconds`) and a structured `BudgetAlertContract` / `SimulatorRunControls` preflight model.

#### Intent

Provide canonical frozen contracts for simulator run preflight (`SimulatorRunControls` + `BudgetAlertContract`) and bounded minute/second duration resolution (`1.0..3600.0`s / `<= 60.0`m), integrated with `RunGovernance`.

#### Boundaries

* Included:
  * `MIN_TIME_LIMIT_SECONDS = 1.0`, `MAX_TIME_LIMIT_SECONDS = 3600.0`, `MAX_TIME_LIMIT_MINUTES = 60.0`.
  * `resolve_duration_seconds(*, max_duration_seconds=None, time_limit_minutes=None) -> float`: rejects `None`/`None` (`TIME_LIMIT_REQUIRED`), `bool`/non-finite/out-of-range (`TIME_LIMIT_REQUIRED`), and conflicting dual values (`TIME_LIMIT_MISMATCH`).
  * `BudgetAlertContract(threshold_percent, alert_rule_reference, alert_owner_reference, threshold_type="Actual", budget_cap_usd=None, budget_alert_gbp=None, budget_cap_gbp=None)` with `validate()` (raising `RUN_OWNER_COST_ALERT_REQUIRED` on invalid/anonymous rule or alert-owner references, `INVALID_BUDGET` on `bool`/non-finite/`<= 0`/`> 100` threshold, invalid `threshold_type` outside `("Actual", "Forecasted")`, invalid `budget_cap_usd <= 0`, or partial/invalid GBP amounts, and `BUDGET_ALERT_NOT_BELOW_CAP` when `alert_gbp >= cap_gbp`), `alert_fires_at_usd`, and `as_dict()`.
  * `SimulatorRunControls(owner, budget_alert, max_duration_seconds=None, time_limit_minutes=None)` with `validate() -> float` (raising `RUN_OWNER_REQUIRED` on invalid/anonymous `owner`, `RUN_OWNER_COST_ALERT_REQUIRED` if `budget_alert` is not a `BudgetAlertContract`, propagating `budget_alert.validate()` and `resolve_duration_seconds()` errors) and `preflight() -> dict[str, Any]`.
  * `RunGovernance.time_limit_minutes`, `RunGovernance.max_duration_seconds`, and `RunGovernance.from_minutes(...)`.
* Excluded: Modifying `RunMeter.summary()` existing keys.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/run_governance.py`: duration resolver and run-control preflight contracts.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `SimulatorRunControls` rejects missing/anonymous owners, missing/unbounded/conflicting `time_limit_minutes` / `max_duration_seconds`, and unlinked/anonymous/out-of-range `BudgetAlertContract` fields with deterministic `StreamError` codes.

#### Completion Evidence

* Updated `run_governance.py` passing `mypy --strict` and unit checks.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Wire Run-Control Contracts and Bicep Alignment Verifier into `run_plan.py`

### Context

`run_plan.py` (`C3`) owns pre-run estimation, `estimate.json` recording (`_body(plan)` using `asdict(plan)`), `RunController`, and CLI `main()`. `infra/` (`C4`–`C6`) declares the IoT Hub and workload Consumption budgets (`actual80` at 80% Actual, `forecast100` at 100% Forecasted, `contactEmails: [alertEmail]`), required `owner` tag policy (`governance.bicep`), and bounded simulator job timeout (`replicaTimeout: 240`, `replicaRetryLimit: 0`, `--once`, `/certs/control.json`).

### Intent

Wire `SimulatorRunControls`, `BudgetAlertContract`, `time_limit_minutes`, and `verify_bicep_run_controls()` into `run_plan.py` while keeping `_body(plan)` byte-compatible for existing `RunPlan` instances.

### Boundaries

* Included: `src/core/src/zava_forward/core/synthetic/run_plan.py`.
* Excluded: Mutating `RunPlan` dataclass field list in ways that break existing `_body(plan)` keys; editing `infra/*.bicep`.

### Likely Targets

* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `RunPlan`, `RunController`, `main()`, `BicepRunControlContract`, `verify_bicep_run_controls()`.

### Dependencies

* P01.

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_run_plan.py src/core/tests/test_simulator_run_budget_controls.py -q` passes unchanged.
* `verify_bicep_run_controls()` succeeds against repository `infra/` and raises `StreamError("BICEP_CONTRACT_MISMATCH")` when any required owner, timeout, or budget-alert declaration is missing or mismatched.

### Completion Evidence

* Updated `run_plan.py` passing `mypy --strict`, `ruff`, and existing `test_run_plan.py` / `test_simulator_run_budget_controls.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Integrate `SimulatorRunControls`, `BudgetAlertContract`, and `--time-limit-minutes` / `--alert-owner` into `RunPlan`, `RunController`, and CLI

#### Context

`RunPlan` (`C3`) uses `asdict(self)` in `_body(plan)` to compute SHA-256 over recorded estimates. Methods, `@property` accessors, and `@classmethod` constructors do not alter `asdict(self)`.

#### Intent

Ensure every `RunPlan`, `RunController`, and `run_plan.main()` invocation executes `SimulatorRunControls` preflight and supports both `time_limit_minutes` and `max_duration_seconds` plus linked `BudgetAlertContract` inspection.

#### Boundaries

* Included:
  * Add defaulted `alert_owner: str | None = None` and `alert_threshold_type: str = "Actual"` to `RunPlan`; in `_body(plan)`, omit `alert_owner` and `alert_threshold_type` from `plan` dict only when at their default (`None` / `"Actual"`) values so legacy `RunPlan` digests remain identical while any explicit `alert_owner` or `Forecasted` threshold type is cryptographically bound into `estimate.json` SHA-256 verification.
  * Add `RunPlan.max_duration_seconds`, `RunPlan.time_limit_minutes`, `RunPlan.budget_alert_contract(alert_owner=None) -> BudgetAlertContract`, `RunPlan.preflight_controls(alert_owner=None) -> SimulatorRunControls`, and `RunPlan.from_controls(controls, *, homes, max_per_second=100.0, budget_usd=None, ...)` normalizing non-`None` GBP fields on `controls.budget_alert` to `str` and preserving `controls.budget_alert.alert_owner_reference` and `controls.budget_alert.threshold_type`.
  * Preserve existing `RunPlan.validate()` error-code precedence (`RUN_OWNER_COST_ALERT_REQUIRED`, `INVALID_RUN_LIMIT`, `INVALID_REPLAY_SPEED`, `INVALID_BUDGET`, `INVALID_SCALE`, `INVALID_DAILY_USAGE`) before validating `alert_owner` (`RUN_OWNER_COST_ALERT_REQUIRED`), `alert_threshold_type` (`INVALID_BUDGET`), and `self.preflight_controls().validate()`.
  * Add `RunController.preflight() -> dict[str, object]` and enrich `RunController.status()` with `"time_limit_minutes"`, `"max_duration_seconds"`, and `"budget_alert"` (`self.plan.budget_alert_contract().as_dict()`) while keeping all existing keys.
  * Update `run_plan.main(argv)` with optional `--time-limit-minutes` (type `float`) and `--alert-owner`, resolving duration via `resolve_duration_seconds()` and constructing/recording `RunPlan` inside `try ... except StreamError` so any invalid flag cleanly prints `refused: <code>` and returns exit code `2`.
* Excluded: Changing existing error codes asserted in `test_run_plan.py` or `test_simulator_run_budget_controls.py`.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `RunPlan`, `RunController`, `main()`.

#### Dependencies

* P01-T02.

#### Validation Expectations

* All existing `test_run_plan.py` and `test_simulator_run_budget_controls.py` assertions pass unchanged, and new minute-based / `from_controls()` / CLI `--time-limit-minutes` & `--alert-owner` invocations validate fail-closed.

#### Completion Evidence

* `RunPlan`, `RunController`, and `run_plan.main` enforce `SimulatorRunControls` preflight without breaking existing callers.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Implement `BicepRunControlContract` and `verify_bicep_run_controls()` in `run_plan.py`

#### Context

`infra/modules/iothub.bicep` (`C4`), `infra/main.bicep` & `infra/governance.bicep` (`C5`), and `infra/live-simulator-job.bicep` (`C6`) declare the Azure-side owner, bounded simulator job runtime, and Consumption budget alerts (`actual80` and `forecast100` routed to `alertEmail`).

#### Intent

Provide a reusable, strictly typed contract extractor and verifier (`verify_bicep_run_controls`) that validates both the Bicep infrastructure declarations and their link to runtime `SimulatorRunControls` / `BudgetAlertContract`.

#### Boundaries

* Included:
  * Frozen `BicepNotificationContract(name: str, threshold_percent: int, threshold_type: str, enabled: bool, contact_reference: str)` and `BicepRunControlContract(owner_tag_required: bool, default_owner_tag: str, alert_email_param_required: bool, job_replica_timeout_seconds: int, job_retry_limit: int, job_runs_once: bool, job_control_file: str, hub_budget_resource_scoped: bool, notifications: tuple[BicepNotificationContract, ...])`.
  * `verify_bicep_run_controls(infra_dir: Path, controls: SimulatorRunControls | None = None) -> BicepRunControlContract`:
    * Verifies `governance.bicep` includes `'owner'` in `requiredTags`.
    * Verifies `main.bicep` sets a governed `param ownerTag`, binds `owner: ownerTag` into `allTags` passed as `tags: allTags` to `module iotHub`, declares a required un-defaulted `param alertEmail string` wired to `iotHub` and `budget-${prefix}` `contactEmails: [alertEmail]`, and declares `Microsoft.Consumption/budgets` (`budget-${prefix}`).
    * Verifies `modules/iothub.bicep` declares `Microsoft.Consumption/budgets` (`budget-${name}`) scoped by `ResourceId` with enabled `actual80` (`80`, `Actual`, `contactEmails: [alertEmail]`) and `forecast100` (`100`, `Forecasted`, `contactEmails: [alertEmail]`).
    * Verifies `live-simulator-job.bicep` bounds `replicaTimeout` to `1..3600`, sets `replicaRetryLimit: 0`, runs `--once`, checks `!empty(trim(approvalReference))`, and mounts `/certs/control.json` read-only.
    * When `controls` is provided, runs `controls.preflight()` and verifies `controls.budget_alert.threshold_type == notification.threshold_type` and `math.isclose(float(controls.budget_alert.threshold_percent), float(notification.threshold_percent), rel_tol=0.0, abs_tol=1e-6)` against an enabled declared Bicep notification; raises `StreamError("BICEP_CONTRACT_MISMATCH")` on any infrastructure drift or unaligned threshold/type.
* Excluded: Modifying any file under `infra/`.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `BicepNotificationContract`, `BicepRunControlContract`, `verify_bicep_run_controls`.

#### Dependencies

* P01-T02, P02-T01.

#### Validation Expectations

* `verify_bicep_run_controls(INFRA, plan.preflight_controls())` returns a populated `BicepRunControlContract` for `80% Actual` and `100% Forecasted` and raises `StreamError("BICEP_CONTRACT_MISMATCH")` on tampered Bicep fixtures or unaligned alert thresholds.

#### Completion Evidence

* `verify_bicep_run_controls` implemented, typed, and exported in `run_plan.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit & Bicep Contract Tests and Validation

### Context

Caller Requirements 3 and 4 require focused unit and Bicep contract tests in `src/core/tests/test_simulator_run_controls_189.py` without touching `server.py`, `test_role_endpoint_inventory.py`, or `README.md`, verified by `unittest`, `ruff check`, `ruff format --check`, `mypy`, and `tools/rename-zava-tests.py`.

### Intent

Author comprehensive, non-redundant unit and Bicep contract tests in `src/core/tests/test_simulator_run_controls_189.py` and verify every required gate.

### Boundaries

* Included: `src/core/tests/test_simulator_run_controls_189.py` and execution of focused + regression validation commands.
* Excluded: Any modification to `server.py`, `test_role_endpoint_inventory.py`, or `README.md`.

### Likely Targets

* `src/core/tests/test_simulator_run_controls_189.py`: new focused test suite for Issue #189 Criterion 3.

### Dependencies

* P01, P02.

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_simulator_run_controls_189.py -q` exits `0`.
* `(cd src/core && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy)` exits `0`.
* `python3 tools/rename-zava-tests.py` exits `0`.
* Sibling and full `src/core/tests` regression discovery (`PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -q` plus `src/api/tests/test_live_control.py`) exit `0`; optional `bicep`/`az bicep build` ARM JSON check runs with a bounded subprocess timeout (`timeout=30`).

### Completion Evidence

* Passing test and lint/type/naming command outputs recorded in `.copilot-tracking/changes/2026-11-15/simulator-run-controls-189-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Author `src/core/tests/test_simulator_run_controls_189.py` and run focused validation

#### Context

Tests in `src/core/tests` run under strict `mypy` and `test_dependency_rule.py` (`C10`) and resolve `INFRA = Path(__file__).resolve().parents[3] / "infra"` (`C9`).

#### Intent

Cover every edge case of named `owner`, bounded `time_limit_minutes` / `max_duration_seconds`, and linked `BudgetAlertContract` across runtime preflight, execution pacing/controller halts, CLI arguments, and Bicep source + compiled ARM JSON contracts.

#### Boundaries

* Included:
  * `OwnerControlTests`: rejects blank, whitespace, overlong, control-character, punctuation-only (`"---"`), `<template>`, placeholder (`"tbd"`, `"pending"`, `"unassigned"`), and anonymous/non-human (`"anonymous"`, `"Anonymous"`, `"anon"`, `"guest"`, `"unattended"`, `"system"`, `"auto"`, `"automated"`, `"bot"`, `"null"`, `"nil"`) owners across `SimulatorRunControls`, `RunGovernance`, `RunPlan`, `RunBudget`, `Pacer`, and `run_plan.main`; accepts human and role identifiers.
  * `BoundedDurationTests`: tests `resolve_duration_seconds`, `SimulatorRunControls`, `RunGovernance.from_minutes`, `RunPlan.from_controls`, `Pacer.__init__`, `Pacer.set_max_per_second`, `RunController.check_time_limit`, and CLI `--time-limit-minutes` (rejecting missing, `0`, negative, `< 1s`, `> 60m` / `> 3600s`, `NaN`, `inf`, `bool`, and mismatched minute/second arguments; halting at deadline with `RUN_DEADLINE`).
  * `BudgetAlertPreflightAndRuntimeTests`: tests `BudgetAlertContract` validation (rejecting blank/anonymous rule or alert owner, invalid threshold `<= 0` or `> 100` or `bool`/`NaN`, invalid `threshold_type`, partial GBP pair, `alert_gbp >= cap_gbp`), `RunController.preflight()` / `status()` schema across `idle`/`running`/`stopped`, and runtime alert-at-threshold + halt-before-cap (`RUN_BUDGET_HALT`).
  * `BicepRunControlContractTests`: verifies `verify_bicep_run_controls(INFRA, ...)` against real `infra/` files (`80% Actual` and `100% Forecasted` notifications, `owner` required tag, `replicaTimeout == 240 <= 3600`, `replicaRetryLimit == 0`, `--once`, `/certs/control.json`), compiles `infra/modules/iothub.bicep` and `infra/live-simulator-job.bicep` via `az bicep build --stdout` when `az` is installed to assert ARM JSON budget notifications and job `replicaTimeout`, and proves `verify_bicep_run_controls` raises `BICEP_CONTRACT_MISMATCH` on tampered temporary copies of each Bicep control and on unaligned runtime threshold (`75%`).
* Excluded: Modifying any existing file outside the 3 planned `src/core/src/zava_forward/core/synthetic/*.py` modules.

#### Likely Targets

* `src/core/tests/test_simulator_run_controls_189.py`: focused unit and Bicep contract suite.

#### Dependencies

* P01, P02.

#### Validation Expectations

* All 3 caller validation commands plus sibling regression tests pass with exit code `0`.

#### Completion Evidence

* Green test, ruff, mypy, and rename-test runs with clean `git diff --name-only` check.

#### Unresolved Items

* None.
