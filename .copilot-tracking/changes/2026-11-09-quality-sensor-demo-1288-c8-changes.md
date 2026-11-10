---
title: Quality sensor demo 1288 C8 recovery changes
ms.date: 2026-11-09
---

Recorded 2026-11-09T08:40Z. Seed `391e42f0d`; local merge of `origin/main` `b46a9ad9a` as `d808e83f1` (no conflicts, no rebase). Refs #1288, #107.

## Source

* `src/api/tests/test_assistants.py`: `MssqlFixture.setUp` also drops `assistant_dispatch_gate` and `assistant_schedule` (tables added in C5 to C7 that the fixed drop list predated). Test fixture only; no product source change.

## Evidence (demo-targeted tier, merged head plus this edit)

Worktree venv `.venv-1288` (editable `src/core`, `src/agents`, `src/api`; hashed API requirements). Commands run from `src/api`, `PYTHONPATH=../core/tests:../agents/tests`, `python -m unittest discover -s tests -p <file>`.

* SQLite and loopback (before the fixture edit, merged head): `test_quality_sensors_c7` 48 OK, 7 skipped; `test_quality_sensors` 187 OK, 92 skipped; `test_assistants` 120 OK, 58 skipped; `test_technical_quality_screens` 16 OK; `test_sensor_consistency` 38 OK; `test_sensor_handover_demo` 4 OK; `test_sensor_sql_check` 4 OK.
* Actual SQL Server 2022 (owned disposable container `zf-1288-sql`, nonqueued `flock -n /tmp/ama-rpi-heavy.lock`, `ZF_TEST_MSSQL=1`, loopback only; removed afterwards; foreign `zf-1292-sql` untouched).
  * Run 1 (before the fixture edit, adverse, retained): `test_assistants` 120 OK; `test_quality_sensors_c7` FAILED (1 error, `SENSOR_DISPATCH_IN_FLIGHT` from a stale `ZF-2` gate row); `test_quality_sensors` FAILED (1 failure, leftover gate row `1 != 0`). Logs `/tmp/c8-sql-test_*.txt`, `/tmp/c8-sql-run.log`.
  * Run 2 (after the fixture edit): `test_quality_sensors_c7` 48 OK, 0 skipped (72 s); `test_quality_sensors` 187 OK, 0 skipped (370 s); `test_assistants` 120 OK, 0 skipped (162 s). All exits 0. Logs `/tmp/c8-sql-run2.log`, `/tmp/c8-sql-test_*.txt` (overwritten by run 2; run 1 results are quoted above).
* So the C7 SQL Server statements (gate table, `COL_LENGTH` migration, `OFFSET/FETCH` adoption, trigger names) now have executed local engineering evidence. Query plans were not captured.

## Not run (missing prerequisites)

* Browser and axe for the employee Quality sensor UI: no existing browser check covers the sensor/flag surface (`assistants_browser_check.py` has no sensor path) and Playwright is not installed in this worktree environment; no new check was written in this recovery.
* #184/#1292 integration, FULL gate (not required by the owner's demo tier), actual model call, live walkthrough, hosted CI.
