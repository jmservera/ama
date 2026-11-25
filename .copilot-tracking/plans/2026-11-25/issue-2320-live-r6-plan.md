---
title: Issue 2320 live r6 plan
ms.date: 2026-11-25
---

* [x] Phase 1: add `SqlStore.write_wait(ms)` (no-op context) and an `MssqlStore` override backed by a thread-local `_Conn` wait used by `_begin`.
* [x] Phase 2: wrap the briefing recording step in `write_wait(2000)`.
* [x] Phase 3: tests (BEGIN uses the override then reverts; briefing cache hit takes no write lock; briefing uses the short wait).
* [x] Phase 4: live re-check and research note with per-criterion table.
