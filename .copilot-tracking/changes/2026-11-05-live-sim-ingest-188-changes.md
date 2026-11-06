---
title: Changes for #188 slice 1
ms.date: 2026-11-05
---

* Modified `src/core/src/zava_forward/core/sensor_consumer.py`, `src/api/tests/test_iot_stream.py`, `src/api/README.md`.
* Added `src/core/tests/test_sensor_consumer_live.py`.
* Validation run: core `tests.test_sensor_consumer_live`, `test_sensor_consumer`, `test_sensor_analysis_store`, `test_live_readings` (68 OK); api `tests.test_iot_stream`, `test_live_simulator` (67 OK); ruff check and format, mypy (CI configuration, tests included, cache /tmp/mypy-188) clean for src/core and src/api.
* Not run: complete gate, full suites, benchmarks, SQL Server (`ZF_SENSOR_MSSQL`) path, any Azure resource. Divergence: none from plan.
