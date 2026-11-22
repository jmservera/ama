---
title: Issue 184 live chain research (2026-11-22)
---

Task `184-live-20261122T201802Z`, slug `issue-184-live`. Research disposition: executed. Planning Readiness: Ready.

Evidence (read only, 20:18 to 20:23 UTC) is under `.copilot-tracking/evidence/2026-11-22/issue-184-live/`.

* Issue #184 has three ticked criteria; the live chain is the open question from its status reconciliation.
* Child stories 185 to 189 are all closed (`gh api .../sub_issues`).
* Simulator: `job-live-simulator` runs on schedule `0,7,15,22,30,37,45,52 * * * *`; the latest 12 executions are Succeeded; 288 homes, 12198 publishes in 6 hours across 288 devices, all `SYN-` ids (0 other).
* Hub: `iot-cutover-test-rzsrg` (B1, Active), route `all-device-messages` to `api-telemetry`; ingress and egress metrics are equal each hour (about 2,050 to 2,090).
* Receiver: `job-live-receiver` every 30 min; Succeeded runs with receipts 1024 to 1052; no Cannot run, Traceback or SENSOR_SQL lines in 6 hours of summary lines.
* Employee app: `/api/map?zoom=14` 200 with 443 items; case sensors `ok`, `fresh`, 12 readings, latest `2026-11-22T20:15:00Z`; another case stale at 20:05; a third consent-withheld.
* Resident app: login 200; `/demo/view` sensors are stored demo history ending 2026-11-21 to 03:30Z (account declined sensor consent, so new readings are not stored). The resident view therefore does not show the live stream for this account.
* Secret scan of 6 hours of job logs for `SharedAccessKey=`, `HostName=...;DeviceId=` and `SharedAccessSignature sr=`: 0 matches. Source greps match only the hygiene tests.

No defect found; no source change planned.
