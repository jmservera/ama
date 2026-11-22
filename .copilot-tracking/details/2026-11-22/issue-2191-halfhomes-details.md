---
title: Issue 2191 half of homes fresh, details (2026-11-22)
---

* Measurement: `COUNT(DISTINCT home_id)` of `sensor_reading` with `observed_at` in the last 15 minutes (and 5 minutes), against 443 homes; job `job-tmp-sampler2191b` in `cae-cutover-test-demo`, image and identity of the receiver, `mssql_python`.
* Reads: `az sql db show`, `az containerapp job show` for env and schedules, `az monitor metrics list` for DTU.
* Success: every sample after the receiver window start at or above 222 homes.
* Cleanup: `az containerapp job delete -g ama -n job-tmp-sampler2191b --yes`; read back the job list.
* Not changed: Bicep, simulator, receiver env, consent data.
