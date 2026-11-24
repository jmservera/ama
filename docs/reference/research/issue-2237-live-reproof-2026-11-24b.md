---
title: Issue 2237 retention 500 live re-proof on revision 0000067 (2026-11-24)
description: Live proof that GET /api/retention answers 200 on revision 0000067 and that no 500 has been logged for it since the 503 mapping fix, with a per-criterion table
ms.date: 2026-11-24
---

Synthetic demo, desktop only. Refs #2237. Live revision `ca-cutover-test-demo-api--0000067` (created 2026-11-24 15:34 UTC, healthy, 100% traffic; forecast fix merged). Evidence: [issue-2237-live-reproof-2026-11-24b/](./issue-2237-live-reproof-2026-11-24b/). The demo employee sign-in was read at runtime and is not recorded; e-mail addresses are scrubbed. No deployment or Azure change was made and no throwaway resource was created.

## Evidence

| Observation | Evidence file |
| --- | --- |
| Signed in as the demo employee with Playwright: `/api/me` 200, role `Retrofit Programme Manager`; `/api/retention` 200 with keys `as_of`, `label`, `records` (0 records); 15 sequential, 20 parallel and 20 mixed (half `/api/cases`) requests, 56 of 56 including the first, all 200 | [r67-2026-11-24T15.json](./issue-2237-live-reproof-2026-11-24b/r67-2026-11-24T15.json), [live_probe.py](./issue-2237-live-reproof-2026-11-24b/live_probe.py) |
| Container console, last 36 h, `http-error` lines for the endpoint by revision: 0000058: 13, 0000059: 11, 0000060: 6, 0000063: 1, 0000065: 1, all `status=503`; none with `status=500` and none on 0000067 | [law-retention-http-error-console.json](./issue-2237-live-reproof-2026-11-24b/law-retention-http-error-console.json), [law-retention-all-lines-by-revision.json](./issue-2237-live-reproof-2026-11-24b/law-retention-all-lines-by-revision.json) |

The 500s of 2026-11-21 and 2026-11-22, their 15 s duration and the SQL error 50002 lock timeout cause are in [the 2026-11-23 note](./issue-2237-live-cause-and-fix-2026-11-23.md); the 0000061 re-proof is in [the earlier 2026-11-24 note](./issue-2237-live-reproof-2026-11-24.md).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history; not reproduced on demand | 500s logged 2026-11-21 to 22; the same lock timeout recurred (32 lines in 36 h) and now answers 503. Deliberate reproduction is excluded (no drills) |
| Find the cause in the demo container logs | Proven | SQL write lock timeout in console, HTTP and SQL error records (2026-11-23 note); lock holder still unidentified |
| Fix with a regression test | Proven, running live | Tests in `test_mssql_startup_lock.py` and `test_error_logging.py`; 503 lines confirm the mapping on 0000058 to 0000065 |
| Re-prove 200 live | Proven on 0000067 | 56 of 56 requests 200 as Programme Manager (46 to `/api/retention`) |

Residual: a user who hits a lock timeout sees a 503 with a retry message; the writers holding the lock are a separate design follow-up.
