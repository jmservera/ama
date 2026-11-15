<!-- markdownlint-disable-file -->
# Review: Issue #189 Simulator Run Controls (Owner, Time Limit, and Budget Alert)

## Scope and Evidence

* Task ID: `issue-189-simulator-run-controls`
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`)
* Assessed boundary: GitHub Issue #189 (`Cost, scale and run controls for the simulator`, PRD FR-050, AC-066, ADR 0003 Decision 6) within the stack-isolated `src/core` and read-only `infra/*.bicep` boundary targeting `origin/feat/demo-164-chat-grounding-provenance-0900` (#1641), with `server.py`, `test_role_endpoint_inventory.py`, `README.md`, and `infra/*.bicep` excluded from modification.
* Plan: .copilot-tracking/plans/2026-11-15/simulator-run-controls-189-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/simulator-run-controls-189-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/simulator-run-controls-189-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/simulator-run-controls-189-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/simulator-run-controls-189-research.md, `src/core/src/zava_forward/core/synthetic/sensor_stream.py`, `src/core/src/zava_forward/core/synthetic/run_governance.py`, `src/core/src/zava_forward/core/synthetic/run_plan.py`, `src/core/tests/test_simulator_run_controls_189.py`, `infra/governance.bicep`, `infra/main.bicep`, `infra/modules/iothub.bicep`, `infra/live-simulator-job.bicep`, and local validation outputs across `src/core`, `src/api`, and `tools/rename-zava-tests.py`.

## Opening Review State

* Interpreted review goal: Verify once with direct source, test, and Bicep contract evidence whether `P01`–`P03` satisfy the plan, critique dispositions (`PC-001`–`PC-003`), stack-isolation constraints, and Issue #189 acceptance criteria.
* Review scope: Full task (`P01` through `P03`)
* Evidence readiness: Ready; all plan markers (`P01`–`P03`), phase details, critique dispositions, changes record, and validation runs are reconciled and consistent.
* Acceptance basis: GitHub Issue #189 acceptance criteria, PRD FR-050 / AC-066, ADR 0003 Decision 6, plan acceptance criteria, and critique findings `PC-001`–`PC-003`.
* First comparison boundary: Plan-to-change marker reconciliation across `P01`–`P03`, implementation-time `P01-T01` update reconciliation, and Issue #189 acceptance-criteria matrix.
* Active read-only boundaries: This review creates only `.copilot-tracking/reviews/2026-11-15/simulator-run-controls-189-review.md` and does not edit source, tests, or earlier RPI artifacts.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 across reconciled `P01`–`P03` artifacts, all four modified/added `src/core` files, read-only `infra/*.bicep` contracts, and passing `src/core`, `src/api`, `ruff`, `mypy`, and `tools/rename-zava-tests.py` checks.

## Verdict Against GitHub Issue #189 Acceptance Criteria

| Issue #189 acceptance criterion | Verdict | Code, Bicep, and test evidence | Commit link governance |
|---------------------------------|---------|--------------------------------|------------------------|
| `[x] Cost and quota are estimated before a run` | Preserved and verified (`Conformant`) | `RunPlan.estimate()`, `record()`, and `RunController.start()` in `src/core/src/zava_forward/core/synthetic/run_plan.py` enforce pre-run B1 unit headroom (`B1_QUOTA_HEADROOM`, `RUN_MESSAGE_LIMIT`), USD cost cap (`BUDGET_CAP_EXCEEDED`), and SHA-256 estimate integrity (`ESTIMATE_NOT_RECORDED`, `ESTIMATE_MISMATCH`), preserving legacy digests when `alert_owner` / `alert_threshold_type` are default while binding explicit overrides into the SHA-256 digest (`test_run_plan.py`, `LinkedBudgetAlertTests`). | Proven locally and preserved |
| `[x] Scale-down and stop controls work` | Preserved and verified (`Conformant`) | `RunController.scale_down()`, `RunController.stop()`, `Pacer.set_max_per_second()`, and `Pacer._wait_until()` enforce monotonic home/rate reduction (`INVALID_SCALE_DOWN`, `INVALID_RUN_LIMIT`) and non-resumable stop (`RUN_STOPPED`), verified by `test_run_plan.py`, `test_sensor_stream.py`, `test_simulator_run_controls_189.py`, and `src/api/tests/test_iot_stream.py`. | Proven locally and preserved |
| `[ ] Run has an owner, a time limit and a budget alert` | Offline code and Bicep/ARM contract slice `Conformant`; hosted Azure billing-alert firing remains external residual verification | Named `owner` enforced in `accountable_text` / `governed_text` across `SimulatorRunControls`, `RunGovernance`, `RunPlan`, `RunController`, `RunBudget`, `Pacer.__init__`, `run_plan.main`, and `src/api/live_control.py` (`OwnerEnforcementTests`); bounded duration (`1.0..3600.0`s / `<= 60.0`m, `RUN_DEADLINE`) enforced via `resolve_duration_seconds`, `RunGovernance.from_minutes`, `RunPlan.from_controls`, `Pacer`, and `RunController.check_time_limit` (`BoundedDurationTests`); linked `BudgetAlertContract` (`threshold_percent`, `threshold_type`, `alert_rule_reference`, `alert_owner_reference`, optional USD/GBP caps) enforced in runtime preflight/status/spend-halt and verified against `infra/governance.bicep`, `infra/main.bicep`, `infra/modules/iothub.bicep`, and `infra/live-simulator-job.bicep` plus compiled ARM JSON (`LinkedBudgetAlertTests`, `BicepRunControlsContractTests`). | Use `Refs #189` (never `Closes #189`) until hosted Azure `Microsoft.Consumption/budgets` notification delivery in `ama` is observed under #146/#189 |

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | `Owner Validation and Stream Pacer Envelope Preflight (P01, P01-T01)` + `Preserve HubPublisher.run Supplied-Pacer INVALID_RUN_RATE Contract (P01-T01)` | Reconciled | `[x]` checked in `plan.md`, `Completed` in `phase-details.md`, and `Pacer` rate/envelope split reconciled across both artifacts |
| `P01`, `P01-T02` | `Bounded Duration Resolution and Linked Budget-Alert Contracts (P01, P01-T02)` | Reconciled | `[x]` checked in `plan.md`; `SimulatorRunControls`, `BudgetAlertContract`, and `resolve_duration_seconds` match plan and details |
| `P02`, `P02-T01` | `RunPlan, RunController, and CLI Run-Control Wiring (P02, P02-T01)` | Reconciled | `[x]` checked in `plan.md`; `from_controls`, `preflight`, `status`, CLI flags, and SHA-256 digest compatibility match `PC-002`/`PC-003` |
| `P02`, `P02-T02` | `Bicep Run-Control Alignment Extractor and Verifier (P02, P02-T02)` | Reconciled | `[x]` checked in `plan.md`; `verify_bicep_run_controls` validates all four Bicep files per `PC-001` and `PC-003` |
| `P03`, `P03-T01` | `Focused Runtime and Bicep Contract Test Suite (P03, P03-T01)` | Reconciled | `[x]` checked in `plan.md`; 11 focused unit/contract tests and full regression/lint/type/naming checks recorded |
| `Follow-Up Items` | Hosted Azure Consumption budget notification verification + post-#1641 FastAPI admin endpoint surfacing | Reconciled | Both items state out-of-scope rationale and owner/next action in `plan.md` and are mirrored in `changes.md` |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | `src/core/src/zava_forward/core/synthetic/sensor_stream.py` | Hardened `_PLACEHOLDERS` and `accountable_text`; added `RunBudget._preflight_envelope()` and `RunBudget.preflight()`; enforced envelope preflight in `Pacer.__init__()`, `INVALID_RUN_RATE` in `Pacer.admit_send()`, and `INVALID_RUN_LIMIT` in `Pacer.set_max_per_second()`. | Rejects blank, placeholder, punctuation-only, control-char, and anonymous/system owners while preserving `"o"`/`"r"` fixtures and `HubPublisher.run` `INVALID_RUN_RATE`. | Passed `test_simulator_run_controls_189.py`, `test_sensor_stream.py`, `src/api/tests/test_iot_stream.py`, `src/api/tests/test_live_control.py`, `ruff`, `mypy` | Reconciled |
| `P01`, `P01-T02` | `src/core/src/zava_forward/core/synthetic/run_governance.py` | Added `MIN_TIME_LIMIT_SECONDS`, `MAX_TIME_LIMIT_MINUTES`, `resolve_duration_seconds()`, `BudgetAlertContract`, `SimulatorRunControls`, and `RunGovernance.from_minutes()` / duration properties. | Deterministic `StreamError` codes (`RUN_OWNER_REQUIRED`, `TIME_LIMIT_REQUIRED`, `TIME_LIMIT_MISMATCH`, `RUN_OWNER_COST_ALERT_REQUIRED`, `INVALID_BUDGET`, `BUDGET_ALERT_NOT_BELOW_CAP`). | Passed `test_simulator_run_controls_189.py`, `test_simulator_run_budget_controls.py`, `ruff`, `mypy` | Reconciled |
| `P02`, `P02-T01` | `src/core/src/zava_forward/core/synthetic/run_plan.py` | Added `RunPlan.from_controls()`, `time_limit_minutes`, `max_duration_seconds`, `budget_alert_contract()`, `preflight_controls()`, `RunController.preflight()`, enriched `status()`, and CLI `--time-limit-minutes` / `--alert-owner`. | Enforces preflight on every plan/controller/CLI path, binds explicit `alert_owner` / `alert_threshold_type` into SHA-256, and preserves legacy digests for defaults. | Passed `test_run_plan.py`, `test_simulator_run_budget_controls.py`, `test_simulator_run_controls_189.py`, `ruff`, `mypy` | Reconciled |
| `P02`, `P02-T02` | `src/core/src/zava_forward/core/synthetic/run_plan.py` | Implemented `BicepNotificationContract`, `BicepRunControlContract`, and `verify_bicep_run_controls()`. | Verifies `governance.bicep`, `main.bicep`, `modules/iothub.bicep`, and `live-simulator-job.bicep` plus runtime threshold/type alignment via `math.isclose`. | Passed `BicepRunControlsContractTests` (real `infra/`, 9 drift mutations, 5 threshold mismatches, ARM build) | Reconciled |
| `P03`, `P03-T01` | `src/core/tests/test_simulator_run_controls_189.py` | Added 11 focused test methods across `OwnerEnforcementTests`, `BoundedDurationTests`, `LinkedBudgetAlertTests`, and `BicepRunControlsContractTests`. | Proves runtime preflight, deadline/spend halts, tamper refusal, Bicep drift refusal, and compiled ARM parity with zero touches to excluded files. | Passed all `src/core` tests, `src/api` regression tests, `ruff`, `mypy`, and `tools/rename-zava-tests.py` | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`In Scope`, `Phase Checklist`, `P01-T01` detail) and `Follow-Up Items` | Split `RunBudget._preflight_envelope()` (enforced in `Pacer.__init__`) from `max_per_second` validation (enforced as `INVALID_RUN_RATE` in `Pacer.admit_send` and `INVALID_RUN_LIMIT` in `Pacer.set_max_per_second`) so `HubPublisher.run(..., pacer=...)` continues raising `INVALID_RUN_RATE`; mirrored the deferred FastAPI admin surfacing item in `plan.md` `## Follow-Up Items`. | Cross-package test `src/api/tests/test_iot_stream.py` (`PublisherTests.test_invalid_supplied_pacer_limits_refuse_before_client_creation`); no new user decision required. | Reconciled in `plan.md`, `phase-details.md`, and `changes.md`. | Not needed (immediately relevant current-state update preserving approved intent and `PC-001`–`PC-003`). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three single-pass critique findings (`PC-001` High on `main.bicep` `alertEmail` and `allTags` contract, `PC-002` High on `RunPlan` `alert_owner`/`alert_threshold_type` digest binding + GBP string normalization + CLI `StreamError` handling, and `PC-003` Medium on unified `_PLACEHOLDERS`, `RunPlan.validate()` precedence, `bool` rate guard, `math.isclose` Bicep threshold check, and bounded `bicep` subprocess timeout) are fully implemented and verified.
* Material revisions: None; no discovery altered confirmed user requirements, architecture, scope, or stack-isolation boundaries.
* Dependent-work pause assessment: No dependent-work pause was triggered; `P01` -> `P02` -> `P03` executed in strict dependency order.
* Justification assessment: Supported by direct unit, cross-package caller, and Bicep/ARM evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live Azure `Microsoft.Consumption/budgets` notification firing verification in `ama` resource group | Offline `src/core` PR slice has no live Azure deployment execution; live cloud verification is gated under #146/#189. | Post-merge hosted Azure deployment validation under Issue #146 / Issue #189 | Open distinct follow-up route (preserves `Refs #189` commit hygiene) |
| Surface `RunController.status()` `time_limit_minutes` and `budget_alert` summary fields in FastAPI admin live-control endpoints | Stack-isolation constraint explicitly prohibits editing `server.py` and `test_role_endpoint_inventory.py` until parent/sibling PR #1641 merges. | Follow-up `src/api` PR after #1641 merges | Open distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No implementation defects, decision gaps, or material evidence gaps were identified across `P01`–`P03`.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: FastAPI admin live-control responses do not yet expose enriched `RunController.status()` fields (`time_limit_minutes`, `budget_alert`)

* Related scope: `Follow-Up Items` (outside active `P01`–`P03` scope)
* Evidence: `src/core/src/zava_forward/core/synthetic/run_plan.py` (`RunController.status`) enriches core status dictionaries with `time_limit_minutes`, `max_duration_seconds`, and `budget_alert`, while `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py` remain untouched per the stack-isolation boundary on `origin/feat/demo-164-chat-grounding-provenance-0900`.
* Impact: Non-blocking residual integration; core preflight and runtime enforcement are active, and only HTTP surface projection awaits parent PR #1641 merge.
* Destination: `follow-up`
* Smallest useful next action: After PR #1641 merges, expose `time_limit_minutes` and `budget_alert` in the FastAPI admin live-control status payload and add corresponding API endpoint tests.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Live Azure `Microsoft.Consumption/budgets` alert delivery in `ama` remains a hosted deployment check

* Related scope: `Follow-Up Items` (outside active `P01`–`P03` offline scope)
* Evidence: `verify_bicep_run_controls()` and `BicepRunControlsContractTests` verify `actual80` (`80% Actual`) and `forecast100` (`100% Forecasted`) notifications to `[alertEmail]` in Bicep source and compiled ARM JSON (`infra/modules/iothub.bicep`, `infra/main.bicep`), while live Azure notification delivery requires hosted subscription deployment under Issues #146 and #189.
* Impact: Non-blocking external gate; requires using `Refs #189` rather than `Closes #189` until hosted cloud verification is recorded.
* Destination: `follow-up`
* Smallest useful next action: Verify `budget-iot-*` and `budget-*` notification delivery in the deployed `ama` resource group during the Issue #146 / #189 hosted deployment check before closing #189.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow-up` | Post-#1641 `src/api` slice exposing `time_limit_minutes` and `budget_alert` in `server.py` | Non-blocking residual work intentionally excluded by stack-isolation boundary |
| `RV-002` | `follow-up` | Hosted Azure deployment verification in `ama` under Issues #146 and #189 | Non-blocking external cloud verification outside offline `src/core` boundary |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Post-#1641 `src/api` admin endpoint projection of `RunController.status()` `time_limit_minutes` and `budget_alert` fields (excluded from this branch to avoid `server.py` / `test_role_endpoint_inventory.py` merge conflicts).
* `RV-002`: Hosted Azure `Microsoft.Consumption/budgets` notification verification in the `ama` resource group under Issues #146 and #189.

## Blockers and Remaining Work

* Blockers: None for local commit, rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900`, and PR stacking with `Refs #189`.
* Remaining active work: None (`P01`–`P03` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `(cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_simulator_run_controls_189.py" -q)` | `src/core` focused #189 runtime + Bicep/ARM contract tests | Passed | 11 tests passed (`OK`), including `az bicep build` ARM JSON verification |
| `(cd src/core && PYTHONPATH="$(pwd)/src:$(pwd)/tests" python3 -m unittest tests/test_sensor_*.py tests/test_synthetic_*.py tests/test_simulator_*.py tests/test_run_plan.py tests/test_dependency_rule.py -q)` | `src/core` synthetic, sensor, simulator, run_plan, and dependency-rule suites | Passed | 400 synthetic/simulator tests + dependency-rule checks passed (`OK`) |
| Full `src/core` unit suite (`unittest discover -s tests -q` + Azure SDK venv check for `test_device_registry_azure.py` + isolated editable venv check for `test_discovery_assistant_demo.py`) | `src/core` (all 3,563 tests) | Passed | All `src/core` tests verified passing with zero regressions |
| `(cd src/api && PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests:tests python3 -m unittest tests/test_iot_stream.py tests/test_live_control.py tests/test_content_standard.py -q)` | `src/api` cross-package `Pacer` / `accountable_text` callers and content standard | Passed | 122 tests passed (`OK`) |
| `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` | `src/core` lint, formatting, and strict static typing | Passed | Ruff clean (`289 files already formatted`); Mypy `0 issues found in 342 source files` |
| `python3 tools/rename-zava-tests.py` | Repository naming regression suite | Passed | 25 tests passed (`OK`) |
| `git --no-pager diff --name-only` | Stack-isolation and production-reference hygiene check | Passed | Only `sensor_stream.py`, `run_governance.py`, `run_plan.py`, and `test_simulator_run_controls_189.py` touched under `src/`; zero `.copilot-tracking/` strings in modified `src/` files; zero edits to `server.py`, `test_role_endpoint_inventory.py`, `README.md`, or `infra/*.bicep` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every in-scope requirement, acceptance criterion, and critique disposition (`PC-001`–`PC-003`) across `P01`–`P03` is satisfied with zero defects, full `src/core` + `src/api` regression compatibility, strict `mypy`/`ruff` cleanliness, and strict adherence to stack-isolation and `Refs #189` governance boundaries. Out-of-scope hosted Azure alert delivery (`RV-002`) and post-#1641 `src/api` surfacing (`RV-001`) remain explicitly tracked follow-up items rather than in-scope defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | No implementation defects found |
| Decision gap or invalid assumption | none | No planning or decision gaps found |
| Material evidence gap | none | No research gaps found |
| Non-blocking residual work | distinct follow-up (`RV-001`, `RV-002`) | Expose enriched status fields in `src/api` after PR #1641 merges (`RV-001`); verify live Azure budget email notifications in `ama` under #146/#189 (`RV-002`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused #189 suite (11 tests), synthetic/simulator suites (400 tests), full `src/core` suite (3,563 tests), `src/api` IoT/live-control/content-standard suites (122 tests), `ruff check`, `ruff format --check`, strict `mypy`, and `tools/rename-zava-tests.py` (25 tests) all passed.
* Blockers: None
