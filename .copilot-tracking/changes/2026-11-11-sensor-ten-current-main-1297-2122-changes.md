---
title: Sensor ten-test MSSQL current-main changes (issue 1297, AC2)
ms.date: 2026-11-11
---

Plan: [plan](../plans/2026-11-11-sensor-ten-current-main-1297-2122-plan.md). Raw output: [raw log](2026-11-11-sensor-ten-current-main-1297-2122-raw.log), sha256 `212234d208835ec771ddf60357e928ef01ef90c1cbf2e810c8dbeaaca6fceef6`.

## Changes

Only tracking evidence was added (research, plan, details, this file, raw log, review). No application, test, runner, workflow or README edit.

## Observation

* Source and base: `HEAD` = `origin/main` = `077ad5ad20293a1d79932ea14e9f639dd11e5a22`, tree `d1dde25bc3476772bd9d97711558ed87d1f7a035`, clean worktree. Import paths for `mssqlstore`, `sensor_analysis_store` and `test_sensor_analysis_mssql` resolved inside this worktree (see log).
* Admission (2026-11-11T21:27:19Z): non-blocking `flock` on `/tmp/ama-rpi-heavy.lock` acquired, no other holder; MemAvailable 6773 MiB (at least 5120 required), 4 CPUs, load 3.02. An unrelated process outside the lock kept running untouched.
* Backend: one task-owned container `01a45974db047bae8957caa0e84b9dc6a10363c70cf09e136f1922d416e2e0e1`, image `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718` (cached, no pull), label `ama.rpi.owner=<random token>`, `--memory=3g --cpus=2`, single binding `127.0.0.1:32773`, ownership proven from `docker inspect` before any test. Database `rpi_disposable` created through the runner's `SQL_QUERY` readiness (attempt 7). The `MssqlRetainedAnalysisTests.setUp` asserts `consumer.mssql`, so each passing test ran on MSSQL.
* Command (cwd `src/api`, exit 0): `ZF_SENSOR_MSSQL=1 ZF_TEST_MSSQL=1 ZF_SQL_*=<owned loopback> python3 -m unittest -v test_sensor_analysis_mssql`, with `PYTHONPATH` the worktree `src/{core,agents,api}/src` then `src/api/tests:src/core/tests:src/agents/tests`.
* Result: `Ran 10 tests in 6.402s`, `OK`, no skips, no failures. The ten `ok` IDs equal `SENSOR_MSSQL_REQUIRED_TESTS` exactly (programmatic set comparison true):

| Test ID (class `MssqlRetainedAnalysisTests`) | Result |
| --- | --- |
| test_any_declined_control_wins | ok |
| test_declined_unknown_and_unmapped_consent_fail_closed | ok |
| test_live_weather_rows_are_not_indoor_input | ok |
| test_matches_pure_derivation_over_retained_rows_and_is_reproducible | ok |
| test_read_only_and_no_task_without_approved_rule | ok |
| test_reopened_store_reproduces_signal_without_writes | ok |
| test_stale_and_missing_readings_are_insufficient | ok |
| test_unmapped_or_invalid_home_is_insufficient | ok |
| test_unreadable_store_is_insufficient_with_no_priority_effect | ok |
| test_weather_only_window_is_insufficient_with_explicit_reason | ok |

* Cleanup: `docker rm -f 01a45974...e0e1` exit 0; `docker inspect` of the ID fails (absent); no container carries the owner label; `docker ps -a` empty afterwards; heavy lock released at script exit. The generated password was never written to the log.
* Environment: Python 3.12.3, `mssql-python 1.15.0`, `mssql-python-odbc 18.6.2.1`, Docker 29.9.0, no packages installed or changed.

## Limitations and open criteria

* Deviations from the runner: host Python, no fresh venv, no image pull; run as a direct selector invocation, not through `tools/rpi-checks.py`. The runner's own SQL group (`SQL_SELECTORS`) and dispatch were not run.
* AC2: supplies the missing current ten-ID execution observation, including the reopened-store test on MSSQL with zero skips; no criterion is ticked here, and the coordinator decides.
* AC5 remains unmet: no full local receipt, independent exact-head review or hosted CI for the combined delivery. The 1299 receipt (eight tests) and adverse history are preserved unchanged.
