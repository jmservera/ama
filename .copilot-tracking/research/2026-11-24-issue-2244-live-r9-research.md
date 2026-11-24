---
title: Issue 2244 live run 9 research (opening)
ms.date: 2026-11-24
---

Opening record. Base 33b330b83 (forecast fix merged). Goal: prove what can be proven live on revision 0000067, read-only, no deployment, no drill. The issue has no tick-box list; criteria C1 to C5 come from the first run note. The earlier run 8 (commit bd5f4d7397, other branch) is the comparison. Evidence follows below.

## Findings (read-only, 2026-11-24 UTC)

* Only active revision `ca-cutover-test-demo-api--0000067`, created 15:34:05Z, Healthy, 100 percent traffic, 2 replicas (created 15:34:05Z and 15:36:22Z), both running, started, restart count 0.
* `GET /healthz` three times: 200 in 0.19 s, 0.10 s, 0.10 s.
* Last 300 system and console lines: 0 matches for write lock, lock timeout, traceback, probe failure, kill or retry.
* Deployed md5 (via `az containerapp exec`, pty) of `mssqlstore.py` 1392a4776214, `sqlstore.py` a585aa578833, `lawstore.py` 55343f798f45 equal the checkout.
* `python3 -m unittest test_mssql_startup_lock` from `src/core`: 21 tests OK.
* Not performed: holding the SQL write lock (drill, excluded), reading `sys.dm_tran_locks`. No sign-in value read; no browser proof applies.
* Planning Readiness: Ready. Disposition: executed.
