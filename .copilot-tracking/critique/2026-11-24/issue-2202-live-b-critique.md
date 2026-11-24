---
title: Issue 2202 live critique b, 2026-11-24
ms.date: 2026-11-24
---

## Critique (executed once, final candidate)

* Verdict: proceed.
* Risk 1: the cause is probable, not proven (watcher stop at control expiry is the other edge cause). Disposition: state it as probable in the note; the fix only covers the deadline case and leaves stop semantics alone. Applied.
* Risk 2: swallowing a post-deadline event could hide data loss. Disposition: the event is not admitted or checkpointed, so it is replayed by the next window (no checkpoint store, lookback start). Accepted.
* Risk 3: a src change raises the tier. Disposition: full tier recorded; gates left to the coordinator. Applied.
* No finding conflicts with a confirmed owner decision.
