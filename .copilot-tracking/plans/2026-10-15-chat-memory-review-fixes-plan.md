---
title: Chat memory review fixes plan (PR 285)
ms.date: 2026-10-15
---

* [x] Time-ordered memory ids (CI flake).
* [x] Require known task in `add_memory`; empty or unknown task raises.
* [x] `_live` filter used by list, edit and prompt view.
* [x] `_admin` reads role from `store.staff`.
* [x] Idempotent ALTER for SQLite (`sqlstore.py`) and Azure SQL (`MSSQL_MIGRATE`).
* [x] Docs, log and PR body record open owner decisions.
* Critique: executed once, no conflicts with confirmed decisions.
