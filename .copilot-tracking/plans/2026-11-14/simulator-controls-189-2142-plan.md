<!-- markdownlint-disable-file -->
# RPI Plan: Issue #189 Simulator Run Owner, Time Limit, and Budget Alert Controls

## Task Metadata

* Task ID: 189-simulator-controls-2142
* Task slug: simulator-controls-189-2142
* Planning status: implementation-ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/simulator-controls-189-2142-critique.md

## Executive Summary

This plan completes the remaining locally verifiable acceptance criterion for Issue #189 in `src/core`: ensuring every simulator run has a validated human owner, a bounded time limit, and an inspectable, enforced budget alert across the full `RunPlan`, `RunGovernance`, `RunMeter`, and `RunController` lifecycle. Building on the existing pre-run B1 quota/USD estimate and GBP spend meter, the changes unify `RunController.status()` across `idle`, `running`, and `stopped` states, freeze elapsed and remaining runtime upon halt or stop, add direct controller deadline enforcement (`check_time_limit()`), close a gap where `planned_cost_gbp` went unvalidated when GBP alert/cap fields were omitted, and align owner/alert placeholder refusals (`"tbc"`, `"pending"`) without touching `sensor_stream.py`.

### User Decisions and Requirements Highlights

* Deliver the locally verifiable acceptance criterion "Run has an owner, a time limit and a budget alert" in `src/core` on branch `feat/iot-189-simulator-controls-2142`, verified with bare `mypy`, `ruff check`, `ruff format --check`, and `unittest discover -s tests -p 'test_*simulator*.py' -v`.
* Write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), commit cleanly with the Copilot `Co-authored-by` trailer, and do **not** push (`git status --short` must be empty).

### What You May Not Know

* `src/core/src/zava_forward/core/synthetic/sensor_stream.py` is hashed into `generator_revision` by `sensor_stream.revision_sources()`, so all owner/alert placeholder refinements stay in `run_governance.py` and `run_plan.py` to avoid changing synthetic stream provenance digests.
* Offline `src/core` governance enforces caller-declared USD and GBP planning figures and static Bicep alignment (`InfraAlignmentTests`), whereas live Azure `Microsoft.Consumption/budgets` notification verification remains tracked separately under #146 and #189 (`Refs #189`).

### Unresolved Decisions or Blockers

* None for local `src/core` delivery. Live Azure budget alert verification (#146) remains a separate external gate outside this offline slice.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (research, plan, implement, review) for Issue #189 on branch `feat/iot-189-simulator-controls-2142` in `/home/azureuser/source/ama-demo-wt/feat-189-simulator-controls-2142` (caller prompt).
* Deliver the remaining locally verifiable acceptance criterion in `src/core`: "Run has an owner, a time limit and a budget alert" (caller prompt; Issue #189; PRD FR-050, AC-066; ADR 0003 Decision 6).
* Write all 4 `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`) (caller prompt).
* Verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*simulator*.py' -v` (caller prompt).
* Commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and `Refs #189` (because live Azure alert verification #146 remains unmet), and do not push so `git status --short` is empty (caller prompt; repository instructions).

## Goals

* Guarantee that every `RunPlan`, `RunGovernance`, `RunMeter`, and `RunController` instance enforces a non-placeholder owner, a bounded `1..3600` second time limit, and a validated budget alert (mandatory USD alert reference/threshold plus optional paired GBP spend alert and pre-cap halt).
* Provide a single, schema-consistent `RunController.status()` and `RunMeter.summary()` surface across `idle`, `running`, and `stopped` states with accurate frozen runtime accounting on stop or halt.
* Prove all Criterion 3 invariants and edge cases under `test_simulator_run_budget_controls.py` with zero `mypy`, `ruff`, or sibling test regressions.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/synthetic/run_governance.py`: `governed_text` placeholder hardening (`"tbc"`, `"pending"`), `RunMeter.check_time_limit()`, `RunMeter.stop()`, frozen halt/stop elapsed and remaining seconds, and consistent `RunMeter.summary()` keys.
* `src/core/src/zava_forward/core/synthetic/run_plan.py`: `governed_text` owner/alert validation, strict `str` and `planned_cost_gbp` validation even when GBP alert/cap are omitted, `Decimal | int | str` typing on `RunController.admit()`, `RunController.check_time_limit()`, stop/halt timestamp freezing, and unified `RunController.status()`.
* `src/core/tests/test_simulator_run_budget_controls.py`: focused unit and CLI tests covering Criterion 3 across `idle`, `running`, and `stopped` states, USD-only and USD+GBP runs, deadline expiry, and invalid inputs.
* `src/core/README.md`: concise documentation of `RunController.status()`, `check_time_limit()`, and strict `planned_cost_gbp` governance.

### Non-Goals

* Modifying `sensor_stream.py` (would alter `generator_revision` synthetic provenance digests) or changing `_body(plan)` top-level JSON estimate keys (would break existing `src/api` and `test_run_plan.py` callers).
* Deploying Azure infrastructure, invoking live Azure IoT Hub or Consumption APIs (#146), or pushing commits to `origin`.

## Functional Requirements

* FR-1: Reject blank, template (`<...>`), overlong (`> 160` chars), and placeholder (`tbd`, `tbc`, `todo`, `n/a`, `na`, `none`, `unknown`, `nobody`, `unassigned`, `pending`) run owner and alert reference values in `RunGovernance` and `RunPlan`.
  * Observable acceptance criteria: `RunGovernance.validate()` raises `StreamError("RUN_OWNER_REQUIRED")` and `RunPlan.validate()` raises `StreamError("RUN_OWNER_COST_ALERT_REQUIRED")` for all placeholder variants including `"TBC"` and `"pending"`.
* FR-2: Validate `planned_cost_gbp`, `budget_alert_gbp`, and `budget_cap_gbp` strictly on `RunPlan` as JSON-safe strings representing finite `Decimal` values, rejecting nonzero or malformed `planned_cost_gbp` when GBP alert/cap are omitted.
  * Observable acceptance criteria: `RunPlan(..., planned_cost_gbp="1.00")` without `budget_alert_gbp`/`budget_cap_gbp`, malformed `planned_cost_gbp`, or non-`str` GBP fields raise `StreamError("INVALID_BUDGET")`.
* FR-3: Enforce the run time limit (`1 <= max_seconds <= 3600`), distinguish idempotent operator stops from budget/deadline halts, and freeze elapsed/remaining runtime on halt or stop across both GBP-metered and USD-only `RunController` runs.
  * Observable acceptance criteria: `RunController.check_time_limit()` and `RunController.admit()` stop the run and raise `StreamError("RUN_DEADLINE")` once elapsed time reaches `max_seconds`; `RunMeter.stop()` and `RunController.stop()` are idempotent, preserve `"halted"` meter status and `halt_reason`, keep `idle` -> `stop()` elapsed time at `0.0`, clamp `remaining_seconds` to `>= 0.0`, and raise `RUN_STOPPED` / `RUN_NOT_RUNNING` on post-stop calls rather than misreporting `RUN_BUDGET_HALT`.
* FR-4: Validate `RunPlan` fail-closed upon `RunController` construction and report a unified governance snapshot from `RunController.status()` across `idle`, `running`, and `stopped` states.
  * Observable acceptance criteria: `RunController(plan)` validates `plan` in `__init__()` and `RunController.status()` always returns `state`, `run_owner`, `time_limit_seconds`, `elapsed_seconds`, `remaining_seconds` (`>= 0.0`), `active_homes`, `alert_reference`, `alert_fires_at_usd`, canonical `budget_alert_gbp` (`str(_gbp(...))` when configured, even in `idle`, else `None`), `alert_raised`, and `halt_reason`, plus `accumulated_gbp`, `alert_gbp`, `cap_gbp`, and `status` when GBP metering is active, accepting `Decimal | int | str` in `RunController.admit()`.

## Non-Functional Requirements

* NFR-1: Deterministic offline execution and strict static type/style cleanliness in `src/core`.
  * Objective threshold or evaluation condition: Zero `mypy` errors (`strict = true`), zero `ruff check` issues, zero `ruff format --check` diffs (line-length 100), and 100% pass rate on `test_*simulator*.py`, `test_run_plan.py`, and `test_sensor_stream.py` using injected deterministic clocks and zero network calls.
  * Operating condition or verification approach, if needed: Run verification directly in `src/core` and confirm `sensor_stream.py` remains untouched (`git diff src/core/src/zava_forward/core/synthetic/sensor_stream.py` empty).
  * Observable acceptance criteria: All verification commands exit 0 and `git status --short` is empty after commit.

## Acceptance Criteria

* Every simulator `RunPlan` and `RunGovernance` refuses missing, template, or placeholder owners (including `"TBC"` and `"pending"`), unbounded or non-finite time limits, and missing, invalid, or un-governed budget alerts/spend.
* `RunController.status()` exposes consistent owner, time-limit (`time_limit_seconds`, frozen `elapsed_seconds`, `remaining_seconds`), and budget-alert (`alert_reference`, `alert_fires_at_usd`, `budget_alert_gbp`, `alert_raised`, `halt_reason`) fields in `idle`, `running`, and `stopped` states for both USD-only and USD+GBP runs.
* `RunController.check_time_limit()` and `RunController.admit()` enforce `RUN_DEADLINE` and `RUN_BUDGET_HALT`, transitioning controller state to `"stopped"`, stopping the `Pacer`, and freezing elapsed time.
* `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*simulator*.py' -v` (plus `test_run_plan.py` and `test_sensor_stream.py`) pass in `src/core`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md                                                                   |
| Phase details                    | .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md                                                        |
| Latest critique                  | .copilot-tracking/critiques/2026-11-14/simulator-controls-189-2142-critique.md with Revise verdict resolved via PC-001 and PC-002        |
| Relevant research                | .copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md                                                            |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/simulator-controls-189-2142-changes.md is created by implementation as its evidence record          |
| Planning execution and readiness | Complete and implementation-ready                                                                                                        |
| Continuation context             | Confirmed automatic RPI Agent continues directly to `rpi-implement`                                                                      |

## Sources

* .copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md: Primary codebase evidence (`C1`-`C6`) and converged design.
* src/core/src/zava_forward/core/synthetic/run_governance.py: Existing `RunGovernance` and `RunMeter` contract.
* src/core/src/zava_forward/core/synthetic/run_plan.py: Existing `RunPlan`, `record()`, `RunController`, and CLI entrypoint.
* src/core/tests/test_simulator_run_budget_controls.py: Canonical simulator governance unit test target matched by `test_*simulator*.py`.
* docs/adrs/0003-journey-derived-capabilities-runtime-fit.md and docs/reference/research/iot-sensor-analytics-research-plan.md: Architectural and live-vs-offline evidence boundaries for Issue #189.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden simulator run governance and unified controller status in `src/core`

* Intent: Enforce complete owner, bounded time-limit, and USD/GBP budget-alert invariants and expose a unified, clock-accurate status surface on `RunMeter` and `RunController`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `RunGovernance` and `RunMeter` placeholder checks, deadline helper, and frozen runtime summary

* Requirement and evidence: FR-1, FR-3, FR-4; Research `C1`, `C2`, `C5`.
* Expected result: `governed_text` rejects `"tbc"` and `"pending"` alongside `accountable_text`; `RunMeter` exposes `check_time_limit()` and `stop()`, freezes `ended` timestamp on halt or stop, and returns consistent `budget_alert_gbp`/`alert_gbp` and `remaining_seconds` in `summary()`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Harden `RunPlan` GBP validation and unify `RunController` status, `admit()`, and deadline controls

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4; Research `C3`, `C4`, `C6`.
* Expected result: `RunPlan` validates `governed_text`, enforces JSON-safe `str` GBP inputs, and rejects nonzero or invalid `planned_cost_gbp` when GBP alert/cap are omitted; `RunController` accepts `Decimal | int | str` in `admit()`, enforces `check_time_limit()`, freezes elapsed time on `stop()`, and returns a consistent `status()` dictionary across `idle`, `running`, and `stopped` states.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Regression tests, documentation, and `src/core` verification

* Intent: Lock Criterion 3 behavior with focused unit tests, update `src/core/README.md`, and verify static typing, formatting, lint, and unit tests.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Expand `test_simulator_run_budget_controls.py` and update `src/core/README.md`

* Requirement and evidence: FR-1..FR-4, NFR-1; Research `C2`, `C3`, `C4`, `C6`.
* Expected result: `test_simulator_run_budget_controls.py` adds <= 8 focused test methods (0 test removals) covering unified `status()` across `idle`/`running`/`stopped`, USD-only vs GBP-governed status, frozen elapsed/remaining time after stop/halt, `check_time_limit()` deadline stop, `"TBC"`/`"pending"` refusal, un-governed `planned_cost_gbp` refusal, `Decimal` admission, and CLI flags; `src/core/README.md` documents `status()` and `check_time_limit()`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Run `src/core` static analysis, formatting, and simulator/sibling unit suites

* Requirement and evidence: NFR-1; caller verification command; Research `C5`, `C6`.
* Expected result: `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, `python3 -m unittest discover -s tests -p 'test_*simulator*.py' -v`, plus `test_run_plan.py` and `test_sensor_stream.py` all pass with exit code 0.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md

## Dependencies

* `src/core` editable install and Python 3.12 toolchain (`mypy`, `ruff`, `unittest`): already installed in environment and verified read-only during research.
* `infra/modules/iothub.bicep`: read-only static alignment target checked by `test_run_plan.py` (`InfraAlignmentTests`).

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 (`Revise`) — PC-001 [High]: Idempotent stop transitions and post-stop error codes across `RunMeter` and `RunController` | applied | Updated FR-3 and P01-T01/P01-T02/P02-T01 details so `RunMeter.stop()` only transitions `"running"` -> `"stopped"` once (preserving `"halted"` and `halt_reason`), `RunMeter.admit()`/`check_time_limit()` raise `RUN_STOPPED` when stopped, `RunController.stop()` records `_stopped_at` only on the `"running"` -> `"stopped"` transition (keeping `idle` -> `stop()` at `0.0`s), and `RunController.check_time_limit()` raises `halt_reason` when halted or `RUN_NOT_RUNNING` otherwise. |
| Run 1 (`Revise`) — PC-002 [Medium]: Fail-closed `RunController.__init__` validation, canonical `idle` GBP alert string, and clamped `remaining_seconds` | applied | Updated FR-4 and P01-T01/P01-T02/P02-T01 details so `RunPlan.governance()` directly enforces `str` GBP inputs and zero `planned_cost_gbp` when ungoverned, `RunController.__init__()` calls `self.plan.validate()` and normalizes configured `idle` `budget_alert_gbp` via `str(gov_alert)`, and `remaining_seconds` is clamped to `max(0.0, ...)`. |

## Follow-Up Items

* Live Azure `Microsoft.Consumption/budgets` alert firing and subscription headroom verification (#146, #189): outside local `src/core` scope; owned by project owner during an approved live Azure IoT Hub exercise.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/simulator-controls-189-2142-changes.md
* Ready phase or task: All phases (`P01`, `P02`) complete; ready for `rpi-review`
* Remaining provisional question or blocker: none
