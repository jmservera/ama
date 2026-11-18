---
title: Live demo evidence for issue 184, simulator stage 2 streaming
description: Per-criterion record of what the 2026-11-18 demo checks prove for the parent issue 184 and why its child-closure criterion cannot be proven
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 184
  - iot hub
  - simulator
  - child stories
estimated_reading_time: 4
---

Refs #184. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). No source files changed and nothing was created in Azure, so there is no residue to delete. Nothing here is production evidence.

## Method

Read-only: `gh issue view` and the sub-issues API for #184, #185 and #189 on 2026-11-18; Azure CLI and the Consumption budgets REST API in resource group `ama`; the deployed API app settings. No credentials were read and no sign-in was needed.

## Child stories (sub-issues API, 2026-11-18)

| Child | State | Notes |
| --- | --- | --- |
| #185 Simulated device identity and provisioning | open | Two criteria unticked. The [live identity note](./issue-185-live-device-identity-evidence-2026-11-18.md) proves them for the demo, but the issue is not ticked or closed |
| #186 Message schema, rate and volume | closed | |
| #187 Replay, speed controls and failure injection | closed | |
| #188 Ingestion into the store and consistency with the backfill | closed | [Live backfill note](./issue-188-live-backfill-evidence-2026-11-18.md) |
| #189 Cost, scale and run controls | open | One criterion unticked: run owner, time limit and budget alert (see below) |

## Live check for the #189 criterion

* Budget alert: budget `budget-iot-cutover-test-rzsrg` exists on the demo hub scope, USD 25 monthly, ends 2036-10-01, current spend USD 5.16. It has two enabled notifications, Actual 80 percent and Forecasted 100 percent, each with one contact email (address not recorded here). Proven for the demo hub as configuration; no alert delivery was triggered.
* Run owner and time limit: the source control in `simulator_admin.py` takes an owner, approval reference and expiry capped at `max_days`, but it reads its control file path from an environment variable that is not set on `ca-cutover-test-demo-api` (no simulator or live-control setting among its app settings). Enabling it needs a deployment change that the owner decision excludes. Unproven live.

## Per-criterion result for #184

| Criterion | Result | Evidence |
| --- | --- | --- |
| All child stories closed or deferred | Not proven. Three of five children are closed; #185 and #189 are open and no owner deferral decision exists | Table above. #185's criteria are met for the demo by its live note but the issue is unticked and open; #189 lacks a live owner and time limit |
| Simulator never connects to, discovers or represents installed real devices | Already ticked; not re-proven | Source tests; the live runs used `SYN-` demo identities only |
| No device key or connection string in source, logs or telemetry | Already ticked; the #185 live run found no key text in job output | [#185 note](./issue-185-live-device-identity-evidence-2026-11-18.md) |

## What this does not prove

* Whether the owner would defer #189's live owner and time-limit criterion for the demo. That is an owner decision; the brief gives none.
* Ticking or closing #185 or #189 and the parent. Issue updates belong to the coordinator after review.
* Production tier, X.509, scale beyond three identities, or any assistive-technology result.
