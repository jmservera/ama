---
title: Issue 2244 live run 7 research (opening)
ms.date: 2026-11-24
---

Opening record. Scope: the issue has no tick-box list; criteria C1 to C5 come from the first run note. Base 470c84c94 already carries the start-up fast paths (`_recommendations_current`, `_seed` and queue early returns). Goal: prove what can be proven live against revision `ca-cutover-test-demo-api--0000061`, read-only, no deployment, no drill. Evidence follows below.

## Findings (read-only, 2026-11-24 UTC)

* Latest and ready revision `ca-cutover-test-demo-api--0000061`, created 12:28:56Z, Healthy, 100 percent traffic, only active revision. Probes: StartUp 40 x 3 s, Readiness 3 x 5 s, Liveness 6 x 10 s.
* Replica `...-zxk4v` created 12:28:57Z, container started 12:29:38Z, restart count 0; second replica started 12:39:35Z, restart count 0. System and console logs (last 300 lines) hold no probe failure, kill, restart, lock or traceback line.
* `GET /healthz` three times: 200 in 0.32 s, 0.29 s, 0.49 s.
* Deployed md5 of `mssqlstore.py` 1392a477..., `sqlstore.py` a585aa57..., `lawstore.py` 55343f79... equal the base checkout, so the live revision carries the retry, read-only schema, seed, queue and recommendation fast paths.
* Not performed: holding the SQL write lock (a drill, excluded by the owner) and any SQL read of `sys.dm_tran_locks`. No sign-in value was read; no browser proof applies to a start-up path.
* Planning Readiness: Ready. Disposition: executed.
