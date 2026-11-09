<!-- markdownlint-disable-file -->
# Changes: #1297 correction C4

* Plan: .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c4-plan.md (P01 complete)
* Start: HEAD 08e13f6e6bafe74a22a65f47151d5c762d6638ef, base fa7ae0c9770e890f82482456bfcb8e97f1e05429

## P01 Add exercised dependency and regression

* tools/rpi-checks.py: added src/core/src/zava_forward/core/synthetic/indoor_projection.py to SENSOR_MSSQL_DIRECT_DEPENDENCIES; comment reworded to direct or exercised dependencies.
* tools/test_rpi_checks.py: the C3 equality assertion now expects the keyword-missed direct imports plus indoor_projection.py to equal the constant; one added test checks that sensor_backfill._indoor calls indoor_projection.project, that indoor_projection.py selects mssql and that household_conditions.py (imported, not exercised) does not. No tests removed.

## Evidence of exercised dependencies

* Throwaway profile scripts /tmp/trace1297.py and /tmp/trace1297b.py (outside the worktree; PYTHONDONTWRITEBYTECODE=1; no SQL) recorded first-party functions called during sensor_consumer_fixture.observations(): indoor_projection (project, _project, _number, _bounded_noise, saturation_pressure), sensor_backfill, sensor_faults and the fixture. Only indoor_projection.py lacks a selecting keyword. Boundary: observations() with no fault and no composed flag; store_at, the SQL stores and test bodies were not traced; no closure claim.

## Divergences and adverse observations

* The first comment line exceeded 100 columns (Ruff E501) and was shortened before commit.
* The throwaway trace scripts were created with a bash heredoc in /tmp (outside the worktree).
* tools/__pycache__/ remains as the retained pre-existing ignored directory.
* Critique skipped by recorded rationale (see the plan).

## Validation (external ruff 0.17.1 venv /tmp/ruff1297-c2, mypy cache /tmp/mypy-1297-c3)

* ruff format --isolated --no-cache --line-length 100 --check: exit 0.
* ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100: exit 0 (after the E501 fix).
* mypy --strict on both files: no issues.
* cd tools; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_rpi_checks: 102 tests OK.
* No SQL, Docker, browser or gate run. The C2 receipt does not cover this head.
