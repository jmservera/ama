<!-- markdownlint-disable-file -->
# Review: Sensor Non-Authority Invariant Enforcement and Acceptance Suite (`Refs #109`)

## Scope and Evidence

* Task ID: issue-109-sensor-non-authority
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`)
* Assessed boundary: Issue #109 core engineering non-authority invariant (`No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking`), `FR-PLAN-01`..`FR-PLAN-05`, `NFR-PLAN-01`..`NFR-PLAN-02`, all 5 acceptance criteria, critique dispositions `PC-001`..`PC-004`, Focused-tier `src/core` validation, and Epic #109 external stabilization follow-up boundary (`#440`)
* Plan: .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/sensor-non-authority-109-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/sensor-non-authority-109-research.md and workspace `git diff` across `src/core/src/zava_forward/core/` and `src/core/tests/test_sensor_non_authority.py`

## Opening Review State

* Interpreted review goal: Independently verify once after implementation that `src/core` enforces fail-closed sensor non-authority invariants across ingestion receipts, continuity reports, deterministic signals, review-task candidates, unapproved review drafts, hazard diagnosis, statutory Awaab's Law / external service clocks, safety/legal hold release, and deterministic home ranking, and that all 5 acceptance criteria and Focused validation checks pass without regression.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan markers, phase details, single-pass critique (`PC-001`..`PC-004`), reconciled changes record, research synthesis (`C1`..`C18`), and Focused validation results are complete and current.
* Acceptance basis: Issue #109 core non-authority criterion, BRD `FR-048` / `RULE-014`, PRD `FR-050` / `AC-066`..`AC-068`, ADR 0002 / ADR 0003 Decision 6, plan `## Functional Requirements` (`FR-PLAN-01`..`FR-PLAN-05`), `## Non-Functional Requirements` (`NFR-PLAN-01`..`NFR-PLAN-02`), `## Acceptance Criteria` (5 criteria), and `## Critique Disposition` (`PC-001`..`PC-004`).
* First comparison boundary: Compare the 7 modified `src/core` source files and `src/core/tests/test_sensor_non_authority.py` against `FR-PLAN-01`..`FR-PLAN-05` and `PC-001`..`PC-004`; live Azure IoT Hub / Azure SQL restart persistence (`#440`) remains outside this offline `src/core` slice.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/2026-11-15/sensor-non-authority-109-review.md` (with parent RPI state transitions persisted in `.copilot-tracking/rpi-sessions/2026-11-15/sensor-non-authority-109-state.json`).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Verdict: PASS
* Review execution evidence: Completed single-pass read-only review on 2026-11-15 across all 7 modified `src/core` production modules, `src/core/tests/test_sensor_non_authority.py`, Focused-tier validation outputs (`576` `src/core` unit tests + `25` migration regression tests, `ruff check`, `ruff format --check`, and `mypy`), and reconciled RPI artifacts.

## Acceptance Criteria Verification (`#109` Slice — All 5 Criteria)

| # | Acceptance criterion (`#109` `src/core` non-authority slice) | Status | Verification evidence |
|---|--------------------------------------------------------------|--------|-----------------------|
| 1 | `Signal`, `ReviewTaskCandidate`, and `WindowReceipt` enforce strict non-authority flags at construction/replacement time, and `enforce_sensor_non_authority` rejects authority-claiming objects and serialized mappings with `ValueError` (`FR-PLAN-01`) | PASS | `Signal.__post_init__`, `ReviewTaskCandidate.__post_init__`, and `enforce_sensor_non_authority` in `src/core/src/zava_forward/core/sensor_analysis.py`; keyword-only defaulted non-authority flags and `WindowReceipt.__post_init__` + `handover_continuity` flags in `src/core/src/zava_forward/core/sensor_ingest.py`; verified by `test_value_and_receipt_constructors_enforce_strict_non_authority` and `test_handover_continuity_and_retained_reproduction_remain_non_authoritative`. |
| 2 | `sensor_review_draft` validates non-authority before persistence and withholds any stored draft with tampered or digest-recomputed authority flags as `INTEGRITY_MISMATCH` (`FR-PLAN-02`) | PASS | `enforce_sensor_non_authority` calls in `_propose` and `_record_non_authoritative` envelope + candidate verification in `_view` in `src/core/src/zava_forward/core/sensor_review_draft.py`, preserving `_VIEW_CANDIDATE` unknown-key stripping; verified across `Store` and `SqlStore` by `test_review_drafts_remain_non_authoritative_and_tampered_drafts_fail_closed` and `test_sensor_review_draft.py`. |
| 3 | `controls.evidence_text`, `workflows` hazard/clock/repair/release operations, and `doc_controls` legal hold operations deterministically refuse sensor telemetry/signal/rule/schema/draft references, structured sensor metadata, tampered stored sensor evidence, and non-manager/sensor actors without affecting human-evidenced workflows (`FR-PLAN-03`) | PASS | `SENSOR_REF`, `SENSOR_REFUSAL`, and `is_sensor_reference` in `src/core/src/zava_forward/core/controls.py`; `_forbid_sensor_actor`, `_forbid_sensor_authority`, and stored-field `release_hazard` checks in `src/core/src/zava_forward/core/workflows.py`; `_manager`, `place_legal_hold`, and `release_legal_hold` checks in `src/core/src/zava_forward/core/doc_controls.py`; verified by `test_absence_of_sensor_alert_never_clears_open_hazard_clock_or_hold`, `test_hazard_and_clock_workflows_refuse_sensor_citations_payloads_and_actors`, `test_safety_release_refuses_tampered_stored_sensor_evidence_and_preserves_gate`, and `test_legal_hold_refuses_sensor_references_actors_and_tampered_release`. |
| 4 | `ranking.rank`, `ranking.reasons`, `ranking.snapshot`, `ranking.sql_key`, and `store._ranking()` produce identical outputs and `snapshot_hash` across normal, extreme, faulty, weather-sim, stale, insufficient, and declined sensor activity and unapproved review drafts, and uniformly raise `ValueError` on sensor ranking rules (`FR-PLAN-04`) | PASS | Unknown-rule `ValueError` alignment in `sql_key` in `src/core/src/zava_forward/core/ranking.py`; verified across `Store` and `SqlStore` by `test_end_to_end_adverse_faulty_weather_and_declined_series_preserve_workflows` and `test_ranking_is_invariant_to_injected_case_sensor_fields_and_rejects_sensor_rules`. |
| 5 | `src/core/tests/test_sensor_non_authority.py` passes alongside the `src/core` unit test suites, `mypy`, `ruff check`, and `ruff format --check` (`FR-PLAN-05`, `NFR-PLAN-01`, `NFR-PLAN-02`) | PASS | `9` test methods (`<= 12` limit, `0` test removals, `0` generated files) pass in `src/core/tests/test_sensor_non_authority.py` alongside `152` sensor tests, `422` controls/hazard/hold/gate/ranking tests, `2` dependency-rule tests, `25` migration regression tests, `ruff check .`, `ruff format --check .`, and strict `mypy` (`343` source files). |

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `Sensor pipeline value, ingestion, and review-draft non-authority guards (P01, P01-T01, P01-T02)` | Reconciled | Markers checked `[x]`; `sensor_analysis.py`, `sensor_ingest.py`, and `sensor_review_draft.py` satisfy `FR-PLAN-01`, `FR-PLAN-02`, `PC-002`, and `PC-003`. |
| `P02` (`P02-T01`, `P02-T02`) | `Active sensor non-authority refusal across hazard, clock, hold, and ranking surfaces (P02, P02-T01, P02-T02)` | Reconciled | Markers checked `[x]`; `controls.py`, `workflows.py`, `doc_controls.py`, and `ranking.py` satisfy `FR-PLAN-03`, `FR-PLAN-04`, and `PC-002`. |
| `P03` (`P03-T01`, `P03-T02`) | `End-to-end src/core sensor non-authority acceptance suite and Focused validation (P03, P03-T01, P03-T02)` | Reconciled | Markers checked `[x]`; `test_sensor_non_authority.py` (`9` methods) and Focused validation satisfy `FR-PLAN-05`, `NFR-PLAN-01`, `NFR-PLAN-02`, `PC-001`, and `PC-004`. |
| `## Follow-Up Items` | Live Azure IoT Hub and Azure SQL restart/persistence stabilization drill (`AC-066` / Issue #440 under Epic #109) | Reconciled | Preserved outside active `P01`..`P03` scope; commit uses `Refs #109` rather than a closing keyword because Epic #109's `#440` stabilization checkpoint remains open. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_ingest.py` | Added `SENSOR_NON_AUTHORITY_ERROR`, strict boolean invariant checks on `Signal`, `ReviewTaskCandidate`, and `WindowReceipt` (keyword-only defaults), `enforce_sensor_non_authority`, entry checks on `review_task_candidate` / `version_provenance`, and explicit `False` non-authority keys on `handover_continuity` | Diff verified; positional `WindowReceipt(...)` construction and canonical `as_dict` digests preserved | Passed (`test_sensor_non_authority.py`, `test_sensor_analysis.py`, `test_sensor_analysis_reproducibility.py`, `test_sensor_ingest.py`, `ruff`, `mypy`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/sensor_review_draft.py` | Enforced `enforce_sensor_non_authority` in `_propose` and added `_record_non_authoritative` envelope + candidate verification inside `_view` so digest-recomputed authority-tampered records return `INTEGRITY_MISMATCH` | Diff verified; `_VIEW_CANDIDATE` unknown-key stripping preserved | Passed (`test_sensor_non_authority.py`, `test_sensor_review_draft.py`, `ruff`, `mypy`) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/controls.py`, `src/core/src/zava_forward/core/workflows.py`, `src/core/src/zava_forward/core/doc_controls.py` | Added `SENSOR_REF`, `SENSOR_REFUSAL`, and `is_sensor_reference` in `controls.evidence_text`; guarded `user`, `metadata`, `note`, `job`, `evidence`, and stored hazard fields in `workflows.py`; guarded `_manager`, `place_legal_hold`, and stored `reference` in `release_legal_hold` in `doc_controls.py` | Diff verified; legitimate surveyor prose mentioning room hardware succeeds while sensor citations/actors/payloads fail closed before `save()` / `audit()` | Passed (`test_sensor_non_authority.py`, `test_hazard_referral.py`, `test_operator_suspension_drill.py`, `test_issue_220_challenge_route.py`, `test_document_rescan.py`, `test_chat_memory.py`, `ruff`, `mypy`) | Reconciled |
| `P02-T02` | `src/core/src/zava_forward/core/ranking.py` | Added unknown-rule check in `ranking.sql_key` raising `ValueError("Unknown ranking rule: ...")` in parity with `ranking._rule_keys` | Diff verified; valid policy hashes and SQL sort keys unchanged | Passed (`test_sensor_non_authority.py`, `test_priority_order.py`, `test_ranking_publication.py`, `test_ranking_publication_runner.py`, `test_ranking_tiebreak_audit.py`, `ruff`, `mypy`) | Reconciled |
| `P03-T01`, `P03-T02` | `src/core/tests/test_sensor_non_authority.py`, `.copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md` | Added 9 strictly typed end-to-end acceptance and fail-closed refusal tests across `Store` and `SqlStore` and recorded Focused-tier validation results | Verified (`9 <= 12` methods, `0` deleted tests, `0` `pyproject.toml` weakenings) | Passed (`576` `src/core` unit tests + `25` migration tests, `ruff check`, `ruff format --check`, `mypy`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` (`workflows.py`) | Used structural attribute checks (`diagnoses_hazard`, `starts_clock`, `releases_hold`, `changes_ranking`) alongside `(Signal, ReviewTaskCandidate)` in `_forbid_sensor_authority` and added `"job"` to stored-field recheck in `release_hazard` | Avoids circular `sensor_ingest` -> `sensor_consumer` -> `sqlstore` -> `workflows` import while still refusing `WindowReceipt` objects and tampered stored `job` references; local judgment | Recorded in `.copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md` | Not needed (preserves `FR-PLAN-03` and `PC-002` intent) | Reconciled |
| `P03-T02` (`src/core/tests/` selectors) | Executed the repository's actual controls, hazard, hold, gate, and ranking suite filenames (`test_chat_memory.py`, `test_hazard_referral.py`, `test_document_rescan.py`, `test_priority_order.py`, `test_ranking_*.py`, `test_gates.py`) alongside the sensor and dependency suites | `src/core/tests/` organizes controls and ranking assertions under feature-named modules rather than standalone `test_controls.py` / `test_ranking.py`; local judgment | Recorded in `.copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md` | Not needed (expands coverage across all touched modules) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass critique findings (`PC-001`..`PC-004`) recorded in `.copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md` (`## Critique Disposition`) are implemented and verified by Focused validation (`mypy` strict `0` issues across `343` files, `WindowReceipt` `kw_only=True` flags, `workflows`/`doc_controls` side-channel refusal, `_VIEW_CANDIDATE` unknown-key stripping preserved, and `tools/rename-zava-tests.py` green on `feat/iot-109-sensor-non-authority`).
* Material revisions: None required during implementation.
* Dependent-work pause assessment: No material revision occurred and plan dependency order (`P01` -> `P02` -> `P03`) was respected.
* Justification assessment: Fully supported by deterministic offline unit and acceptance test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live Azure IoT Hub and Azure SQL restart/persistence stabilization drill (`AC-066` / Issue #440 under Epic #109) | Requires live Azure IoT Hub and Azure SQL cloud integration and Epic #440 stabilization checkpoint outside this offline `src/core` slice | Epic #109 / Issue #440 delivery owner | Distinct follow-up route (`Refs #109` maintained accurately) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Legacy migrated authority modules (`controls.py`, `workflows.py`, `doc_controls.py`, `ranking.py`) remain under ADR-0006 `pyproject.toml` format and strict-typing exclusions

* Related scope: `P02-T01`, `P02-T02`
* Evidence: `src/core/pyproject.toml` (`[tool.ruff.format].exclude` and `[[tool.mypy.overrides]]`) and typed `cast(...)` `Protocol`/`Callable` bindings in `src/core/tests/test_sensor_non_authority.py`
* Impact: Non-blocking maintainability / engineering-quality opportunity only; runtime non-authority enforcement, `ruff check`, `ruff format --check`, and strict `mypy` across all `343` files pass cleanly. Graduating `controls.py` and `ranking.py` to full static type annotations in a dedicated post-cut-over cleanup slice will eliminate `cast(...)` wrappers in typed callers and tests.
* Destination: follow-up
* Smallest useful next action: Offer optional strict-typing graduation of `controls.py` and `ranking.py` alongside `src/api` HTTP route non-authority parity checks and Issue #440 Epic #109 cloud stabilization at the post-Review follow-up checkpoint.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | follow-up | User-selectable post-Review follow-up backlog | Non-blocking engineering-quality typing graduation opportunity outside `#109` acceptance defects |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Issue #440 / Epic #109 scoped stabilization checkpoint and live Azure IoT Hub / Azure SQL persistence drill (`AC-066`), outside this offline `src/core` slice.
* Optional M6 strict-typing graduation for `controls.py` and `ranking.py` in `src/core/pyproject.toml` (`RV-001`).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`, `P02`, and `P03` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src:tests python3 -m unittest tests/test_sensor_non_authority.py tests/test_sensor_ingest.py tests/test_sensor_consumer.py tests/test_sensor_review_draft.py tests/test_sensor_analysis.py -q` | `src/core` sensor ingestion, consumer, review-draft, analysis, and non-authority acceptance suites | Passed | `Ran 135 tests in 344.771s - OK (skipped=22)` (`9/9` passed in `test_sensor_non_authority.py`) |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_sensor_analysis_store.py tests/test_sensor_analysis_reproducibility.py -q` | `src/core` retained store analysis and reproducibility suites | Passed | `Ran 17 tests in 221.513s - OK` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_hazard_referral.py tests/test_operator_suspension_drill.py tests/test_issue_220_challenge_route.py tests/test_document_rescan.py tests/test_priority_order.py tests/test_ranking_publication.py tests/test_ranking_publication_runner.py tests/test_ranking_tiebreak_audit.py tests/test_gates.py tests/test_chat_memory.py -v` | `src/core` controls, hazard/clock workflows, legal/safety holds, gates, and deterministic ranking suites | Passed | `Ran 422 tests in 287.816s - OK (skipped=87)` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_dependency_rule.py -v` | `src/core` package dependency boundary | Passed | `Ran 2 tests in 5.831s - OK` |
| `/home/azureuser/.local/bin/ruff check . && /home/azureuser/.local/bin/ruff format --check . && /home/azureuser/.local/bin/mypy` | `src/core` lint, format, and strict static type checks | Passed | `All checks passed!`; `290 files already formatted`; `Success: no issues found in 343 source files` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression check | Passed | `Ran 25 tests in 0.782s - OK` |
| `python3 tools/rpi-checks.py --all` | Repository-wide full gate | Skipped | Explicitly excluded by caller Focused-tier validation instructions |

## Outcome

* Verdict: PASS
* Outcome: Conformant
* Outcome rationale: All 5 acceptance criteria of the `#109` `src/core` sensor non-authority slice (`FR-PLAN-01`..`FR-PLAN-05` and `NFR-PLAN-01`..`NFR-PLAN-02`), all four limbs of Issue #109's core engineering invariant (`diagnoses_hazard=False`, `starts_clock=False`, `releases_hold=False`, `changes_ranking=False`), and all single-pass critique dispositions (`PC-001`..`PC-004`) are satisfied with zero implementation defects and clean Focused validation.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Ranked post-Review follow-up selection (`RV-001` typing graduation and Issue #440 / Epic #109 cloud stabilization) |

* Execution status: Complete
* Verdict: PASS
* Outcome: Conformant
* Validation coverage: Focused tier passed (`576` `src/core` unit tests across sensor, controls, hazard/clock, hold, gate, ranking, and dependency suites + `25` migration regression tests, `ruff check`, `ruff format --check`, and `mypy`); `tools/rpi-checks.py --all` skipped per explicit caller instruction
* Blockers: None
