---
title: "RPI Plan: Pin Sensor MSSQL Retained Reproduction Test in Local Gate"
description: "Cycle-2 CI fix plan for tools/rpi-checks.py and tools/test_rpi_checks.py on PR #1741 (Refs #111)"
ms.date: 2026-11-14
---

## Task Metadata

* Task ID: 111-sensor-reproducibility-2142-c2
* Task slug: 111-sensor-reproducibility-2142-c2
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-c2-critique.md

## Executive Summary

This Cycle-2 plan fixes the `src-namespace` CI failure on PR #1741 (`feat/iot-111-sensor-reproducibility-2142`) by adding `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py` and asserting its explicit membership in `tools/test_rpi_checks.py`. Updating this single source-of-truth tuple reconciles the AST-enforced suite inventory (`RetainedAnalysisTests` union `MssqlRetainedAnalysisTests`), `project-core` discovery-skip verification (`SENSOR_MSSQL_DISCOVERY_SKIPS`), and Full SQL execution count/name verification (`required_sql_tests` and `required_sql_count`).

### User Decisions and Requirements Highlights

* Update the pinned sensor MSSQL test list in `tools/rpi-checks.py` (and `tools/test_rpi_checks.py`) so `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` passes with `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only`.
* Record the Cycle-2 fix in `.copilot-tracking/` across research, plan, phase details, critique, changes, and review artifacts while preserving Cycle-1 artifacts intact.
* Validate with `python3 -m unittest discover -s tools -p test_rpi_checks.py -v`, `python3 -m unittest discover -s tools -p test_ci_affected.py -v`, `ruff`, and `mypy --strict`, then commit cleanly on `feat/iot-111-sensor-reproducibility-2142` with the Copilot trailer and do NOT push.

### What You May Not Know

* `SENSOR_MSSQL_REQUIRED_TESTS` governs two separate gate invariants in `tools/rpi-checks.py`: without the 11th test ID, `project-core` unit discovery fails closed on the 34th skipped MSSQL test when `ZF_SENSOR_MSSQL` is unset, and the `mssql` group fails closed on `Ran 11 tests` vs expected `10` when `ZF_SENSOR_MSSQL=1`.
* Under the repository's two-tier validation rule, editing `tools/rpi-checks.py` tightens gate semantics (10 -> 11 required SQL tests) on a branch that also modifies `sensor_analysis.py`, so the branch remains classified under the **Full SQL tier** prior to final PR merge, while Cycle 2 executes the exact `src-namespace` local gate-orchestration checks without pushing.

### Unresolved Decisions or Blockers

* None for Cycle-2 implementation and local commit. Full SQL receipt (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1`) and hosted CI on the updated commit remain pre-merge follow-up gates.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run a Cycle-2 RPI fix (`research`, `plan`, `implement`, `review`) for Issue #111 / PR #1741 in worktree `/home/azureuser/source/ama-demo-wt/feat-111-sensor-reproducibility-2142` on branch `feat/iot-111-sensor-reproducibility-2142` targeting `feat/demo-164-chat-grounding-provenance-0900` (caller prompt).
* Inspect `tools/test_rpi_checks.py` around line 474 and `tools/rpi-checks.py`, and update the pinned sensor MSSQL test list so `test_pinned_sensor_mssql_tests_match_the_real_suite` passes with `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` (caller prompt; research `C1`, `C2`).
* Record the Cycle-2 fix in `.copilot-tracking/{changes,reviews}/` and research/plans as part of the Cycle-2 RPI loop without overwriting historical Cycle-1 records (caller prompt; tracking retention policy).
* Run `python3 -m unittest discover -s tools -p test_rpi_checks.py -v` and `python3 -m unittest discover -s tools -p test_ci_affected.py -v` from the repo root of the worktree, plus `ruff` and `mypy` on `tools/` matching `src-namespace` CI (caller prompt; research `C5`, `C6`).
* Commit cleanly on `feat/iot-111-sensor-reproducibility-2142` using privacy-safe Git author config, `Refs #111`, and the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, and do NOT push (caller prompt; `.github/copilot-instructions.md`).

## Goals

* Restore exact parity between the `MssqlRetainedAnalysisTests` suite inventory (`RetainedAnalysisTests` + `MssqlRetainedAnalysisTests`, 11 tests) and `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py`.
* Ensure `src-namespace` local gate orchestration tests (`test_rpi_checks.py` and `test_ci_affected.py`), isolated `ruff` lint/format checks, and `mypy --strict` checks pass with zero errors.
* Preserve complete Cycle-1 `src/core` deliverables and tracking evidence while recording full Cycle-2 RPI artifacts and committing cleanly without pushing.

## Scope and Non-Goals

### In Scope

* Adding `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only"` in alphabetical position to `SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py`.
* Adding an explicit `self.assertIn(...)` pin check for `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` in `tools/test_rpi_checks.py`.
* Running `test_rpi_checks.py`, `test_ci_affected.py`, `ruff check`, `ruff format --check`, and `mypy --strict` from the worktree root, plus verifying `project-core` skip validation (`check_skips`) against `src/core` sensor discovery output.
* Recording Cycle-2 RPI tracking artifacts and creating one clean local commit on `feat/iot-111-sensor-reproducibility-2142`.

### Non-Goals

* Modifying `src/core` source or test files delivered in Cycle 1 (`79b9cd1be`).
* Changing `.github/workflows/src-ci.yml` or `WORKFLOW_HASHES`.
* Pushing to `origin` or altering PR state remotely.

## Functional Requirements

* FR-1: Pinned sensor MSSQL required-test inventory parity (`SENSOR_MSSQL_REQUIRED_TESTS` in `tools/rpi-checks.py`).
  * Observable acceptance criteria: `SENSOR_MSSQL_REQUIRED_TESTS` includes `"test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only (test_sensor_analysis_mssql.MssqlRetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only)"` in alphabetical order (11 tests total), automatically updating `SENSOR_MSSQL_DISCOVERY_SKIPS`, `required_sql_tests`, and `required_sql_count`.
* FR-2: Explicit contract regression coverage in `tools/test_rpi_checks.py`.
  * Observable acceptance criteria: `GateTests.test_pinned_sensor_mssql_tests_match_the_real_suite` verifies both exact AST set equality against `RetainedAnalysisTests | MssqlRetainedAnalysisTests` and explicit membership of `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only`.

## Non-Functional Requirements

* NFR-1: Exact `src-namespace` CI lint, format, type-check, and unit-test compliance on `tools/`.
  * Objective threshold or evaluation condition: Zero failures across all 103 tests in `tools/test_rpi_checks.py` and all tests in `tools/test_ci_affected.py`; zero issues under isolated `ruff check`, `ruff format --check` (`--select E,F,I,B,UP --target-version py312 --line-length 100`), and `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py`; test removals = `none`; net new test methods = `0` (<= 1 lock).
  * Operating condition or verification approach, if needed: Execute directly from `/home/azureuser/source/ama-demo-wt/feat-111-sensor-reproducibility-2142` matching `.github/workflows/src-ci.yml` lines 258-267.
  * Observable acceptance criteria: Every command exits with code `0` and `git status --short` is empty after commit.

## Acceptance Criteria

* AC-1: `python3 -m unittest discover -s tools -p test_rpi_checks.py -v` passes all 103 tests, including `test_pinned_sensor_mssql_tests_match_the_real_suite`.
* AC-2: `python3 -m unittest discover -s tools -p test_ci_affected.py -v` passes all tests.
* AC-3: `ruff check` and `ruff format --check` (isolated `src-ci.yml` flags) and `mypy --strict` pass on `tools/rpi-checks.py` and `tools/test_rpi_checks.py` (and `ruff` on `tools/ci-affected.py` and `tools/test_ci_affected.py`).
* AC-4: Cycle-2 RPI artifacts (`.copilot-tracking/{research,plans,details,critiques,changes,reviews}/2026-11-14/111-sensor-reproducibility-2142-c2-*` and session state) are complete, reconciled, and disclose Full SQL tier classification accurately.
* AC-5: Changes are committed cleanly on `feat/iot-111-sensor-reproducibility-2142` with privacy-safe author identity, `Refs #111`, and the Copilot trailer, without pushing (`git status --short` empty).

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-c2-plan.md |
| Phase details | .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md |
| Latest critique | .copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-c2-critique.md with Pass (0 findings; test_ci_affected count corrected to 19) |
| Relevant research | .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-c2-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-c2-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for Implementation |
| Continuation context | Confirmed automatic RPI Agent parent return; transitions automatically to Implement |

## Sources

* .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-c2-research.md: Primary codebase evidence (`C1`-`C7`), failure reproduction, and MSSQL compatibility verification.
* .github/workflows/src-ci.yml: Canonical `src-namespace` step commands for `tools/` tests, `ruff`, and `mypy --strict`.
* src/README.md: Two-tier validation rules and `SENSOR_MSSQL_REQUIRED_TESTS` local SQL gate contract.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Update Pinned Sensor MSSQL Gate Contract and Verify `tools/` Suite

* Intent: Pin `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `tools/rpi-checks.py`, lock its membership assertion in `tools/test_rpi_checks.py`, and pass all `src-namespace` gate orchestration, lint, format, and strict type checks.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add `test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` to `SENSOR_MSSQL_REQUIRED_TESTS` and `test_rpi_checks.py`

* Requirement and evidence: FR-1, FR-2; research `C1`, `C2`, `C3`, `C4`.
* Expected result: `tools/rpi-checks.py` pins all 11 `MssqlRetainedAnalysisTests` test IDs in alphabetical order, and `tools/test_rpi_checks.py` explicitly asserts the new test ID alongside AST set equality.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Execute `test_rpi_checks.py`, `test_ci_affected.py`, `ruff`, and `mypy --strict` validation

* Requirement and evidence: AC-1, AC-2, AC-3, NFR-1; research `C5`, `C6`, `C7`.
* Expected result: All 103 tests in `test_rpi_checks.py`, all 19 tests in `test_ci_affected.py`, isolated `ruff check` + `ruff format --check`, and `mypy --strict` exit 0 cleanly from the worktree root.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-c2-phase-details.md

## Dependencies

* Cycle-1 commit `79b9cd1be` on `feat/iot-111-sensor-reproducibility-2142`: Defines `RetainedAnalysisTests.test_reproduce_retained_matches_pure_reproduction_and_fails_closed_read_only` in `src/core/tests/test_sensor_analysis_store.py`.
* Local `python3`, `ruff`, and `mypy` tools in `/home/azureuser/.local/bin`: Execute the exact `src-namespace` test, lint, format, and strict type checks offline.

## Critique Disposition

Single-pass final-candidate critique completed in `.copilot-tracking/critiques/2026-11-14/111-sensor-reproducibility-2142-c2-critique.md` (`Verdict: Pass`; 0 findings). Also incorporated non-blocking accuracy polish (`19` test methods in `tools/test_ci_affected.py` and `PYTHONPATH=src/core/src:src/core/tests` for `check_skips` discovery verification).

| Critique run and finding | Disposition | Plan response or residual risk |
| --- | --- | --- |
| `111-sensor-reproducibility-2142-c2-critique` (`Pass`, 0 `PC-xxx` findings) | resolved | Finalized directly; corrected `test_ci_affected.py` expected test count (`19`) and `PYTHONPATH` note in phase details. |

## Follow-Up Items

* Run the complete external SQL gate (`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <external-dir>` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) and hosted CI on the updated branch head before final PR merge, per the Full SQL tier classification in `src/README.md`.
* Complete analytics research phases R1 to R3 in `docs/reference/research/iot-sensor-analytics-research-plan.md` before replacing `EXERCISE VALUE` thresholds or approving an operational rule (`Refs #111`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/111-sensor-reproducibility-2142-c2-changes.md
* Ready phase or task: P01 (`P01-T01`, `P01-T02`)
* Remaining provisional question or blocker: none
