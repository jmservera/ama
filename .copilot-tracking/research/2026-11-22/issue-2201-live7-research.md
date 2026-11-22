---
title: Issue 2201 live7 research (receiver streak on current image, SQL S3 DTU)
ms.date: 2026-11-22
---

Research disposition: executed (read-only Azure). Planning Readiness: Ready.

* Job digest 541068 on every execution since 12:01 UTC; scheduled runs 14:00 to 18:00 Succeeded (nine); 13:30 Failed.
* SQL `retrofit` Standard 100 DTU (S3) since 13:54 UTC; DTU max 89 percent after, 100 percent before; connection_failed and deadlock 0.
* Log Analytics (as approved): one failure line, 13:30 `IOT_CALLBACK_FAILED`, none after.
* Map probe 18:32 UTC: 200, readings to 18:30:00Z fresh.
* Evidence: `.copilot-tracking/evidence/2026-11-22/issue-2201-live7/`.
* Gap: exception class behind `IOT_CALLBACK_FAILED` not logged (full-tier source change, out of scope).
