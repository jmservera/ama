<!-- markdownlint-disable-file -->
# RPI Phase Details: Sensor Non-Authority Invariant Enforcement and Acceptance Suite

## Metadata

* Task ID: issue-109-sensor-non-authority
* Task slug: sensor-non-authority-109
* Related plan: .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/sensor-non-authority-109-research.md, docs/brds/agentic-retrofit-programme-brd.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0002-pilot-readiness-architecture.md, docs/adrs/0003-journey-derived-capabilities-runtime-fit.md

## Phase Index

| Phase ID | Name                                                                                       | Status  | Detail sections          |
|----------|--------------------------------------------------------------------------------------------|---------|--------------------------|
| P01      | Enforce sensor pipeline value, ingestion, and review-draft non-authority invariants        | Completed | P01, P01-T01, P01-T02    |
| P02      | Enforce active sensor non-authority refusal across hazard, clock, hold, and ranking surfaces | Completed | P02, P02-T01, P02-T02    |
| P03      | Deliver end-to-end `src/core` sensor non-authority acceptance suite and Focused validation | Completed | P03, P03-T01, P03-T02    |

<!-- rpi:phase id=P01 -->
## P01: Enforce sensor pipeline value, ingestion, and review-draft non-authority invariants

### Context

Research findings `C5`, `C7`, `C8`, and `C10` show that `sensor_ingest.py`, `sensor_analysis.py`, and `sensor_review_draft.py` maintain passive non-authority during normal derivation, yet allow `Signal`, `ReviewTaskCandidate`, and `WindowReceipt` instances to be constructed or `dataclasses.replace`-mutated with authority-claiming values, and allow `sensor_review_draft._view` to project stored drafts without re-checking non-authority flags when a digest is recomputed.

### Intent

Enforce fail-closed non-authority invariants on sensor ingestion outputs, deterministic signals, review task candidates, and stored review drafts so no object or serialized payload leaving the sensor modules can represent hazard diagnosis, clock initiation, hold release, resident-report override, or ranking mutation.

### Boundaries

* Included: `src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_ingest.py`, and `src/core/src/zava_forward/core/sensor_review_draft.py`.
* Excluded: Changing SQL table schemas in `sensor_consumer.py` or changing existing analysis thresholds, versions, or digest formulas for valid non-authoritative records.

### Likely Targets

* src/core/src/zava_forward/core/sensor_analysis.py: Add `SENSOR_NON_AUTHORITY_ERROR`, `enforce_sensor_non_authority`, `__post_init__` checks on `Signal` and `ReviewTaskCandidate`, and entry validation in `review_task_candidate`.
* src/core/src/zava_forward/core/sensor_ingest.py: Add defaulted boolean non-authority flags (`diagnoses_hazard`, `starts_clock`, `releases_hold`, `changes_ranking`) with `__post_init__` enforcement on `WindowReceipt` and non-authority metadata fields in `handover_continuity`.
* src/core/src/zava_forward/core/sensor_review_draft.py: Enforce `sa.enforce_sensor_non_authority` in `_propose` and verify stored record envelope and candidate non-authority flags inside `_view`.

### Dependencies

* None

### Validation Expectations

* Existing `test_sensor_analysis.py`, `test_sensor_analysis_store.py`, `test_sensor_analysis_reproducibility.py`, `test_sensor_ingest.py`, and `test_sensor_review_draft.py` continue to pass unchanged, and `mypy`, `ruff check`, and `ruff format --check` pass on all three modules.

### Completion Evidence

* Constructor/replacement attempts setting any authority flag on `Signal`, `ReviewTaskCandidate`, or `WindowReceipt` raise `ValueError("SENSOR_NON_AUTHORITY_VIOLATION")`, and digest-recomputed authority-tampered records in `case["sensor_review_drafts"]` project as `INTEGRITY_MISMATCH`.

### Unresolved Items

* None

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add constructor and payload non-authority invariant enforcement in `sensor_analysis.py` and `sensor_ingest.py`

#### Context

`Signal` and `ReviewTaskCandidate` in `sensor_analysis.py` are frozen dataclasses whose non-authority attributes (`priority_effect="NONE"`, `diagnoses_hazard=False`, `resident_report_unaffected=True`, `changes_ranking=False`, `starts_clock=False`, `releases_hold=False`) can currently be overridden via positional/keyword arguments or `dataclasses.replace`. In `sensor_ingest.py`, `WindowReceipt` is compared via `WindowReceipt()` and `WindowReceipt(accepted, replayed, rejected)` in `test_sensor_ingest.py`.

#### Intent

Reject any `Signal`, `ReviewTaskCandidate`, serialized signal/task mapping, or `WindowReceipt` that deviates from strict non-authority invariants while preserving backward compatibility for all valid callers and existing tests.

#### Boundaries

* Included: `Signal.__post_init__`, `ReviewTaskCandidate.__post_init__`, `enforce_sensor_non_authority(value: object) -> None` (supporting `Signal`, `ReviewTaskCandidate`, `WindowReceipt`, and serialized mappings by checking exact boolean/string authority invariants without rejecting unrelated extra keys stripped by `_VIEW_CANDIDATE`), `review_task_candidate` input check, keyword-only (`*`) `WindowReceipt` defaulted fields + `__post_init__`, and `handover_continuity` non-authority keys (`diagnoses_hazard`, `starts_clock`, `releases_hold`, `changes_ranking` all `False`).
* Excluded: Changing `SignalPayload` / `ReviewTaskPayload` canonical digest inputs in `as_dict` (which must remain byte-compatible with `test_sensor_analysis_reproducibility.py` and `sensor_review_draft._digest`).

#### Likely Targets

* src/core/src/zava_forward/core/sensor_analysis.py: Enforce exact `type(x) is bool` (`False` for authority flags, `True` for `resident_report_unaffected`), `priority_effect == "NONE"`, `task_type == TASK_TYPE`, `queue == TASK_QUEUE`, and `status == "PROPOSED"`.
* src/core/src/zava_forward/core/sensor_ingest.py: Enforce exact `type(x) is bool and x is False` on `WindowReceipt` non-authority fields (`diagnoses_hazard`, `starts_clock`, `releases_hold`, `changes_ranking`) and include those four `False` fields in `handover_continuity` report output.

#### Dependencies

* None

#### Validation Expectations

* Strict `mypy`, `ruff check`, `ruff format --check`, and `unittest` pass for `test_sensor_analysis.py`, `test_sensor_analysis_reproducibility.py`, and `test_sensor_ingest.py`.

#### Completion Evidence

* `Signal`, `ReviewTaskCandidate`, `enforce_sensor_non_authority`, and `WindowReceipt` deterministically raise `ValueError("SENSOR_NON_AUTHORITY_VIOLATION")` for truthy, non-bool (such as `1` or `"false"`), or altered task/status/priority values.

#### Unresolved Items

* None

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce non-authority checks on draft proposal and stored draft read projection in `sensor_review_draft.py`

#### Context

`sensor_review_draft._propose` builds a `ReviewTaskCandidate` and persists an unapproved draft under `case["sensor_review_drafts"]`, while `_view` verifies `record.get("draft_digest") == _digest(record)`. If a stored JSON/SQLite case body were edited directly and `draft_digest` recomputed with `state="APPROVED"`, `activation="ACTIVE"`, `manual_review_only=False`, `approval_verified=True`, or `changes_ranking=True`, `_digest` alone would match.

#### Intent

Enforce `sa.enforce_sensor_non_authority` before writing a draft and verify envelope + candidate non-authority invariants inside `_view` so tampered stored records always fail closed to `INTEGRITY_MISMATCH`.

#### Boundaries

* Included: `_propose` and `_view` (plus helper `_record_non_authoritative(record: Mapping[str, object]) -> bool`) in `src/core/src/zava_forward/core/sensor_review_draft.py`.
* Excluded: Changing valid draft JSON layout, `draft_digest` calculation, role gates (`DRAFT_ROLES`), or default-off `ZF_ENABLE_SENSOR_REVIEW_DRAFTS` behavior.

#### Likely Targets

* src/core/src/zava_forward/core/sensor_review_draft.py: Validate `signal` and `cand` in `_propose`, and check envelope (`state == STATE`, `manual_review_only is True`, `approval_verified is False`, `activation is None`) and candidate non-authority via `sa.enforce_sensor_non_authority` inside `_view` while preserving `_VIEW_CANDIDATE` unknown-key stripping on valid records.

#### Dependencies

* P01-T01

#### Validation Expectations

* `test_sensor_review_draft.py` passes on both JSON `Store` and SQLite `SqlStore`, plus `mypy`, `ruff check`, and `ruff format --check`.

#### Completion Evidence

* Stored draft records with recomputed digests and forged authority fields return `{"state": "INTEGRITY_MISMATCH", "task_key": ...}` on both `_propose` idempotent reopen and `read_drafts`.

#### Unresolved Items

* None

<!-- rpi:phase id=P02 -->
## P02: Enforce active sensor non-authority refusal across hazard, clock, hold, and ranking surfaces

### Context

Research findings `C11` through `C15` show that `controls.evidence_text` already blocks chat memory (`MEMORY_REF`) across hazard diagnosis, statutory clocks, and safety hold release, and `workflows.release_hazard` re-verifies stored `receipt_evidence`, `acceptance_evidence`, and `repair_evidence`. Adding an analogous exact sensor artefact check (`SENSOR_REF`) plus metadata/actor guards in `workflows.py`, `doc_controls.py`, and `ranking.sql_key` actively prevents sensor readings, signals, or drafts from mutating authority state.

### Intent

Actively refuse sensor artefact citations, structured sensor payloads, sensor/non-manager actors, tampered stored sensor evidence, and sensor ranking rules across all hazard, statutory clock, hold, and ranking entrypoints in `src/core`.

### Boundaries

* Included: `src/core/src/zava_forward/core/controls.py`, `src/core/src/zava_forward/core/workflows.py`, `src/core/src/zava_forward/core/doc_controls.py`, and `src/core/src/zava_forward/core/ranking.py`.
* Excluded: Reformatting legacy migrated files listed in `src/core/pyproject.toml` `[tool.ruff.format] exclude`, or blocking ordinary human surveyor prose that does not cite sensor telemetry/signal/rule/schema/draft identifiers.

### Likely Targets

* src/core/src/zava_forward/core/controls.py: Add `SENSOR_REF`, `SENSOR_REFUSAL`, `is_sensor_reference`, and enforce inside `evidence_text`.
* src/core/src/zava_forward/core/workflows.py: Add `_forbid_sensor_authority` on hazard/clock/repair/release inputs and stored-evidence sensor check in `release_hazard`.
* src/core/src/zava_forward/core/doc_controls.py: Reject sensor actors in `_manager` and sensor references in `place_legal_hold`.
* src/core/src/zava_forward/core/ranking.py: Validate unknown rules in `sql_key` to raise `ValueError("Unknown ranking rule: ...")`.

### Dependencies

* P01

### Validation Expectations

* All existing hazard, challenge, suspension, governance, document-control, and ranking tests in `src/core/tests/` pass without regression, and `ruff check` + `mypy` pass cleanly.

### Completion Evidence

* Every direct or stored attempt to use a sensor signal, reading, rule, schema, draft, or sensor rule code to raise a hazard, start/update clocks, release a safety/legal hold, or alter ranking raises `ValueError` or `PermissionError` with zero state change.

### Unresolved Items

* None

<!-- rpi:task id=P02-T01 -->
### P02-T01: Refuse sensor artefact citations, sensor metadata smuggling, and tampered stored sensor evidence in `controls.py`, `workflows.py`, and `doc_controls.py`

#### Context

All 7 hazard/clock/hold-release workflow methods (`raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, `release_hazard`) pass their `source` or `evidence` string through `controls.evidence_text`. In addition, `raise_hazard`, `refer_hazard`, and `observe_hazard_times` accept a `metadata` dict, and `doc_controls.place_legal_hold` / `release_legal_hold` accept `user` and `reference`.

#### Intent

Block sensor telemetry, signals, absence-of-alert (`NO_SIGNAL`), and review drafts from entering hazard diagnosis, Awaab's Law / external service clocks, safety hold release, and legal hold mutations, while preserving 100% of human-evidenced calls.

#### Boundaries

* Included:
  * `controls.py`: `SENSOR_REF` compiled regex matching exact case-insensitive tokens/prefixes (`SENSOR_REVIEW_DUE`, `SENSOR-RH-PERSISTENCE-EXERCISE`, `sensor-analysis-exercise-v\d+`, `sensor-comparator-exercise-v\d+`, `sensor-review-draft-v\d+`, `sensor-fault-input-v\d+`, `sensor-live-weather-sim-v\d+`, `(?:sensor_reading|sensor_signal|sensor_analysis|sensor_review_draft|sensor_candidate|iot-hub):(?=\S)`, and `SENS-(?:SYN|[0-9]{2,})[A-Z0-9-]*` bounded by non-alphanumeric boundaries), `SENSOR_REFUSAL`, `is_sensor_reference(value)`, and refusal in `evidence_text`.
  * `workflows.py`: `_forbid_sensor_authority(*payloads)` recursively rejecting `Signal` / `ReviewTaskCandidate` / `WindowReceipt` instances, forbidden sensor payload keys (`sensor_signal`, `sensor_reading`, `sensor_readings`, `sensor_review_draft`, `sensor_review_drafts`, `sensor_candidate`, `sensor_id`, `reading_id`, or `task_type == "SENSOR_REVIEW_DUE"`), and `controls.is_sensor_reference` strings across `user`, `metadata`, `note`, and `job` in `raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, and `release_hazard`; plus stored-evidence check `if any(controls.is_sensor_reference(h.get(k)) for k in ("source", "note", "sent_evidence", "receipt_evidence", "acceptance_evidence", "repair_evidence")): raise ValueError(controls.SENSOR_REFUSAL)` in `release_hazard`.
  * `doc_controls.py`: Reject `user` mappings carrying `sensor_id`, `reading_id`, sensor `source_type`, or `controls.is_sensor_reference` actor `email`/`name` in `_manager`, reject `controls.is_sensor_reference(reference)` in `place_legal_hold`, and reject stored `controls.is_sensor_reference(c["legal_hold"].get("reference"))` in `release_legal_hold`.
* Excluded: Blocking plain English human prose such as `"Surveyor inspected bedroom wall near sensor casing; damp confirmed visually"`.

#### Likely Targets

* src/core/src/zava_forward/core/controls.py: `SENSOR_REF`, `SENSOR_REFUSAL`, `is_sensor_reference`, `evidence_text`.
* src/core/src/zava_forward/core/workflows.py: `_forbid_sensor_authority`, `raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, `release_hazard`.
* src/core/src/zava_forward/core/doc_controls.py: `_manager`, `place_legal_hold`.

#### Dependencies

* P01-T01

#### Validation Expectations

* `test_hazard_referral.py`, `test_operator_suspension_drill.py`, `test_issue_220_challenge_route.py`, and `test_document_rescan.py` pass unchanged alongside new sensor refusal assertions.

#### Completion Evidence

* Citing sensor tokens or smuggling sensor metadata into hazard/clock/hold operations raises `ValueError` / `PermissionError` before `self.save()` or `self._log(...)` runs, leaving store state, version, and audit count unchanged.

#### Unresolved Items

* None

<!-- rpi:task id=P02-T02 -->
### P02-T02: Align unknown and sensor ranking rule refusal in `ranking.py`

#### Context

`ranking._rule_keys(policy)` validates `unknown = [r["code"] for r in policy["rules"] if r["code"] not in table]` and raises `ValueError(f"Unknown ranking rule: {', '.join(unknown)}")`, whereas `ranking.sql_key(c, policy)` indexes `seg[k]()` directly and raises `KeyError` on an injected sensor rule code.

#### Intent

Ensure `ranking.sql_key` raises the same `ValueError("Unknown ranking rule: ...")` as `ranking.rank` and `ranking.snapshot` whenever a policy includes an unknown or sensor-derived rule code.

#### Boundaries

* Included: `sql_key` in `src/core/src/zava_forward/core/ranking.py`.
* Excluded: Changing sort order, reason codes, tie-breaking, or `snapshot_hash` for valid policies.

#### Likely Targets

* src/core/src/zava_forward/core/ranking.py: Check `unknown = [k for k in codes if k not in seg]` in `sql_key` and raise `ValueError(f"Unknown ranking rule: {', '.join(unknown)}")`.

#### Dependencies

* None

#### Validation Expectations

* `test_priority_order.py`, `test_ranking_publication.py`, `test_ranking_publication_runner.py`, and `test_ranking_tiebreak_audit.py` pass unchanged.

#### Completion Evidence

* `ranking.rank`, `ranking.snapshot`, and `ranking.sql_key` all raise `ValueError("Unknown ranking rule: ...")` when passed a policy with a sensor rule code such as `"sensor_signal"` or `"sensor_humidity"`.

#### Unresolved Items

* None

<!-- rpi:phase id=P03 -->
## P03: Deliver end-to-end `src/core` sensor non-authority acceptance suite and Focused validation

### Context

Research findings `C17` and `C18` confirm `src/core/tests/` has unit tests for individual sensor helpers (`test_sensor_ingest.py`, `test_sensor_analysis.py`, `test_sensor_analysis_store.py`, `test_sensor_review_draft.py`) while `src/api/tests/test_sensor_non_authority_boundary.py` lives in `src/api`. `src/core` needs a self-contained, strictly typed acceptance and invariant test suite proving Issue #109's core engineering criterion across all `src/core` ingestion, analysis, draft, hazard, clock, hold, gate, and ranking surfaces.

### Intent

Author `src/core/tests/test_sensor_non_authority.py` under locked test-ownership bounds and execute Focused validation (`unittest`, `mypy`, `ruff check`, `ruff format --check`) in `src/core`.

### Boundaries

* Included:
  * Canonical test target: `src/core/tests/test_sensor_non_authority.py`
  * Exact test removals: `none`
  * Maximum test additions: `<= 12` test methods in `src/core/tests/test_sensor_non_authority.py`
  * Generated targets: `none`
  * Semantic vs regression coverage: Semantic end-to-end workflow proof across `SqlStore` and in-memory `Store` (proving `sensor_ingest.ingest_window` + `handover_continuity` + `sensor_analysis` + `sensor_analysis_store` + `sensor_review_draft` leave hazards, Awaab's Law / external service clocks, safety holds, legal holds, booking/safety gates, and portfolio ranking untouched across normal, adverse, faulty/schema-smuggled, weather-sim, stale, insufficient, and declined series) paired with targeted fail-closed invariant regression tests for `Signal`/`ReviewTaskCandidate`/`WindowReceipt` construction, tampered stored drafts, sensor citation/metadata refusal on `workflows`/`controls`/`doc_controls`, and sensor rule refusal on `ranking`.
* Excluded: Running `tools/rpi-checks.py`, modifying `src/api/tests/`, or editing `src/core/pyproject.toml` (bind untyped `Store`, `SqlStore`, `ranking.*`, and `gates.*` constructors and functions via `typing.cast` to typed `Callable` / `Protocol` signatures so `mypy --strict` passes natively).

### Likely Targets

* src/core/tests/test_sensor_non_authority.py: New end-to-end invariant and acceptance suite.
* .copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md: Implementation and Focused validation evidence record (created during `rpi-implement`).

### Dependencies

* P01, P02

### Validation Expectations

* From repository root / `src/core`:
  * `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_sensor*.py" -q`
  * `cd src/core && python3 -m unittest discover -s tests -q`
  * `cd src/core && /home/azureuser/.local/bin/ruff check . && /home/azureuser/.local/bin/ruff format --check . && /home/azureuser/.local/bin/mypy`
  * `python3 tools/rename-zava-tests.py`

### Completion Evidence

* All four Focused validation commands exit `0` in `src/core`, proving both new acceptance cases and zero regressions across existing `src/core` suites.

### Unresolved Items

* None

<!-- rpi:task id=P03-T01 -->
### P03-T01: Implement `src/core/tests/test_sensor_non_authority.py` end-to-end acceptance and invariant test suite

#### Context

Issue #109 requires proving across `sensor_ingest.py`, `sensor_analysis.py`, and store/ranking/hazard/hold surfaces that no sensor reading or derived sensor signal can diagnose a hazard, start an Awaab's Law or statutory clock, release a hold/blocker, or alter deterministic home ranking.

#### Intent

Create a concise, high-signal acceptance suite (`<= 12` test methods) in `src/core/tests/test_sensor_non_authority.py` typed cleanly with `Callable` / `Protocol` `cast(...)` bindings over legacy untyped entrypoints so `mypy` (`strict = true`), `ruff check`, and `ruff format --check` pass without `pyproject.toml` edits.

#### Boundaries

* Included:
  1. End-to-end `SqlStore` + `SensorConsumer` + `sensor_ingest.ingest_window` + `handover_continuity` + `sensor_analysis_store.analyse_retained`/`reproduce_retained` + `sensor_analysis.derive_signal`/`review_task_candidate` across adverse (`100% RH`, overnight peaks), normal (`NO_SIGNAL`, proving RULE-014 absence-of-alert non-clearance), live weather-sim, stale/missing, declined-consent, and schema-smuggled authority-field observations — verifying zero hazard creation, unchanged statutory clocks (`aware_at`, `response_due_at`, `resident_update_due_at`, `responded_at`), active safety/legal holds and `safety_release_gate`/`booking_gates` blockers, and byte-identical `ranking.rank`, `ranking.sql_key`, `ranking.snapshot` (`snapshot_hash`), and `store._ranking()`.
  2. Case-local `sensor_review_draft` creation (`_record_draft_synthetic` and default-refused `draft_from_retained`) on `SqlStore` and JSON `Store`, proving drafts stay `PROPOSED_UNAPPROVED`, never diagnose hazards, start clocks, release holds, or alter ranking/`snapshot_hash`, and that digest-recomputed authority-tampered stored drafts fail closed as `INTEGRITY_MISMATCH`.
  3. Value-object invariant enforcement tests proving `Signal`, `ReviewTaskCandidate`, `enforce_sensor_non_authority`, and `WindowReceipt` reject any truthy, non-boolean, or altered authority/status/queue/priority flag with `ValueError("SENSOR_NON_AUTHORITY_VIOLATION")`.
  4. Active authority-surface refusal tests across both `SqlStore` and JSON `Store` proving `raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, `release_hazard` (including tampered stored `repair_evidence` / `acceptance_evidence` / `receipt_evidence`), and `place_legal_hold` / `release_legal_hold` reject sensor citations, structured sensor metadata, and sensor actors with zero state/version/audit mutation, while legitimate human surveyor prose mentioning room hardware succeeds.
  5. Deterministic ranking invariance and rule-refusal tests on `Store` and `SqlStore` proving declined/insufficient/stale/adverse signals and injected case sensor keys never change rank order, `reasons()`, `sql_key()`, or `snapshot_hash`, and `ranking.rank`, `ranking.snapshot`, and `ranking.sql_key` reject sensor rule codes with `ValueError`.
* Excluded: Duplicate unit tests of sensor physics or HTTP transport already covered elsewhere.

#### Likely Targets

* src/core/tests/test_sensor_non_authority.py: New acceptance and invariant test module.

#### Dependencies

* P01-T01, P01-T02, P02-T01, P02-T02

#### Validation Expectations

* `python3 -m unittest discover -s tests -p "test_sensor_non_authority.py" -v` passes with zero warnings or errors.

#### Completion Evidence

* Every sub-clause of Issue #109's non-authority criterion has both an end-to-end positive non-mutation assertion and an active fail-closed negative assertion that would fail without the `P01`/`P02` guards.

#### Unresolved Items

* None

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run Focused tier validation (`unittest`, `mypy`, `ruff`) in `src/core` and record implementation evidence

#### Context

Repository instructions and the user prompt specify Focused tier validation in `src/core` (`unittest`, `mypy`, `ruff check`, `ruff format --check`) and explicitly forbid running `tools/rpi-checks.py`.

#### Intent

Verify full `src/core` regression safety, strict typing, lint, and formatting compliance and record exact command outcomes in `.copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md`.

#### Boundaries

* Included: Running `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_sensor*.py" -q`, `cd src/core && python3 -m unittest discover -s tests -q`, `cd src/core && /home/azureuser/.local/bin/ruff check . && /home/azureuser/.local/bin/ruff format --check . && /home/azureuser/.local/bin/mypy`, and `python3 tools/rename-zava-tests.py` on branch `feat/iot-109-sensor-non-authority`.
* Excluded: `tools/rpi-checks.py` and `git push`.

#### Likely Targets

* .copilot-tracking/changes/2026-11-15/sensor-non-authority-109-changes.md: Record files changed, plan task markers reconciled, and Focused validation receipts during `rpi-implement`.

#### Dependencies

* P03-T01

#### Validation Expectations

* Zero test failures, zero `mypy` errors, zero `ruff check` violations, and zero `ruff format --check` diffs in `src/core`.

#### Completion Evidence

* Recorded command outputs and reconciled `[x]` task checkboxes across plan, phase details, and changes artifacts.

#### Unresolved Items

* None
