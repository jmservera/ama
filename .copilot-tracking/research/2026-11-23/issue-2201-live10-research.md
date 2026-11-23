---
title: Issue 2201 live10 research
ms.date: 2026-11-23
---

Research disposition: executed (live read-only Azure probe plus code read). Planning Readiness: Ready.

* All four acceptance criteria are ticked on the issue. Earlier workers (live7 to live9) proved criteria 1, 2 and 4 and added receive-side error classes in `iot_stream.py`.
* Live probe 2026-11-23 20:24 UTC: `az containerapp job execution list -g ama -n job-live-receiver` shows 16 Succeeded and 1 Running since the last failure (12:47:30 UTC, a manual run); the 20:00 run was still running at probe time. Failures from 09:30 to 11:30 and 12:42/12:47 UTC are earlier history. Schedule `*/30 * * * *`.
* Uncovered code angle: `live_receiver.main` maps any non-StreamError exception (for example the SQL connector failing before `receiver.run`) to the fixed `Cannot run: RECEIVER_FAILED`, exit 4, with no class name. live9 covered only failures inside `receiver.run`. No test exercises the exit-4 path (`grep RECEIVER_FAILED src/api/tests` is empty).
* Plan: print `error_type=<ExceptionClass>` (class only, never message or traceback) before the fixed code, and add a regression test.
