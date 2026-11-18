---
title: "RPI Changes: Deterministic Versioned Sensor Analysis and Review Task"
description: "Implementation evidence record for Issue #111 in src/core"
ms.date: 2026-11-14
---

## Metadata

* Task ID: 111-sensor-reproducibility-2142
* Related plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: All planned pure, SQL-retained, test, documentation, and bare verification deliverables in `src/core` completed with zero errors.

## Execution Summary

Delivered deterministic versioned sensor analysis, `SENSOR_REVIEW_DUE` human review task candidate reproduction, and explicit `VersionProvenance` across `zava_forward.core.sensor_analysis` and `zava_forward.core.sensor_analysis_store`, backed by per-row bound canonical input digests, approval-gated provenance metadata, strict `TypedDict` typing, component documentation in `src/core/README.md`, and 291 passing sensor unit tests.

## Completed Work

### Pure `VersionProvenance`, Bound Digests, and Reproduction Helpers (`sensor_analysis.py`)

* Related phase or task: `P01-T01`
* Files: `src/core/src/zava_forward/core/sensor_analysis.py`
* What changed and why:
  * Added `COMPARATOR_VERSION` (`"sensor-comparator-exercise-v1"`), `SCHEMA_VERSION` (`"sensor-fault-input-v1"`), frozen `VersionProvenance`, `TypedDict` payloads (`ProvenanceDict`, `SignalDict`, `ReviewTaskDict`, `ReproducedReviewTask`, `ReproducedSensorAnalysis`), `policy_digest`, `output_digest`, `version_provenance`, and `format_reproduced_review_task`.
  * Replaced independent `reading_tuples` + `_quality_tuples` hashing inside `_digest` with per-row bound canonical tuples (`_row_digest_tuples` + `_schema_marker` using `isinstance(v, str)`) while retaining public `reading_tuples` unchanged, closing `reading_id`, row-schema, and duplicate-timestamp cross-row swap collisions.
  * Updated `review_task_candidate` and `version_provenance` to verify `analysis_version`, `policy_version`, and `threshold_label` consistency and to mask `approver_role` and `approval_reference` to `None` unless `policy.rule_approved` is `True`.
  * Hardened `_home_and_window` to reject missing, non-string, whitespace-padded, mixed, or conflicting `home_id` values with `SINGLE_HOME_REQUIRED` while allowing empty retained reading slices when explicit `home_id` and `window` are provided.
  * Enriched `reproduce_sensor_analysis` (`output_digest`, `provenance`, `review_task`, optional `home_id`) to preserve backwards compatibility with `src/api` while maintaining exact parity with `reproduce_review_task`.
* Completion evidence: `src/core/src/zava_forward/core/sensor_analysis.py`
* Validation: Passed (`mypy`, `ruff check`, `ruff format --check`, `test_sensor_analysis.py`, `src/api/tests/test_sensor_analysis_reproducibility.py`).

### Read-Only Retained-Store Reproduction (`sensor_analysis_store.py`)

* Related phase or task: `P01-T02`
* Files: `src/core/src/zava_forward/core/sensor_analysis_store.py`
* What changed and why: Added `reproduce_retained(consumer, home_id, window, as_of, policy=None)` validating policy up front, running read-only `analyse_retained`, deriving `review_task_candidate` and `version_provenance`, and failing closed to `INSUFFICIENT` (`priority_effect="NONE"`, `review_task=None`) across declined/unknown consent, missing/stale windows, weather-only rows, and unreadable stores without mutating SQL tables.
* Completion evidence: `src/core/src/zava_forward/core/sensor_analysis_store.py`
* Validation: Passed (`test_sensor_analysis_store.py`, `test_sensor_analysis_reproducibility.py`).

### Focused Reproducibility, Collision, and Subprocess Tests (`src/core/tests/`)

* Related phase or task: `P02-T01`
* Files: `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_reproducibility.py`
* What changed and why: Expanded `test_reproduce_review_task_is_deterministic_with_version_provenance` (zero `# type: ignore` suppressions) and added 4 focused test methods (`test_reproduce_handles_empty_window_and_rejects_missing_or_mixed_home`, `test_digest_detects_reading_id_schema_shape_and_cross_row_swaps`, `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only`, and `test_reproduce_retained_and_pure_match_across_batches_and_fresh_processes`) while preserving all existing test names and assertions (including `test_sensor_review_draft.py`).
* Completion evidence: `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_reproducibility.py`
* Validation: Passed (291 tests run in `src/core/tests/test_*sensor*.py`, 0 failures, 34 live-MSSQL tests skipped).

### Component Documentation and Bare Isolated Verification (`src/core/README.md`)

* Related phase or task: `P02-T02`
* Files: `src/core/README.md`
* What changed and why: Updated `### Versioned sensor analysis slice (111)` in `src/core/README.md` to document `VersionProvenance`, `version_provenance`, `reproduce_review_task`, `reproduce_sensor_analysis`, and window-bounded `sensor_analysis_store.reproduce_retained`, keeping explicit exercise-value, non-authority, and open R1-R3 boundaries. Executed the exact bare verification command inside cleaned worktree-local `.venv-verify-111` and removed `.venv-verify-111`.
* Completion evidence: `src/core/README.md`
* Validation: Passed (`mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*sensor*.py' -v`, and downstream `src/api/tests/test_sensor_analysis_reproducibility.py` + `test_sensor_non_authority_boundary.py`).

## Implementation-Time Plan and Detail Updates

None. Implementation matched the post-critique plan (`PC-001`..`PC-004`).

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| `python3 -m mypy` | `src/core` (316 source files, strict) | Passed | `Success: no issues found in 316 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (263 files) | Passed | `263 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*sensor*.py' -v` | `src/core/tests` | Passed | `Ran 291 tests in 138.952s — OK (skipped=34)` (34 skipped require live SQL Server `ZF_SENSOR_MSSQL=1`) |
| `python3 -m unittest tests/test_sensor_analysis_reproducibility.py tests/test_sensor_non_authority_boundary.py -q` | `src/api/tests` downstream compatibility | Passed | `Ran 10 tests in 12.318s — OK` |
| `tools/rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1` + hosted CI | Full SQL publication tier (`src/README.md`) | Skipped | Caller explicitly forbade `git push`; local SQL Server and PR publication gates remain required follow-ups prior to PR publication/merge |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all checked and marked `complete`)
* Completed-work evidence and handoff prose: current
* Validation, blockers, remaining work, and follow-up items: current
* Review readiness: ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None within declared scope.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md, `## Follow-Up Items`
* Run the complete external gate (`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>` including local SQL Server `ZF_SENSOR_MSSQL=1`) and hosted CI when pushing/opening a PR, as required by `src/README.md` for `sensor_analysis.py`.
* Complete analytics research phases R1 to R3 in `docs/reference/research/iot-sensor-analytics-research-plan.md` before using or approving any derived sensor measure beyond a labelled exercise rule.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining `none`
* Validation coverage: `mypy` (316 files), `ruff check`, `ruff format --check` (263 files), `src/core` sensor unit tests (291 run, 34 MSSQL skipped, 0 failed), and `src/api` sensor reproducibility/non-authority tests (10/10 passed)
* Blockers: none
* Current plan and detail updates: none beyond post-critique readiness
* Planning and critique state: ready (`PC-001`..`PC-004` resolved)
* Follow-up items: full SQL publication gate (`rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1` + hosted CI) and R1-R3 research phases
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
