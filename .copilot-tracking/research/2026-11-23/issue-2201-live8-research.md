---
title: Issue 2201 live8 research (receiver failures 09:30 to 11:30 UTC, diagnostic gap)
ms.date: 2026-11-23
---

Research disposition: executed (read-only Azure). Planning Readiness: Ready.

* Issue #2201 is closed; all four criteria are ticked, so no unticked criterion exists. The goal is a new code change or test.
* Job `job-live-receiver` on digest 541068: 22:00 UTC (22 Nov) to 09:00 UTC all Succeeded; 09:30, 10:00, 10:30, 11:00, 11:30 Failed; 12:00 Succeeded; 12:30 Running (excluded). Evidence: `.copilot-tracking/evidence/2026-11-23/issue-2201-live8/receiver-executions.json`.
* The "three consecutive runs" streak is therefore not unbroken today; the cause of the failures is not recorded.
* Code gap: `src/api/src/zava_forward/api/iot_stream.py` collapses every unexpected callback exception to `IOT_CALLBACK_FAILED` with no exception class, so a failure cannot be attributed from the logs (the open item routed by the live7 review).
* Candidate change: record the exception class name only (no message, which may carry connection detail), print it as `callback_error_type=<Class>` on stderr in `live_receiver.run_window`, and test it. Full tier (src change); `rpi-checks.py --all` is left to the coordinator.
