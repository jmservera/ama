<!-- markdownlint-disable-file -->
# Plan: #1297 correction C4

* Task ID: issue-1297-c4; slug sensor-mssql-gate-1297-c4
* Date: 2026-11-09
* Research: .copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c4-research.md
* Details: .copilot-tracking/details/2026-11-09/sensor-mssql-gate-1297-c4-phase-details.md
* Changes path: .copilot-tracking/changes/2026-11-09/sensor-mssql-gate-1297-c4-changes.md

## Executive Summary

C3 left indoor_projection.py unselected although the sensor MSSQL fixture calls it at runtime (evidence: profile trace of observations()). C4 adds that one exercised path to the existing exact-path constant and extends the C3 regression. No SQL-for-all-core policy is adopted; transitive closure remains an owner decision. Readiness: Ready.

## User Decisions and Requirements

* Smallest fail-closed focused-selection change for the demonstrated dependency, with a regression.
* Preserve C3 direct dependency coverage, skip/selector/execution-evidence guards, unrelated selections, the full gate.
* Investigate other exercised dependencies, report evidence, no exhaustive-closure claim; stop and report if a broader policy is required.
* No heavy workloads; pinned Ruff lint and format, strict mypy, focused tests; commit locally only.

## Goals

* mssql is selected when indoor_projection.py changes.

## Scope and Non-Goals

* In: tools/rpi-checks.py constant; tools/test_rpi_checks.py regression.
* Non-goals: closure-wide or project-core-wide selection, check_skips changes, #184 overlaps, other worktrees.

## Functional Requirements

* The constant name and exact-path rule from C3 are retained; indoor_projection.py is added.
* household_conditions.py (imported, not exercised) stays unselected.

## Non-Functional Requirements

* Fail-closed, no new ignored files in the worktree, formatted with pinned Ruff 0.17.1.

## Acceptance Criteria

* changed_groups for indoor_projection.py includes mssql; C3 paths still select; unrelated paths do not.
* Regression ties the added path to sensor_backfill's static call of indoor_projection.
* Ruff format/lint, strict mypy, tools tests pass.

## Critique Disposition

Critique skipped (recorded rationale, as in C2): a one-element addition to an existing exact-path set using the mechanism critiqued in C3 (PC-001 to PC-004 already applied); the exercised-dependency evidence is in the research. Independent Review by the coordinator remains required.

## Phase Checklist

* [x] P01 Add exercised dependency and regression

## Follow-Up Items

* Owner policy: closure-wide or project-core-wide mssql selection (alternative B) remains open.
* #184 overlaps (sensor IDs to ten; DEFAULT_TESTS conflict) out of scope.
