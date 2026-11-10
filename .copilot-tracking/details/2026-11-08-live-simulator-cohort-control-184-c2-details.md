---
title: "Details: #184 correction 2"
ms.date: 2026-11-08
---

* New `src/core/src/zava_forward/core/sensor_sql.py`: `SensorMssqlConnector(env)`
  with `dberror` (mssql_python.Error) and `assistant_connection()`; construction
  calls `connection_string(env)` only (no connection).
* `src/core/src/zava_forward/core/sensor_consumer.py`: constructor type check and
  `mssql` flag only.
* `src/api/src/zava_forward/api/live_receiver.py`: `_window(control, seconds,
  now) -> float`; `main` calls it before `_persistence(env)`; `_persistence`
  returns the connector for `ZF_STORE=mssql` and `open_store(env)` otherwise.
* Receiver principal statement set (exact grants): SELECT on `dbo.cases`,
  `dbo.sensor_consumer_control`, `dbo.sensor_consumer_policy`; SELECT and INSERT
  on `dbo.sensor_reading`, `dbo.sensor_delivery`,
  `dbo.sensor_data_quality_exception`. Plus AcrPull and Event Hubs Data
  Receiver (Azure scope, not tested locally).
* Local SQL test uses a SQL login/user created by the task-owned fixture with
  exactly those grants; no real Azure grant.
* Tests: `src/api/tests/test_live_control.py` (refusal-before-connect, valid
  entry) and the SQL test beside the maintained sensor SQL tests.
