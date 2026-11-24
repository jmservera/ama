---
title: Issue 2237 retention 500 live re-proof on revision 0000061 (2026-11-24)
description: Live proof that GET /api/retention answers 200 on revision 0000061 and that lock timeouts now answer 503 instead of 500 on revisions 0000058 to 0000060, with a per-criterion table
ms.date: 2026-11-24
---

Synthetic demo, desktop only. Refs #2237. Live revision `ca-cutover-test-demo-api--0000061` (created 2026-11-24 12:28 UTC, healthy, 100% traffic; main 470c84c94). Evidence: [issue-2237-live-reproof-2026-11-24/](./issue-2237-live-reproof-2026-11-24/). The demo employee sign-in was read at runtime and is not recorded; e-mail addresses are scrubbed. No deployment or Azure change was made.

## Evidence

| Observation | Evidence file |
| --- | --- |
| Signed in as the demo employee: `/api/me` role `Retrofit Programme Manager`; `/api/retention` 200 with keys `as_of`, `label`, `records` (0 records); 15 sequential, 20 parallel and 20 mixed requests all 200 (55 of 55) | [r61-2026-11-24T12.json](./issue-2237-live-reproof-2026-11-24/r61-2026-11-24T12.json), [live_probe.py](./issue-2237-live-reproof-2026-11-24/live_probe.py) |
| Container console, last 30 h: 30 lines `http-error GET /api/retention status=503 exc=ProgrammingError cause=sql-write-lock-busy` (revisions 0000058: 13, 0000059: 11, 0000060: 6) and no `status=500` line for the endpoint. This is the lock timeout that produced the 500s of 2026-11-21 and 2026-11-22, now mapped to 503 with `Retry-After` by the fix | [law-retention-http-error-console.json](./issue-2237-live-reproof-2026-11-24/law-retention-http-error-console.json) |
| HTTP log, last 30 h, by revision and status: 0000058 503 x13; 0000059 503 x10 (plus 8 client-closed, status 0); 0000060 503 x6; no 500 on any revision; the single 0000061 row is a 200 (the rest of the 55 probes had not reached the log when queried) | [law-retention-status-by-revision.json](./issue-2237-live-reproof-2026-11-24/law-retention-status-by-revision.json) |

The earlier 500s, their 15 s duration and the SQL error 50002 cause are in [the 2026-11-23 note](./issue-2237-live-cause-and-fix-2026-11-23.md).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history and observed live after the fix | 11 logged 500s (2026-11-21 to 22); the same lock timeout recurred 30 times on 0000058 to 0000060 and is now a 503. No deliberate reproduction (no drills) |
| Find the cause in the demo container logs | Proven | Console, HTTP and SQL `Errors` records in the 2026-11-23 note and the 503 lines above; lock holder still unidentified |
| Fix with a regression test | Proven, now live | Tests in `test_mssql_startup_lock.py` and `test_error_logging.py`; the live 503 lines show the fix running |
| Re-prove 200 live | Proven on 0000061 | 55 of 55 requests 200 as Programme Manager |

Residual: a user hitting a lock timeout still sees a 503 retry message; reducing lock hold time (finding the writers) is a separate design change. The 503 rate was 29 requests in 30 h.
