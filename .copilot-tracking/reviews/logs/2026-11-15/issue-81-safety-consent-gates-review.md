<!-- markdownlint-disable-file -->
# Review: Issue #81 Exercise-Scenario Safety and Resident Consent Gate Verification

## Scope and Evidence

* Task ID: issue-81-safety-consent-gates
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`)
* Assessed boundary: Proving the two exercise-scenario acceptance criteria of `#81` (`No controlled progression with unresolved safety evidence in the exercise scenarios` and `No work started without valid resident agreement or authorised exception in the exercise scenarios`) across all six `src/core` exercise scenario suites on JSON `Store` and SQLite `SqlStore`, fail-closed safety and works-exception hardening (`FR-PLAN-01` to `FR-PLAN-03`, `AC-1` to `AC-4`), `src/core/README.md` documentation, and Focused-tier `src/core` validation.
* Plan: .copilot-tracking/plans/2026-11-15/issue-81-safety-consent-gates-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-81-safety-consent-gates-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-81-safety-consent-gates-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-81-safety-consent-gates-research.md (`C1`–`C18`), `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`, `src/core/src/zava_forward/core/gates.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/taskqueues.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, `src/core/README.md`, and live `ruff`, `mypy`, and `unittest` execution outputs.

## Opening Review State

* Interpreted review goal: Verify once with read-only discipline that the completed `src/core` implementation, tests, documentation, and RPI tracking artifacts conform to the approved `#81` exercise-scenario plan, critique dispositions (`PC-001`–`PC-005`), fail-closed BRD/PRD governance rules (`RULE-001`, `RULE-002`, `FR-008`, `FR-011`, `FR-014`), and Focused validation tier.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; research, plan, phase details, one-pass plan critique, and reconciled changes record are all present and synchronized.
* Acceptance basis: `FR-PLAN-01` through `FR-PLAN-03`, `AC-1` through `AC-4`, critique dispositions `PC-001` through `PC-005`, and repository coding/content/validation rules.
* First comparison boundary: Plan-to-change marker reconciliation across `P01`, `P02`, `P03`, and `## Follow-Up Items`, followed by direct code/test/validation evidence comparison.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/issue-81-safety-consent-gates-review.md` (plus parent RPI session state transitions) and makes zero edits to `src/` or earlier RPI artifacts.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Executed on `2026-11-15` across the complete full-plan boundary (`P01`–`P03`), comparing plan requirements, critique dispositions (`PC-001`–`PC-005`), source diffs across 7 `src/core` source/test/doc files, and Focused-tier plus cross-package content-standard and rename-regression test runs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Fail-Closed Safety and Authorised-Exception Gate Hardening` | Reconciled | Markers `[x]`, target files (including `taskqueues.py` current-state update), and fail-closed invariants match between plan, phase details, and changes record. |
| `P02` (`P02-T01`) | `P02: Deterministic Exercise-Scenario Safety and Consent Verifier` | Reconciled | Marker `[x]`, `safety_consent_exercise_gate.py` coverage across all 6 suites on JSON `Store` and SQLite `SqlStore` (`107/107` safety blocks, `90/90` consent/exception blocks), and tamper checks match plan and critique `PC-001`–`PC-005`. |
| `P03` (`P03-T01`, `P03-T02`) | `P03: Verification Suite, Core Documentation, and Focused Validation` | Reconciled | Markers `[x]`, 8-test suite (`<= 12` ceiling) in `test_safety_consent_exercise_scenarios_81.py`, `src/core/README.md` section (`Refs #81`), and `ruff` / `mypy` / `unittest` validation records match. |
| `## Follow-Up Items` | `Follow-Up Items` (`None` in active `src/core` scope; epic `#81` tracked via `Refs #81`) | Reconciled | Active plan scope contains no deferred defects; broader parent-epic criteria remain outside this focused task. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/gates.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/taskqueues.py` | Enforced strict boolean `released is True`, standalone `safeguarding_items` and legacy `safeguarding` fail-closed checks, malformed `hazards` fail-closed blockers, and legacy string `appointments` tolerance in `Store.summary` / `SqlStore._row`. | `booking_gates` returns `UNKNOWN`/`FAIL` and `Store._open_safety_items` / `taskqueues.has_open_safety` fail closed on non-boolean `released`, open/malformed safeguarding, and `hazards=None` without regressing minimal hazard-only or note-only canary dicts. | Passed (`ruff check`, `mypy`, `test_gates.py`, `test_hazard_referral.py`, `test_taskqueues.py`, `test_sqlstore.py`, `test_safety_consent_exercise_scenarios_81.py`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/resident_decisions.py` | Added `"authorised_works_exceptions"` to `RESIDENT_FIELDS`, implemented fail-closed `validate_authorised_works_exception` (`RULE-002`, `FR-008`, `FR-011`, `FR-014`), rejected automated approvers (including `"Copilot Agent"`) and memory/sensor references, and threaded `*, now=None` (accepting ISO date/UTC strings and timezone-aware `datetime`) into `authority_for`, `resident_gate`, and `_resident_decision_gate`. | Valid human-authorised, resident-notified, current-scope, in-window exceptions clear measure-decision refusal while preserving tenure, retention, human-review, and safety holds; `delete_resident_records` purges `authorised_works_exceptions`. | Passed (`ruff check`, `mypy`, `test_resident_decisions.py`, `test_resident_journey_design.py`, `test_safety_consent_exercise_scenarios_81.py`) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/safety_consent_exercise_gate.py` | Implemented `verify_exercise_safety_and_consent_gates` and `verify_store_safety_and_consent_invariants` covering `constructed_workbench`, `resident_preview`, `sensor_retrofit` (`SEED = 190`, `C01`–`C11`), `scale_matrix`, `authorised_exception_controls`, and `learning_bundles` (`story-once`, `pre-visit-pack`, `change-impact`) across `Store` and `SqlStore`. | `passed=True` with `107/107` unresolved-safety progressions blocked (`0` breaches), `90/90` unconsented/invalid-exception work starts blocked (`0` breaches), full case/audit-chain immutability checks on every refused probe, positive control proofs, and static + isolated-dynamic tamper detection. | Passed (`ruff check`, `ruff format --check`, `mypy`, `test_safety_consent_exercise_scenarios_81.py`, `src/api/tests/test_content_standard.py`) | Reconciled |
| `P03-T01` | `src/core/tests/test_safety_consent_exercise_scenarios_81.py` | Added 8 focused unit/integration test methods covering JSON `Store`, SQLite `SqlStore`, determinism, `extra_stores` (`tests/dataset.DATA`), fail-closed safeguarding/non-boolean `released`/`hazards=None`, runtime `advance` refusal, exception validator + retention purge, tampered active work-order breach detection, and invalid `as_of` fail-closed `ValueError`. | All 8 test methods execute deterministically and assert exact refusal and immutability invariants (`<= 12` plan ceiling satisfied). | Passed (`Ran 8 tests ... OK`) | Reconciled |
| `P03-T02` | `src/core/README.md` | Documented `safety_consent_exercise_gate` and `validate_authorised_works_exception` with `Refs #81`, invariant coverage, plain-language human-approval phrasing, and explicit synthetic-exercise boundaries (zero `.copilot-tracking/` references in `src/`). | Documentation section present, Markdown-clean, and verified against `src/api/tests/test_content_standard.py`. | Passed (`ruff check`, `ruff format --check`, `mypy`, `unittest`, `test_content_standard.py`, `rename-zava-tests.py`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`taskqueues.py` alignment) | Extended strict boolean `released` and malformed safety-container guards to `src/core/src/zava_forward/core/taskqueues.py` (`is_open_safety_item`, `has_open_safety`, `_raw_hazard_dicts`). | Triggered during `P02-T01` `SqlStore(use_sql=True)` execution when `SqlStore._row` called `taskqueues.has_open_safety` on the `hazards=None` malformed-safety exercise case; classified as an immediately relevant current-state update requiring no user decision. | Reflected in `plan.md` (`P01-T01`), `phase-details.md` (`P01-T01` Likely Targets), and `changes.md` (`Implementation-Time Plan and Detail Updates`). | Preserved approved fail-closed intent (`PC-001` / `PC-002`); no repeat critique required or performed. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five critique findings (`PC-001` SQLite compatibility, `PC-002` strict boolean `released` and legacy `safeguarding` fail-closed handling, `PC-003` deterministic `as_of`/`now` clock propagation + wall-clock-free summaries + memory/sensor citation rejection + `RESIDENT_FIELDS` retention purge, `PC-004` `ZF-3` `dataset.DATA` parity + `sensor_scenarios` `C01`–`C11` + `learning_test_bundles.run_report`, and `PC-005` expanded static and isolated-dynamic tamper checks) were applied to the plan prior to implementation and verified in source and tests.
* Material revisions: None; only one immediately relevant current-state update (`taskqueues.py`) and ordinary local backward-compatibility judgments (`datetime` support in `_resolve_gate_clock`, `"copilot"`/`"agent"` tokens in `_AUTOMATED_APPROVER_TOKENS`, and plain-language `"approved by a named human"` phrasing for `test_content_standard.py`) occurred during implementation.
* Dependent-work pause assessment: No pause was needed because no material scope, architecture, or acceptance-criteria divergence arose.
* Justification assessment: Fully supported by deterministic execution and unit/integration test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| None in plan `## Follow-Up Items` (parent epic `#81` non-exercise criteria tracked separately on `#81`) | Caller bounded this task to proving the two exercise-scenario acceptance criteria of `#81` in `src/core`; `#81` also requires `#440` stabilization and closure/deferral of all child features before epic closure. | Parent epic `#81` owner (`Refs #81` on PR; do not use `Closes #81`). | Open outside active task scope; routed as distinct parent-epic follow-up work, not a task defect. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

* None (`0` Critical, `0` High, `0` Medium, `0` Low defects or gaps within the declared `#81` exercise-scenario task boundary).

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | None | No routed `rpi-implement`, `rpi-plan`, or `rpi-research` remediation required for this task. | Full conformance across declared `#81` exercise-scenario scope. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Parent epic `#81` remaining non-exercise acceptance criteria (`Refs #81`): (1) closing or deferring all remaining `#81` child features, and (2) completing the `#440` scoped stabilization checkpoint before closing epic `#81`. Both lie outside this bounded `src/core` exercise-scenario task.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff check` | `src/core` | Passed | `All checks passed!` (0 findings) |
| `python3 -m ruff format --check` | `src/core` | Passed | `302 files already formatted` |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 355 source files` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_safety_consent_exercise_scenarios_81.py -v` | `src/core` (`#81` verification suite) | Passed | `Ran 8 tests ... OK` (`Store` + `SqlStore`, determinism, `dataset.DATA`, fail-closed edge cases, exception controls, retention purge, tamper detection, invalid `as_of`) |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_scenario_manifest.py tests/test_needs_inventory.py tests/test_resident_journey_design.py -q` | `src/core` manifest & journey regression | Passed | `Ran 56 tests ... OK` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` (plus editable `.pth` verification for CLI subprocess modules) | `src/core` full suite | Passed | Zero failures across all touched and non-optional modules (`710` targeted + CLI tests `OK (skipped=154)`; optional `azure-iot-hub` absent on host for `test_device_registry_azure.py` only) |
| `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/agents/src:src/core/tests:src/agents/tests python3 -m unittest src/api/tests/test_content_standard.py -q` | Cross-package content-standard audit | Passed | `Ran 29 tests ... OK` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression check | Passed | `Ran 25 tests ... OK` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every requirement (`FR-PLAN-01`–`FR-PLAN-03`), acceptance criterion (`AC-1`–`AC-4`), and applied plan-critique disposition (`PC-001`–`PC-005`) is satisfied with deterministic code, test, documentation, and validation evidence across JSON `Store` and SQLite `SqlStore` (`107/107` unresolved-safety progression attempts blocked with `0` breaches; `90/90` unconsented/invalid-exception work-start attempts blocked with `0` breaches), with zero open defects or governance regressions.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up (`Refs #81`) | Parent epic `#81` child-feature closure and `#440` stabilization checkpoint outside this `src/core` exercise-scenario task |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier complete (`ruff check`, `ruff format --check`, `mypy`, `src/core` unit/integration suites, `src/api/tests/test_content_standard.py`, and `tools/rename-zava-tests.py` all passed)
* Blockers: None
