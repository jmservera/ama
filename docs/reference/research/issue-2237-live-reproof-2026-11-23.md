---
title: Issue 2237 live re-proof on revision 0000055 (2026-11-23 14:30 UTC)
description: Evidence that live API revision 0000055 contains the 503 write-lock mapping, that the mapping fired in production-like use, that /api/retention answers 200 for the Programme Manager, and a per-criterion table
ms.date: 2026-11-23
---

Synthetic demo, desktop only, resource group `ama`. Refs #2237. No Azure change was made and no resource was created; sign-in values were read at run time and not printed. Files: [issue-2237-live-reproof-2026-11-23/](./issue-2237-live-reproof-2026-11-23/). The cause analysis is in [issue-2237-live-cause-and-fix-2026-11-23.md](./issue-2237-live-cause-and-fix-2026-11-23.md); this note closes the gap it and the [0055 smoke note](./issue-2237-smoke-0055-live-2026-11-23.md) left open.

## Findings

* Live revision `ca-cutover-test-demo-api--0000055` is the only active revision ([revisions.json](./issue-2237-live-reproof-2026-11-23/revisions.json)).
* The deployed code has the fix. `az containerapp exec` on replica `...0000055-7959bcd8f8-mbzml` ran `grep -rl sql-write-lock-busy` and found `/usr/local/lib/python3.12/site-packages/zava_forward/api/server.py` (the marker text exists only in the 503 mapping from #2290).
* The mapping works live. Log Analytics (`ContainerAppConsoleLogs`, last 40 h) shows 14 `http-error GET ... status=503 exc=ProgrammingError cause=sql-write-lock-busy` lines on 0000055 between 2026-11-23 07:09 and 13:39 UTC (12 on `/api/briefing`, 2 on `/api/ai/report`). Before the fix the same contention produced 500s ([law-503-write-lock-busy.json](./issue-2237-live-reproof-2026-11-23/law-503-write-lock-busy.json), [law-lock-events-by-revision.json](./issue-2237-live-reproof-2026-11-23/law-lock-events-by-revision.json)).
* No `/api/retention` 500 has been logged since 2026-11-22 10:34:49 UTC (revision 0000046); the last five are in [law-retention-errors-since-0055.json](./issue-2237-live-reproof-2026-11-23/law-retention-errors-since-0055.json).
* Live probe at 14:30 UTC ([live_probe.py](./issue-2237-live-reproof-2026-11-23/live_probe.py), [result-1430.json](./issue-2237-live-reproof-2026-11-23/result-1430.json)): `/api/me` role `Retrofit Programme Manager`; `/api/retention` 200 with `as_of`, `label`, `records` (0 records); 15 sequential, 20 parallel and 20 mixed requests all 200.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history, not on demand | 11 logged 500s of about 15 s; local regression test reproduces the lock error deterministically; a live lock held over 15 s was not forced (no drills) |
| Find the cause in the demo container logs | Proven | Cause note; lock holder unidentified |
| Fix with a regression test | Proven | #2290 on main (tests in `src/core/tests/test_mssql_startup_lock.py`, `src/api/tests/test_error_logging.py`), deployed on 0000055 as shown above |
| Re-prove 200 live | Proven | 56 of 56 requests 200 on 0000055 at 14:30 UTC; the 503 mapping also observed firing live |

Limits: the 503 was observed on `/api/briefing` and `/api/ai/report`, not on `/api/retention`; the retention-specific 503 path is proven by unit test. Contention continues (14 events), so the underlying lock hold time remains a design follow-up, not part of this fix.
