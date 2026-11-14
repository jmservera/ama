<!-- markdownlint-disable-file -->
# Review: Issue #189 Simulator Run Owner, Time Limit, and Budget Alert Controls

## Scope and Evidence

* Task ID: 189-simulator-controls-2142
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Locally verifiable `src/core` simulator governance acceptance criterion for Issue #189 ("Run has an owner, a time limit and a budget alert") across `run_governance.py`, `run_plan.py`, `test_simulator_run_budget_controls.py`, and `src/core/README.md`; excludes live Azure IoT Hub / `Microsoft.Consumption/budgets` execution (#146) and remote git push per caller instructions.
* Plan: .copilot-tracking/plans/2026-11-14/simulator-controls-189-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/simulator-controls-189-2142-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/simulator-controls-189-2142-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/simulator-controls-189-2142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/simulator-controls-189-2142-research.md, `git diff -- src/` across `src/core/src/zava_forward/core/synthetic/{run_governance,run_plan,sensor_stream}.py`, `src/core/tests/test_simulator_run_budget_controls.py`, `src/core/README.md`, and local verification runs in `src/core` and `src/api`.

## Opening Review State

* Interpreted review goal: Verify that the completed `src/core` implementation satisfies FR-1..FR-4, NFR-1, and critique dispositions `PC-001` and `PC-002` for Issue #189 Criterion 3 without modifying `sensor_stream.py` or breaking `_body(plan)` compatibility.
* Review scope: Full task (`P01` and `P02`)
* Evidence readiness: Ready; research, implementation-ready plan, phase details, single-pass critique, changes log, and source diffs are complete and reconciled.
* Acceptance basis: Plan FR-1..FR-4, NFR-1, Acceptance Criteria, Critique Dispositions (`PC-001`, `PC-002`), and caller `mypy`/`ruff`/`unittest` verification requirements.
* First comparison boundary: Plan checklist markers and critique dispositions (`PC-001`, `PC-002`) against `run_governance.py` and `run_plan.py` diffs.
* Active read-only boundaries: Read-only comparison across repository sources and prior RPI artifacts; writes restricted exclusively to `.copilot-tracking/reviews/logs/2026-11-14/simulator-controls-189-2142-review.md`.
* Initial blockers: none.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation comparison on 2026-11-14 across all planned markers (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`), critique findings (`PC-001`, `PC-002`), source diffs, and executed `src/core` / `src/api` verification outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | RunGovernance placeholder hardening, deadline check, and frozen RunMeter runtime | Reconciled | `[x]` in plan, `complete` in phase details, and backed by `run_governance.py` diff |
| `P01`, `P01-T02` | Fail-closed RunPlan GBP validation and unified RunController lifecycle status | Reconciled | `[x]` in plan, `complete` in phase details, and backed by `run_plan.py` diff |
| `P02`, `P02-T01`, `P02-T02` | Focused simulator governance unit tests and core README update | Reconciled | `[x]` in plan, `complete` in phase details, and backed by 21 passing simulator tests + 44 sibling core tests + 37 API stream tests |
| `Follow-Up Items` | Live Azure `Microsoft.Consumption/budgets` alert firing and subscription headroom verification (#146, #189) | Reconciled | Preserved outside active `Pxx` completion claims in both plan and changes record |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/synthetic/run_governance.py` | Added `governed_text` (`"tbc"`, `"pending"` refusal), `RunMeter.ended`, `check_time_limit()`, `_ensure_running()` (`RUN_STOPPED`), idempotent `stop()`, and frozen `elapsed_seconds` / clamped `remaining_seconds` / `budget_alert_gbp` in `summary()` | Verified in `git diff` without modifying `sensor_stream.py` | Passed (`mypy`, `ruff`, `GovernanceValidation`, `BudgetMeter`) | Reconciled and conformant |
| `P01-T02` | `src/core/src/zava_forward/core/synthetic/run_plan.py` | Enforced `governed_text`, JSON-safe `str` GBP checks, and zero ungoverned `planned_cost_gbp` in `RunPlan.governance()`; added fail-closed `RunController.__init__()` validation, canonical `idle` `budget_alert_gbp`, `Decimal \| int \| str` `admit()`, `check_time_limit()`, idempotent `_stopped_at`, and unified `status()` | Verified in `git diff`; `_body(plan)` SHA-256 record schema preserved | Passed (`mypy`, `ruff`, `RunPlanWiring`, `test_run_plan.py`, `test_iot_stream.py`) | Reconciled and conformant |
| `P02-T01`, `P02-T02` | `src/core/tests/test_simulator_run_budget_controls.py`, `src/core/README.md` | Added 3 focused test methods and expanded 3 existing tests (21 total, 0 removals) covering `idle`/`running`/`stopped` `status()`, USD-only and GBP deadline enforcement, idempotent `stop()`, placeholder/ungoverned GBP refusals, `Decimal` admission, and CLI error exits; updated `src/core/README.md` | Verified in `git diff` and verbose `unittest` execution | Passed (`21` simulator tests, `44` sibling core tests, `37` API tests, `mypy`, `ruff`) | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time plan revisions were needed; implementation matched finalized `P01`..`P02` | None | Checklist markers and handoff status updated on completion | Implementation-ready plan with `PC-001` and `PC-002` applied | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Both findings from `.copilot-tracking/critiques/2026-11-14/simulator-controls-189-2142-critique.md` (`PC-001` High on idempotent `stop()` / post-stop `RUN_STOPPED` & `RUN_NOT_RUNNING` codes, and `PC-002` Medium on fail-closed `RunController.__init__()` validation, canonical `idle` `budget_alert_gbp`, and clamped `remaining_seconds >= 0.0`) were directly applied in the plan/details, implemented in `run_governance.py` and `run_plan.py`, and verified by dedicated assertions in `test_simulator_run_budget_controls.py`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No pause was needed; `P02` executed after `P01` completed.
* Justification assessment: Supported by direct code and test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live Azure `Microsoft.Consumption/budgets` alert firing and subscription headroom verification (#146, #189) | Requires live Azure subscription / IoT Hub exercise; local `src/core` code is strictly offline and credential-free | Project owner during an approved live Azure exercise (#146); use `Refs #189` in commit message | Open outside-scope follow-up; routed to distinct follow-up owner (not a defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No actionable `RV-xxx` implementation defects, decision gaps, or material evidence gaps were found within the assessed `src/core` boundary.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | none | All in-scope `src/core` requirements and critique dispositions are conformant |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Live Azure `Microsoft.Consumption/budgets` notification delivery and subscription quota headroom verification (#146, #189): tracked outside offline `src/core` scope; commit uses `Refs #189` rather than a closing keyword in accordance with repository policy.

## Blockers and Remaining Work

* Blockers: none.
* Remaining active work: none.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (316 source & test files, `strict = true`) | Passed | `Success: no issues found in 316 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (263 formatted files) | Passed | `263 files already formatted` |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*simulator*.py' -v` | `src/core/tests/test_simulator_run_budget_controls.py` | Passed | `Ran 21 tests in 0.015s — OK` (`PYTHONPATH=src` ensures discovery imports this worktree's `src/core/src` rather than the shared host's `~/.local` editable install pointing to `/home/azureuser/source/ama/src/core/src`) |
| `PYTHONPATH=src python3 -m unittest tests/test_run_plan.py tests/test_sensor_stream.py tests/test_dependency_rule.py -v` | `src/core` sibling & dependency contracts | Passed | `44 tests — OK`; `git diff` on `sensor_stream.py` verified empty |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_iot_stream.py -q` | `src/api` `RunController` integration | Passed | `Ran 37 tests in 11.262s — OK` |
| `tools/rpi-checks.py --all` and hosted CI | Repository-wide | Skipped | Focused local tier applies to scoped offline `src/core` unit slice; caller prohibited `git push` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every simulator `RunPlan`, `RunGovernance`, `RunMeter`, and `RunController` instance in `src/core` enforces an accountable non-placeholder human owner, a bounded `1..3600` second time limit with frozen post-stop/halt runtime accounting, and a validated USD + optional paired GBP budget alert across `idle`, `running`, and `stopped` states, with strict `mypy`, `ruff`, simulator unit tests, and sibling `core`/`api` suites passing and `sensor_stream.py` untouched.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up (#146, #189) | Project owner: verify live Azure `Microsoft.Consumption/budgets` alert delivery during approved live hub exercise |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `mypy` (316 files), `ruff check`, `ruff format --check`, simulator tests (21 passed), sibling `core` tests (44 passed), and `api` `test_iot_stream` (37 passed)
* Blockers: none
