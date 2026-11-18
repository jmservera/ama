<!-- markdownlint-disable-file -->
# RPI Plan: Issue #189 Simulator Run Controls (Owner, Time Limit, and Budget Alert)

## Task Metadata

* Task ID: issue-189-simulator-run-controls
* Task slug: simulator-run-controls-189
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/simulator-run-controls-189-plan-critique.md

## Executive Summary

This plan delivers the sole remaining unticked acceptance criterion of Issue #189 (`Run has an owner, a time limit and a budget alert`, PRD FR-050, AC-066, and ADR 0003 Decision 6) inside `src/core` without touching `server.py`, `test_role_endpoint_inventory.py`, or any `README.md`, ensuring conflict-free stacking onto `feat/demo-164-chat-grounding-provenance-0900` (#1641). It closes four concrete bypasses discovered during research: (1) anonymous, unattended, system/bot, control-character, and punctuation-only owner strings passing `accountable_text` / `governed_text`; (2) direct `Pacer(budget)` construction bypassing `RunBudget` preflight validation; (3) missing first-class `time_limit_minutes` / `max_duration_seconds` and linked `BudgetAlertContract` (`threshold_percent`, `alert_rule_reference`, `alert_owner_reference`) runtime preflight across `RunGovernance`, `RunPlan`, `RunController`, and CLI `run_plan.main`; and (4) incomplete runtime-to-Bicep contract verification across `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, and `infra/live-simulator-job.bicep`.

### User Decisions and Requirements Highlights

* Enforce a named `owner` (non-empty human or role identifier, rejecting blank, placeholder, and anonymous owners), a bounded `time_limit_minutes` / `max_duration_seconds` preventing unattended runs, and a linked `budget_alert` contract (threshold + alert rule/owner reference) in runtime preflight and Bicep/infra contract tests.
* Add focused unit and contract tests in `src/core/tests/test_simulator_run_controls_189.py` while leaving `server.py`, `test_role_endpoint_inventory.py`, and `README.md` untouched for conflict-free PR stacking.
* Validate with `unittest`, `ruff check`, `ruff format --check`, strict `mypy`, and `tools/rename-zava-tests.py`, then commit locally with `Refs #189` and the Copilot trailer without pushing.

### What You May Not Know

* `RunPlan` serialises `asdict(plan)` into `estimate.json` via `_body(plan)` and verifies its SHA-256 digest before `RunController.start()`; keeping existing `RunPlan` fields intact while exposing `RunPlan.from_controls()`, `time_limit_minutes` / `max_duration_seconds`, `budget_alert_contract()`, and `preflight_controls()` preserves 100% compatibility with existing `src/core` and `src/api` callers.
* `src/api`'s `live_control.py` delegates `owner` validation directly to `zava_forward.core.synthetic.sensor_stream.accountable_text`, so hardening `accountable_text` simultaneously blocks anonymous owners in live control files while preserving short alphanumeric fixture identifiers (`"o"`, `"r"`) used in `src/api/tests/test_live_control.py`.
* Keeping `infra/*.bicep` read-only and verifying the real Bicep declarations (`iothub.bicep`, `main.bicep`, `governance.bicep`, `live-simulator-job.bicep`) from `src/core` contract checks avoids triggering infrastructure deployment gates and prevents merge conflicts with sibling branches.

### Unresolved Decisions or Blockers

* None for local delivery. Live Azure `Microsoft.Consumption/budgets` notification delivery remains an external hosted gate under #146/#189, so the commit honestly uses `Refs #189` rather than a closing keyword.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated artifacts under `.copilot-tracking/` for Issue #189 on branch `feat/iot-189-run-controls` targeting `feat/demo-164-chat-grounding-provenance-0900` (#1641) (caller prompt).
* Deliver the unticked acceptance criterion `[ ] Run has an owner, a time limit and a budget alert` per PRD FR-050, AC-066, and ADR 0003 Decision 6 (caller prompt; Issue #189).
* Require every simulator run configuration and invocation to specify a named `owner` (non-empty human/role identifier, rejecting anonymous/blank owners), a bounded `time_limit_minutes` / `max_duration_seconds` (`1..3600` seconds / `<= 60` minutes), and a linked `budget_alert` contract (threshold + alert rule/owner reference) verified in both runtime preflight and Bicep/infra contract tests (caller prompt).
* Place focused unit and Bicep contract tests in `src/core/tests/test_simulator_run_controls_189.py` without touching `server.py`, `test_role_endpoint_inventory.py`, or `README.md` (caller prompt).
* Pass `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_simulator_run_controls_189.py -q`, `(cd src/core && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy)`, and `python3 tools/rename-zava-tests.py`, commit with `Refs #189` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave a clean working tree, and do not push (caller prompt).

## Goals

* Eliminate anonymous, unattended, placeholder, and non-identifier owner bypasses across all `src/core` simulator configuration and execution surfaces (`RunBudget`, `Pacer`, `RunGovernance`, `RunPlan`, `RunController`, `SimulatorRunControls`).
* Enforce bounded run duration (`1.0 <= max_duration_seconds <= 3600.0`, `time_limit_minutes <= 60.0`) at both configuration preflight and runtime pacing/controller admission so no simulator run can execute open-ended.
* Enforce a structured, linked `BudgetAlertContract` (numeric threshold percentage, governed alert rule reference, and named alert owner/contact reference, plus optional USD/GBP caps) verified at runtime preflight and cross-checked against `infra/` Bicep declarations.
* Deliver deterministic unit and Bicep contract coverage in `src/core/tests/test_simulator_run_controls_189.py` with zero edits to conflict-prone files.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/synthetic/sensor_stream.py`: harden `accountable_text`, extract `RunBudget.preflight()` and `RunBudget._preflight_envelope()`, enforce owner/duration/message envelope preflight in `Pacer.__init__()`, enforce `INVALID_RUN_RATE` in `Pacer.admit_send()`, and bound `Pacer.set_max_per_second()`.
* `src/core/src/zava_forward/core/synthetic/run_governance.py`: add `MIN_TIME_LIMIT_SECONDS`, `MAX_TIME_LIMIT_MINUTES`, `resolve_duration_seconds()`, `BudgetAlertContract`, `SimulatorRunControls`, and `RunGovernance.from_minutes()` / duration properties.
* `src/core/src/zava_forward/core/synthetic/run_plan.py`: wire `BudgetAlertContract` and `SimulatorRunControls` into `RunPlan` (`from_controls()`, `time_limit_minutes`, `max_duration_seconds`, `budget_alert_contract()`, `preflight_controls()`), `RunController` (`preflight()`, `status()`), CLI `main()` (`--time-limit-minutes`, `--alert-owner`), and `verify_bicep_run_controls()`.
* `src/core/tests/test_simulator_run_controls_189.py`: focused unit tests and Bicep/infra contract alignment + fail-closed negative tests.

### Non-Goals

* Modifying `server.py`, `test_role_endpoint_inventory.py`, any `README.md`, or `infra/*.bicep`.
* Live Azure IoT Hub or `Microsoft.Consumption/budgets` deployment/runtime notification testing (#146).
* Pushing commits to `origin` (`git push` prohibited).

## Functional Requirements

* **Named owner enforcement**: `accountable_text` and `governed_text` reject blank, whitespace, overlong (`> 160` chars), control-character, punctuation-only, `<template>`, placeholder, and anonymous/unattended/system tokens (`anonymous`, `anon`, `guest`, `unattended`, `unowned`, `null`, `nil`, `tbd`, `tbc`, `todo`, `pending`, `n/a`, `na`, `none`, `unknown`, `nobody`, `unassigned`, `system`, `auto`, `automated`, `bot`), while accepting human names and role identifiers containing alphanumeric characters.
  * Observable acceptance criteria: Passing any blank, placeholder, punctuation-only, or anonymous owner to `SimulatorRunControls`, `RunGovernance`, `RunPlan`, `RunBudget`, `Pacer`, or `run_plan.main` raises `StreamError` (`RUN_OWNER_REQUIRED` or `RUN_OWNER_COST_ALERT_REQUIRED` / CLI exit `2`).
* **Bounded duration (`time_limit_minutes` / `max_duration_seconds`)**: `resolve_duration_seconds`, `SimulatorRunControls`, `RunGovernance.from_minutes`, `RunPlan.from_controls`, `Pacer.__init__`, and `run_plan.main` require a finite duration in `1.0..3600.0` seconds (`<= 60.0` minutes), reject missing/zero/negative/over-limit/NaN/infinite/`bool` durations and conflicting minute-vs-second inputs, and stop execution with `RUN_DEADLINE` when elapsed time reaches the limit.
  * Observable acceptance criteria: Omitting both duration inputs, exceeding `60` minutes (`3600` seconds), passing `max_seconds <= 0` to `Pacer(RunBudget(...))`, or passing mismatched `time_limit_minutes` and `max_duration_seconds` raises `StreamError` before execution starts; reaching the limit halts `RunController` / `Pacer` with `RUN_DEADLINE`.
* **Linked `BudgetAlertContract` preflight and Bicep alignment**: `BudgetAlertContract` links `threshold_percent` (`0 < threshold <= 100`), `alert_rule_reference`, and named `alert_owner_reference` (plus optional USD/GBP caps with `alert < cap`), is enforced by `SimulatorRunControls.preflight()` and `RunPlan.validate()` / `RunController`, and is verified against `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, and `infra/live-simulator-job.bicep` via `verify_bicep_run_controls()`.
  * Observable acceptance criteria: Missing/anonymous alert rule or alert owner references, out-of-range thresholds, or Bicep contract drift (missing `owner` in `requiredTags`, unbounded `replicaTimeout`, disabled `actual80`/`forecast100`, missing `contactEmails`, or unaligned runtime threshold/type) fail closed with `StreamError`.

## Non-Functional Requirements

* **Strict static typing, lint cleanliness, and core dependency isolation**: All touched and added files in `src/core` satisfy `mypy` (`strict = true`), `ruff check`, `ruff format --check`, `test_dependency_rule.py` (no imports outside `zava_forward.core`), and `tools/rename-zava-tests.py`.
  * Objective threshold or evaluation condition: Zero `mypy`, `ruff`, dependency-rule, or Zava-naming errors.
  * Operating condition or verification approach, if needed: Execute the exact validation commands from Requirement 4 plus existing `src/core` simulator regression suites.
  * Observable acceptance criteria: All validation commands exit `0`.
* **Backward compatibility and conflict-free stacking**: Existing `RunPlan` JSON estimate SHA-256 digests (`_body(plan)`) and existing `src/core` / `src/api` simulator tests remain unbroken, and excluded files remain untouched.
  * Objective threshold or evaluation condition: Zero regressions across `test_sensor_stream.py`, `test_run_plan.py`, `test_simulator_run_budget_controls.py`, and `src/api/tests/test_live_control.py`; `git diff --name-only` contains none of `server.py`, `test_role_endpoint_inventory.py`, or `*README.md`.
  * Observable acceptance criteria: Existing test suites pass and excluded paths show zero changes.

## Acceptance Criteria

* Every simulator run configuration/invocation surface (`SimulatorRunControls`, `RunPlan`, `RunController`, `RunGovernance`, `RunBudget`, `Pacer`, `run_plan.main`) requires a non-empty named `owner` and rejects blank, placeholder, and anonymous/unattended/system owners.
* Every simulator run requires a bounded duration (`1.0 <= max_duration_seconds <= 3600.0`, `time_limit_minutes <= 60.0`), supports configuring duration in minutes or seconds, refuses conflicting or unbounded values in preflight, and halts at the deadline (`RUN_DEADLINE`).
* Every simulator run requires a linked `BudgetAlertContract` (`threshold_percent`, `alert_rule_reference`, `alert_owner_reference`) verified both in runtime preflight and against `infra/` Bicep declarations (`iothub.bicep`, `main.bicep`, `governance.bicep`, `live-simulator-job.bicep`).
* `src/core/tests/test_simulator_run_controls_189.py` covers positive and negative cases for owner, duration, runtime budget-alert preflight/halt, and Bicep contract verification (including tampered Bicep negative tests and optional `az bicep build` check).
* Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `tools/rename-zava-tests.py`) passes with zero touches to `server.py`, `test_role_endpoint_inventory.py`, or `README.md`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md                                                                    |
| Phase details                    | .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md                                                         |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/simulator-run-controls-189-plan-critique.md with Revise disposition resolved directly (PC-001, PC-002, PC-003) |
| Relevant research                | .copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md                                                             |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/simulator-run-controls-189-changes.md is created by implementation as its evidence record           |
| Planning execution and readiness | Complete and Ready for implementation (`P01` through `P03`)                                                                              |
| Continuation context             | Confirmed automatic RPI Agent session transitions automatically to `rpi-implement`                                                       |

## Sources

* `.copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md`: `C1`–`C10` codebase, Bicep, caller, and tooling evidence.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (FR-050, AC-066) & `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` (Decision 6): simulator owner, bounded duration, and budget-alert governance specification.
* `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, `infra/live-simulator-job.bicep`: authoritative Bicep declarations for `actual80` / `forecast100` budget notifications, `alertEmail`, required `owner` tag, and `replicaTimeout: 240`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Owner Validation, Stream Budget Preflight, and Core Run-Control Contracts

* Intent: Close anonymous/non-identifier owner and unvalidated `Pacer` bypasses in `sensor_stream.py`, and introduce `resolve_duration_seconds`, `BudgetAlertContract`, and `SimulatorRunControls` in `run_governance.py`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `accountable_text` and enforce `RunBudget` preflight in `Pacer`

* Requirement and evidence: Anonymous/blank owner rejection and `Pacer` preflight bypass (`C1`, `C8` in research; `src/api/tests/test_iot_stream.py` caller compatibility).
* Expected result: `accountable_text` rejects anonymous/unattended/system/control-char/punctuation-only strings while preserving alphanumeric identifiers; `RunBudget.preflight()` runs in `RunBudget.validate()`, `RunBudget._preflight_envelope()` runs in `Pacer.__init__()`, `Pacer.admit_send()` enforces `INVALID_RUN_RATE` before admitting sends, and `Pacer.set_max_per_second()` rejects invalid rates with `INVALID_RUN_LIMIT`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `resolve_duration_seconds`, `BudgetAlertContract`, and `SimulatorRunControls` to `run_governance.py`

* Requirement and evidence: Bounded `time_limit_minutes` / `max_duration_seconds` and linked `budget_alert` contract (`C2` in research).
* Expected result: `run_governance.py` defines `MIN_TIME_LIMIT_SECONDS`, `MAX_TIME_LIMIT_MINUTES`, `resolve_duration_seconds()`, `BudgetAlertContract`, `SimulatorRunControls`, and `RunGovernance.from_minutes()` + duration properties with strict fail-closed `StreamError` codes.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Wire Run-Control Contracts and Bicep Alignment Verifier into `run_plan.py`

* Intent: Integrate `BudgetAlertContract`, `SimulatorRunControls`, `time_limit_minutes`, and deterministic Bicep contract verification into `RunPlan`, `RunController`, and `run_plan.main` without altering existing `estimate.json` SHA-256 digests.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Integrate `SimulatorRunControls`, `BudgetAlertContract`, and `--time-limit-minutes` / `--alert-owner` into `RunPlan`, `RunController`, and CLI

* Requirement and evidence: Every simulator run configuration/invocation enforces owner, bounded duration, and linked budget alert (`C3`, `C9` in research).
* Expected result: `RunPlan` provides `from_controls()`, `max_duration_seconds`, `time_limit_minutes`, `budget_alert_contract()`, and `preflight_controls()` (invoked in `validate()`); `RunController` exposes `preflight()` and includes `time_limit_minutes`, `max_duration_seconds`, and `budget_alert` in `status()`; `run_plan.main()` supports `--time-limit-minutes` and `--alert-owner` while preserving existing `_body(plan)` digests.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Implement `BicepRunControlContract` and `verify_bicep_run_controls()` in `run_plan.py`

* Requirement and evidence: Linked `budget_alert`, owner, and bounded runtime verified against `infra/` Bicep declarations (`C4`, `C5`, `C6` in research).
* Expected result: `verify_bicep_run_controls(infra_dir, controls=...)` parses and validates `governance.bicep` (`owner` in `requiredTags`), `main.bicep` (`ownerTag`, `alertEmail`, `budget-${prefix}`), `modules/iothub.bicep` (`budget-${name}` scoped by `ResourceId`, enabled `actual80` / `forecast100` to `[alertEmail]`), and `live-simulator-job.bicep` (`replicaTimeout <= 3600`, `replicaRetryLimit == 0`, `--once`, `approvalReference`, `/certs/control.json`), and cross-checks runtime `SimulatorRunControls` / `BudgetAlertContract` alignment.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit & Bicep Contract Tests and Validation

* Intent: Prove runtime preflight, deadline/budget enforcement, and Bicep contract alignment in `src/core/tests/test_simulator_run_controls_189.py` and pass all focused checks cleanly.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author `src/core/tests/test_simulator_run_controls_189.py` and run focused validation

* Requirement and evidence: Caller Requirements 2, 3, and 4 (`C4`–`C10` in research).
* Expected result: `src/core/tests/test_simulator_run_controls_189.py` passes alongside existing simulator suites, `ruff check`, `ruff format --check`, `mypy`, and `tools/rename-zava-tests.py`, with zero changes to excluded files.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md

## Dependencies

* Python 3.12 toolchain in `src/core` (`unittest`, `ruff`, `mypy`): executes unit, lint, formatting, and strict type checks (`PYTHONPATH=src/core/src:src/core/tests` isolates worktree `src/core` from `~/.local` editable install).
* Read-only `infra/` Bicep templates (`infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, `infra/live-simulator-job.bicep`): verified as source contracts (and compiled via `az bicep build` when `az` CLI is available).

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High] (`main.bicep` `alertEmail` & `allTags` contract) | Resolved | Updated `P02-T02` and `P03-T01` so `verify_bicep_run_controls()` verifies `main.bicep`'s actual required un-defaulted `param alertEmail string` wired to `contactEmails: [alertEmail]` and `owner: ownerTag` bound via `allTags` -> `tags: allTags` (`infra/main.bicep:20-21,165-185,345,585-611`). |
| `PC-002` [High] (`RunPlan` `alert_owner` / `alert_threshold_type`, GBP `str` normalization, CLI `StreamError` catch) | Resolved | Updated `P02-T01` to persist defaulted `alert_owner: str \| None = None` and `alert_threshold_type: str = "Actual"` on `RunPlan` (omitting default values in `_body(plan)` for legacy digest parity while binding non-defaults into SHA-256), normalize GBP fields to `str` in `from_controls()`, and wrap CLI duration resolution + `RunPlan` construction in `try ... except StreamError`. |
| `PC-003` [Medium] (unified `_PLACEHOLDERS`, `RunPlan.validate()` error precedence, `bool` rate guard, `math.isclose` Bicep threshold match, full `src/core/tests` discovery + timeout) | Resolved | Updated `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, and `P03-T01` to unify all placeholder/anonymous tokens in `sensor_stream._PLACEHOLDERS`, lock `RunPlan.validate()` error-code precedence, reject `bool`/non-finite rates in `set_max_per_second()`, use `math.isclose(..., abs_tol=1e-6)` on Bicep thresholds, bound `bicep` subprocess checks with `timeout=30`, and run full `src/core/tests` discovery. |

## Follow-Up Items

* Live Azure `Microsoft.Consumption/budgets` notification firing verification in the `ama` resource group: outside immediate scope because this PR slice is an offline `src/core` + Bicep contract slice without live Azure deployment privileges; triggered by Issue #189 and Issue #146 hosted deployment governance; next action owned by post-merge Azure deployment validation under Issue #146 / Issue #189.
* Surface `time_limit_minutes` and `budget_alert` summary fields in FastAPI admin live-control endpoints: outside immediate scope due to the explicit stack-isolation constraint prohibiting edits to `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py` while sibling PRs are active; triggered by `RunController.status()` schema enrichment in `P02-T01`; next action owned by a post-stack `src/api` follow-up PR once #1641 merges.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/simulator-run-controls-189-changes.md
* Ready phase or task: Review (`P01`, `P02`, and `P03` completed and reconciled)
* Remaining provisional question or blocker: None
