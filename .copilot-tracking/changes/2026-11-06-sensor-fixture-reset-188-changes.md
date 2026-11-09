---
title: Changes for #188 sensor test-fixture reset isolation
ms.date: 2026-11-06
---

* Planning commit f6920bc4 (research, plan, details) preceded every edit below.
* `src/core/tests/sensor_consumer_fixture.py`: added `SENSOR_STATE_TABLES`; `store_at(reset=True)` now also clears the five consumer tables beside the existing MSSQL `cases` delete, and clears them in an existing constructed SQLite file via stdlib `sqlite3` (table list read from `sqlite_master`, no broad handler). reset=False is unchanged.
* `src/core/tests/test_sensor_consumer_live.py`: one regression, `test_reset_clears_retained_state_but_reopen_preserves_it`. RED before the fix (`1 != 0 : sensor_reading`, /tmp/188-light-r15/red.log), GREEN after.
* No runtime, schema, retention, consent, calibration, selector, assertion or threshold change. Wrapper and helper untouched.
* Checks (bytecode off, ambient ZF_* cleared, explicit i188 PYTHONPATH, import proof: fixture and consumer resolve under i188 `src`): live module 10 tests OK; sensor consistency, live, ingestion, consumer, analysis store, retrofit retained store, historical backfill and iot stream 199 tests OK, 0 skips; after formatting live, consistency, consumer OK. Ruff check first failed E501 (103 > 100) at fixture line 90 (/tmp/188-light-r15/ruff-1-failed.log); `ruff format` fixed it; then Ruff check and format pass. mypy core 128 files and api 24 files, no issues (external cache /tmp/188-light-r15/mypy). Logs in /tmp/188-light-r15.
* Not run: any SQL, Docker, gate, `--changed`, install. The MSSQL effect is unverified until an admitted owned run; r13 remains the actual RED for it.
