<!-- markdownlint-disable-file -->
# RPI Plan: Sensor Non-Authority Invariant Enforcement and Acceptance Suite

## Task Metadata

* Task ID: issue-109-sensor-non-authority
* Task slug: sensor-non-authority-109
* Planning status: Implemented (ready for review)
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/sensor-non-authority-109-plan-critique.md

## Executive Summary

This plan delivers explicit runtime invariant enforcement and a deterministic end-to-end acceptance test suite in `src/core` for Issue #109's core engineering criterion: **no sensor signal diagnoses a hazard, starts a clock, releases a hold, or changes ranking**. While `src/core` already isolates retained telemetry tables and keeps deterministic sensor analysis pure, contrarian research uncovered four runtime enforcement gaps where constructed or mutated value objects, cited sensor artefacts, recomputed stored review drafts, or custom ranking policies could cross or obscure the authority boundary.

The implementation closes all four gaps across three bounded phases (`P01` through `P03`):

1. **Sensor pipeline value and draft guards (`P01`)**: Enforce constructor and payload non-authority invariants on `Signal`, `ReviewTaskCandidate`, and `WindowReceipt` (`sensor_analysis.py`, `sensor_ingest.py`) and enforce non-authority verification when proposing or projecting stored `sensor_review_drafts` (`sensor_review_draft.py`).
2. **Authority surface refusal guards (`P02`)**: Refuse sensor telemetry, signal, rule, schema, and review-draft citations and structured sensor metadata payloads across hazard diagnosis, statutory Awaab's Law / external service clocks, repair/hold release, legal hold controls, and deterministic home ranking (`controls.py`, `workflows.py`, `doc_controls.py`, `ranking.py`).
3. **End-to-end `src/core` acceptance suite and Focused validation (`P03`)**: Add `src/core/tests/test_sensor_non_authority.py` proving both passive state invariance and active fail-closed refusal across `sensor_ingest.py`, `sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `Store`, `SqlStore`, `ranking.py`, hazards, clocks, and holds, verified with `src/core` unit tests, `mypy`, and `ruff`.

### User Decisions and Requirements Highlights

* **Scope locked to `src/core` invariant enforcement and end-to-end proof**: All production guards and acceptance tests reside in `src/core` (`src/core/src/zava_forward/core/` and `src/core/tests/`), proving Issue #109's non-authority criterion across ingestion, analysis, and store/ranking/hazard/hold surfaces.
* **Focused validation tier without `tools/rpi-checks.py` or `git push`**: Validation runs `src/core` unit tests (`test_sensor*.py` and full suite), `mypy`, `ruff check`, `ruff format --check`, and `python3 tools/rename-zava-tests.py` only, and commits locally on `feat/iot-109-sensor-non-authority` with `Refs #109` and the Copilot co-author trailer without pushing.
* **Continuous automatic RPI execution**: Planning advances directly through independent plan critique (`rpi-plan-critique`), implementation (`rpi-implement`), and review (`rpi-review`) without pausing for routine confirmation.

### What You May Not Know

* **Surgical formatting boundary in `src/core/pyproject.toml`**: Legacy migrated modules (`controls.py`, `workflows.py`, `doc_controls.py`, `ranking.py`) are intentionally excluded from `ruff format` and `mypy` strictness in `src/core/pyproject.toml` to preserve move-not-copy git blame, whereas `sensor_analysis.py`, `sensor_ingest.py`, `sensor_review_draft.py`, and new test modules must pass `mypy` (`strict = true`), `ruff check`, and `ruff format --check` cleanly.
* **Exact sensor artefact matching preserves human surveyor prose**: Matching exact sensor tokens and prefixes (`SENSOR_REF`, analogous to existing `MEMORY_REF` in `controls.py`) blocks citing telemetry readings, rules, schemas, signals, and drafts as authority evidence without false-rejecting legitimate human inspection notes that mention physical room hardware in ordinary prose.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop continuously in a single run without stopping after any phase summary (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`), writing dated artifacts under `.copilot-tracking/` for Issue #109 (`Epic: In-use monitoring with Azure IoT Hub (simulated)`).
* Work in `/home/azureuser/source/ama-demo-wt/feat-109-sensor-non-authority` on stacked branch `feat/iot-109-sensor-non-authority` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Deliver explicit end-to-end invariant enforcement and an acceptance test suite in `src/core` for Issue #109's core engineering criterion: `No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking` (source: user prompt, Issue #109, `docs/brds/agentic-retrofit-programme-brd.md` FR-048 and RULE-014, `docs/prds/zava-forward-retrofit-programme-demonstrator.md` FR-050 and AC-066..AC-068).
* Prove across ingestion (`sensor_ingest.py`), deterministic sensor analysis (`sensor_analysis.py`), and store/ranking/hazard/hold surfaces that no sensor reading or derived sensor signal can diagnose a hazard, start an Awaab's Law or statutory clock, release a hold/blocker, or alter deterministic home ranking.
* Validate at the Focused tier (`src/core` unit tests, `ruff check`, `ruff format --check`, `mypy`, and `python3 tools/rename-zava-tests.py`) and do not run `tools/rpi-checks.py`.
* Commit all code changes and `.copilot-tracking/` artifacts locally with `Refs #109` and the Copilot `Co-authored-by` trailer, and do not push.

## Goals

* Enforce fail-closed non-authority invariants on sensor ingestion receipts, deterministic sensor signals, condition-review task candidates, and unapproved case-local sensor review drafts in `src/core`.
* Prevent sensor telemetry identifiers, derived signals, absence-of-alert outcomes (`NO_SIGNAL`), or sensor review drafts from being cited or smuggled into hazard diagnosis, statutory Awaab's Law / external service clocks, safety/legal hold release, or deterministic home ranking rules.
* Prove end-to-end across both `SqlStore` and in-memory `Store` in `src/core/tests/test_sensor_non_authority.py` that sensor ingestion, deterministic analysis, reproduction, and draft creation never diagnose a hazard, start a clock, release a hold/blocker, penalize declined/insufficient homes, or alter deterministic home ranking.

## Scope and Non-Goals

### In Scope

* Runtime non-authority invariant enforcement in `src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_ingest.py`, and `src/core/src/zava_forward/core/sensor_review_draft.py`.
* Active refusal of sensor telemetry/signal/draft references and structured sensor authority payloads in `src/core/src/zava_forward/core/controls.py`, `src/core/src/zava_forward/core/workflows.py`, `src/core/src/zava_forward/core/doc_controls.py`, and `src/core/src/zava_forward/core/ranking.py`.
* End-to-end acceptance and invariant test suite in `src/core/tests/test_sensor_non_authority.py`.
* Focused local validation (`unittest`, `mypy`, `ruff check`, `ruff format --check` in `src/core`), dated RPI tracking artifacts, and local git commit referencing `#109` without pushing.

### Non-Goals

* Provisioning or testing live cloud Azure IoT Hub or Azure SQL infrastructure (tracked separately under Epic #109 / Issue #440).
* Modifying HTTP routes in `src/api`, agent orchestration in `src/agents`, or Bicep templates in `infra/`.
* Running `tools/rpi-checks.py` or pushing branch commits to `origin`.
* Reformatting legacy migrated modules excluded in `src/core/pyproject.toml`.

## Functional Requirements

* **FR-PLAN-01 (Sensor value and ingestion non-authority invariants)**: `Signal`, `ReviewTaskCandidate`, `enforce_sensor_non_authority` (`sensor_analysis.py`), and `WindowReceipt` (`sensor_ingest.py`) shall enforce at construction and validation time that `diagnoses_hazard`, `starts_clock`, `releases_hold`, and `changes_ranking` are strictly boolean `False`, `Signal.priority_effect` is `"NONE"`, `ReviewTaskCandidate.resident_report_unaffected` is strictly boolean `True`, and `ReviewTaskCandidate` carries only `task_type == "SENSOR_REVIEW_DUE"`, `queue == "condition-assessment"`, and `status == "PROPOSED"`.
  * Observable acceptance criteria: Constructing or `dataclasses.replace`-mutating `Signal`, `ReviewTaskCandidate`, or `WindowReceipt` with any authority-claiming value, or passing an authority-claiming mapping to `enforce_sensor_non_authority`, raises `ValueError` containing `"SENSOR_NON_AUTHORITY_VIOLATION"`.
* **FR-PLAN-02 (Unapproved sensor review draft integrity)**: `sensor_review_draft` shall verify `enforce_sensor_non_authority` before persisting a draft and verify stored non-authority invariants in `_view` alongside `draft_digest`.
  * Observable acceptance criteria: Even if a stored record under `case["sensor_review_drafts"]` has its `draft_digest` recomputed after altering `state`, `manual_review_only`, `approval_verified`, `activation`, or any candidate authority flag, `read_drafts` and `_propose` withhold it as `{"state": "INTEGRITY_MISMATCH", "task_key": ...}`.
* **FR-PLAN-03 (Hazard diagnosis, statutory clock, and hold-release refusal)**: `controls.evidence_text`, `workflows` hazard lifecycle methods (`raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, `release_hazard`), and `doc_controls` legal hold methods (`place_legal_hold`, `release_legal_hold`) shall refuse sensor telemetry/signal/rule/schema/draft citations (`SENSOR_REF`), structured sensor payload metadata, sensor/non-manager actors, and tampered stored sensor evidence.
  * Observable acceptance criteria: Attempting to raise a hazard, start or update Awaab's Law / external service clocks, record a repair, release a safety hold (including when stored `receipt_evidence`, `acceptance_evidence`, or `repair_evidence` contains a sensor reference), or place/release a legal hold using sensor signals, readings, drafts, or sensor actors raises `ValueError` or `PermissionError` and leaves case, hazard, clock, hold, and audit state unchanged, while legitimate human-evidenced calls succeed.
* **FR-PLAN-04 (Deterministic ranking isolation and rule allowlist)**: `ranking.rank`, `ranking.reasons`, `ranking.snapshot`, and `ranking.sql_key` shall reject any policy containing a sensor or unknown rule code with `ValueError("Unknown ranking rule: ...")` and produce identical rank order, reason codes, deciding rules, SQL sort keys, and `snapshot_hash` regardless of retained sensor readings, derived signals, declined/insufficient monitoring states, case-local `sensor_review_drafts`, or injected sensor attributes on case records.
  * Observable acceptance criteria: Portfolio ranking and `snapshot_hash` across `Store` and `SqlStore` are byte-identical before and after sensor ingestion, analysis, reproduction, and draft creation, and `ranking.rank`, `ranking.snapshot`, and `ranking.sql_key` raise `ValueError` on sensor rule injection.
* **FR-PLAN-05 (End-to-end `src/core` acceptance test suite)**: `src/core/tests/test_sensor_non_authority.py` shall prove all four limbs of Issue #109's non-authority invariant end-to-end across `sensor_ingest.py`, `sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `Store`, `SqlStore`, `ranking.py`, hazards, statutory clocks, and safety/legal/gate holds.
  * Observable acceptance criteria: Test ownership is locked to canonical target `src/core/tests/test_sensor_non_authority.py` (`0` test removals, at most `12` test methods added, `0` generated targets), covering both semantic end-to-end invariance (`SqlStore` + `Store`) and active fail-closed regression checks.

## Non-Functional Requirements

* **NFR-PLAN-01 (Strict static typing and lint cleanliness)**: All touched typed modules (`sensor_analysis.py`, `sensor_ingest.py`, `sensor_review_draft.py`) and the new test module (`tests/test_sensor_non_authority.py`) satisfy `src/core` strict typing and formatting rules without weakening `src/core/pyproject.toml` lint or type gates.
  * Objective threshold or evaluation condition: Zero errors from `mypy`, `ruff check`, and `ruff format --check` in `src/core`.
  * Operating condition or verification approach: Run `mypy`, `ruff check`, and `ruff format --check` from `src/core`.
  * Observable acceptance criteria: Commands exit `0` with zero diagnostics, and legacy migrated files retain surgical diffs compatible with `ruff check`.
* **NFR-PLAN-02 (Deterministic offline execution)**: The new acceptance suite runs reproducibly offline using synthetic fixtures (`dataset.DATA`, `sensor_consumer_fixture`, `sensor_scenarios`) and temporary SQLite/JSON stores with zero network, wall-clock flakiness, or external service dependencies.
  * Objective threshold or evaluation condition: `100%` pass rate across `python3 -m unittest discover -s tests -q` in `src/core`.
  * Operating condition or verification approach: Fixed UTC timestamps, deterministic RNG seeds, and isolated `tempfile.TemporaryDirectory` instances cleaned up automatically.
  * Observable acceptance criteria: Full `src/core` unittest discovery passes cleanly with zero skipped-for-error or flaky tests.

## Acceptance Criteria

* `Signal`, `ReviewTaskCandidate`, and `WindowReceipt` enforce strict non-authority flags at construction/replacement time, and `enforce_sensor_non_authority` rejects authority-claiming objects and serialized mappings with `ValueError`.
* `sensor_review_draft` validates non-authority before persistence and withholds any stored draft with tampered or digest-recomputed authority flags as `INTEGRITY_MISMATCH`.
* `controls.evidence_text`, `workflows` hazard/clock/repair/release operations, and `doc_controls` legal hold operations deterministically refuse sensor telemetry/signal/rule/schema/draft references, structured sensor metadata, tampered stored sensor evidence, and non-manager/sensor actors without affecting human-evidenced workflows.
* `ranking.rank`, `ranking.reasons`, `ranking.snapshot`, `ranking.sql_key`, and `store._ranking()` produce identical outputs and `snapshot_hash` across normal, extreme, faulty, weather-sim, stale, insufficient, and declined sensor activity and unapproved review drafts, and uniformly raise `ValueError` on sensor ranking rules.
* `src/core/tests/test_sensor_non_authority.py` passes alongside the full `src/core` unit test suite, `mypy`, `ruff check`, and `ruff format --check`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md                                                                      |
| Phase details                    | .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md                                                           |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/sensor-non-authority-109-plan-critique.md (`Complete`, verdict `Revise`; `PC-001`..`PC-004` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/sensor-non-authority-109-research.md                                                               |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Ready for implementation after one-pass critique revision                                                                                |
| Continuation context             | Confirmed automatic RPI Agent parent applied compatible critique dispositions and advances directly to `rpi-implement`                   |

## Sources

* .copilot-tracking/research/2026-11-15/sensor-non-authority-109-research.md: Cycle 1 codebase and requirements synthesis (`C1` through `C18`) and convergence selection (Option A).
* docs/brds/agentic-retrofit-programme-brd.md: FR-048 and RULE-014 business rules forbidding sensor signals or absence of alerts from diagnosing hazards, starting clocks, releasing holds, or changing ranking.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: FR-050 and AC-066..AC-068 product requirements and acceptance criteria for simulated IoT Hub ingestion and deterministic review signals.
* docs/adrs/0002-pilot-readiness-architecture.md and docs/adrs/0003-journey-derived-capabilities-runtime-fit.md: Architectural separation between telemetry retention / review proposals and statutory clocks, hazards, holds, and ranking.
* src/core/src/zava_forward/core/sensor_ingest.py, src/core/src/zava_forward/core/sensor_analysis.py, src/core/src/zava_forward/core/sensor_review_draft.py, src/core/src/zava_forward/core/controls.py, src/core/src/zava_forward/core/workflows.py, src/core/src/zava_forward/core/doc_controls.py, src/core/src/zava_forward/core/ranking.py: Production target modules in `src/core`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Enforce sensor pipeline value, ingestion, and review-draft non-authority invariants

* Intent: Guarantee at the sensor domain boundary (`sensor_analysis.py`, `sensor_ingest.py`, `sensor_review_draft.py`) that no ingestion receipt, continuity report, derived signal, review-task candidate, or stored review draft can represent or project authority over hazards, clocks, holds, resident reports, or ranking.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add constructor and payload non-authority invariant enforcement in `sensor_analysis.py` and `sensor_ingest.py`

* Requirement and evidence: FR-PLAN-01, NFR-PLAN-01 (`C5`, `C7`, `C8`)
* Expected result: `Signal.__post_init__`, `ReviewTaskCandidate.__post_init__`, `enforce_sensor_non_authority`, and `WindowReceipt.__post_init__` enforce strict boolean/string non-authority invariants (`ValueError("SENSOR_NON_AUTHORITY_VIOLATION")` on violation), `review_task_candidate` validates incoming `Signal`, and `handover_continuity` records explicit `False` non-authority flags while keeping existing positional construction and equality intact.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce non-authority checks on draft proposal and stored draft read projection in `sensor_review_draft.py`

* Requirement and evidence: FR-PLAN-02, NFR-PLAN-01 (`C10`, `C17`)
* Expected result: `_propose` verifies `enforce_sensor_non_authority` on both `Signal` and `ReviewTaskCandidate` before persistence, and `_view` withholds any stored draft whose envelope or candidate authority flags violate non-authority invariants (even with a recomputed `draft_digest`) as `INTEGRITY_MISMATCH`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Enforce active sensor non-authority refusal across hazard, clock, hold, and ranking surfaces

* Intent: Close authority-surface entrypoints (`controls.py`, `workflows.py`, `doc_controls.py`, `ranking.py`) so sensor readings, signals, absence-of-alert outcomes, review drafts, sensor actors, and sensor ranking rules are actively refused before mutating hazards, statutory clocks, holds, or deterministic home ranking.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Refuse sensor artefact citations, sensor metadata smuggling, and tampered stored sensor evidence in `controls.py`, `workflows.py`, and `doc_controls.py`

* Requirement and evidence: FR-PLAN-03 (`C1`, `C2`, `C11`, `C12`, `C13`, `C14`)
* Expected result: `controls.is_sensor_reference` and `controls.evidence_text` refuse exact sensor telemetry/signal/rule/schema/draft tokens (`SENSOR_REFUSAL`); `workflows` hazard/clock/repair/release methods reject sensor payload keys/objects, sensor `note`/`job` citations, sensor-tagged `user` actors, and tampered stored `source`, `note`, `sent_evidence`, `receipt_evidence`, `acceptance_evidence`, and `repair_evidence` before hold release; `doc_controls.place_legal_hold` and `release_legal_hold` reject sensor references, tampered stored legal-hold references, and sensor/non-manager actors.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Align unknown and sensor ranking rule refusal in `ranking.py`

* Requirement and evidence: FR-PLAN-04 (`C15`)
* Expected result: `ranking.sql_key` validates rule codes against the 5-rule allowlist (`safety_open`, `support`, `waiting_days`, `stage_order`, `case_id`) and raises `ValueError("Unknown ranking rule: ...")` identically to `ranking._rule_keys`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Deliver end-to-end `src/core` sensor non-authority acceptance suite and Focused validation

* Intent: Prove Issue #109's core engineering criterion end-to-end in `src/core/tests/test_sensor_non_authority.py` across `SqlStore` and `Store`, then verify all `src/core` unit tests, `mypy`, and `ruff` checks pass.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Implement `src/core/tests/test_sensor_non_authority.py` end-to-end acceptance and invariant test suite

* Requirement and evidence: FR-PLAN-01..FR-PLAN-05, NFR-PLAN-01, NFR-PLAN-02 (`C1`..`C18`)
* Expected result: Canonical test module `src/core/tests/test_sensor_non_authority.py` (`0` removals, `<= 12` test methods, `0` generated files) proves across `sensor_ingest.py`, `sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `Store`, `SqlStore`, `ranking.py`, hazards, statutory clocks, and safety/legal/gate holds that neither passive telemetry/signal/draft processing nor active authority-crossing attempts can diagnose a hazard, start a clock, release a hold/blocker, or alter deterministic home ranking.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Run Focused tier validation (`unittest`, `mypy`, `ruff`) in `src/core` and record implementation evidence

* Requirement and evidence: NFR-PLAN-01, NFR-PLAN-02 (`C16`)
* Expected result: `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_sensor*.py" -q`, full `src/core` `unittest`, `mypy`, `ruff check .`, `ruff format --check .`, and `python3 tools/rename-zava-tests.py` all exit `0` (without running `tools/rpi-checks.py`), with results recorded in `.copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md

## Dependencies

* Existing `src/core` editable install and dev tools (`unittest`, `mypy==2.4.0`, `ruff==0.17.1`): Required to execute Focused tier checks cleanly in `src/core`.
* Shared test fixtures in `src/core/tests/` (`dataset.py`, `sensor_consumer_fixture.py`, `zava_forward.core.synthetic.sensor_scenarios`): Reused by `src/core/tests/test_sensor_non_authority.py` for deterministic synthetic telemetry and case state.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High] (`mypy --strict` untyped legacy constructor/function calls in `test_sensor_non_authority.py`) | Applied | Updated `P03-T01` to bind unannotated `Store`, `SqlStore`, `ranking.*`, and `gates.*` callables via `typing.cast` to typed `Callable`/`Protocol` signatures so `mypy` (`strict = true`) passes without `pyproject.toml` edits |
| `PC-002` [High] (`workflows` `note`/`job`/`user`/stored `source`+`sent_evidence` and keyword-only `WindowReceipt` fields) | Applied | Updated `P01-T01` to use keyword-only (`*`) non-authority defaults on `WindowReceipt` and `P02-T01` to guard `user`, recursive `metadata`, `note`, `job`, stored `source`/`note`/`sent_evidence`, and stored `legal_hold["reference"]` |
| `PC-003` [Medium] (`sensor_review_draft._view` unknown-key stripping compatibility) | Applied | Updated `P01-T01` and `P01-T02` so mapping validation checks exact authority/envelope invariants without rejecting extra PII keys stripped by `_VIEW_CANDIDATE` |
| `PC-004` [Low] (Branch `feat/iot-109-sensor-non-authority` and `python3 tools/rename-zava-tests.py`) | Applied | Aligned branch name to `feat/iot-109-sensor-non-authority` and added `python3 tools/rename-zava-tests.py` to `P03-T02` Focused validation |
| Residual risk (live cloud IoT Hub / Azure SQL persistence drill) | Accepted | Explicitly out of scope for this offline `src/core` slice; tracked under Epic #109 / Issue #440 |

## Follow-Up Items

* Live Azure IoT Hub and Azure SQL restart/persistence stabilization drill (`AC-066` / Issue #440 under Epic #109): Outside this focused offline `src/core` slice; remains owned by Epic #109 cloud stabilization work.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` implemented and validated; ready for `rpi-review`)
* Remaining provisional question or blocker: None
