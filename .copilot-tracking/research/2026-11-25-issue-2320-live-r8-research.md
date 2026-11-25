---
title: Issue 2320 live r8 research
ms.date: 2026-11-25
---

Disposition: executed. Planning Readiness: Ready.

## Question

Why does a quiet `GET /api/briefing` take 2.1 to 16.4 s on revision 0000071 (r7 note)?

## Evidence (read-only)

* `az containerapp show`: min replicas 1, max 4, latest revision `--0000071`. A replica min 0 cold start is ruled out.
* `az sql db list`: database `retrofit` is Standard tier with no auto-pause; SQL serverless resume is ruled out.
* Container log, last 300 lines (about 16:19Z to 16:25Z, no briefing calls from this run): repeated `GET /api/retention` 503 `sql-write-lock-busy` about every 20 s and `map sensor summary unavailable ... sql-write-lock-busy`. Some client or thread holds or contends for the SQL write lock while the demo is otherwise idle. The holder was not identified.
* Code (`store.py` `briefing`): a hit needs `hit[0] == self.version`; `SqlStore.version` is the global DB `seq`, so any write by any client or background worker invalidates it. A miss runs `run_text_task` then `add_record`, which holds `store.lock` and waits on the SQL applock (capped at 2 s by #2379). On busy, `_briefing_unrecorded` answers but never caches that answer, so every following GET repeats the 2 s wait while holding `store.lock`. That matches the 2.1 to 2.4 s cluster and the queueing of concurrent calls.

## Cause

Cache miss recompute plus an uncached busy fallback: each GET during a busy period pays the full capped lock wait. Not cold start, not SQL resume.

## Follow-ups

1. Short-lived cache of the unrecorded answer so repeat GETs return at once.
2. Identify the persistent SQL lock holder (separate issue; needs `sys.dm_tran_locks`).
