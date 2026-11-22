# Research: issue 2245 employee chat thread creation 500 (2026-11-22)

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Main check: `b6a8c0fd9a` (#2267) already cut avoidable ledger writes on chat admission for 2245; `e36fee3027` (#2249) made the AI-hold banner honest; `e4f99600ac` (#2227) serialises statements on the shared SQL connection; `42546c9221` (#2273) retries the start-up lock. Thread creation code is unchanged since `a6c0910c97`.
* Cause class of the 500: container console shows `POST /api/chat/threads status=500 exc=ProgrammingError at=exceptions.py:583:raise_exception` at 19:44:05 UTC on revision 0000053. `BEGIN IMMEDIATE` runs `sp_getapplock ... @LockTimeout 15000` then `THROW 50002` (mssqlstore.py), which the driver raises as ProgrammingError. Thread creation takes the lock twice (insert, then audit ledger entry), measured on the SQL store.
* Live probe (revision 0000053, 23:03 UTC): 12 of 12 `POST /api/chat/threads` returned 200 (0.07 to 2.73 s) including after 20 s idles; the 500 was not reproduced. One ask returned the plain hold answer with no model call (suspension SUS-1 open).
* Which image is deployed relative to #2267 and #2273 cannot be read (ACR and Log Analytics refuse this client).

## Gap

Main has no test pinning the number of write-lock transactions in thread creation.
