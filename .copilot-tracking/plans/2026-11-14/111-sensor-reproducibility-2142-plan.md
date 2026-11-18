---
title: "RPI Plan: Deterministic Versioned Sensor Analysis and Review Task"
description: "Implementation plan for deterministic versioned sensor analysis, SENSOR_REVIEW_DUE task generation, and explicit version provenance from retained readings in src/core (Refs #111)"
ms.date: 2026-11-14
---

## Task Metadata

* Task ID: 111-sensor-reproducibility-2142
* Task slug: 111-sensor-reproducibility-2142
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-critique.md

## Executive Summary

This plan delivers the locally verifiable reproducibility and provenance capabilities for Issue #111 in `src/core`: deterministic re-derivation of versioned sensor signals and `SENSOR_REVIEW_DUE` human review task candidates from retained readings alone, paired with an explicit `VersionProvenance` record across both the pure calculation layer (`zava_forward.core.sensor_analysis`) and the SQL retained-store adapter (`zava_forward.core.sensor_analysis_store`).

### User Decisions and Requirements Highlights

* Deliver deterministic versioned sensor analysis and `SENSOR_REVIEW_DUE` review task generation with explicit version provenance from retained readings in `src/core` on branch `feat/iot-111-sensor-reproducibility-2142`, preserving existing uncommitted worktree progress while hardening its edge cases.
* Keep every threshold labelled as an exercise value (`EXERCISE VALUE: fictional, not sourced`), fail closed to `INSUFFICIENT` with priority effect `NONE` on missing, stale, unconsented, weather-only, or unreadable data, and never create a task without an approved rule matching the active rule ID and policy version.
* Verify in `src/core` with bare `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*sensor*.py' -v`, write all four `.copilot-tracking/` artifacts, commit cleanly with `Refs #111` and the Copilot trailer, and do not push.

### What You May Not Know

* `sensor_review_draft.py` pins the exact serialized field sets of `ReviewTaskCandidate` (`_VIEW_CANDIDATE`) and `Signal` (`_VIEW_LINEAGE`), and expects `ReviewTaskCandidate.task_key` to remain stable across `as_of` shifts within the staleness limit; placing new provenance metadata in a dedicated `VersionProvenance` record avoids breaking draft digests or API callers.
* The shared user site-packages editable install currently resolves `zava_forward.core` to `/home/azureuser/source/ama/src/core` (an older checkout), so verification runs inside a cleaned worktree-local virtual environment (`.venv-verify-111`, removed before commit) that exposes `mypy` and `ruff` while resolving `zava_forward.core` exclusively to this worktree without mutating shared `~/.local` state.
* Under `src/README.md`, changes touching `sensor_analysis.py` fall under the Full SQL publication tier (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and a verified external receipt plus hosted CI) before PR publication or merge; because this task explicitly forbids pushing, those publication gates remain recorded follow-up prerequisites.

### Unresolved Decisions or Blockers

* None for local `src/core` implementation. Analytics research phases R1 to R3 and full SQL/PR publication gates remain tracked follow-up items outside this slice.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for Issue #111 on branch `feat/iot-111-sensor-reproducibility-2142` in `/home/azureuser/source/ama-demo-wt/feat-111-sensor-reproducibility-2142` (caller prompt).
* Deliver locally verifiable acceptance criteria in `src/core` so outputs are reproducible from retained readings with deterministic versioned sensor analysis, `SENSOR_REVIEW_DUE` review task candidate generation, and explicit version provenance (caller prompt; Issue #111; PRD FR-050, AC-067, AC-068; ADR 0003 decision 6).
* Keep thresholds labelled as exercise values until R1 to R3 complete, ensure missing/stale/declined data is `INSUFFICIENT` and never lowers priority, and propose `SENSOR_REVIEW_DUE` only from an approved signal (Issue #111; ADR 0003 decision 6).
* Write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), verify in `src/core` with bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*sensor*.py' -v`, commit cleanly with the required trailer, and do not push so `git status --short` is empty (caller prompt).

## Goals

* Make both pure (`sensor_analysis`) and SQL-retained (`sensor_analysis_store`) sensor analysis and `SENSOR_REVIEW_DUE` review task candidate generation strictly deterministic, order-independent, and reproducible from retained readings alone.
* Attach explicit, canonical `VersionProvenance` (`analysis_version`, `comparator_version`, `schema_version`, `policy_version`, `policy_digest`, `threshold_label`, `humidity_threshold_pct`, `max_staleness_hours`, `rule_id`, `rule_approved`, `approver_role`, `approval_reference`, `home_id`, `window_start`, `window_end`, `as_of`, `input_digest`, `output_digest`) to reproduced outputs without leaking raw readings, sensor IDs, or unapproved rule references.
* Elimination of input-digest collisions and version-mismatch edge cases while preserving 100% compatibility with `sensor_review_draft` and `src/api`.

## Scope and Non-Goals

### In Scope

* Hardening `src/core/src/zava_forward/core/sensor_analysis.py` (`VersionProvenance`, `version_provenance`, `_digest`, `_home_and_window`, `review_task_candidate`, `reproduce_sensor_analysis`, `reproduce_review_task`).
* Adding read-only `reproduce_retained` in `src/core/src/zava_forward/core/sensor_analysis_store.py`.
* Updating `src/core/README.md` to document pure and retained-store reproduction and provenance helpers alongside existing non-authority and R1-R3 caveats.
* Adding focused unit and reproducibility tests in `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, and `src/core/tests/test_sensor_analysis_reproducibility.py`.

### Non-Goals

* Modifying `Signal` or `ReviewTaskCandidate` field sets or changing `ReviewTaskCandidate.task_key` across `as_of` shifts.
* Writing tasks to operational queues, altering case ranking/hazards/clocks/holds, adding HTTP endpoints in `src/api`, or changing UI components.
* Completing R1 to R3 primary-standards research, running paid Azure services, mutating shared `~/.local` site-packages, or pushing to `origin`.

## Functional Requirements

* FR-1: Pure deterministic reproduction of signal, candidate, and provenance from retained readings (`reproduce_review_task` and `reproduce_sensor_analysis` in `sensor_analysis.py`).
  * Observable acceptance criteria: Given identical sets of retained reading rows in any permutation, `reproduce_review_task` and `reproduce_sensor_analysis` produce identical `provenance`, `signal`, and `review_task` (`SENSOR_REVIEW_DUE` when approved and `SUFFICIENT` + `REVIEW_CANDIDATE`, otherwise `None`), without consulting wall-clock time or storage state.
* FR-2: Collision-free canonical input, policy, and output digests (`_digest`, `policy_digest`, `output_digest`).
  * Observable acceptance criteria: `input_digest` changes on any comparator-relevant input mutation (metric value, unit, timestamp, sensor ID, `reading_id`, `calibrated`, `source_type`, `schema_version`, or row-schema validity) while remaining invariant to row order and policy changes; `policy_digest` changes when policy version, thresholds, staleness limit, label, or rule approval changes; `output_digest` commits to `(signal, review_task)`.
* FR-3: Strict version, threshold-label, and approval gating on `SENSOR_REVIEW_DUE` task generation and provenance (`review_task_candidate` and `version_provenance`).
  * Observable acceptance criteria: `review_task_candidate` returns `None` when `policy.rule_approved` is `False` or `signal.analysis_version != ANALYSIS_VERSION` or `signal.policy_version != policy.version` or `signal.threshold_label != policy.threshold_label`; `version_provenance` resolves and validates the canonical candidate for `(signal, policy)` and exposes `approver_role` and `approval_reference` only when `policy.rule_approved` is `True` (recording `None` when unapproved or mismatched).
* FR-4: Empty-window and malformed-home handling in pure reproduction (`_home_and_window`).
  * Observable acceptance criteria: Mixed homes and missing, whitespace-padded, or non-string `home_id` values raise `ValueError("SINGLE_HOME_REQUIRED")`; an empty reading sequence with explicit `home_id` and `window` deterministically yields `STALE` / `INSUFFICIENT` (`NO_READINGS_IN_WINDOW`) with `priority_effect="NONE"` and `review_task=None`.
* FR-5: Read-only SQL retained-store reproduction (`reproduce_retained` in `sensor_analysis_store.py`).
  * Observable acceptance criteria: `reproduce_retained(consumer, home_id, window, as_of, policy)` reads retained envelopes and consent without mutating SQL tables, produces output identical to pure `reproduce_review_task` over window-bounded retained indoor series (`observed_series([home_id], {home_id: (first, last)})`, including across fresh Python processes with varied `PYTHONHASHSEED`), and fails closed to `INSUFFICIENT` (`priority_effect="NONE"`, `review_task=None`) on declined/unknown consent, missing/stale rows, weather-only rows, or store errors.

## Non-Functional Requirements

* NFR-1: Privacy and non-authority preservation (PRD AC-067, ADR 0003 decision 6).
  * Objective threshold or evaluation condition: Zero raw reading values (`temperature_c`, `humidity_pct`), `sensor_id`, or `reading_id` strings appear in `VersionProvenance`, `Signal`, or `ReviewTaskCandidate`; `priority_effect` is `"NONE"` and `changes_ranking`, `starts_clock`, `releases_hold`, `diagnoses_hazard` remain `False`.
  * Operating condition or verification approach, if needed: Unit assertions over serialized `reproduce_review_task` and `reproduce_retained` payloads.
  * Observable acceptance criteria: Privacy and non-authority assertions pass for both approved and unapproved policies.
* NFR-2: Static typing, formatting, and test-budget discipline in `src/core`.
  * Objective threshold or evaluation condition: Zero errors under bare `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core`; test removals = `none`; maximum net new test methods <= 8 across existing `test_sensor_analysis*.py` files.
  * Operating condition or verification approach, if needed: Execute inside a cleaned worktree-local venv (`.venv-verify-111`) pointing editable `zava-forward-core` at this worktree with `mypy` and `ruff` available, plus verify `src/api/tests/test_sensor_analysis_reproducibility.py` compatibility.
  * Observable acceptance criteria: All checks exit 0 and `.venv-verify-111` is removed so `git status --short` is empty after commit.

## Acceptance Criteria

* AC-1: `reproduce_review_task` and `reproduce_sensor_analysis` deterministically reproduce identical `VersionProvenance`, `Signal`, and `ReviewTaskCandidate` payloads across arbitrary row orderings, redeliveries, and `PYTHONHASHSEED` values from retained readings alone.
* AC-2: `VersionProvenance` explicitly records `analysis_version`, `comparator_version`, `schema_version`, `policy_version`, `policy_digest`, `threshold_label`, `humidity_threshold_pct`, `max_staleness_hours`, `rule_id`, `rule_approved`, `approver_role`, `approval_reference` (null when unapproved/mismatched), `home_id`, `window_start`, `window_end`, `as_of`, `input_digest`, and `output_digest`, with no raw readings or device/sensor identifiers.
* AC-3: `input_digest` detects `reading_id` duplication/mutation and row-schema invalidity in addition to metric, unit, timestamp, sensor, and quality-field changes, while remaining invariant to row order and policy threshold changes.
* AC-4: `sensor_analysis_store.reproduce_retained` matches pure `reproduce_review_task` over SQL-retained indoor readings without database writes and fails closed to `INSUFFICIENT` (`review_task=None`, `priority_effect="NONE"`) on unreadable store, weather-only readings, missing/stale windows, or unconfirmed/declined consent.
* AC-5: `src/core/README.md` documents the deterministic reproduction and version provenance APIs and remaining R1-R3 / full-gate boundaries accurately.
* AC-6: Bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*sensor*.py' -v` pass in `src/core`, all four `.copilot-tracking/` artifacts exist, and the branch is committed cleanly without pushing.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md |
| Phase details | .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md |
| Latest critique | .copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-critique.md with Revise (all findings PC-001..PC-004 resolved directly in plan and phase details) |
| Relevant research | .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for Implementation |
| Continuation context | Confirmed automatic RPI Agent parent return; transitions automatically to Implement |

## Sources

* .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md: Primary codebase evidence (`C1`-`C10`), contrarian defect analysis, and convergence selection.
* docs/adrs/0003-journey-derived-capabilities-runtime-fit.md: Decision 6 invariants for deterministic versioned `sensor_analysis` and approved-only `SENSOR_REVIEW_DUE` human review proposals.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: FR-050, AC-067, and AC-068 functional, privacy, sufficiency, and comparator provenance requirements.
* docs/reference/research/iot-sensor-analytics-research-plan.md: Open R1-R3 status requiring `EXERCISE VALUE` threshold labelling and `Refs #111` non-closure.
* src/README.md: Validation tier matrix mapping `sensor_analysis.py` to the Full SQL publication gate prior to PR merge.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Pure and Retained-Store Versioned Reproduction

* Intent: Harden pure deterministic sensor analysis, digest canonicalization, `SENSOR_REVIEW_DUE` candidate gating, and explicit `VersionProvenance`, and expose read-only retained-store reproduction in `sensor_analysis_store.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add `VersionProvenance`, harden digests and bounds, and complete `reproduce_review_task` in `sensor_analysis.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1; research `C2`, `C3`, `C5`, `C8`.
* Expected result: `sensor_analysis.py` exports `COMPARATOR_VERSION`, `SCHEMA_VERSION`, `VersionProvenance`, `policy_digest`, `output_digest`, `version_provenance`, hardened `_digest` and `_home_and_window` (with optional `home_id`), `analysis_version`-checked `review_task_candidate`, backwards-compatible `reproduce_sensor_analysis`, and `reproduce_review_task`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add read-only `reproduce_retained` in `sensor_analysis_store.py`

* Requirement and evidence: FR-5, NFR-1; research `C4`.
* Expected result: `sensor_analysis_store.py` exposes `reproduce_retained(consumer, home_id, window, as_of, policy=None)` returning the canonical `{"provenance", "signal", "review_task"}` dictionary read-only and failing closed to `INSUFFICIENT` with `review_task=None`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Reproducibility Tests, Documentation, and Verification

* Intent: Prove semantic and edge-case reproducibility across pure, SQLite-retained, and fresh-process boundaries, update component documentation, run all verification gates cleanly, and create the clean local commit.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Expand focused sensor reproducibility and provenance tests in `src/core/tests/`

* Requirement and evidence: AC-1, AC-2, AC-3, AC-4, NFR-1, NFR-2; research `C2`, `C3`, `C4`, `C5`, `C8`.
* Expected result: Existing test files (`test_sensor_analysis.py`, `test_sensor_analysis_store.py`, `test_sensor_analysis_reproducibility.py`) cover `VersionProvenance`, unapproved/mismatched `RuleApproval` masking, `reading_id`/schema digest sensitivity, empty-window `home_id` reproduction, `analysis_version` mismatch rejection, `reproduce_retained` parity/fail-closed behavior, and fresh-process `PYTHONHASHSEED` reproduction, with zero test removals and <= 8 new test methods.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update `src/core/README.md` and run isolated bare verification gates

* Requirement and evidence: AC-5, AC-6, NFR-2; research `C6`, `C7`, `C9`, `C10`.
* Expected result: `src/core/README.md` documents `reproduce_sensor_analysis`, `reproduce_review_task`, `VersionProvenance`, and `sensor_analysis_store.reproduce_retained`; bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*sensor*.py' -v` pass in `src/core` (plus downstream `src/api/tests/test_sensor_analysis_reproducibility.py` check); temporary venv is removed.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md

## Dependencies

* `zava_forward.core.synthetic.sensor_scenarios` and `sensor_faults`: Supply canonical `METHOD_VERSION`, `SCHEMA_VERSION`, `READING_FIELDS`, `Window`, and `analyse()`.
* `zava_forward.core.sensor_consumer.SensorConsumer`: Supplies read-only `retained_envelopes` and `home_consent` for `sensor_analysis_store`.
* Cleaned worktree-local Python 3.12 virtual environment (`.venv-verify-111`): Exposes `mypy` and `ruff` while resolving `zava_forward.core` exclusively to this worktree during bare `mypy`, `ruff`, and `unittest` execution without touching shared `~/.local` or `/tmp`.

## Critique Disposition

Single-pass critique completed in `.copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-critique.md` (`Verdict: Revise`; 4 findings, 0 requiring user input). All findings were resolved directly in this plan and phase details:

| Critique run and finding | Disposition | Plan response or residual risk |
| --- | --- | --- |
| PC-001 (independent sorting cross-row swap collision in `_digest` and `type(v) is str`) | resolved | Updated P01-T01 so `_digest` hashes per-row bound canonical tuples combining metric, unit, timestamp, sensor, `reading_id`, quality flags, and `isinstance(v, str)` schema markers (while keeping `reading_tuples` unchanged for existing callers), and added duplicate-timestamp cross-row swap coverage in P02-T01. |
| PC-002 (`version_provenance` / `reproduce_sensor_analysis` candidate parity, `threshold_label` check, float normalization, `TypedDict` strict typing) | resolved | Updated FR-3 and P01-T01 so `review_task_candidate` checks `threshold_label`, `version_provenance` resolves/validates the canonical candidate, `reproduce_sensor_analysis` includes `"review_task"` alongside `"provenance"` and `"output_digest"`, `policy_digest` normalizes float thresholds, and `TypedDict` return types preserve zero `# type: ignore` under `mypy --strict`. |
| PC-003 (`/tmp` venv restriction and `~/.local` user-site tool visibility) | resolved | Replaced `/tmp` venv with a cleaned worktree-local `.venv-verify-111` (deleted before `git status` and commit) exposing `mypy` and `ruff` without loading `~/.local`'s stale editable `.pth`. |
| PC-004 (`SCHEMA_VERSION` literal `"sensor-fault-input-v1"`, window-bounded `observed_series` parity, and keeping `test_digest_changes_with_calibration_flag` unrenamed) | resolved | Corrected P01-T01 (`"sensor-fault-input-v1"`), updated FR-5, P01-T02, P02-T01, and P02-T02 to state window-bounded `observed_series([home_id], {home_id: (first, last)})` parity, and retained `test_digest_changes_with_calibration_flag` without renaming. |

## Follow-Up Items

* Run the complete external gate (`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>` including local SQL Server `ZF_SENSOR_MSSQL=1`) and hosted CI when pushing/opening a PR, as required by `src/README.md` for `sensor_analysis.py`.
* Complete analytics research phases R1 to R3 in `docs/reference/research/iot-sensor-analytics-research-plan.md` before using or approving any derived sensor measure beyond a labelled exercise rule.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-changes.md
* Ready phase or task: Complete (ready for `rpi-review`)
* Remaining provisional question or blocker: none
