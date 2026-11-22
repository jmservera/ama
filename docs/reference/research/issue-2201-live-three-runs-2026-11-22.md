---
title: Issue 2201 three consecutive receiver runs (demo, 2026-11-22)
description: Three consecutive scheduled Succeeded runs of job-live-receiver on the PR 2231 image, with the cause of the earlier failures and a per-criterion table
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`. Azure was read only; no resource was created, so none needs deleting. No Bicep ran and the registry `crcutovertestrzsrg` still reads `publicNetworkAccess` Disabled. Sign-in values were read at runtime and never printed. It extends the [earlier proof](./issue-2201-live-receiver-proof-2026-11-21.md). Refs #2201, #184.

## Evidence

Recorded under `.copilot-tracking/evidence/2026-11-22/issue-2201-live3/` (executions JSON and table, probe script, probe JSON).

* Image: `job-live-receiver` runs digest `sha256:295164ca739d5602ca323c65c305cff9d76a3e72faa4623e0dfa931363fd4f72`, the same digest as `ca-cutover-test-demo-api` (revision `--0000045`, main at PR 2231, see the [2202 rollout note](./issue-2202-live-deploy-2026-11-22.md)). The job was last modified 2026-11-22 03:34:29 UTC; schedule `*/30 * * * *`, args `--seconds 1500`.
* Three consecutive scheduled runs, all after that update, none manual (cron-named):

| Execution | Start (UTC) | End (UTC) | Status |
| --- | --- | --- | --- |
| `job-live-receiver-29922000` | 2026-11-22 04:00:00 | 04:25:37 | Succeeded |
| `job-live-receiver-29922030` | 2026-11-22 04:30:00 | 04:55:29 | Succeeded |
| `job-live-receiver-29922060` | 2026-11-22 05:00:00 | 05:25:44 | Succeeded |

* Before the update: 03:30, 03:00 and 02:30 runs Failed. At 05:15 UTC 64 executions were retained: 52 Failed, 11 Succeeded, 1 Running; no Failed run starts after the 03:34 update.
* Store and map (staff app, probe at 05:14 UTC): `/api/map` returned 200 with 443 items. `/api/cases/ZF-2025-0030/sensors` returned `state` `ok`, `freshness` `fresh`, 12 readings, latest `observed_at` `2026-11-22T05:10:00Z`, reading id `LIVE-STQEOYP62W2-20261122T0510Z`. Four other probed cases return `consent-withheld` (consent behaviour from #2192), which hides values by design.

## Cause of the earlier failures

From the [earlier note](./issue-2201-live-receiver-failure-2026-11-21.md): the deadline reaching an in-flight write was treated as failure (`IOT_OPERATION_TIMEOUT`), fixed in #2231, and `SENSOR_SQL_UNAVAILABLE` was captured on 2026-11-21 for two runs. The three runs above ran on the fixed image and stayed Succeeded. Not proven: the cause of the database refusal, the numeric exit code of older failures (replica logs are not retained and the workspace denies this client), and whether the image digest was built from the commit that adds the SQL retry (`sql_retries` is present in `live_receiver.py` on main at 8bc751023f, but the digest-to-commit link is taken from the 2202 note, not rebuilt).

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Partly proven | Deadline-as-failure defect (source, test, then Succeeded runs) and captured `SENSOR_SQL_UNAVAILABLE` lines; numeric exit code and older-run logs unavailable |
| Fix merged and deployed | Proven | #2231 on main; job image equals the API revision `--0000045` digest, updated 03:34 UTC |
| Three consecutive scheduled runs Succeeded | Proven | 29922000, 29922030, 29922060, table above |
| Readings from IoT Hub appear in the store and the employee map, with timestamps | Proven for the demo | Map 200 with 443 items and a fresh case sensors response with UTC timestamps at five minute steps; the hub-to-store hop is inferred from the live path, not traced per message |
