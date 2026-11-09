# Plan: bind sensor MSSQL skips to required SQL execution (issue #1297)

* Task ID: issue-1297 / sensor-mssql-gate-1297
* Date: 2026-11-08. Branch fix/sensor-mssql-gate-1297, base fa7ae0c9770e890f82482456bfcb8e97f1e05429, target main.
* Research: .copilot-tracking/research/2026-11-08/sensor-mssql-gate-1297-research.md (disposition executed, readiness Ready)
* Details: .copilot-tracking/details/2026-11-08/sensor-mssql-gate-1297-phase-details.md
* Changes record (created by implementation): .copilot-tracking/changes/2026-11-08/sensor-mssql-gate-1297-changes.md

## Executive Summary

The full local gate rejects project-core because ten sensor MSSQL tests skip with a reason the runner does not recognise, and the required SQL group never runs that suite. The plan adds one exact discovery exception (group project-core, eight test IDs on main, one reason) and one required, separately dispatched sensor MSSQL command in the mssql group with ZF_SENSOR_MSSQL=1. Runtime and receipt verification both demand each of the eight tests to report ok exactly once, eight tests and zero skips. Existing suites, flags and workflows are unchanged. Two residuals are reported, not fixed: #184 raises the inherited set to ten tests, and its DEFAULT_TESTS change conflicts with a main test. Actual SQL execution is deferred to the coordinator.

## User Decisions and Requirements

* Fail closed: only precisely identified expected discovery skips are exempt; never allowlist the reason alone or infer SQL success from a selector.
* The required disposable SQL group explicitly runs the complete retained sensor MSSQL suite with correct flags and imports, zero skips, and evidence that test_reopened_store_reproduces_signal_without_writes ran.
* Reject missing or substituted selectors, test IDs, reasons, flags, counts and failed or skip evidence; preserve mandatory suites; test execution and receipt verification against tampering.
* Preserve main's sensor_sql_check.DEFAULT_TESTS contract; report #184 overlap.
* Owned, disposable loopback resources only; no heavy workload, push, PR, live or private-data use in this phase; stop at a committed local handoff.
* Do not modify pinned workflows, other worktrees or existing gate evidence.

## Goals

* Make sensor MSSQL skips in project-core exact and attributable, and make the SQL group prove the suite ran.

## Scope and Non-Goals

* In scope: tools/rpi-checks.py, tools/test_rpi_checks.py, tracking evidence.
* Non-goals: .github/workflows, sensor tests or product code, sensor_sql_check, #184 ID extension, #111 work, running SQL or full gates here.

## Functional Requirements

* FR1: check_skips accepts the sensor reason only for the exact (group project-core, test ID) pairs in the pinned set; any other group, ID or reason variant raises GateError.
* FR2: required_checks and Runner.sql both add, after the SQL_SELECTORS command, `python -m unittest -v test_sensor_analysis_mssql` in cwd src/api with sqlenv plus ZF_SENSOR_MSSQL=1, suite and integration true.
* FR3: for that argv, command() and verify_commands require every pinned ID to report ok exactly once, count equal to the pinned count and zero skips.
* FR4: the existing SQL_SELECTORS command keeps identical argv and env.

## Non-Functional Requirements

* Smallest behaviour-preserving diff; no new dependencies; loopback owned SQL only; strict mypy and ruff for tools/ stay clean.

## Acceptance Criteria

* AC1 exact exception and rejection cases pass in unit tests (altered ID, reason, group, integration flag, extra skip).
* AC2 matrix contains the sensor command with the flag; tampered argv, env, cwd, missing command, skipped, failed, missing or substituted test, wrong count are rejected by verify_commands.
* AC3 the named reopened-store test is in the required set.
* AC4 existing tools tests still pass; ruff, format and strict mypy clean for the two files.
* AC5 heavy validation plan reported; none executed.

## Phase Checklist

* [x] P01 Runner contract change
* [x] P02 Regression tests
* [x] P03 Focused validation and handoff

## Phases

### P01 Runner contract change

* [x] P01-T01 Add SENSOR_MSSQL_SELECTOR, pinned ID tuple, discovery-skip pairs and reason constant.
* [x] P01-T02 Extend check_skips with exact project-core scoping.
* [x] P01-T03 Generalise required_sql_tests plus a count helper; wire into command() and verify_commands.
* [x] P01-T04 Add the sensor command to Runner.sql and required_checks.

### P02 Regression tests

* [x] P02-T01 Discovery exception exact and fail-closed tests.
* [x] P02-T02 Matrix, dispatch and flag tests.
* [x] P02-T03 Receipt tamper tests via verify_commands.

### P03 Focused validation and handoff

* [x] P03-T01 Run tools tests, ruff, format, mypy (focused only).
* [x] P03-T02 Review phase, commit with repository-local privacy-safe identity, report.

## Follow-Up Items

* #184: extend pinned IDs to ten and count when its two inherited tests land; separately resolve DEFAULT_TESTS vs test_sensor_sql_check.
* Heavy validation (coordinator-admitted): full gate with --all, verified receipt, independent exact-head review, hosted CI.

## Critique Disposition

Critique executed once (artifact: .copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-critique.md), verdict Revise, 8 findings, all direct planner corrections, none needs a user decision. No second critique.

* PC-001 accepted: pinned IDs use the full `name (module.Class.name)` verbose form (details P01-T01).
* PC-002 accepted: skip predicate is explicit and scoped: group == "project-core", not integration, exact (test, reason) pair in the pinned set; the reason is not added to EXPECTED_SKIP_REASONS (details P01-T02).
* PC-003 accepted: a test compares the pinned IDs with the real module's methods via unittest discovery of the class, including the named test (details P02).
* PC-004 accepted: existing receipt fixtures near test_rpi_checks.py 1691 (log chosen by required_sql_tests) and the suite count assertion near 1795 (10 to 11) are modified, not removed (details P02-T04).
* PC-005 accepted: six named test methods (details P02).
* PC-006 accepted: module collection from src/api without SQL already recorded (research C8 ran from src/core; src/api run repeated in implementation, 8 skips).
* PC-007 accepted: lint and mypy use RUFF_GROUPS and TYPE_GROUPS arguments; `--changed` gate deferred to the coordinator.
* PC-008 accepted: only project-core collects the module for discovery; earlier receipts become invalid by design; recorded as residual.
