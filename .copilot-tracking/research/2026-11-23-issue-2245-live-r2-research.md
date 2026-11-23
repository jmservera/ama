---
title: Research for issue 2245 round 2 (employee chat 500 and no generative answer)
ms.date: 2026-11-23
---

Task: issue-2245-live-20261123T153732Z. Opening note; findings follow.

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Live recheck at 15:38 to 15:41 UTC, revision `ca-cutover-test-demo-api--0000055` (created 2026-11-23T03:25, before the thread-create 503 fix of 10:20 in #2300, so the live image lacks it). The first `POST /api/chat/threads` after idle returned 500 after 27 s; the next two returned 200 after 16 s and 9 s, then five returned 200 in about 120 ms. The console log at the same time shows `POST /api/chat/threads status=500 exc=ProgrammingError` and, 28 s earlier, `GET /api/briefing status=503 cause=sql-write-lock-busy`. So the 500 reproduces live and is a driver ProgrammingError of the same class as the lock timeout (the old image names no cause). The 2026-11-22 cause is now probable, not certain.
* The open `SYN-221-PROBE` all-scope AI suspension is still present (restart null), so no model call; restart is a human action and was not performed.
* Gap found: tests cover lock-busy on thread create (503) and on other POSTs (500) but not a different driver error on thread create, which must stay a 500 so the 503 path is not over-broad.

Evidence: [issue-2245-live-r2-2026-11-23/](../../docs/reference/research/issue-2245-live-r2-2026-11-23/).
