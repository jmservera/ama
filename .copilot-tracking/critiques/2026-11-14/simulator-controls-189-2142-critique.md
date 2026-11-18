<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #189 Simulator Run Owner, Time Limit, and Budget Alert Controls

## Metadata

* Task ID: 189-simulator-controls-2142
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the remaining locally verifiable acceptance criterion for Issue #189 ("Run has an owner, a time limit and a budget alert") in `src/core` on branch `feat/iot-189-simulator-controls-2142`, produce all four `.copilot-tracking/` stage artifacts (`research/`, `plans/`, `changes/`, `reviews/`), verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*simulator*.py' -v`, and commit cleanly with the Copilot `Co-authored-by` trailer without pushing (`git status --short` empty).
* Research and evidence considered: .copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md, .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md, .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md, src/core/src/zava_forward/core/synthetic/run_governance.py, src/core/src/zava_forward/core/synthetic/run_plan.py, src/core/src/zava_forward/core/synthetic/sensor_stream.py, src/core/tests/test_simulator_run_budget_controls.py, src/core/tests/test_run_plan.py, and src/core/README.md.
* Decisions, dependencies, and acceptance criteria considered: Preserve `sensor_stream.py` untouched because `sensor_stream.revision_sources()` hashes its bytes into `generator_revision` (`C5`); preserve `_body(plan)` top-level JSON schema for `RunController.start()` and `src/api` compatibility (`C3`, `C6`); enforce non-placeholder owner (`"tbc"` and `"pending"` included), `1 <= max_seconds <= 3600` time limit, and USD + optional paired GBP budget alerts; reference `#189` honestly (`Refs #189`) because live Azure `Microsoft.Consumption/budgets` alert firing remains tracked externally under #146.
* Assessment boundary: Evaluates local `src/core` governance correctness, state transitions, type/lint/test verifiability, and artifact hygiene from supplied repository files. Cannot assess live Azure IoT Hub or Consumption API behavior, which is explicitly out of scope (#146).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1-2 (Criterion 3 in `src/core`) | Partial | Covered across FR-1..FR-4 and P01..P02, subject to PC-001 (stop vs halt semantics and post-stop error codes) and PC-002 (fail-closed `RunController` construction, canonical `idle` GBP alert string, and clamped `remaining_seconds`). |
| Caller Req 3-5 (4 RPI artifacts, verification command, clean commit without push) | Covered | Recorded in User Decisions and Requirements, NFR-1, Implementation Context Record, and P02-T02 validation commands. |
| Research C1, C5 (`RunGovernance` baseline and `sensor_stream.py` provenance boundary) | Covered | Plan Non-Goals, P01 Boundaries, and P02-T02 explicitly forbid modifying `sensor_stream.py` and verify an empty diff on that file. |
| Research C2, FR-1, FR-3 (`governed_text` placeholders and frozen stop/halt elapsed time) | Partial | `governed_text` placeholder hardening is well specified; `RunMeter.stop()` / `RunController.stop()` idempotence, preservation of `status == "halted"`, and non-negative `remaining_seconds` clamping need explicit contract guards (PC-001, PC-002). |
| Research C3, FR-2 (strict `str` GBP inputs and un-governed `planned_cost_gbp` refusal) | Partial | FR-2 and P01-T02 reject nonzero or invalid `planned_cost_gbp` when GBP alert/cap are omitted; P01-T02 should ensure `RunPlan.governance()` enforces this directly and `RunController.__init__()` validates `plan` before `idle` inspection (PC-002). |
| Research C4, FR-4 (`RunController.status()` unification and `Decimal` admission) | Partial | Core key set and `Decimal \| int \| str` typing on `admit()` are covered, except `idle`-state canonicalization of `budget_alert_gbp` and non-negative `remaining_seconds` clamping (PC-002). |
| P01-T01 (`run_governance.py` hardening) | Partial | Missing guard against `RunMeter.stop()` overwriting `"halted"` state or `RunMeter.admit()`/`check_time_limit()` misreporting `"stopped"` as `"RUN_BUDGET_HALT"`, plus `remaining_seconds` lower bound `0.0` (PC-001, PC-002). |
| P01-T02 (`run_plan.py` hardening) | Partial | Missing idempotent `_stopped_at` transition rules from `"idle"` vs `"running"`, post-stop `check_time_limit()` error contract, and fail-closed `RunController.__init__()` validation (PC-001, PC-002). |
| Research C6, P02-T01, P02-T02 (`test_simulator_run_budget_controls.py`, `src/core/README.md`, and checks) | Covered | Targets the sole `-p 'test_*simulator*.py'` match plus sibling `test_run_plan.py` and `test_sensor_stream.py` suites alongside bare `mypy` and `ruff`. |

## Verdict

* Verdict: Revise
* Rationale: The candidate plan and phase details accurately isolate the four `src/core` target files, protect `sensor_stream.py` provenance hashes and `_body(plan)` digest compatibility, and wire the exact caller verification commands. Two bounded specification gaps in `P01-T01` and `P01-T02` (`PC-001` and `PC-002`) could cause manual stops to overwrite `"halted"` state, misreport `"RUN_BUDGET_HALT"`, drift timestamps on repeated `stop()` calls, or expose unvalidated/negative fields in `status()`. Both findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify idempotent stop transitions and post-stop error codes across RunMeter and RunController

* Related IDs: FR-3, FR-4, Research C2, Research C4, P01-T01, P01-T02, P02-T01
* Evidence: src/core/src/zava_forward/core/synthetic/run_governance.py (lines 86-93, 109-123), src/core/src/zava_forward/core/synthetic/run_plan.py (lines 182-191, 222-225), src/core/tests/test_simulator_run_budget_controls.py (lines 66, 89-95), .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md (P01-T01, P01-T02)
* Concern: `RunMeter.admit()` currently guards non-running meters with `if self.status != "running": raise StreamError(self.halt_reason or "RUN_BUDGET_HALT")` (`run_governance.py:111-112`), and `RunController.admit()` calls `self.stop()` inside its `except StreamError` handler after `self.meter.status == "halted"` (`run_plan.py:188-190`). Adding `RunMeter.stop()` and `RunController.check_time_limit()` without explicit transition rules creates three failure modes: (1) a manually stopped `RunMeter` has `halt_reason is None`, so subsequent `meter.admit()` or `meter.check_time_limit()` calls fall back to `"RUN_BUDGET_HALT"` instead of `"RUN_STOPPED"`; (2) `RunController.stop()` delegating to `self.meter.stop()` after a budget or deadline halt will overwrite `meter.status == "halted"` (breaking `test_simulator_run_budget_controls.py:66`) or overwrite `ended` / `_stopped_at` on repeated `stop()` calls or when `stop()` is called from `"idle"`; and (3) `RunController.check_time_limit()` lacks a defined error code when called outside `"running"`.
* Impact: Without idempotent transition guards and distinct `"stopped"` vs `"halted"` error codes, repeated `stop()` calls unfreeze `elapsed_seconds` (violating FR-3), budget/deadline halts lose `meter.status == "halted"`, and post-stop calls misclassify normal operator stops as budget breaches.
* Smallest useful change: Update `P01-T01`, `P01-T02`, and `P02-T01` in `.copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md` (and record disposition in `.copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md`) so that: (1) `RunMeter.stop()` only transitions `"running"` to `"stopped"` and records `ended = self.clock()` once when `ended is None`, leaving `"halted"` and `halt_reason` intact; (2) `RunMeter.admit()` and `RunMeter.check_time_limit()` raise `StreamError("RUN_STOPPED")` when `status == "stopped"` and `StreamError(self.halt_reason or "RUN_BUDGET_HALT")` when `status == "halted"`; (3) `RunController.stop()` only records `_stopped_at = self.clock()` when transitioning from `"running"` (`_started_at is not None and _stopped_at is None`), keeping `idle` -> `stopped` elapsed time at `0.0` and repeated `stop()` calls idempotent; and (4) `RunController.check_time_limit()` raises `StreamError(self.halt_reason)` if already halted (`"RUN_DEADLINE"` or `"RUN_BUDGET_HALT"`) and `StreamError("RUN_NOT_RUNNING")` if `"idle"` or manually `"stopped"`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, and `P02-T01` detail sections specifying idempotent `stop()` / `ended` / `_stopped_at` guards and post-stop `StreamError` codes, backed during implementation by unit assertions on repeated `stop()`, `idle` -> `stop()`, and post-stop `admit()` / `check_time_limit()` calls.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Enforce fail-closed RunPlan validation on RunController construction, canonical idle GBP alert strings, and non-negative remaining_seconds

* Related IDs: FR-1, FR-2, FR-3, FR-4, Research C2, Research C3, Research C4, P01-T01, P01-T02, P02-T01
* Evidence: src/core/src/zava_forward/core/synthetic/run_plan.py (lines 73-123, 173-201), src/core/src/zava_forward/core/synthetic/run_governance.py (lines 95-107), src/core/tests/test_simulator_run_budget_controls.py (lines 89-95, 181-184), src/core/tests/test_run_plan.py (lines 139-209), .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md (FR-2, FR-4), .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md (P01-T01, P01-T02)
* Concern: Three boundary behaviors remain implicit across `RunPlan`, `RunMeter.summary()`, and `RunController.status()`: (1) `RunController.__init__()` currently stores `plan` without calling `plan.validate()`, so calling `RunController(plan).status()` in `"idle"` state before `start()` can surface placeholder owners (`"TBD"`, `"TBC"`, `"pending"`), unvalidated time limits, or invalid GBP configurations instead of failing closed, and raw `plan.budget_alert_gbp` strings (such as `" 4.00 "`) can differ from `RunMeter.summary()["budget_alert_gbp"]` (`str(self.alert)`); (2) `RunPlan.governance()` is a public method that should directly enforce `isinstance(..., str)` on GBP fields and `planned_cost_gbp == 0` when GBP alert/cap are omitted so callers of `plan.governance()` cannot bypass `RunPlan.validate()`; and (3) when elapsed time exceeds `time_limit_seconds` (such as `now[0] = 700.0` against `600` seconds in `test_simulator_run_budget_controls.py:92`), unclamped `time_limit_seconds - elapsed_seconds` yields negative `remaining_seconds` (`-100.0`).
* Impact: Callers inspecting `RunController(plan).status()` in `"idle"` state can observe unvalidated or non-canonical governance fields, direct `plan.governance()` calls can ignore malformed/nonzero `planned_cost_gbp`, and post-deadline `remaining_seconds` becomes negative.
* Smallest useful change: Update `P01-T01` and `P01-T02` in `.copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md` (and `FR-4` / Critique Disposition in `.copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md`) to: (1) enforce `isinstance(..., str)` and `planned_cost_gbp` zero-when-ungoverned checks inside `RunPlan.governance()` (invoked by `RunPlan.validate()`); (2) call `self.plan.validate()` in `RunController.__init__()` (all existing `test_run_plan.py` and `test_simulator_run_budget_controls.py` `RunController` callers pass valid `RunPlan` instances) and normalize configured `budget_alert_gbp` via `str(_gbp(...))` in `"idle"`; and (3) clamp `remaining_seconds` to `max(0.0, round(time_limit_seconds - elapsed_seconds, 3))` (with `elapsed_seconds = 0.0` before `start()`).
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01` and `P01-T02` phase details and `FR-4` acceptance wording, verified by unit assertions covering `RunController` construction refusal on invalid `RunPlan`, identical `budget_alert_gbp` formatting in `"idle"` and `"running"`, and `remaining_seconds == 0.0` when halted past `max_seconds`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Preserves synthetic stream provenance digests by explicitly keeping `src/core/src/zava_forward/core/synthetic/sensor_stream.py` unmodified (`C5`) and checking its empty diff during `P02-T02`.
* Preserves backward compatibility with existing `RunPlan` estimate records (`_body(plan)` top-level schema and `sha256` verification) and `InfraAlignmentTests` against `infra/modules/iothub.bicep` (`C3`, `C6`).
* Covers both the caller's exact `-p 'test_*simulator*.py'` test discovery target (`test_simulator_run_budget_controls.py`) and sibling regression suites (`test_run_plan.py`, `test_sensor_stream.py`) under strict `mypy` and `ruff`.
* Explicitly accepted residual risk: Live Azure `Microsoft.Consumption/budgets` notification firing and live subscription quota headroom cannot be exercised offline in `src/core` and remain tracked separately under #146 and #189 (`Refs #189`).

## Questions or Blocking Evidence Gaps

* None. All findings are resolvable directly from supplied codebase evidence without user input.

## Limitations

* Critique is bounded to offline `src/core` code, tests, documentation, and supplied RPI research/planning artifacts; live Azure IoT Hub and Consumption budget execution (#146) is outside the local evaluation boundary.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for PC-001 and PC-002 in `.copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md` and record their dispositions in `.copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md`, then finalize the plan and proceed to `rpi-implement` without another critique pass.
* User response required: no
