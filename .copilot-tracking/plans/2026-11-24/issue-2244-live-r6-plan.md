---
title: Issue 2244 live run 6 plan
ms.date: 2026-11-24
---

* [x] Phase 1 research: read-only live check of revision 0000059 and file hashes.
* [x] Phase 2 critique, once.
* [ ] Phase 3 implement: add read-only fast paths for `_seed`, `_migrate_recommendations`, `_ensure_queue_membership` (core `sqlstore.py`, `mssqlstore.py`) and a test counting `BEGIN IMMEDIATE` on a reopen.
* [ ] Phase 4 validate: `test_mssql_startup_lock`, `test_sqlstore`, mypy, ruff in `src/core`.
* [ ] Phase 5 research note with per-criterion table, index and log entries, review, commit.
