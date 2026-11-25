---
title: Issue 2237 retention live re-proof on revision 0000068 (2026-11-25)
description: Fresh live proof that GET /api/retention answers 200 for the Programme Manager on revision 0000068, that the 503 mapping fires live under lock contention, and that no 500 was logged for the endpoint in 48 hours
ms.date: 2026-11-25
---

Synthetic demo, desktop only. Refs #2237. Live revision `ca-cutover-test-demo-api--0000068` (created 2026-11-24 16:18 UTC, healthy, 100% traffic). Evidence: [issue-2237-live-reproof-2026-11-25/](./issue-2237-live-reproof-2026-11-25/). The demo employee sign-in was read at runtime and is not recorded; e-mail addresses are scrubbed. No Azure change was made and no throwaway resource was created.

## Evidence

| Observation | Evidence file |
| --- | --- |
| Playwright sign-in as the demo employee: `/api/me` 200, role `Retrofit Programme Manager`; `/api/retention` 200 with keys `as_of`, `label`, `records` (0 records); 15 sequential and 20 parallel requests all 200 | [r68-2026-11-25T14.json](./issue-2237-live-reproof-2026-11-25/r68-2026-11-25T14.json), [live_probe.py](./issue-2237-live-reproof-2026-11-25/live_probe.py) |
| In the same probe 2 of the 10 `/api/retention` requests in the 20-request mixed burst answered 503 (the other 18 requests, including all 10 `/api/cases`, answered 200); none answered 500 | same file |
| Container console, last 48 h, `http-error` lines for `/api/retention`: 39 lines, all `status=503` (0000058: 13, 0000059: 11, 0000060: 6, 0000063: 1, 0000065: 1, 0000068: 8); none with `status=500` | [law-retention-http-error-48h.json](./issue-2237-live-reproof-2026-11-25/law-retention-http-error-48h.json) |
| `status=500` lines in the same window belong to other endpoints or revisions (0000055 to 0000068); none name `/api/retention` | [law-status500-any-48h.json](./issue-2237-live-reproof-2026-11-25/law-status500-any-48h.json) |
| Active revision list | [revisions.json](./issue-2237-live-reproof-2026-11-25/revisions.json) |

The probe's 503 responses are not in the log query above because Log Analytics ingestion lags the probe by several minutes; the latest ingested 503 is 2026-11-24 18:42 UTC. The cause (SQL write lock timeout, error 50002, 15 s) and the fix are in [the 2026-11-23 note](./issue-2237-live-cause-and-fix-2026-11-23.md); earlier re-proofs are in [the 2026-11-24 note](./issue-2237-live-reproof-2026-11-24b.md).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history; not reproduced on demand | 11 logged 500s on 2026-11-21 to 22; the same lock contention now surfaces as 503 (2 more in this probe). Deliberate reproduction is excluded (no drills) |
| Find the cause in the demo container logs | Proven | SQL write lock timeout in console, HTTP and SQL error records (2026-11-23 note); the lock holder is unidentified |
| Fix with a regression test | Proven, running live | `test_mssql_startup_lock.py` and `test_error_logging.py`; the 503 mapping answered live in this probe |
| Re-prove 200 live | Proven on 0000068 | `/api/retention` 200 as Programme Manager, 35 of 35 sequential and parallel requests plus 8 of 10 in the mixed burst |

Residual: a lock timeout answers 503 with a retry message instead of 500. Finding and shortening the writers that hold the lock is a design follow-up; it is not needed for the demo acceptance.
