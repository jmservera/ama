---
title: Issue 2304 forecast live 503 research (2026-11-24)
ms.date: 2026-11-24
---

# Research: forecast 503 after 13 to 17 s on revision 0000061

Disposition: executing. Opening note; findings follow.

Disposition: executed. Planning Readiness: Ready. Evidence note: `docs/reference/research/issue-2304-live-2026-11-24.md`.

## Findings

* The 2026-11-23 fix is live on revision 0000061 (statements are flat per case) and the 10 s budget works: the live GET returns the named 503 `state: unavailable`, not a hang. Probe 2026-11-24: 503 after 16.77, 13.44, 10.23, 13.44 s while `/api/stats` took 6.08 s and `/api/assistants` 5.4 s.
* Why 13 to 17 s and not 10: `ForecastReads` starts its clock after `_read_connection` has opened the Azure SQL connection, and a statement in flight cannot be cut, so total time is connection time plus 10 s plus the last statement. Even bare reads cost 5 to 6 s on this system, so each remaining round trip is slow.
* The result is recomputed from nothing on every request; a timeout throws the work away, so every retry restarts and cannot succeed if the full read needs more than the budget.
* No SQL write lock is taken: the path is lock-free (`_read_connection`, `rel.read_only()`).
* Fix direction: compute in a background job that is not cut off at the client wait, keep the last answer in a short TTL cache keyed per staff identity and period, and bound the client wait to under 10 s including connection time. The first request after a cold start may still return the named 503 while the job finishes; the retry is served from the cache.

## Follow-ups

1. Owner deploys and re-measures the live forecast.
2. Measure the live statement trace once SQL is reachable.
