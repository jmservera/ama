<!-- markdownlint-disable-file -->
# Phase details: #1297 correction C4

* Plan: .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c4-plan.md

## P01 Add exercised dependency and regression

* P01-T01: add "src/core/src/zava_forward/core/synthetic/indoor_projection.py" to SENSOR_MSSQL_DIRECT_DEPENDENCIES in tools/rpi-checks.py and reword its comment to "direct or exercised dependencies".
* P01-T02: tests (added/changed within test_direct_sensor_suite_dependencies_select_mssql and one new test; removals none; at most one addition): the keyword-missed set of resolved direct imports must be a subset of the constant; the constant must equal that set plus indoor_projection.py; a new test AST-checks that sensor_backfill.py calls indoor_projection.project in `_indoor` and that indoor_projection.py selects mssql while household_conditions.py (imported, not exercised) does not.
* Completion: format, lint, mypy and tools unit tests pass.
