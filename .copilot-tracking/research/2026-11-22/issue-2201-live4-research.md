---
title: Issue 2201 live4 research, 2026-11-22 13:40 UTC
---

Task 2201-live-20261122T133906Z. Disposition: executed (read-only Azure). Parent: 2201-live-20261122T051147Z.

* Scope: every scheduled `job-live-receiver` run since 10:34 UTC; the employee map; failed-run logs and cause.
* Findings: scheduled 10:00 Succeeded, 10:30 Stopped, 11:00 Failed, 11:30 Failed, 12:00 Succeeded (temporary `--seconds 240`), 12:30 Succeeded, 13:00 Succeeded, 13:30 Failed. Manual starts carry random names.
* Log Analytics access is refused (network security perimeter); job logs show no replica. Exit codes are not in execution records.
* Template differs between 11:30 and 12:30 only by `ZF_RECEIVER_BATCH_SIZE=10`; 13:30 failed with settings identical to 13:00. SQL S0 at 100 percent DTU 12:55 to 13:50.
* Map probe 13:55 UTC: 200, 443 items; case readings to 13:35:00Z, stale.
* Evidence: `.copilot-tracking/evidence/2026-11-22/issue-2201-live4/`.
* Planning Readiness: Ready.
