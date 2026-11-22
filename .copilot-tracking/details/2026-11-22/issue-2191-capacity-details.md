---
title: Issue 2191 capacity details
ms.date: 2026-11-22
---

* Diagnosis: `az sql db show`, `az monitor metrics list` (`dtu_consumption_percent`, `dtu_limit`, `connection_failed`, `deadlock`), `az containerapp job show` and `execution list` for `job-live-simulator` and `job-live-receiver`.
* Change: `az sql db update -g ama -s sql-cutover-test-rzsrg -n retrofit --service-objective S3`. Rollback: the same command with `S0`.
* Measurement: manual job `job-tmp-sampler2191` (receiver image and identity, `COUNT(DISTINCT home_id)` of `sensor_reading` where `observed_at` is within 15 minutes, 443 total homes). Delete the job afterwards.
* Success: at least half of 443 homes (222) fresh across a 30 minute sample.
* Not changed: Bicep, simulator, receiver env, consent data, registry.
