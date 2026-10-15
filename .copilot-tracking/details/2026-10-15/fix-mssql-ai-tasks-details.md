---
title: mssql CI fix phase details
task_slug: fix-mssql-ai-tasks
ms.date: 2026-10-15
---

## Phase 1

`mvp/zavaforward_mvp/sqlstore.py` `_proc_write`: replace the direct `INSERT OR REPLACE INTO meta` with `self._meta_set(key, body)`. The MERGE in `MssqlStore._meta_set` is already proven by the seeding path. It runs inside the save transaction that holds the exclusive application lock, so no HOLDLOCK is needed.

## Phase 2

`mvp/tests/test_mssqlstore.py`: `SharedSqlIsPortableTests` (always runs) records statements from save paths and statically confines `INSERT OR REPLACE/IGNORE` to `_meta_set` and `_insert_ignore` in sqlstore.py and assistants.py. `TABLES` in `wipe()` gains the four assistant tables.

## Phase 3

`cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests`, then the CI command with `ZF_TEST_MSSQL=1` against `mcr.microsoft.com/mssql/server:2022-latest`.
