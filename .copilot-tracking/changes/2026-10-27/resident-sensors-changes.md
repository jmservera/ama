<!-- markdownlint-disable-file -->
# RPI Changes: Resident sensors

## Metadata

* Task ID: 468; date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/resident-sensors-plan.md
* Details: .copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md

## Execution Status

Complete; full plan P01-P03. All phase/task markers complete with evidence below.

## Execution Summary

Own-home source SQL projection, strict Python boundary, native gauges/history/
table and local constructed-data tests delivered. No Azure, SQL Server operation
or private input. Existing unit suites use temporary fictional SQLite fixtures.

## Implementation-Time Plan and Detail Updates

Single independent critique returned Revise. PC-001-PC-003 resolved directly in
plan/details before source implementation: exact ownership/provenance, nullable
fault contract and controlled unit/browser subprocess environments.

## Validation Record

Initial dependency probe failed: system Python lacked installed packages, ruff,
mypy and Playwright. Created session-local venv and installed editable
core[dev,sql,blob], agents, api[dev] with pip; Chromium install completed.
Final results are recorded below; initial missing-dependency failure is retained.

### P01: Stored-history boundary

Source view now optionally projects TOP 48 stored readings through binary
case/register/reading equality and both synthetic labels, preserving nulls.
No new grant, SQL execution or runtime generator. Reader validates home,
provenance, timestamp, shape and bounds; faults/missing channels remain explicit.
Response strips home/sensor/reading IDs. Core/API tests include foreign/case-
distinct homes, forged selectors and revoked sessions.

Focused command (controlled env, ZF_TEST_MSSQL=0, shared test paths):
`python -m unittest test_resident_sensors test_resident_showcase
test_resident_showcase_sql test_resident_demo_api -q`: 113 tests,
OK, 19 opt-in SQL skips. Expected injected-error logs only.
Initial Ruff found local closure/format issues; extracted channel helper and
formatted; changed Python Ruff now passes.

### P02: Accessible native display

demo.js/demo.css now show latest stored temperature/humidity using labelled
native meters with visible text, static unit-specific SVG histories and exact
native data table. Null/fault channels have words and gaps, never zero or an
older fallback. Intl dates/numbers, UTC alternatives, Fluent tokens, responsive
layout and existing focus styles retained. Header markup unchanged.

`python src/api/checks/resident_sensors_browser_check.py` passed 23 assertions:
actual loopback app health/login/cookies, values equal fresh existing-generator
output, two own-home sessions, forged selectors, 48-row table/timestamps,
keyboard/focus, 320/390/1280 reflow, reduced motion, missing/singleton/outlier/
stuck/empty states, no browser errors. Constructed reader, not SQL integration.
API changed-file mypy passed. Core mypy found one test loop annotation;
added explicit Any test-input annotation; final rerun passed.

### P03: Verification and documentation

README documents the new response contract, source generator/table lineage,
binary ownership predicates, optional tables, future view-apply/deployment
coordination, unavailable channels, synthetic/non-live/safety limits and
SQL-free constructed-reader browser command.

All unit commands used `env -i` with PATH to session venv, an isolated HOME and
`ZF_TEST_MSSQL=0`. API additionally used
`PYTHONPATH=../core/tests:../agents/tests`. No inherited ZF integration opt-ins
or credential values were loaded. No .env or private data was read.

| Check | Exact scope | Result |
| --- | --- | --- |
| Core units | From src/core: python -m unittest discover -s tests -q | OK: 1380 tests, 186 skipped, 624.748s |
| API units | From src/api: python -m unittest discover -s tests -q | OK: 1068 tests, 308 skipped, 721.139s |
| Focused boundary | test_resident_sensors, test_resident_showcase, test_resident_showcase_sql, test_resident_demo_api | OK: 113 tests, 19 skips |
| Focused generator/API | test_resident_sensors, test_sensor_stock, test_sensor_backfill, test_resident_demo_api | OK: 65 tests, no skips |
| Core Ruff/format/mypy | resident_showcase.py, resident_showcase_sql.py, test_resident_sensors.py, test_resident_showcase.py | Passed |
| API Ruff/format/mypy | test_resident_demo_api.py, resident_sensors_browser_check.py | Passed |
| Local HTTP/Playwright | Fresh generator output, actual app, constructed reader, Chromium | Passed: 23 assertions |
| Git diff --check | All changes | Passed |
| SQL Server/integration, T-SQL compile, hosted CI/rubric, human screen reader | Excluded or later owner/PR gates | Not run, not claimed |

Unit suites emitted expected injected-failure logs; focused backfill tests also
emitted pre-existing unclosed-file ResourceWarnings. Both full suites exited 0.
No two-hour gate ran, per explicit owner instruction.

## Pre-Review Reconciliation

Plan markers/details, completed source/test/docs, validation, follow-ups and
handoff are current. Full implementation ready for one independent Review.
No new user decision or divergent scope change; original critique retained.

## Blockers

None for source work. SQL execution is excluded; real SQL integration will not run.

## Remaining Work

No implementation markers remain. Independent Review/publication remain.

## Follow-Up Items

Later separately authorised source-view apply and populated SQL verification;
human screen-reader acceptance.
