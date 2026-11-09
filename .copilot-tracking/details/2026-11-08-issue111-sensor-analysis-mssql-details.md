---
title: Issue 111 sensor analysis MSSQL test increment, details
ms.date: 2026-11-08
---

## Test module

`src/core/tests/test_sensor_analysis_mssql.py`

* Import `test_sensor_analysis_store as base` (module import, so the SQLite class is not rediscovered here).
* `MssqlRetainedAnalysisTests(base.RetainedAnalysisTests)` replaces `setUp`: require `ZF_SENSOR_MSSQL=1`, otherwise skip at module/class level for ordinary SQLite discovery; build the store with `store_at(reset=True)`, assert `consumer.mssql`, drop the sensor tables and `cases` row `ZF-2` as `SensorConsumerTests` does, configure `POLICY`/`CONTROL`, ingest `preflight(observations())`.
* The seven inherited methods run unchanged. The dropped-table test is restored by a cleanup that calls `consumer.configure(POLICY, [CONTROL])`, which recreates the table.
* `test_reopened_store_reproduces_signal`: compute the signal, close the store, reopen with `store_at(directory)` and a new `SensorConsumer`, assert equal signal, unchanged snapshot, and `priority_effect == "NONE"`.
* Normalise driver representation only where a real difference is observed in the run.

## Harness

`src/api/checks/sensor_sql_check.py`

* `SELECTORS = {"default": (existing tuple), "analysis": ("test_sensor_analysis_mssql",)}` and `EXPECTED_RUN = {"analysis": 8}`.
* `argparse` with `choices=sorted(SELECTORS)`, default `default`.
* `validate(selector, returncode, output) -> bool`: for `analysis` require exit 0, `Ran 8 tests` and a final `OK` line without `skipped`.
* The `analysis` run captures stderr, redacts the password and echoes it; `default` keeps inheriting streams as before.

## Harness test

`src/api/tests/test_sensor_sql_check.py`: default tuple unchanged, analysis selector maps to the module, unknown selector rejected, validate accepts exact result, rejects skips, wrong count, non-zero exit, missing summary. No Docker or SQL.

## Validation

Unit tests, then `ruff check`, `ruff format --check`, `mypy` on changed files, then actual MSSQL via `flock -n`-style heavy lock with a finite timeout.
