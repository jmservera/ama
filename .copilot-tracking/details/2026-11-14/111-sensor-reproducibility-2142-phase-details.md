---
title: "RPI Phase Details: Deterministic Versioned Sensor Analysis and Review Task"
description: "Phase and task implementation details for Issue #111 in src/core"
ms.date: 2026-11-14
---

## Metadata

* Task ID: 111-sensor-reproducibility-2142
* Task slug: 111-sensor-reproducibility-2142
* Related plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md, docs/adrs/0003-journey-derived-capabilities-runtime-fit.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, src/core/README.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Pure and Retained-Store Versioned Reproduction | complete | P01, P01-T01, P01-T02 |
| P02 | Focused Reproducibility Tests, Documentation, and Verification | complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Pure and Retained-Store Versioned Reproduction

### Context

`src/core/src/zava_forward/core/sensor_analysis.py` already provides `derive_signal`, `reproduce_sensor_analysis`, and `review_task_candidate`, and the working tree holds an uncommitted draft of `_home_and_window` and `reproduce_review_task`. Research (`C2`, `C3`, `C4`, `C5`, `C8`) identified four defects to close while completing explicit version provenance across both pure and SQL-retained entry points:
1. `_quality_tuples` omits `reading_id` and exact `READING_FIELDS` string-schema validity even though `comparator.analyse` branches on duplicate/empty `reading_id` and `SCHEMA_FIELDS`.
2. The uncommitted `reproduce_review_task` draft exposes `approval.approval_reference` in provenance even when `policy.rule_approved` is `False` (for example, mismatched `rule_id` or `policy_version`), and omits `comparator_version`, `schema_version`, `policy_digest`, `output_digest`, `approver_role`, `home_id`, and numeric policy thresholds.
3. `review_task_candidate` checks `signal.policy_version == policy.version` without verifying `signal.analysis_version == ANALYSIS_VERSION`, and `_home_and_window` coerces `None` `home_id` via `str(...)` while rejecting empty reading slices even when `(home_id, window)` are explicitly supplied.
4. `sensor_analysis_store.py` lacks a read-only `reproduce_retained` helper pairing `analyse_retained`, `review_task_candidate`, and `version_provenance`.

### Intent

Deliver complete, collision-free, pure and retained-store deterministic reproduction of sensor signals, `SENSOR_REVIEW_DUE` task candidates, and `VersionProvenance` without altering `Signal` or `ReviewTaskCandidate` serialized fields.

### Boundaries

* Included: `src/core/src/zava_forward/core/sensor_analysis.py` and `src/core/src/zava_forward/core/sensor_analysis_store.py`.
* Excluded: `Signal` and `ReviewTaskCandidate` field changes, `ReviewTaskCandidate.task_key` formula changes, `sensor_review_draft.py`, operational task creation, ranking/hazard/clock/hold paths, and `src/api` route additions.

### Likely Targets

* `src/core/src/zava_forward/core/sensor_analysis.py`: Add `COMPARATOR_VERSION`, `SCHEMA_VERSION`, `VersionProvenance`, `policy_digest`, `output_digest`, `version_provenance`, hardened `_digest` and `_home_and_window`, `analysis_version` check in `review_task_candidate`, enriched `reproduce_sensor_analysis`, and `reproduce_review_task`.
* `src/core/src/zava_forward/core/sensor_analysis_store.py`: Add `reproduce_retained`.

### Dependencies

* None.

### Validation Expectations

* Pure `mypy` and `ruff` checks pass strictly on both modules; existing `sensor_review_draft` and `src/api/tests/test_sensor_analysis_reproducibility.py` expectations remain green.

### Completion Evidence

* Updated `sensor_analysis.py` and `sensor_analysis_store.py` passing strict type-checking and unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add `VersionProvenance`, harden digests and bounds, and complete `reproduce_review_task` in `sensor_analysis.py`

#### Context

`sensor_scenarios.py` defines `METHOD_VERSION = "sensor-comparator-exercise-v1"` and uses `sensor_faults.SCHEMA_VERSION` (`"sensor-fault-input-v1"`) and `sensor_faults.READING_FIELDS` (`C8`). Downstream `sensor_review_draft.py` pins `Signal` and `ReviewTaskCandidate` keys (`C5`), while `src/api/tests/test_sensor_analysis_reproducibility.py` expects `reproduce_sensor_analysis` to return `"analysis_version"`, `"policy_version"`, `"input_digest"`, and `"signal"`.

#### Intent

Provide a canonical frozen `VersionProvenance` dataclass, `TypedDict` payload definitions, and pure helpers so both `reproduce_sensor_analysis` and `reproduce_review_task` carry identical, verifiable version, policy, approval, window, input, and output provenance, with per-row bound collision-free digests and strict input validation.

#### Boundaries

* Included:
  * Export `COMPARATOR_VERSION = comparator.METHOD_VERSION` (`"sensor-comparator-exercise-v1"`) and `SCHEMA_VERSION = sensor_faults.SCHEMA_VERSION` (`"sensor-fault-input-v1"`).
  * Define frozen `VersionProvenance` dataclass (`TypedDict` counterparts `ProvenanceDict`, `SignalDict`, `ReviewTaskDict`, `ReproducedReviewTask`, `ReproducedSensorAnalysis`) with fields: `home_id`, `analysis_version`, `comparator_version`, `schema_version`, `policy_version`, `policy_digest`, `threshold_label`, `humidity_threshold_pct`, `max_staleness_hours`, `rule_id`, `rule_approved`, `approver_role`, `approval_reference`, `window_start`, `window_end`, `as_of`, `input_digest`, `output_digest`.
  * Normalize `humidity_threshold_pct` as `0.0 if val == 0 else float(val)` in `policy_digest` and `VersionProvenance`.
  * Implement `policy_digest(policy: AnalysisPolicy) -> str` (validates policy, hashes canonical JSON of version, normalized `humidity_threshold_pct`, `max_staleness_hours`, `threshold_label`, `rule_approved`, and approved `(rule_id, policy_version, approver_role, approval_reference)` when `rule_approved` is `True`).
  * Implement `output_digest(signal: Signal, candidate: ReviewTaskCandidate | None) -> str` (SHA-256 over canonical sorted JSON of `{"signal": asdict(signal), "review_task": asdict(candidate) if candidate else None}`).
  * Require `signal.analysis_version == ANALYSIS_VERSION`, `signal.policy_version == policy.version`, and `signal.threshold_label == policy.threshold_label` in `review_task_candidate`.
  * Implement `version_provenance(signal: Signal, policy: AnalysisPolicy | None = None, candidate: ReviewTaskCandidate | None | _Unset = _UNSET) -> VersionProvenance`, verifying `signal.analysis_version == ANALYSIS_VERSION`, `signal.policy_version == effective_policy.version`, and `signal.threshold_label == effective_policy.threshold_label`, resolving `expected = review_task_candidate(signal, effective_policy)` when `candidate` is omitted (and raising `ValueError("CANDIDATE_MISMATCH")` if an explicit `candidate != expected` is passed), and setting `approver_role` and `approval_reference` only when `effective_policy.rule_approved` and `effective_policy.approval is not None` (otherwise `None`).
  * Keep `reading_tuples` unchanged for public callers while updating `_digest` to hash sorted per-row bound canonical tuples (`_row_digest_tuples`) binding `(sensor_id, observed_at, reading_id, temperature_c, temperature_unit, humidity_pct, humidity_unit, calibrated, source_type, schema_version, schema_marker)` using `isinstance(v, str)` to match `comparator.analyse`, eliminating cross-row swap collisions on duplicate `(sensor_id, observed_at)`.
  * Update `_home_and_window(retained_readings, window, home_id=None)` to require non-empty unpadded string `home_id` values (`isinstance(raw, str) and bool(raw) and raw == raw.strip()`), reject conflicting/mixed `home_id` with `ValueError("SINGLE_HOME_REQUIRED")`, allow empty `retained_readings` when both valid `home_id` and `window` are supplied, and raise `ValueError("NO_VALID_OBSERVATIONS")` when `window is None` and no valid canonical UTC `observed_at` exists.
  * Update `reproduce_sensor_analysis` (deriving `candidate = review_task_candidate(signal, effective_policy)` and `prov = version_provenance(signal, effective_policy, candidate)`, preserving `analysis_version`, `policy_version`, `input_digest`, `signal`, and adding `review_task`, `output_digest`, and `provenance` plus optional keyword `home_id: str | None = None`) and `reproduce_review_task` (returning `{"provenance": ..., "signal": ..., "review_task": ...}` with optional keyword `home_id: str | None = None`), and extend `as_dict` to accept `VersionProvenance`.
* Excluded: Changing `Signal` or `ReviewTaskCandidate` fields or `task_key` inputs.

#### Likely Targets

* `src/core/src/zava_forward/core/sensor_analysis.py`

#### Dependencies

* `zava_forward.core.synthetic.sensor_scenarios` and `zava_forward.core.synthetic.sensor_faults`.

#### Validation Expectations

* Strict `mypy` passes with zero `# type: ignore` additions in `sensor_analysis.py`; `ruff check` and `ruff format --check` pass.

#### Completion Evidence

* Pure unit tests in `test_sensor_analysis.py` and `src/api/tests/test_sensor_analysis_reproducibility.py` pass.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add read-only `reproduce_retained` in `sensor_analysis_store.py`

#### Context

`sensor_analysis_store.analyse_retained` derives a `Signal` from `SensorConsumer.retained_envelopes` and `SensorConsumer.home_consent`, filtering outdoor `LIVE_VERSIONS` rows (`WEATHER_NOT_INDOOR`) and failing closed to `INSUFFICIENT` (`RETAINED_READINGS_UNAVAILABLE`) on `ConsumerError` (`C4`). Callers reproducing review-task decisions from the SQL store currently have to stitch `analyse_retained`, `review_task_candidate`, and provenance manually.

#### Intent

Expose `reproduce_retained(consumer, home_id, window, as_of, policy=None) -> dict[str, object]` in `sensor_analysis_store.py` returning the exact same `{"provenance", "signal", "review_task"}` structure as `reproduce_review_task`, guaranteed read-only and fail-closed.

#### Boundaries

* Included: Validate `effective_policy = policy or AnalysisPolicy()` up front (`effective_policy.validate()`), call `analyse_retained(consumer, home_id, window, as_of, effective_policy)`, derive `candidate = review_task_candidate(signal, effective_policy)`, construct `prov = version_provenance(signal, effective_policy, candidate)`, and return `{"provenance": as_dict(prov), "signal": as_dict(signal), "review_task": as_dict(candidate) if candidate else None}`.
* Excluded: Any database writes, task persistence, or network/clock access.

#### Likely Targets

* `src/core/src/zava_forward/core/sensor_analysis_store.py`

#### Dependencies

* P01-T01 (`sensor_analysis.py`).

#### Validation Expectations

* `reproduce_retained` leaves SQLite tables byte-identical before and after execution, matches pure `reproduce_review_task` over window-bounded retained indoor rows (`consumer.observed_series([home_id], {home_id: (first, last)})`), and returns `review_task=None` with complete `provenance` on all fail-closed paths.

#### Completion Evidence

* Retained-store and subprocess reproducibility tests pass in `test_sensor_analysis_store.py` and `test_sensor_analysis_reproducibility.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Reproducibility Tests, Documentation, and Verification

### Context

Test ownership is locked before critique:
* Canonical test targets: `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_reproducibility.py`.
* Generated targets: `none`.
* Exact test removals: `none` (0 existing tests removed or weakened).
* Maximum test additions: at most 7 focused test methods total across the 3 existing files, covering semantic provenance, contrarian collision/gating regressions, and cross-process retained-store parity.

### Intent

Verify every new behavior and contrarian edge case with focused, non-redundant tests, update `src/core/README.md`, execute the exact bare verification suite in a cleaned worktree-local venv (`.venv-verify-111`) without touching shared `~/.local` or `/tmp`, and commit cleanly on `feat/iot-111-sensor-reproducibility-2142` without pushing.

### Boundaries

* Included: `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_reproducibility.py`, `src/core/README.md`, and the four `.copilot-tracking/` artifacts.
* Excluded: Unrelated test modules, `docs/` problem-specification edits (no architecture or requirement change), shared `~/.local` site-packages mutation, `/tmp` writes, and `git push`.

### Likely Targets

* `src/core/tests/test_sensor_analysis.py`
* `src/core/tests/test_sensor_analysis_store.py`
* `src/core/tests/test_sensor_analysis_reproducibility.py`
* `src/core/README.md`

### Dependencies

* P01.

### Validation Expectations

* Inside a cleaned worktree-local venv (`.venv-verify-111` exposing `mypy` and `ruff` and installing `--no-build-isolation --no-deps -e src/core`), run:
  `cd /home/azureuser/source/ama-demo-wt/feat-111-sensor-reproducibility-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*sensor*.py' -v`
* Also run `src/api/tests/test_sensor_analysis_reproducibility.py` and `src/api/tests/test_sensor_non_authority_boundary.py` against the worktree to confirm zero regressions in downstream `src/api`.
* Remove `.venv-verify-111` and confirm `git status --short` is empty after committing.

### Completion Evidence

* Recorded command outputs and zero-exit statuses in `.copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-changes.md` and `.copilot-tracking/reviews/2026-11-14/111-sensor-reproducibility-2142-review.md`, plus clean `git status --short` and commit SHA.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Expand focused sensor reproducibility and provenance tests in `src/core/tests/`

#### Context

Existing tests cover scenario outcomes, order-independent `Signal.input_digest`, basic SQLite retained `Signal` derivation, and subprocess `Signal` + `ReviewTaskCandidate` rendering. New coverage must prove explicit `VersionProvenance` fields, approval mismatch masking, `reading_id` / schema-shape digest collision resistance, empty-window `home_id` reproduction, stale `analysis_version` candidate rejection, and `sensor_analysis_store.reproduce_retained` parity across permutations, batch sizes, and fresh processes.

#### Intent

Add focused semantic and edge-case tests without restating implementation constants or duplicating existing cases.

#### Boundaries

* Included:
  * `test_sensor_analysis.py`:
    1. `test_reproduce_review_task_is_deterministic_with_version_provenance` (expanded from working-tree draft without `# type: ignore`: verifies permutation invariance, `reproduce_sensor_analysis` parity on `provenance` / `signal` / `review_task` / `output_digest`, `VersionProvenance` fields including `comparator_version="sensor-comparator-exercise-v1"` and `schema_version="sensor-fault-input-v1"`, unapproved and mismatched-`RuleApproval` masking of `approval_reference`/`approver_role` to `None`, policy threshold change shifting `policy_digest` + `output_digest` while preserving `input_digest`, and absence of raw readings/sensor IDs in provenance).
    2. `test_reproduce_handles_empty_window_and_rejects_missing_or_mixed_home` (verifies empty `retained_readings` with explicit `home_id` and `window` reproduces `STALE`/`INSUFFICIENT` `NO_READINGS_IN_WINDOW` and `review_task=None`, while missing/None/whitespace-padded/mixed `home_id` raises `SINGLE_HOME_REQUIRED` and mismatched `Signal.analysis_version` or `threshold_label` returns `None` from `review_task_candidate`).
    3. Keep existing `test_digest_changes_with_calibration_flag` intact and add `test_digest_detects_reading_id_schema_shape_and_cross_row_swaps` (verifies `reading_id` duplication/mutation, missing/extra/non-string row fields, and duplicate-timestamp cross-row metric/quality swaps each change `input_digest`).
  * `test_sensor_analysis_store.py`:
    4. `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` (verifies `store.reproduce_retained` with `APPROVED` and default policy matches `sa.reproduce_review_task` over window-bounded `observed_series([HOME], {HOME: (first, last)})`, writes nothing to SQLite, and returns `review_task=None` with valid `provenance` on declined consent, weather-only rows, and unreadable store).
  * `test_sensor_analysis_reproducibility.py`:
    5. Update `FRESH` and add `test_reproduce_retained_and_pure_match_across_batches_and_fresh_processes` (verifies `sas.reproduce_retained` equals `sa.reproduce_review_task(consumer.observed_series([HOME], {HOME: (first, last)}), ...)` across batch sizes 37 and 100 and across subprocesses with `PYTHONHASHSEED` in `("0", "1", "random")`).
* Excluded: Removing or renaming any existing test; adding trivial getter/constant tests.

#### Likely Targets

* `src/core/tests/test_sensor_analysis.py`
* `src/core/tests/test_sensor_analysis_store.py`
* `src/core/tests/test_sensor_analysis_reproducibility.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* All `test_*sensor*.py` tests pass with zero `mypy` or `ruff` errors.

#### Completion Evidence

* Passing verbose test run covering all new and existing sensor tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update `src/core/README.md` and run isolated bare verification gates

#### Context

`src/core/README.md` (`### Versioned sensor analysis slice (111)`) documents `sensor_analysis` and `sensor_analysis_store`. Repository rules require updating directly related documentation and verifying Markdown/diff cleanliness alongside executable checks.

#### Intent

Document `VersionProvenance`, `reproduce_sensor_analysis`, `reproduce_review_task`, and window-bounded `sensor_analysis_store.reproduce_retained` concisely in `src/core/README.md` (preserving existing exercise-value and non-authority disclaimers), run all required checks in a cleaned worktree-local `.venv-verify-111`, and commit cleanly after review reconciliation.

#### Boundaries

* Included: `src/core/README.md` (`### Versioned sensor analysis slice (111)`), worktree-local `.venv-verify-111` verification, cleanup of `.venv-verify-111`.
* Excluded: Claiming R1-R3 completion, full external SQL receipt, or hosted CI execution.

#### Likely Targets

* `src/core/README.md`

#### Dependencies

* P01, P02-T01.

#### Validation Expectations

* Exact command `cd /home/azureuser/source/ama-demo-wt/feat-111-sensor-reproducibility-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*sensor*.py' -v` succeeds with 0 failures and 0 errors when `PATH` activates `.venv-verify-111` for this worktree.

#### Completion Evidence

* Clean `mypy`, `ruff check`, `ruff format --check`, and `200+` passing `test_*sensor*.py` tests recorded in the changes artifact.

#### Unresolved Items

* None.
