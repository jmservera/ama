---
title: Issue 188 live handover verifier changes
ms.date: 2026-11-01
---

* Plan: ../../plans/2026-11-01/2026-11-01-issue-188-live-handover-verifier-plan.md
* Added `SensorConsumer.observed_series` (src/core `sensor_consumer.py`), `src/api/src/zava_forward/api/sensor_handover_verify.py`, test extensions in `src/api/tests/test_sensor_consistency.py`, API README section, research plan section and log entry.
* Critique (single pass, executed, verdict: proceed): home identifiers are lowercase for stock homes, so validation uses the printable-ASCII bound, not the uppercase identity rule (applied; first test run failed on this). Zero-tolerance default uses the `ZERO_TOLERANCE` singleton (ruff B008).
* Validation (local focused tier, venv with pip): api `test_sensor_consistency` + `test_sensor_ingestion` 81 tests OK; core `test_sensor_consumer` + `test_sensor_handover` 42 OK; ruff check and format --check clean for src/api and src/core; mypy src/core clean; src/api mypy shows only 33 pre-existing missing `playwright` stubs, none in touched files.
* Not run: SQL Server (`ZF_SENSOR_MSSQL`), Azure SQL, live Hub, full local RPI gate (CI is the evidence).
