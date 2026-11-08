---
title: "Plan: #184 correction 2"
ms.date: 2026-11-08
---

Critique: executed once, before implementation. Verdict: compatible with
confirmed decisions (source-only, no grants, no Azure, no schema widening).
Advice applied directly: assert exact statement set from the test, do not rely
on a mock identity; keep `configure` and DDL out of the receiver path.

## Phases

* [ ] 1. Add `SensorMssqlConnector` (core, new module `sensor_sql.py`):
  `dberror`, `assistant_connection()` over the existing `_Conn` and
  `connection_string`; validates settings at construction, never connects or
  runs DDL, seeding, metadata or queue set-up.
* [ ] 2. `SensorConsumer.__init__` accepts `SqlStore | SensorMssqlConnector`;
  `mssql` is true for `MssqlStore` and the connector. Nothing else in the
  consumer changes (no retained-reading, consent or provenance change).
* [ ] 3. `live_receiver`: share one `_window()` check (SEND and at least 1 s)
  used by `main` BEFORE any persistence object exists and by `run_window`.
  `ZF_STORE=mssql` uses the connector; other values keep `open_store`. Add the
  command/env identity assertions (`ZF_STORE=mssql`, `ZF_SQL_AUTH=msi`,
  `ZF_SQL_CLIENT_ID`) to the receiver main with fixed refusal codes.
* [ ] 4. Docs: drop `sensor_register` from the receiver grant list in
  `infra/README.md`; state that the receiver never runs DDL. Update
  `src/api/README.md` accordingly.
* [ ] 5. Tests: refusal before any store connection for stopped, expired,
  invalid and sub-second control; valid-control entry builds the connector
  only. Task-owned SQL Server test: setup/admin provisions schema via
  `SensorConsumer.configure`; a separate principal gets exactly the documented
  grants; the receiver connector retains one reading; assert identity
  (`SUSER_NAME()`/`USER_NAME()` is the receiver user, not admin), the row, and
  that sensor/application table data and object lists are otherwise unchanged
  (counts and `sys.objects` modify_date snapshot). Registered in the maintained
  `sensor_sql_check.py` only if it fits its existing selector structure.
* [ ] 6. Validate with each command's own exit code: unit tests, ruff check and
  format, mypy (`--cache-dir=/tmp/mypy-184`), Bicep build/lint, infra tests,
  `sensor_sql_check.py` under a non-queued lock attempt.

Out of scope: UI, #1288 Quality logic, any grant, deployment, model call, send.
