---
title: Issue 120 time capture in the shared SQL store, research
description: Evidence for moving time capture out of a local SQLite file and separating requester from enabler
ms.date: 2026-10-15
---

## Task

Task `issue-120`, slug `time-capture-shared-store` (PR 267 review follow-up).

## Evidence

* `mvp/zavaforward_mvp/timecapture.py` opened its own `time.sqlite` with `AUTOINCREMENT`, `PRAGMA table_info` and `INSERT OR IGNORE`; none of it ran on Azure SQL and a file on an App Service instance is not shared, backed up or access controlled with the case store.
* `SqlStore` and `MssqlStore` expose `assistant_connection()`, `_limit()` and the `_meta_set` / `_insert_ignore` dialect pattern; `assistants.py` already keeps per-dialect DDL constants (`SQLITE_DDL`, `MSSQL_DDL`) and `test_mssqlstore` scans for SQLite-only syntax outside dialect hooks.
* `MANAGER_ROLES` has two roles (Retrofit Programme Manager, Programme Support Officer); seeded demo data has one manager role only.
* Local run of the mssql CI selection against a SQL Server 2022 container passed after merging `origin/main` (85 tests); the earlier CI failure came from SQLite-only syntax reaching SQL Server before the `_meta_set` fix.

## Disposition

Research disposition `executed`. Planning Readiness `Ready`.
