---
title: Issue 2304 live critique (2026-11-24)
ms.date: 2026-11-24
---

# Critique (executed once)

Verdict: proceed, findings applied directly.

* Risk: stale answer after a revoke. Accepted for a counts-only demo forecast; TTL is 60 s and the limit is documented. Authorisation by role is still checked on every request before the cache.
* Risk: unbounded threads. One job per key, daemon thread, job cap 120 s.
* Risk: tests with `FORECAST_BUDGET_SECONDS=-1`. The job reports the timeout and the request re-raises it, so the existing test stays valid.
* Risk: a cold first request still returns 503. Accepted and stated; the retry succeeds from the cache once the job finishes. Live proof needs a deployment (not allowed here).
