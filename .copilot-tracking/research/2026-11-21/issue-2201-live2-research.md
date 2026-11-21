---
title: Issue 2201 live research (second pass)
ms.date: 2026-11-21
---

Research disposition: executed. Planning Readiness: Ready.

## Findings (2026-11-21 22:43 to 23:00 UTC)

* #2210 (end the window normally, skip refused events) is on main. The job image digest `sha256:60b1d026...7878` equals the demo API image; the job was last modified 21:33 UTC.
* 50 retained executions: 41 Failed, 8 Succeeded, 1 Running at the start. Failures are intermittent, both before and after 21:33. Executions 21:30 and 22:00 Failed; 22:30 Succeeded (final stdout line `receipts=5220`, no `rejected=` line, so no refused event in that window).
* Logs of finished replicas are not retained (`ExecutionReplicaNotFound`) and `log-cutover-test` denies this client (`NspValidationFailedError`); a live stream gave only the final stdout line.
* Store and map: `/api/map` (443 homes) and `/api/cases/{id}/sensors` for three granted homes show readings every 5 minutes up to the current minute, `freshness: fresh`, `age_seconds` 24; two withheld homes show `consent-withheld`.

Evidence: `.copilot-tracking/evidence/2026-11-21/issue-2201-live2/`.
