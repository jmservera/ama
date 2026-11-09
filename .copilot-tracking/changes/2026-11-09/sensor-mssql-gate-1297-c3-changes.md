<!-- markdownlint-disable-file -->
# Changes: #1297 correction C3

* Plan: .copilot-tracking/plans/2026-11-09/sensor-mssql-gate-1297-c3-plan.md (P01 complete)
* Start: HEAD 1cc88544284744efce20ae7a42458e15473b2768, base fa7ae0c9770e890f82482456bfcb8e97f1e05429

## P01 Direct dependency selection and tests

* tools/rpi-checks.py: added SENSOR_MSSQL_DIRECT_DEPENDENCIES (src/core/tests/dataset.py, src/core/src/zava_forward/core/synthetic/__init__.py) and an exact-path term in the changed_groups mssql condition. Both runtime `--changed` and receipt verification use changed_groups, so both enforce it. check_skips, the matrix and the receipt format are unchanged.
* tools/test_rpi_checks.py: two added tests, none removed.
  * test_direct_sensor_suite_dependencies_select_mssql: ast.walk over the three suite files, resolves bare names to src/core/tests and zava_forward.core.* to src/core/src (package __init__ and submodules when they exist), asserts dataset.py, synthetic/__init__.py, mssqlstore.py and sensor_backfill.py are resolved, every resolved path selects mssql, and the set missed by the keyword rules equals the constant.
  * test_non_dependency_paths_do_not_select_mssql_through_the_dependency_rule: building_fixture.py, synthetic/climate_history.py, api tests/scale_load.py (existence asserted, no keyword) do not select mssql.

## Divergences and adverse observations

* Initial negative api path src/api/tests/test_health.py did not exist; the new existence assertion caught it and it was replaced with scale_load.py.
* The first comment line exceeded 100 columns (Ruff E501); shortened. Pinned format was checked before commit.
* The first full unittest run printed a TimeoutExpired line from a tool-call wrapper; a rerun completed normally.
* Two small edits were applied with a bash Python one-liner rather than the edit tool (recorded).
* tools/__pycache__/ remains as the retained pre-existing ignored directory.
* Closure beyond direct imports (for example workflows.py, ai.py, ledger.py) remains unselected by design; no coverage claim is made.

## Validation (external ruff 0.17.1 venv /tmp/ruff1297-c2, cache /tmp/mypy-1297-c3)

* ruff format --isolated --no-cache --line-length 100 --check on both tools files: exit 0.
* ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100: exit 0 (after the E501 fix).
* mypy --strict on both files: Success, no issues.
* cd tools; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_rpi_checks: 101 tests OK.
* No SQL, Docker, browser or gate run. The C2 receipt does not cover this head.
