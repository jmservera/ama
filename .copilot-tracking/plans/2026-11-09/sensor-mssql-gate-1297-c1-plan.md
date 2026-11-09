---
title: Plan - #1297 correction C1
date: 2026-11-09
task_id: issue-1297-c1
---

## Executive Summary

Correct the independent Medium finding: `--changed` can accept the exact sensor discovery skips in project-core without selecting the `mssql` group. Select `mssql` in `changed_groups` for every `src/core` path containing `sensor`, keeping the skip exception, full gate and receipt contract unchanged. Add focused regression tests. No heavy validation runs here.

## User Decisions and Requirements

* Minimal fail-closed solution covering sensor-analysis implementation, shared fixture and directly related paths.
* Retain precise skip validation and all required suites; never weaken the full gate or allowlist broad reasons.
* Tests for affected changed paths, unrelated paths, receipt selection and the required SQL sensor command/evidence.
* No heavy workloads, no push/PR, preserve prior evidence, #184 items out of scope.
* Research: .copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c1-research.md (alternative A).

## Goals

Focused `--changed` runs for sensor core changes always include `mssql`, so the flagged zero-skip sensor command runs.

## Scope and Non-Goals

* In: `changed_groups` in tools/rpi-checks.py; tests in tools/test_rpi_checks.py.
* Out: check_skips, receipt format, matrix, #184 pins, DEFAULT_TESTS, api sensor modules.

## Functional Requirements

* Any `src/core/**` path with `sensor` in its lowercase path selects `mssql` (and its dependency closure).
* Unrelated core and api paths do not gain `mssql` through this rule.

## Non-Functional Requirements

* Ruff, mypy --strict clean; tools tests pass; no generated files in the worktree.

## Acceptance Criteria

* changed_groups selects mssql for sensor_analysis.py, sensor_consumer_fixture.py, sensor_consumer.py, synthetic/sensor_faults.py, test_sensor_analysis_mssql.py.
* A sensor-only core change yields a selection whose command list includes the flagged sensor command with expected_count 8 (receipt selection) and no change for unrelated paths (e.g. core/.../timeline.py, api sensor_ingestion.py).

## Phase Checklist

* [x] P01 Selection rule and tests

## Critique Disposition

One critique, verdict Revise (minor), 4 findings, all accepted as direct planner corrections; no second critique.

* PC-001 accepted: P01-T01 also updates `SKIP_REASONS["mssql"]` to mention sensor paths; test asserts the text for a skipped mssql group.
* PC-002 accepted: P01-T02 names `required_checks` and asserts the flagged sensor command (argv selector, ZF_SENSOR_MSSQL, `required_sql_count` 8) is present for the executed groups of a sensor-only `changed_groups` result, table-driven with subTest.
* PC-003 accepted with bounded residual: static import closure of the suite checked (sensor_analysis_store, sensor_analysis, sensor_consumer, synthetic.sensor_scenarios, test_sensor_analysis_store, sensor_consumer_fixture, synthetic.sensor_backfill/sensor_faults, sqlstore; third-party `dataset`). All first-party modules match `sensor`, `sql` or `store`; `src/api` sensor modules are not imported by the core suite. Residual: a change to a shared first-party module not named sensor/sql/store that sensor code uses (for example a general core helper) still selects only project-core, but then discovery skips are also accepted; accepted risk, full gate remains authoritative.
* PC-004 accepted: /tmp and /mnt pointers are historical and non-load-bearing.

## Follow-Up Items

* #184: extend pinned IDs to ten; DEFAULT_TESTS conflict (unchanged, out of scope).
* Coordinator: new current-base full gate; prior receipt is historical.
