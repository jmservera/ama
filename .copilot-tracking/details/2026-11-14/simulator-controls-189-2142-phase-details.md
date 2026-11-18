<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #189 Simulator Run Owner, Time Limit, and Budget Alert Controls

## Metadata

* Task ID: 189-simulator-controls-2142
* Task slug: simulator-controls-189-2142
* Related plan: .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md

## Phase Index

| Phase ID | Name                                                                 | Status   | Detail sections        |
|----------|----------------------------------------------------------------------|----------|------------------------|
| P01      | Harden simulator run governance and unified controller status        | complete | P01, P01-T01, P01-T02  |
| P02      | Regression tests, documentation, and `src/core` verification         | complete | P02, P02-T01, P02-T02  |

<!-- rpi:phase id=P01 -->
## P01: Harden simulator run governance and unified controller status in `src/core`

### Context

Research (`C1`-`C5`) showed that `RunPlan` and `RunGovernance` already enforce owner, bounded `max_seconds` (`<= 3600`), USD budget alert reference/threshold, and optional GBP threshold alert/pre-cap halt, while a partial uncommitted draft in the worktree introduced `RunMeter.summary()` and `RunController.status()` with five concrete gaps: inconsistent dictionary keys (`budget_alert_gbp` vs `alert_gbp`), idle-state `budget_alert_gbp: None` even when configured on the plan, post-halt/stop `elapsed_seconds` drift, unvalidated `planned_cost_gbp` when GBP alert/cap are omitted, and missing `"tbc"`/`"pending"` placeholder rejection. `sensor_stream.py` must remain untouched (`C5`).

### Intent

Make `run_governance.py` and `run_plan.py` fail-closed and schema-consistent across all states and currency modes without breaking `_body(plan)` estimate digests or `sensor_stream.py` provenance hashes.

### Boundaries

* Included: `src/core/src/zava_forward/core/synthetic/run_governance.py` and `src/core/src/zava_forward/core/synthetic/run_plan.py`.
* Excluded: `src/core/src/zava_forward/core/synthetic/sensor_stream.py`, `src/api/`, `infra/`.

### Likely Targets

* `src/core/src/zava_forward/core/synthetic/run_governance.py`: `governed_text()`, `RunMeter.ended`, `RunMeter.check_time_limit()`, `RunMeter.stop()`, `RunMeter.summary()`.
* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `RunPlan.governance()`, `RunPlan.validate()`, `RunController` lifecycle timestamps, `RunController.admit()`, `RunController.check_time_limit()`, `RunController.status()`.

### Dependencies

* None.

### Validation Expectations

* `python3 -m mypy` and `python3 -m ruff check .` pass with zero errors on both modules.

### Completion Evidence

* Updated `run_governance.py` and `run_plan.py` passing strict type and lint checks.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `RunGovernance` and `RunMeter` placeholder checks, deadline helper, and frozen runtime summary

#### Context

`RunGovernance.validate()` currently delegates owner checking to `sensor_stream.accountable_text()`, which lacks `"tbc"` and `"pending"` (`C2`), and `RunMeter.summary()` computes `self.clock() - self.started` live even after `_halt()` or deadline termination (`C2`).

#### Intent

Reject `"tbc"` and `"pending"` in `governed_text()`, expose deterministic `check_time_limit()` and idempotent `stop()` methods on `RunMeter` (transitioning `"running"` -> `"stopped"` and setting `ended = self.clock()` once without overwriting `"halted"` or `halt_reason`, and raising `StreamError("RUN_STOPPED")` when `status == "stopped"` vs `StreamError(self.halt_reason or "RUN_BUDGET_HALT")` when `"halted"`), freeze `ended` on halt or stop, clamp `remaining_seconds` to `max(0.0, ...)`, and report both `budget_alert_gbp` and `alert_gbp` plus `remaining_seconds` in `RunMeter.summary()`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/synthetic/run_governance.py`.
* Excluded: `sensor_stream.py`.

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/run_governance.py`: add `_EXTRA_PLACEHOLDERS = frozenset({"tbc", "pending"})` + `governed_text()`, `ended: float | None = None`, `check_time_limit()`, `stop()`, and updated `summary()`.

#### Dependencies

* None.

#### Validation Expectations

* `RunGovernance` rejects `"TBC"` and `"pending"` with `StreamError("RUN_OWNER_REQUIRED")`; `RunMeter.summary()` freezes `elapsed_seconds` and `remaining_seconds` after budget halt, deadline halt, or `stop()`.

#### Completion Evidence

* Clean `mypy` check and passing `GovernanceValidation` and `BudgetMeter` unit tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Harden `RunPlan` GBP validation and unify `RunController` status, `admit()`, and deadline controls

#### Context

`RunPlan.governance()` skips `planned_cost_gbp` when `budget_alert_gbp` and `budget_cap_gbp` are `None` and does not verify `isinstance(..., str)` before `json.dumps(asdict(plan))` (`C3`). `RunController.status()` returns mismatched keys depending on `self.meter`, `RunController.admit()` narrows `cost_gbp` to `str | int`, and USD-only runs have no direct deadline check or frozen elapsed clock on `RunController` (`C4`).

#### Intent

Enforce `isinstance(..., str)` and `planned_cost_gbp == 0` when ungoverned directly inside `RunPlan.governance()` (invoked by `RunPlan.validate()`), validate `governed_text` on `RunPlan`, call `self.plan.validate()` in `RunController.__init__()` so `idle` inspection is fail-closed and `budget_alert_gbp` is canonicalized via `str(Decimal)` in `idle` as well as `running`/`stopped`, widen `RunController.admit()` to `Decimal | int | str`, add `RunController.check_time_limit()` (raising `StreamError(self.halt_reason)` if halted or `StreamError("RUN_NOT_RUNNING")` if `idle`/manually `stopped`), record `_stopped_at = self.clock()` idempotently only when transitioning from `"running"` (keeping `idle` -> `stop()` elapsed time at `0.0` and clamping `remaining_seconds >= 0.0`), and unify `RunController.status()` across `idle`, `running`, and `stopped` states.

#### Boundaries

* Included: `src/core/src/zava_forward/core/synthetic/run_plan.py`.
* Excluded: `_body(plan)` top-level JSON schema (`plan`, `estimate`, `alert_fires_at_usd`, `sha256` remain unchanged for caller compatibility).

#### Likely Targets

* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `RunPlan.governance()`, `RunPlan.validate()`, `RunController.__init__()`, `admit()`, `check_time_limit()`, `status()`, `start()`, `stop()`, and CLI `--planned-cost-gbp` handling.

#### Dependencies

* P01-T01 (`governed_text`, `_gbp` validation helper or `RunGovernance`/`RunMeter` methods).

#### Validation Expectations

* `RunController.status()` exposes identical core governance keys before `start()`, while `running`, and after `stop()` or halt for both USD-only and USD+GBP plans; `check_time_limit()` stops the controller and raises `StreamError("RUN_DEADLINE")` at or past `max_seconds`.

#### Completion Evidence

* Clean `mypy` check and passing `test_simulator_run_budget_controls.py` and `test_run_plan.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Regression tests, documentation, and `src/core` verification

### Context

In `src/core/tests/`, only `test_simulator_run_budget_controls.py` matches the caller's `-p 'test_*simulator*.py'` pattern (`C6`), while `test_run_plan.py` and `test_sensor_stream.py` guard sibling contracts and Bicep static alignment.

### Intent

Lock all Criterion 3 behaviors in `test_simulator_run_budget_controls.py` (with zero removals and bounded focused additions), update `src/core/README.md`, and run all required static, format, and unit checks.

### Boundaries

* Included: `src/core/tests/test_simulator_run_budget_controls.py` and `src/core/README.md` (canonical source targets; no generated artifacts).
* Excluded: Unrelated test modules and docs outside `src/core/README.md`.

### Likely Targets

* `src/core/tests/test_simulator_run_budget_controls.py`: canonical test owner (0 removals, <= 8 focused test methods added/refined covering semantic Criterion 3 contracts and edge-case regressions).
* `src/core/README.md`: simulator cost/run-control section (`#189`).

### Dependencies

* P01.

### Validation Expectations

* Exact caller command passes: `cd /home/azureuser/source/ama-demo-wt/feat-189-simulator-controls-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*simulator*.py' -v`.
* Additional regression check passes: `python3 -m unittest tests/test_run_plan.py tests/test_sensor_stream.py -v`.

### Completion Evidence

* Command outputs recorded in `.copilot-tracking/changes/2026-11-14/simulator-controls-189-2142-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Expand `test_simulator_run_budget_controls.py` and update `src/core/README.md`

#### Context

Existing tests in `test_simulator_run_budget_controls.py` cover basic `RunGovernance`, `RunMeter`, and `RunController.admit()` wiring; they need semantic coverage of unified `status()` across `idle`/`running`/`stopped`, frozen runtime on stop/halt, `check_time_limit()` on USD-only and GBP-governed runs, `"TBC"`/`"pending"` refusal, un-governed `planned_cost_gbp` refusal, `Decimal` admission, and CLI error exits.

#### Intent

Add concise, non-duplicative regression tests in `test_simulator_run_budget_controls.py` (including repeated idempotent `stop()`, `idle` -> `stop()` elapsed `0.0`, post-stop `RUN_STOPPED` / `RUN_NOT_RUNNING` error codes, fail-closed `RunController(bad_plan)` construction, canonical `idle` `budget_alert_gbp`, and clamped `remaining_seconds == 0.0`) and document the updated `RunController` surface in `src/core/README.md`.

#### Boundaries

* Included: `src/core/tests/test_simulator_run_budget_controls.py` (0 removals, <= 8 added/expanded test methods), `src/core/README.md`.
* Excluded: Trivial constant/getter assertions.

#### Likely Targets

* `src/core/tests/test_simulator_run_budget_controls.py`
* `src/core/README.md`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Every new test fails without the P01 hardening and passes with it.

#### Completion Evidence

* Passing verbose `unittest` output for `test_*simulator*.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Run `src/core` static analysis, formatting, and simulator/sibling unit suites

#### Context

`src/core/pyproject.toml` enforces `mypy` `strict = true` and `ruff` `line-length = 100` (`E`, `F`, `I`, `B`, `UP`).

#### Intent

Prove full type, lint, format, and unit-test compliance in `src/core` and verify `sensor_stream.py` was not modified.

#### Boundaries

* Included: Running `mypy`, `ruff check`, `ruff format --check`, and `unittest` in `src/core`.
* Excluded: Network or Azure calls.

#### Likely Targets

* `src/core/` verification run only (no additional file edits unless fixing a check failure).

#### Dependencies

* P02-T01.

#### Validation Expectations

* Exit code 0 across all commands; `git diff -- src/core/src/zava_forward/core/synthetic/sensor_stream.py` is empty.

#### Completion Evidence

* Exact command exit statuses and test counts captured in changes artifact.

#### Unresolved Items

* None.
