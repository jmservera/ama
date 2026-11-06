---
title: Details for #188 real-SQL coverage correction
ms.date: 2026-11-06
---

* Phase 1, tests first: add the backend assertion to `WeatherContinuityTests.seeded`, `LiveEnvelopeReplayTests.seeded` (`src/api/tests/test_sensor_consistency.py`) and `LiveReadingTests.setUp` (`src/core/tests/test_sensor_consumer_live.py`). Import `MssqlStore` lazily, only when `ZF_SENSOR_MSSQL == "1"`, so SQLite runs do not require the SQL driver path. Run the three modules on SQLite and confirm they stay green.
* Phase 2, helper: extend the `unittest` selector list in `src/api/checks/sensor_sql_check.py`. Check by static reading that the selected set matches the README. Syntax check with `compile()`; no bytecode.
* Phase 3, docs and records: update the api README sensor SQL sections and, if listed there, the core README; write changes and review artifacts and the state record for this slice; commit with a Conventional Commit, Copilot trailer and the repository-local privacy-safe identity from `gh api user`.
* Verification handoff (not run here): admitted owner runs `python src/api/checks/sensor_sql_check.py` under the coordinator's lock decision and records actual exit, run count, skips and the backend proof; then the maintained FULL gate. Results are recorded as supplementary evidence and never as fabricated receipt entries.
* Stop conditions: any failed check preserves output and stops; no automatic retry; no change to thresholds or schemas to obtain green.
