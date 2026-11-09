---
title: "Changes: #184 correction 2"
ms.date: 2026-11-08
---

Source-only. No Azure change, send, grant, device registration or model call.
Research and Plan/Details were committed first (`a5c2468b`) before any source edit.

## Files

* `src/core/src/zava_forward/core/sensor_sql.py` (new): `SensorMssqlConnector`.
* `src/core/src/zava_forward/core/sensor_consumer.py`: constructor accepts the
  connector; `mssql` flag true for it. No retained-reading, consent or
  provenance change. Shared-contract note for #1288: constructor only.
* `src/api/src/zava_forward/api/live_receiver.py`: `window_seconds()` runs in
  `main` before any persistence; `persistence()` returns the connector for
  `ZF_STORE=mssql`, else `open_store`.
* `src/api/tests/test_live_control.py`, `src/api/tests/test_live_receiver_sql.py`
  (new), `src/api/checks/sensor_sql_check.py` (adds the SQL test to the default
  selector), `infra/README.md` (exact grants, `sensor_register` removed, no
  DDL), `src/api/README.md`.

## Validation (each command's own exit; output redirected to files)

| Check | Exit | Result |
| --- | --- | --- |
| Unit: test_live_control, test_live_simulator, test_iot_credential_hygiene, test_dependency_rule, test_live_readings, test_iot_stream, test_live_receiver_sql, test_sensor_consumer, test_sensor_ingestion (worktree PYTHONPATH) | 0 | 216 OK, 2 skipped (the SQL-only receiver tests, which need the task-owned SQL Server) |
| `ruff check --no-cache src/api src/core/src` | 0 | pass |
| `ruff format --check` on 6 touched files | 1 | only `sensor_consumer.py` differs, and it is already unformatted at `c80f507b` (pre-existing); not reformatted to keep the shared file diff minimal |
| `mypy --cache-dir=/tmp/mypy-184` on live_receiver, live_simulator, live_control, sensor_sql, sensor_consumer | 0 | no issues in 5 files |
| `az bicep build` and `lint`, receiver and simulator jobs | 0, 0, 0, 0 | pass (only a Bicep upgrade notice) |
| Infra test_container_contract, test_identity_rbac, test_bicep_policy | 0 | 76 OK |
| `sensor_sql_check.py` under `flock -n /tmp/ama-rpi-heavy.lock`, task-owned SQL Server, worktree venv | 0 | 70 OK, no skips (68 prior + 2 new) |

SQL history, preserved: the first C2 attempts failed on my test's own defects
(login cleanup while sessions were open; `sys.objects.type` padding that made
the state comparison empty). Both were test bugs, fixed, then 70 OK. The
earlier lock holder (task 1288) had finished before the successful non-queued
attempt; no duplicate SQL job was started. The C1 first-run import errors came
from stale editable installs; the same temporary venv was used and removed.

The SQL test uses a disposable login holding exactly the documented grants
(SELECT on cases, sensor_consumer_control, sensor_consumer_policy; SELECT and
INSERT on sensor_reading, sensor_delivery, sensor_data_quality_exception),
asserts `SUSER_NAME()` is that login and not sysadmin, `CREATE TABLE` and
`DELETE FROM cases` are denied, a retained live row is written and replays, no
`sys.objects` entry or modify_date changes, only `sensor_reading` and
`sensor_delivery` row counts change, and a missing table is refused rather than
created.

Not run: browser suite, full gate, benchmarks, any cloud step. Not proven:
that the pre-C2 `open_store` path fails under these grants (no mutation run).
Historical limitation kept: C1's Bicep and infra exits were not transcribed.
