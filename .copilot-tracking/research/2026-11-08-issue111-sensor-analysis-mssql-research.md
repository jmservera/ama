---
title: Issue 111 sensor analysis MSSQL test increment, research
ms.date: 2026-11-08
---

Task: `issue111-sensor-analysis-mssql`. Original, isolated RPI for a test-only post-delivery increment. It does not resume any historical CLI session and leaves the earlier issue 111 rounds (r1 to r4 artifacts, stale historical heads and worktrees) unchanged.

Research disposition: executed (fresh source inspection on 2026-11-08).

## Identity

* Worktree `/home/azureuser/source/ama-wt/issue-111-sensor-analysis-mssql`, branch `test/sensor-analysis-mssql-111`, HEAD `4bc1e3f3361a762cc9f0c187d394fdab9a11b033`, clean.
* `origin/main` was fetched at `9d035ee9e4fa34c783571f69e878ffb88ecf0259`. `git diff --stat 4bc1e3f..origin/main -- src` is empty: the single newer commit is a rubric score record. The instructed base `4bc1e3f` therefore stays the candidate base; no rebase.
* Parent 109 engineering and dependency 110 offline ingestion are already on Main (src/core `sensor_analysis*.py`, `sensor_consumer.py`). No unmerged parent PR is depended on.

## Context read

Original case study, addendum purpose and status, `docs/reference/README.md`, `docs/reference/memory.md` (context only), `src/core/README.md` sensor sections, `src/api/README.md` sensor SQL sections. The bounded readiness audit `demo-readiness-1108.json` was read: it found no overlapping open PR or frozen MSSQL test increment and records that `src/` is unchanged. Its research was not copied; the source facts below are from this inspection.

## Confirmed current source facts

* `src/core/tests/test_sensor_analysis_store.py` `RetainedAnalysisTests.setUp` calls `self.skipTest("SQLite-only focused test")` when `consumer.mssql` is true. Seven test methods exist: pure-derivation match and reproducibility, read-only and no task without approved rule, declined/unknown/unmapped consent, any declined control wins, stale and missing readings, unreadable store (deliberate `DROP TABLE sensor_consumer_control`), unmapped or invalid home.
* `src/core/tests/sensor_consumer_fixture.py` `store_at` returns `MssqlStore` when `ZF_SENSOR_MSSQL=1` (with `reset` deleting `cases` rows) and SQLite otherwise.
* `src/core/src/zava_forward/core/sensor_analysis_store.py` is read-only: it calls `home_consent` and `observed_series`, maps `ConsumerError` to INSUFFICIENT with reason `RETAINED_READINGS_UNAVAILABLE` and no priority effect.
* `SensorConsumer._schema` creates the policy, control, delivery, data-quality-exception and reading tables with `IF OBJECT_ID ... IS NULL CREATE TABLE`, so `configure` restores a dropped table. `test_sensor_consumer.SensorConsumerTests.setUp` is the prior art for MSSQL isolation: drop the six sensor tables and delete `cases` row `ZF-2`.
* `src/api/checks/sensor_sql_check.py` starts a uniquely named container (`ama-sensor110-<hex>`, `--memory 3g --cpus 2`, loopback port, random `sa` password, database `sensor110`), runs `unittest test_sensor_ingestion test_sensor_consistency.SqlHandoverTests.test_composed_joint_query_statistics_and_reopened_window_replay -q` with `PYTHONPATH=src/api/tests:src/core/tests`, and removes the container by exact name in `finally`. It has no argument parsing and no result validation (the exit code only).
* Prior art for backend assertion: `SqlHandoverTests` asserts `consumer.mssql == (ZF_SENSOR_MSSQL == "1")`. Prior art for unit-testing a harness: `src/api/tests/test_capacity_browser_check.py` (`checks.*` imports, patching, no browser or Docker).
* No existing test selects `RetainedAnalysisTests` on MSSQL, and no test covers `sensor_sql_check.py` selection or result handling. The README documents the harness as running only the ingestion and handover selectors.

## Environment

* The preinstalled `zava-forward-*` distributions point at a different checkout (`/home/azureuser/source/ama`), so they are not candidate-qualified. A private venv at `/tmp/ama-issue111-rt/venv` is created and the candidate's `src/core[sql]`, `src/agents` and `src/api` are installed editable with pip, plus `ruff==0.17.1` and `mypy==2.4.0` as pinned in CI.
* Docker is available. Heavy ownership is inspected immediately before SQL (see the changes record).

## Findings and constraints

* Smallest coherent slice: a new MSSQL subclass of the existing tests (no edit to the SQLite test file or shared fixture), an allowlisted selector for the harness and a harness unit test. No production change appears necessary; this is confirmed or refuted only by actual MSSQL execution.
* Skips must not silently pass: unittest exits 0 with `OK (skipped=N)`. The harness therefore needs result validation (count and zero skips) for the new selector.
* Driver representation differences, if any, can only be found by running. The plan normalises only observed, documented differences.

## Unmet criteria (unchanged by this increment)

* Outputs reproducible from retained readings: gains actual-MSSQL evidence for the analysis path only if the run passes; the criterion is not claimed as met by this PR (Refs, not Closes).
* Research R1 to R3 complete before a derived measure is used beyond an exercise rule: unmet and untouched; needs human and competent method sign-off.
* Thresholds sourced or labelled exercise values: already ticked; not edited.

Planning Readiness: Ready.
