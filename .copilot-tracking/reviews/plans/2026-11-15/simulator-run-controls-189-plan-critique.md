<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #189 Simulator Run Controls (Owner, Time Limit, and Budget Alert)

## Metadata

* Task ID: issue-189-simulator-run-controls
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the sole remaining unticked acceptance criterion of Issue #189 (`[ ] Run has an owner, a time limit and a budget alert`; PRD FR-050, AC-066; ADR 0003 Decision 6) on branch `feat/iot-189-run-controls` targeting `feat/demo-164-chat-grounding-provenance-0900` (#1641). Require every simulator run configuration/invocation to enforce a named `owner` (rejecting blank, placeholder, and anonymous owners), a bounded `time_limit_minutes` / `max_duration_seconds`, and a linked `budget_alert` contract (threshold + alert rule/owner reference) verified in both runtime preflight and Bicep/infra contract tests. Place focused tests in `src/core/tests/test_simulator_run_controls_189.py` without touching `server.py`, `test_role_endpoint_inventory.py`, or `README.md`; pass `unittest`, `ruff check`, `ruff format --check`, `mypy`, and `tools/rename-zava-tests.py`; commit locally with `Refs #189` and the Copilot trailer without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md`, `.copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md`, `src/core/src/zava_forward/core/synthetic/sensor_stream.py`, `src/core/src/zava_forward/core/synthetic/run_governance.py`, `src/core/src/zava_forward/core/synthetic/run_plan.py`, `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, and `infra/live-simulator-job.bicep`.
* Decisions, dependencies, and acceptance criteria considered: Keep `infra/*.bicep`, `server.py`, `test_role_endpoint_inventory.py`, and all `README.md` files untouched; preserve backward compatibility with existing `RunPlan` / `RunController` / `RunGovernance` / `live_control` callers; record `Refs #189` honestly because live Azure `Microsoft.Consumption/budgets` notification firing remains an external hosted check.
* Assessment boundary: Evaluates plan and phase-detail accuracy, internal consistency, backward compatibility, and Bicep contract fidelity against the supplied source and infrastructure templates. Does not evaluate live Azure subscription deployment behavior or uninspected sibling test files outside the supplied set.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Rule 1: Named `owner` enforcement (`C1`, `C2`, `C8`, `P01-T01`) | Partial | Hardening `accountable_text` and `Pacer.__init__` covers stream and plan surfaces, but `"tbc"` and `"pending"` remain split in `run_governance._EXTRA_PLACEHOLDERS` unless moved into `sensor_stream._PLACEHOLDERS` (`PC-003`). |
| Caller Rule 1: Bounded `time_limit_minutes` / `max_duration_seconds` (`C1`, `C2`, `P01-T01`, `P01-T02`, `P02-T01`) | Covered | `resolve_duration_seconds`, `SimulatorRunControls`, `RunGovernance.from_minutes`, `Pacer.__init__`, `RunController.check_time_limit`, and CLI `--time-limit-minutes` cover `1.0..3600.0`s (`<= 60.0`m), subject to `bool` rate guard and CLI `StreamError` catch block (`PC-002`, `PC-003`). |
| Caller Rule 1: Linked `budget_alert` runtime preflight (`C2`, `C3`, `P01-T02`, `P02-T01`) | Partial | `P02-T01` freezes `RunPlan`'s dataclass fields without storing `alert_owner` or `threshold_type`, dropping distinct alert-owner and `100% Forecasted` contracts across `RunPlan.from_controls()`, `--alert-owner`, `record()`/`start()`, and `RunController.status()` (`PC-002`). |
| Caller Rule 1: Bicep/infra contract verification (`C4`, `C5`, `C6`, `P02-T02`, `P03-T01`) | Partial | `P02-T02` asserts nonexistent `@minLength(5)` and `@` guards on `param alertEmail string` in `infra/main.bicep:20-21` (`PC-001`) and uses permissive `round(...)` threshold matching (`PC-003`). |
| Caller Rules 2-4: Conflict-free file boundary, focused tests, validation, and local commit (`C9`, `C10`, `P03-T01`) | Covered | Canonical edit list excludes `server.py`, `test_role_endpoint_inventory.py`, `README.md`, and `infra/*.bicep`, and runs all required checks; adding full `src/core/tests` discovery closes any untested internal `Pacer` caller risk (`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: The architecture and file-isolation strategy are sound, but two `High` findings (`PC-001`, `PC-002`) and one `Medium` boundary finding (`PC-003`) would cause deterministic runtime or test failures if implemented verbatim: `P02-T02` checks `infra/main.bicep` for `@minLength(5)` and `@` parameter guards that do not exist in `infra/main.bicep:20-21`, and `P02-T01` prohibits adding fields to `RunPlan` while simultaneously requiring `RunPlan.from_controls()`, CLI `--alert-owner`, `RunController.status()`, and `verify_bicep_run_controls()` to preserve distinct `alert_owner_reference` and `Forecasted` alert contracts. All three findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `P02-T02` asserts nonexistent `@minLength(5)` and `@` guards on `param alertEmail` in read-only `infra/main.bicep`

* Related IDs: `C5`, `P02`, `P02-T02`, `P03-T01`
* Evidence: `infra/main.bicep:20-21`, `infra/main.bicep:165-185`, `infra/main.bicep:341-358`, `infra/main.bicep:585-611`, `.copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md:137`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md:201`
* Concern: `P02-T02` (following `C5` in research) instructs `verify_bicep_run_controls()` to verify that `infra/main.bicep` guards `param alertEmail string` with `@minLength(5)` and `@` (`alert_email_param_guarded: bool`). In `infra/main.bicep:20-21`, `param alertEmail string` has only `@description('Mailbox for platform alerts.')` and no `@minLength(5)` decorator or `@` validation anywhere in `infra/main.bicep` (nor in `infra/modules/iothub.bicep:28`), while `infra/*.bicep` is read-only per Non-Goals. In addition, `owner: ownerTag` in `infra/main.bicep:178-185` is defined inside `var allTags = union(tags, { ... owner: ownerTag })` and forwarded as `tags: allTags` (`infra/main.bicep:345`) rather than an inline module literal.
* Impact: Implementing `verify_bicep_run_controls()` per `P02-T02` will immediately raise `StreamError("BICEP_CONTRACT_MISMATCH")` against the real repository `infra/main.bicep`, blocking `P02` and `P03`.
* Smallest useful change: Update `P02-T02` and `P03-T01` so `verify_bicep_run_controls()` checks `infra/main.bicep`'s actual contract: a required un-defaulted `param alertEmail string` wired to `monitoring`, `iotHub`, and `budget-${prefix}` `actual80`/`forecast100` `contactEmails: [alertEmail]`, plus governed `param ownerTag` bound via `owner: ownerTag` in `allTags` and `tags: allTags` on `iotHub` and workload resources.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P02-T02` and `P03-T01` sections in `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md` and `Critique Disposition` in `.copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md` aligned with `infra/main.bicep:20-21,165-185,345,585-611`.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `P02-T01` omits `alert_owner` and `threshold_type` storage on `RunPlan`, dropping distinct alert-owner and `100% Forecasted` contracts across `from_controls()`, CLI `--alert-owner`, `record()`/`start()`, and `status()`

* Related IDs: `C3`, `C4`, `C9`, `P02`, `P02-T01`, `P02-T02`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/synthetic/run_plan.py:54-86`, `src/core/src/zava_forward/core/synthetic/run_plan.py:181-193`, `src/core/src/zava_forward/core/synthetic/run_plan.py:258-296`, `src/core/src/zava_forward/core/synthetic/run_plan.py:314-350`, `infra/modules/iothub.bicep:233-248`, `.copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md:117`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md:165-175`
* Concern: Contradicting research Wave 3 (`simulator-run-controls-189-research.md:117`), `P02-T01` states that `RunPlan`'s dataclass field layout must stay completely unchanged. Without defaulted `alert_owner: str | None = None` and `alert_threshold_type: str = "Actual"` fields on `RunPlan`: (1) `RunPlan.from_controls(controls, ...)` silently overwrites a distinct `controls.budget_alert.alert_owner_reference` with `plan.owner` and overwrites `threshold_type="Forecasted"` with `"Actual"`, causing a valid `100% Forecasted` Bicep contract (`infra/modules/iothub.bicep:241-247`) to fail `verify_bicep_run_controls()`; (2) `run_plan.main()` accepts `--alert-owner` without persisting it into `RunPlan`, `record(plan, out)` SHA-256 verification in `RunController.start()`, or `RunController.status()["budget_alert"]`; (3) `RunPlan.governance()` (`run_plan.py:80`) requires `budget_alert_gbp` and `budget_cap_gbp` to be `str`, so `RunPlan.from_controls()` must normalize non-`None` GBP amounts to `str`; and (4) `run_plan.main()` (`run_plan.py:329-348`) currently constructs `RunPlan` outside its `try ... except StreamError` block, so calling `resolve_duration_seconds()` before `try:` would raise an uncaught traceback instead of returning CLI exit code `2`.
* Impact: Distinct `alert_owner_reference` values and `100% Forecasted` alert contracts are lost or rejected across `RunPlan.from_controls()`, `--alert-owner`, `estimate.json` tamper checks, and `RunController.status()`, and invalid CLI duration flags risk uncaught exceptions instead of exit code `2`.
* Smallest useful change: Revise `P02-T01` to add defaulted `alert_owner: str | None = None` and `alert_threshold_type: str = "Actual"` on `RunPlan` (research `C3`/`C9` verified existing tests round-trip `record()` -> `start()` dynamically; if legacy `_body(plan)["plan"]` key parity is also desired when unset, omit those keys in `_body(plan)` only when at their default `None`/`"Actual"` values while binding non-default values into the digest), normalize GBP fields to `str` in `RunPlan.from_controls()`, and place `resolve_duration_seconds()` + `RunPlan(...)` inside `try ... except StreamError` in `run_plan.main()`.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P02-T01` section in `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md` and `Critique Disposition` in `.copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md` specifying `RunPlan` persistence for `alert_owner` and `alert_threshold_type`, GBP `str` normalization, and CLI `try ... except StreamError` wrapping.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Split placeholder sets, unspecified error-code precedence in `RunPlan.validate()`, `bool` rate guard, and `round()` Bicep threshold matching leave avoidable edge-case gaps

* Related IDs: `C1`, `C2`, `C3`, `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/synthetic/sensor_stream.py:110-120`, `src/core/src/zava_forward/core/synthetic/sensor_stream.py:346-349`, `src/core/src/zava_forward/core/synthetic/run_governance.py:12-21`, `src/core/src/zava_forward/core/synthetic/run_plan.py:88-117`, `.copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md:78-80`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md:32-33`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md:92-135`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md:169`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md:206`, `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md:247`
* Concern: Four boundary specifications across `P01`-`P03` need tightening so implementation and tests agree on first run: (1) `"tbc"` and `"pending"` currently sit in `run_governance._EXTRA_PLACEHOLDERS` (`run_governance.py:12`) rather than `sensor_stream._PLACEHOLDERS` (`sensor_stream.py:110`), so `RunBudget` and `Pacer` would still accept `owner="pending"` unless the full disallowed set lives in `sensor_stream._PLACEHOLDERS`; (2) `P01-T02` omits exact `StreamError` code names for `BudgetAlertContract.validate()` and `SimulatorRunControls.validate()`, and `P02-T01` must run existing `RunPlan.validate()` checks before `self.preflight_controls().validate()` (mapping `alert_owner` failures to `RUN_OWNER_COST_ALERT_REQUIRED` and `alert_threshold_type` failures to `INVALID_BUDGET`) so existing `test_run_plan.py` assertions do not see `RUN_OWNER_REQUIRED` or `TIME_LIMIT_REQUIRED`; (3) `P01-T01` checks `0 < rate <= 100` in `Pacer.set_max_per_second()` without explicitly rejecting `bool` and non-finite floats (`type(rate) not in (int, float) or not math.isfinite(rate)`), which in Python admits `True`; and (4) `P02-T02` compares `round(float(controls.budget_alert.threshold_percent))` against Bicep thresholds (silently accepting `79.6%` as `80%`), while `P03` lists four sibling test files rather than running full `src/core/tests` discovery (`python3 -m unittest discover -s src/core/tests -q`) to catch any other `src/core` synthetic caller of `Pacer`, and `P03-T01`'s optional `az bicep build` subprocess should bound execution with a timeout and prefer local `bicep` / installed `az bicep` without network hangs.
* Impact: Leaving these implicit risks failing `OwnerControlTests` on `RunBudget(owner="pending", ...)`, changing error codes asserted by `test_run_plan.py`, accepting `79.6%` thresholds in `verify_bicep_run_controls()`, admitting `set_max_per_second(True)`, or missing an internal `src/core` caller regression.
* Smallest useful change: Unify all disallowed placeholder and anonymous tokens in `sensor_stream._PLACEHOLDERS`; record exact `StreamError` codes in `P01-T02` and preserve `RunPlan.validate()` error precedence in `P02-T01`; enforce `type(rate) not in (int, float) or not math.isfinite(rate)` in `Pacer.set_max_per_second()`; replace `round(...)` with `math.isclose(..., rel_tol=0.0, abs_tol=1e-6)` in `verify_bicep_run_controls()`; and include bounded-timeout `bicep`/`az bicep` checks plus `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -q` in `P03`.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, and `P03-T01` sections in `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md` and `Critique Disposition` in `.copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md`.
* Decision route: Direct planner correction (no user decision required).

## Strengths and Residual Risk

* Strong stack-safety boundary: Isolating changes to `sensor_stream.py`, `run_governance.py`, `run_plan.py`, and `src/core/tests/test_simulator_run_controls_189.py` avoids merge conflicts in `server.py`, `test_role_endpoint_inventory.py`, `README.md`, and `infra/*.bicep` while protecting `src/api/live_control.py` automatically via `accountable_text`.
* Complete bypass closure at the lowest primitive: Enforcing `RunBudget.preflight()` inside `Pacer.__init__()` prevents direct stream pacing callers from bypassing `RunPlan` or `RunController` validation.
* Explicitly accepted residual risk: Live Azure `Microsoft.Consumption/budgets` email delivery in the `ama` resource group cannot be proven by offline unit tests and remains gated under #146/#189 hosted checks, so committing with `Refs #189` rather than `Closes #189` is accurate and compliant with repository workflow rules.

## Questions or Blocking Evidence Gaps

* None. All three findings are resolved directly from the supplied source and Bicep templates without user input or further research.

## Limitations

* Critique stayed strictly within the supplied artifact and target-file boundary (`sensor_stream.py`, `run_governance.py`, `run_plan.py`, `infra/modules/iothub.bicep`, `infra/main.bicep`, `infra/governance.bicep`, `infra/live-simulator-job.bicep`, and the 2026-11-15 research, plan, and phase-details documents). Unsupplied sibling modules (`sensor_injector.py`, `loadcheck.py`, `infra/iot-hub-live.bicep`) were not opened directly; running full `src/core/tests` discovery during `P03` (`PC-003`) verifies all `src/core` callers during implementation.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, and `PC-003` in `.copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md` and record their disposition in `.copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md`, then finalize planning and proceed to `rpi-implement` without another critique pass.
* User response required: No
