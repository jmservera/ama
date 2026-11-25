---
title: Issue 2320 live r8 critique
ms.date: 2026-11-25
---

Executed once on the final candidate plan. Verdict: proceed.

* Risk: a cached unrecorded answer could show stale cases. Mitigation: 10 s TTL, key includes the visible case ids, answer already says it is not recorded, and any later successful record replaces it.
* Risk: hiding a lock problem. Accepted: the holder is a separate follow-up; the cache only stops repeated 2 s waits.
* Compatible change: also drop the busy entry when a record succeeds.
* Not changed: write lock design, `store.lock` scope (larger refactor, routed to follow-up).
