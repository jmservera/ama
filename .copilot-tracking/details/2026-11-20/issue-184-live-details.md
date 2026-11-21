---
title: Issue 184 live demo phase details
ms.date: 2026-11-20
---

* Cohort: first 20 open case ids in order, a bounded demo cohort (device cap 100). Consent split: the three existing granted homes stay granted; seven more are granted (10 granted, 50 percent); the other ten alternate declined and no control. Policy window: now to now plus 13 days; `max_past_seconds` 7200 as before.
* Identity: simulator job uses `id-cutover-test-internal` (AcrPull and SELECT on cases already present); receiver job uses `id-cutover-test-api` (Event Hubs Data Receiver on `sensor-readings`, SQL writer, AcrPull). No role is added for the jobs.
* Temporary: IoT Hub Registry Contributor for `id-cutover-test-api` to register devices, removed after; throwaway job `job-184-ops` removed after each use.
* Approval reference: `OWNER-2026-11-20-demo-184`. Control expiry: 13 days.
* Receiver schedule: every 30 minutes, 2400 s window, `--events` 20000, `routingReady` true because the route and `api-consumer` group were read back.
* Simulator schedule `*/5 * * * *`, 20 homes, well inside the 400,000 per day B1 budget (5,760 per day).
* Validation: `az bicep build/lint` on both files, `infra/tests` for the touched templates, new tool unit test, mypy/ruff only if `src/` changes (none planned).
