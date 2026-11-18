<!-- markdownlint-disable-file -->
# RPI Changes: Sensor Non-Authority Invariant Enforcement and Acceptance Suite

## Metadata

* Task ID: issue-109-sensor-non-authority
* Related plan: .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: `none`
* Status basis: Completed `P01`, `P02`, and `P03` (`P01-T01`..`P03-T02`) with Focused validation passing across `src/core` unit tests, `ruff check`, `ruff format --check`, `mypy`, and `tools/rename-zava-tests.py`.

## Execution Summary

Completed all three planned phases (`P01` through `P03`) across seven `src/core` production modules and `src/core/tests/test_sensor_non_authority.py`, enforcing fail-closed sensor non-authority invariants at construction, ingestion, review-draft projection, hazard/clock/hold workflows, legal-hold controls, and deterministic home ranking, with Focused validation green (`576` focused `src/core` unit tests + `25` migration regression tests, `ruff check`, `ruff format --check`, and strict `mypy`).

## Completed Work

### Sensor pipeline value, ingestion, and review-draft non-authority guards (`P01`, `P01-T01`, `P01-T02`)

* Added `SENSOR_NON_AUTHORITY_ERROR`, strict boolean invariant helpers, `Signal.__post_init__`, `ReviewTaskCandidate.__post_init__`, `enforce_sensor_non_authority`, and input verification in `review_task_candidate` and `version_provenance` in `src/core/src/zava_forward/core/sensor_analysis.py`.
* Added keyword-only defaulted non-authority flags (`diagnoses_hazard`, `starts_clock`, `releases_hold`, `changes_ranking`) and `__post_init__` enforcement on `WindowReceipt` plus explicit `False` non-authority report flags in `handover_continuity` in `src/core/src/zava_forward/core/sensor_ingest.py`.
* Enforced `sa.enforce_sensor_non_authority` in `_propose` before persistence and envelope + candidate non-authority verification (`_record_non_authoritative`) inside `_view` in `src/core/src/zava_forward/core/sensor_review_draft.py`, withholding digest-recomputed authority-tampered records as `INTEGRITY_MISMATCH` while preserving unknown-key stripping on valid records.

### Active sensor non-authority refusal across hazard, clock, hold, and ranking surfaces (`P02`, `P02-T01`, `P02-T02`)

* Added `SENSOR_REF`, `SENSOR_REFUSAL`, and `is_sensor_reference` in `src/core/src/zava_forward/core/controls.py`, enforcing sensor citation refusal inside `evidence_text`.
* Added `_forbid_sensor_actor` and `_forbid_sensor_authority` across `raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, and `release_hazard` (plus stored-hazard field verification on `source`, `note`, `job`, `sent_evidence`, `receipt_evidence`, `acceptance_evidence`, and `repair_evidence` before safety hold release) in `src/core/src/zava_forward/core/workflows.py`, using structural attribute checks alongside `Signal`/`ReviewTaskCandidate` to avoid circular store imports.
* Added sensor actor refusal in `DocControlsMixin._manager`, non-string/sensor reference refusal in `place_legal_hold`, and tampered stored reference refusal in `release_legal_hold` in `src/core/src/zava_forward/core/doc_controls.py`.
* Aligned `ranking.sql_key` rule-code validation with `ranking._rule_keys` in `src/core/src/zava_forward/core/ranking.py` so unknown or sensor rule codes uniformly raise `ValueError("Unknown ranking rule: ...")`.

### End-to-end `src/core` sensor non-authority acceptance suite and Focused validation (`P03`, `P03-T01`, `P03-T02`)

* Created `src/core/tests/test_sensor_non_authority.py` (`9` test methods `<= 12` limit, `0` generated files, `0` test removals) verifying constructor/receipt invariants, handover continuity and retained reproduction non-authority, adverse/faulty/weather/declined telemetry invariance, absence-of-alert invariance on active hazards/clocks/holds, default-off and tampered review-draft withholding across `Store` and `SqlStore`, active hazard/clock/repair/release sensor refusal (including legitimate surveyor prose containing `"sensor"` and tampered stored hazard fields), legal-hold sensor refusal and tampered-release refusal, and deterministic home ranking invariance and unknown/sensor rule refusal.
* Executed Focused validation across `src/core` sensor, hazard/controls/hold/gate/ranking, and dependency-boundary unit suites (`576` tests run, `0` failures), `ruff check .`, `ruff format --check .`, strict `mypy` (`343` source files), and `python3 tools/rename-zava-tests.py` (`25` tests).

## Implementation-Time Plan and Detail Updates

* Local judgment (`P02-T01`, `workflows.py`): Used structural attribute checks (`diagnoses_hazard`, `starts_clock`, `releases_hold`, `changes_ranking`) alongside `(Signal, ReviewTaskCandidate)` in `_forbid_sensor_authority` so `WindowReceipt` instances are refused without introducing a circular `sensor_ingest` -> `sensor_consumer` -> `sqlstore` -> `workflows` import, and included stored `"job"` alongside `"source"`, `"note"`, `"sent_evidence"`, `"receipt_evidence"`, `"acceptance_evidence"`, and `"repair_evidence"` in `release_hazard`. Preserves approved `FR-PLAN-03` and `PC-002` intent with `test_dependency_rule.py` passing.
* Local judgment (`P03-T02` test selector mapping): `src/core/tests/` names its controls, workflow, hold, gate, and ranking suites `test_chat_memory.py`, `test_hazard_referral.py`, `test_operator_suspension_drill.py`, `test_issue_220_challenge_route.py`, `test_document_rescan.py`, `test_gates.py`, `test_priority_order.py`, `test_ranking_publication.py`, `test_ranking_publication_runner.py`, and `test_ranking_tiebreak_audit.py` (rather than standalone `test_controls.py` / `test_ranking.py` filenames); ran all ten suites alongside the sensor and dependency-rule suites.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PYTHONPATH=src:tests python3 -m unittest tests/test_sensor_non_authority.py tests/test_sensor_ingest.py tests/test_sensor_consumer.py tests/test_sensor_review_draft.py tests/test_sensor_analysis.py -q` | `src/core` sensor ingestion, consumer, draft, analysis, and non-authority acceptance suites | Passed | `Ran 135 tests in 344.771s - OK (skipped=22)` (`9/9` passed in `test_sensor_non_authority.py`) |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_sensor_analysis_store.py tests/test_sensor_analysis_reproducibility.py -q` | `src/core` retained store analysis and reproducibility suites | Passed | `Ran 17 tests in 221.513s - OK` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_hazard_referral.py tests/test_operator_suspension_drill.py tests/test_issue_220_challenge_route.py tests/test_document_rescan.py tests/test_priority_order.py tests/test_ranking_publication.py tests/test_ranking_publication_runner.py tests/test_ranking_tiebreak_audit.py tests/test_gates.py tests/test_chat_memory.py -v` | `src/core` controls, hazard/clock workflows, legal/safety holds, gates, and deterministic ranking suites | Passed | `Ran 422 tests in 287.816s - OK (skipped=87)` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_dependency_rule.py -v` | `src/core` package dependency boundary | Passed | `Ran 2 tests in 5.831s - OK` |
| `/home/azureuser/.local/bin/ruff check . && /home/azureuser/.local/bin/ruff format --check . && /home/azureuser/.local/bin/mypy` | `src/core` lint, format, and strict static type checks | Passed | `All checks passed!`; `290 files already formatted`; `Success: no issues found in 343 source files` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression check | Passed | `Ran 25 tests in 0.782s - OK` |
| `python3 tools/rpi-checks.py --all` | Full repository gate | Skipped | Explicitly excluded by caller Focused-tier validation instructions |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, `P03`, and `P01-T01`..`P03-T02` all `[x]` and `Completed`)
* Completed-work evidence and handoff prose: Reconciled across `7` modified `src/core` modules and `src/core/tests/test_sensor_non_authority.py`
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active markers, `1` distinct Epic #109 / Issue #440 follow-up preserved)
* Review readiness: Ready for `rpi-review`

## Blockers

* None.

## Remaining Work

* None (`P01`, `P02`, and `P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md, `## Follow-Up Items`
* Live Azure IoT Hub and Azure SQL restart/persistence stabilization drill (`AC-066` / Issue #440 under Epic #109): Outside this focused offline `src/core` slice; owned by Epic #109 cloud stabilization work.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`; remaining `none`
* Validation coverage: Focused tier passed (`576` `src/core` unit tests across sensor, controls, hazard/clock, hold, gate, ranking, and dependency suites + `25` migration regression tests, `ruff check`, `ruff format --check`, and `mypy`)
* Blockers: None
* Current plan and detail updates: Local-judgment structural check in `workflows._forbid_sensor_authority` and mapped `src/core/tests/` controls/ranking selector filenames recorded above
* Planning and critique state: Ready (`PC-001`..`PC-004` applied and verified)
* Follow-up items: Issue #440 / Epic #109 live IoT Hub and Azure SQL stabilization drill
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
