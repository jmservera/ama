<!-- markdownlint-disable-file -->
# RPI Changes: Issue #81 Exercise-Scenario Safety and Resident Consent Gate Verification

## Metadata

* Task ID: issue-81-safety-consent-gates
* Related plan: .copilot-tracking/plans/2026-11-15/issue-81-safety-consent-gates-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-81-safety-consent-gates-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: `none`
* Status basis: Full plan (`P01` through `P03`) implemented, documented, and verified cleanly across `ruff check`, `ruff format --check`, `mypy`, `src/core` unit/integration tests, `src/api/tests/test_content_standard.py`, and `tools/rename-zava-tests.py`.

## Execution Summary

Completed full-plan implementation for `#81` exercise-scenario safety and resident consent gate verification: hardened fail-closed standalone safeguarding, strict boolean `released`, and malformed safety-container handling across `gates.py`, `store.py`, `sqlstore.py`, and `taskqueues.py`; implemented `validate_authorised_works_exception` (`RULE-002`, `FR-008`, `FR-011`, `FR-014`) and timezone-aware `datetime`/`str` clock support in `resident_decisions.py`; added `safety_consent_exercise_gate.py` (`verify_exercise_safety_and_consent_gates` and `verify_store_safety_and_consent_invariants`) proving zero unblocked unresolved-safety progressions (`107/107` blocked) and zero unconsented/invalid-exception work starts (`90/90` blocked) across all six exercise suites on JSON `Store` and SQLite `SqlStore`; added `src/core/tests/test_safety_consent_exercise_scenarios_81.py` (8 focused tests, `<= 12` ceiling); and documented the verifier in `src/core/README.md`.

## Completed Work

### Fail-closed standalone safeguarding, strict boolean `released`, and SQLite legacy appointment tolerance

* Related phase or task: `P01-T01`
* Files: `src/core/src/zava_forward/core/gates.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`
* What changed and why: Added `_safeguarding_item_closed` and `_case_safety_state` in `gates.py` and guarded `Store._open_safety_items` so non-boolean `released` values, open or malformed `safeguarding_items`, malformed legacy `safeguarding`, and missing/non-list `hazards` all fail closed while preserving minimal hazard-only dicts and note-only canary fixtures; guarded `isinstance(a, dict)` in `Store.summary` and `SqlStore._row` so `resident_preview_fixture.build` datasets open cleanly under `SqlStore`.
* Completion evidence: Updated source modules verified against existing gate, hazard, taskqueue, and resident-preview suites.
* Validation: Passed (`ruff check`, `mypy`, and 568 targeted `unittest` cases).

### Fail-closed `validate_authorised_works_exception` and deterministic `now` clock support

* Related phase or task: `P01-T02`
* Files: `src/core/src/zava_forward/core/resident_decisions.py`
* What changed and why: Added `"authorised_works_exceptions"` to `RESIDENT_FIELDS` for retention deletion, implemented `validate_authorised_works_exception` enforcing `RULE-002`, `FR-008`, `FR-011`, and `FR-014` (`AC-018`) (including automated/AI approver rejection and memory/sensor citation rejection), and threaded optional `*, now=None` into `resident_gate` and `_resident_decision_gate` while keeping tenure, retention, and `"Needs human review"` holds unconditional.
* Completion evidence: Updated `resident_decisions.py` verified against `test_resident_decisions.py`.
* Validation: Passed (`ruff check`, `mypy`, and 568 targeted `unittest` cases).

### Deterministic exercise-scenario safety and consent gate verifier

* Related phase or task: `P02-T01`
* Files: `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`, `src/core/src/zava_forward/core/taskqueues.py`
* What changed and why: Created `safety_consent_exercise_gate.py` implementing `verify_exercise_safety_and_consent_gates` and `verify_store_safety_and_consent_invariants` across `constructed_workbench`, `resident_preview`, `sensor_retrofit`, `scale_matrix`, `authorised_exception_controls`, and `learning_bundles` on both JSON `Store` (`use_sql=False`) and SQLite `SqlStore` (`use_sql=True`), proving 107/107 unresolved-safety progression attempts blocked (`controlled_progressions_with_unresolved_safety == 0`) and 90/90 unconsented/invalid-exception work-start attempts blocked (`work_started_without_agreement_or_exception == 0`). Also applied an immediately relevant current-state hardening in `taskqueues.py` (`_raw_hazard_dicts`, `_has_malformed_safety_containers`, strict boolean `released` check in `is_open_safety_item`) so `SqlStore._row` derived-column indexing fails closed instead of raising `TypeError` when `hazards` is `None` or malformed.
* Completion evidence: Repeated deterministic runs on JSON `Store` and SQLite `SqlStore` passed with identical structured outputs (`passed=True`, zero breaches).
* Validation: Passed (`ruff check`, `mypy` across 354 source files, `test_taskqueues.py`, and live JSON/SQLite verifier execution).

### P03: Verification Suite, Core Documentation, and Focused Validation

* Plan marker: `P03`, `P03-T01`, `P03-T02`
* Files: `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, `src/core/README.md`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`
* What changed and why: Added `src/core/tests/test_safety_consent_exercise_scenarios_81.py` with 8 focused test methods (`<= 12` ceiling) proving JSON `Store` and SQLite `SqlStore` parity across all six exercise suites, byte-identical determinism across repeated runs, `extra_stores` coverage on `tests/dataset.DATA`, standalone safeguarding / non-boolean `released` / `hazards=None` fail-closed checks, runtime `advance` safety refusal across JSON and SQLite, `validate_authorised_works_exception` positive and negative controls (automated approver, resident-not-notified, missing legal review, expired window, cross-measure leak, memory/sensor citation, retention purge via `delete_resident_records`), tampered pre-existing active work-order breach detection, and invalid `as_of` fail-closed `ValueError`. Documented `safety_consent_exercise_gate` and `validate_authorised_works_exception` in `src/core/README.md` (`Refs #81`). During full cross-suite validation, tightened `_AUTOMATED_APPROVER_TOKENS` (`"copilot"`, `"agent"`), extended `_resolve_gate_clock` to accept timezone-aware `datetime` objects (`test_resident_journey_design.py` compatibility), and aligned plain-language approval copy (`"approved by a named human"`) with `src/api/tests/test_content_standard.py`.
* Completion evidence: All 8 tests in `test_safety_consent_exercise_scenarios_81.py` pass; all `ruff`, `mypy`, content-standard, scenario-manifest, rename-regression, and `src/core` unit/CLI test suites pass.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

* Immediately relevant current-state update (`P01-T01` / `P02-T01`): Extended fail-closed malformed-container and strict-boolean `released` handling to `src/core/src/zava_forward/core/taskqueues.py` (`is_open_safety_item`, `has_open_safety`, `_raw_hazard_dicts`) after `SqlStore._row` hit `taskqueues.has_open_safety` on the `hazards=None` exercise shape during `P02-T01` SQLite verification, and reflected `taskqueues.py` in `P01-T01` plan and phase details. Preserves approved fail-closed intent without altering scope or acceptance criteria.
* Local judgment (`P01-T02` / `P03`): Extended `_resolve_gate_clock` in `resident_decisions.py` to accept timezone-aware `datetime` objects alongside ISO strings (`None` defaulting to UTC wall-clock) for backward compatibility with `test_resident_journey_design.py`, expanded `_AUTOMATED_APPROVER_TOKENS` to catch `"Copilot Agent"`, and used `"approved by a named human"` wording to satisfy `src/api/tests/test_content_standard.py`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m ruff check` | `src/core` | Passed | `All checks passed!` (0 findings) |
| `python3 -m ruff format --check` | `src/core` | Passed | `302 files already formatted` |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 355 source files` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_safety_consent_exercise_scenarios_81.py -v` | `src/core` (`#81` suite) | Passed | `Ran 8 tests ... OK` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_scenario_manifest.py tests/test_needs_inventory.py tests/test_resident_journey_design.py -q` | `src/core` manifest & journey compatibility | Passed | `Ran 56 tests ... OK` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` (with editable `.pth` for subprocess CLI modules) | `src/core` full suite | Passed | Zero failures across all touched and non-optional modules (`710` targeted + CLI tests `OK (skipped=154)`; optional `azure-iot-hub` dev dependency absent on host for `test_device_registry_azure.py` only) |
| `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/agents/src:src/core/tests:src/agents/tests python3 -m unittest src/api/tests/test_content_standard.py -q` | Cross-package content-standard audit | Passed | `Ran 29 tests ... OK` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression check | Passed | `Ran 25 tests ... OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all checked `[x]`; `taskqueues.py` reflected in `P01-T01`)
* Completed-work evidence and handoff prose: Reconciled and current
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan markers)
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-81-safety-consent-gates-plan.md, `## Follow-Up Items`
* None inside the `src/core` exercise-scenario scope; parent epic `#81` retains its broader non-exercise acceptance criteria outside this focused `src/core` delivery (`Refs #81`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`; remaining `none`
* Validation coverage: Focused tier complete (`ruff check`, `ruff format --check`, `mypy`, `src/core` unit/integration tests, `test_content_standard.py`, `rename-zava-tests.py`)
* Blockers: None
* Current plan and detail updates: `taskqueues.py` recorded under `P01-T01` as an immediately relevant current-state fail-closed alignment
* Planning and critique state: `Ready` (`PC-001` through `PC-005` applied prior to implementation)
* Follow-up items: Broader non-exercise epic `#81` acceptance criteria remain tracked on `#81` (`Refs #81`)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
