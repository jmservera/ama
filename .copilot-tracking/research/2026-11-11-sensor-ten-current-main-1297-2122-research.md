---
title: Sensor ten-test MSSQL current-main research (issue 1297, AC2)
ms.date: 2026-11-11
---

Task slug: `sensor-ten-current-main-1297-2122`. Research disposition: executed. Planning Readiness: Ready.

## Pinned identity

* Worktree `/home/azureuser/source/ama-demo-wt/issue-1297-current-ten-2122`, branch `test/sensor-ten-current-main-2122`.
* `HEAD` and fetched `origin/main` are both `077ad5ad20293a1d79932ea14e9f639dd11e5a22`; tree `d1dde25bc3476772bd9d97711558ed87d1f7a035`; worktree clean before this task.
* Runner and sensor test sources last changed by 1312 (`1464b4d85`, runner) and 1304 (`23e944c1f`, sensor test files); no application, test, runner or workflow edit is made here.

## Findings

* `tools/rpi-checks.py` pins `SENSOR_MSSQL_REQUIRED_TESTS` for class `MssqlRetainedAnalysisTests` in module `test_sensor_analysis_mssql`: ten methods (the nine inherited `test_sensor_analysis_store.RetainedAnalysisTests` methods plus `test_reopened_store_reproduces_signal_without_writes`). The merged 1299 runner pinned eight (`b46a9ad9a`).
* The canonical dispatch (`Runner.sql`, line 2578 area) runs, with cwd `src/api`, `python -m unittest -v test_sensor_analysis_mssql` under `ZF_SENSOR_MSSQL=1` plus the owned-SQL environment (`ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, owned published port, `ZF_SQL_DATABASE=rpi_disposable`, password auth as `sa`, trust-cert) and `PYTHONPATH` `src/api/tests:src/core/tests:src/agents/tests`.
* The test class skips unless `ZF_SENSOR_MSSQL=1` and its `setUp` asserts `consumer.mssql`, so a pass cannot occur on a non-MSSQL backend.
* Existing evidence: 1299 exact-head full receipt covers eight tests with zero skips; 1312 supplies tool regressions only. The 2026-11-10 sensor actual-main review (440) only routes #1297 follow-up. No existing artifact records an execution of the current ten selectors. Duplicate evidence is therefore not present.
* Environment facts at 2026-11-11T21:26Z: Docker 29.9.0 with the `mcr.microsoft.com/mssql/server:2022-latest` image present locally (`cf8f0ab2ebe6`); `/tmp/ama-rpi-heavy.lock` exists, not held (`lsof` empty); about 6.7 GiB available memory, 4 CPUs, load about 4.6 from an unrelated unit-test process outside the lock; no containers present.
* Python 3.12.3 has `mssql-python 1.15.0`, the `libltdl`/`libkrb5` libraries load, but editable `zava_forward` installs point at a different checkout (`/home/azureuser/source/ama`). Source identity must therefore be proven by explicit import paths into this worktree.

## Limitations

* This is a focused observation, not the AC5 full receipt, not independent review and not hosted CI.
* The observation is a separate invocation of the runner's selector, not a receipt produced by the runner; it does not prove runner dispatch itself (covered by 1299/1312 regression tests).
