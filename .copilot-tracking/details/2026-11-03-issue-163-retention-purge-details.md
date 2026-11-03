---
title: "Issue 163 retention purge details (2026-11-03)"
ms.date: 2026-11-03
---
* `chatthreads.py`: `purge_threads(cutoff)` on MemoryRepo and SqlRepo deletes threads with `updated_at` before the cutoff and their messages; returns (threads, messages).
* `chat_privacy.py`: `purge_retention(now=None)` reads the decision; with no `retention_days` returns zeros and `applied` False; otherwise cutoff is now minus the period, deletes threads and expired memory in one transaction. Counts only, no content.
* Human approval, consent and model boundaries are unchanged; no UI change, so the web guidance is not engaged.
* Tier: focused. Touches the SQL repository: complete gate not run, left to the coordinator.
