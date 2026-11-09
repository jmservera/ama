---
title: Issue 111 sensor analysis MSSQL test increment, changes
ms.date: 2026-11-08
---

Plan: [plan](../plans/2026-11-08-issue111-sensor-analysis-mssql-plan.md). No production, shared fixture, runner, workflow, schema, consent, threshold or browser change.

## Files

* `src/core/tests/test_sensor_analysis_mssql.py` (new): `MssqlRetainedAnalysisTests` inherits the seven existing behavioural tests unchanged, replaces `setUp` (asserts `consumer.mssql`, drops the sensor tables and `cases` row `ZF-2`, configures, ingests), restores any deliberately dropped table by cleanup `configure`, and adds `test_reopened_store_reproduces_signal_without_writes`. Skipped only when `ZF_SENSOR_MSSQL` is not `1`.
* `src/api/checks/sensor_sql_check.py`: closed `SELECTORS` (`default`, `analysis`), `--selector` via `argparse`, and `validate`. `default` keeps its exact tests, inherited streams and cleanup. `analysis` captures output, redacts the generated password, requires exit 0, `Ran 8 tests` and a clean `OK`.
* `src/api/tests/test_sensor_sql_check.py` (new): four tests, no Docker or SQL.
* `src/api/README.md`: one paragraph documenting the selector and its limits.

No driver representation difference was observed, so no normalisation was added. No amendment or divergence from the plan, except the README paragraph, which is directly related documentation.

## Validation (actual, 2026-11-08)

Environment: private venv `/tmp/ama-issue111-rt/venv` (Python 3.12.3, pip), candidate `src/core[sql]`, `src/agents`, `src/api` installed editable from this worktree, `ruff==0.17.1`, `mypy==2.4.0`, `mssql-python 1.15.0`. Source base and HEAD `4bc1e3f3361a762cc9f0c187d394fdab9a11b033` (tree `85ef5852bcdd17ce73d1684e76f96b70f8d2274f`) plus the uncommitted changes above. `origin/main` is `9d035ee9e` with `src/` identical to the base.

* `python -m unittest test_sensor_sql_check` (src/api): 4 tests OK.
* `ruff check` with each component config, changed files: clean. `ruff format --check` on the two new test files: clean (`checks/*.py` is format-excluded by the component config).
* `mypy` strict, component configs: `sensor_sql_check.py` and `test_sensor_sql_check.py` clean; `test_sensor_analysis_mssql.py` clean.
* SQLite discovery of the new module: 8 tests, all skipped (expected without `ZF_SENSOR_MSSQL=1`).
* Heavy ownership inspected first: no Docker containers, no process holding `/tmp/ama-rpi-heavy.lock`, load 0.57, about 8 GB available, image `mcr.microsoft.com/mssql/server:2022-latest` (`cf8f0ab2ebe6`) already present.
* Actual SQL, analysis: `env -i HOME=/tmp/ama-issue111-rt PATH=<venv>:/usr/bin:/bin timeout -k 30s 600s flock -n /tmp/ama-rpi-heavy.lock python src/api/checks/sensor_sql_check.py --selector analysis`. Exit 0, raw output `Ran 8 tests in 3.433s`, `OK`, `Selector analysis: accepted.`, container removed, no residual container. Zero skips (validated by the harness, selector count 8).
* Actual SQL, default regression (same lock and environment): exit 0, `Ran 48 tests in 20.685s`, `OK`, container removed.

Not run by design: full local gate, whole-API suite, browser, hosted CI, any push or PR. The generated SQL password was never printed or stored.

## Criteria

* Outputs reproducible from retained readings: strengthened with actual local SQL Server evidence for the analysis path; still unticked, no claim of whole acceptance.
* R1 to R3 research complete before a derived measure is used beyond an exercise rule: unmet and untouched.
* Thresholds sourced or labelled exercise values: already ticked; untouched.
