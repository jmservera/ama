# Phase details: issue #1297 sensor MSSQL gate

Plan: .copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-plan.md. Evidence: research C1-C12.

## P01 Runner contract change

* P01-T01 constants near SQL_CHAT_REQUIRED_TESTS (rpi-checks.py ~147): module test_sensor_analysis_mssql, class MssqlRetainedAnalysisTests, eight methods on main: test_any_declined_control_wins, test_declined_unknown_and_unmapped_consent_fail_closed, test_matches_pure_derivation_over_retained_rows_and_is_reproducible, test_read_only_and_no_task_without_approved_rule, test_reopened_store_reproduces_signal_without_writes, test_stale_and_missing_readings_are_insufficient, test_unmapped_or_invalid_home_is_insufficient, test_unreadable_store_is_insufficient_with_no_priority_effect. Reason "requires ZF_SENSOR_MSSQL=1". Evidence: C8, C9.
* P01-T02 check_skips: the reason is not added to EXPECTED_SKIP_REASONS; a skip with it is accepted only when group == "project-core" and (test, reason) is in the pinned pair set, and never when integration is true (SQL_NOT_APPLICABLE unchanged). Evidence: C2, C7.
* P01-T03 required_sql_tests returns the sensor tuple when argv ends with the sensor selector (and still SQL_CHAT tuple for SQL_SELECTORS tail); add required_sql_count returning the pinned count for the sensor argv; pass expected_count to check_skips at both call sites (expected_count already forces zero skips and exact count). Evidence: C5.
* P01-T04 add the command after SQL_SELECTORS in Runner.sql and in required_checks with env {**sqlenv, "ZF_SENSOR_MSSQL": "1"}, cwd src/api, suite and integration true, timeout 1800 (matches existing). Evidence: C3, C6, C11.

## P02 Regression tests (tools/test_rpi_checks.py, existing GateTests); at most six new methods, no removals

* Revision per critique: IDs are full verbose strings `name (test_sensor_analysis_mssql.MssqlRetainedAnalysisTests.name)` built with _sql_tests.
* P02-T04 modify existing fixtures: the receipt fixture near line 1691 must supply a matching sensor log for the new argv; the suite-count assertion near line 1795 changes from 10 to 11.
* Six new methods: (1) discovery exception exact and rejections, (2) pinned IDs equal the module's real methods and include the named test, (3) matrix order, flag and unchanged SQL_SELECTORS env, (4) check_skips evidence mutations, (5) verify_commands tampering of argv/env/cwd/missing command, (6) runtime command() accepts a good sensor log and rejects a skipped one.

* P02-T01 exact exception: accepted for project-core with the pinned pairs, rejected for other group, integration true, altered ID, altered reason, ninth unknown ID, skip-count mismatch.
* P02-T02 matrix: required_checks for mssql contains SQL_SELECTORS argv with unchanged env lacking ZF_SENSOR_MSSQL, followed by the sensor argv with the flag; Runner.sql dispatch ordering consistent with the matrix.
* P02-T03 receipt: build a passing sensor log (eight ok, Ran 8, OK) and verify via check_skips; mutations missing, duplicate, failed, skipped, extra test (count nine), substituted ID, named test absent; verify_commands rejects flag removed, argv selector substituted, cwd changed. Write each case once.

## P03

* P03-T01 `python3 -m unittest` for tools/test_rpi_checks (focused selectors then file), ruff check/format --isolated line length 100, mypy --strict on the two files per TYPE_GROUPS.
* P03-T02 independent rpi-review, then commit with gh-derived noreply email and the Copilot trailer.
