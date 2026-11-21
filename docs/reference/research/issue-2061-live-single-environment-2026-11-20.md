---
title: Issue 2061 live single-environment move with sqlTier dtu
description: Live deploy of the one-external-environment demo, SQL Standard S0 kept, own Event Hubs namespace, old environment deleted; per-criterion status with evidence
ms.date: 2026-11-20
---

Refs #2061. Synthetic demo only, desktop, resource group `ama`. Evidence files are under
`/home/azureuser/.local/share/ama/phase-witness/2061-live-20261120T185228Z/live/` (outside the repository).
Sources: owner decisions 2026-11-20 on the issue, [runbook](../../../infra/demo-single-environment-runbook.md),
[earlier inventory](./issue-2061-live-single-environment-2026-11-19.md).

## What was done

* Source commit `16331ca89`: optional `sqlTier=dtu` (Standard, S0, 10 DTU, no serverless settings), a guard that limits it to the development profile, tests, README and runbook text. Default tier unchanged.
* Source commit `ed3890a32`: two live deploy rejections fixed. The new `eh-` namespace set `maximumThroughputUnits` with auto-inflate off (Event Hubs refused it), and the `ledgerVerifyMissing` alert used `overrideQueryTimeRange` `PT26H`, which Azure Monitor does not accept (now `PT48H`, a supported value that still covers the 26 hour search).
* What-if built from the runbook profile in a parameters file, not from the stale 2026-10-16 deployment: no Delete entries. Ledger digest immutability parameters were set false so the what-if did not alter the existing `ledger-digests` container.
* Deployed from `ed3890a32` in two stages: stage 1 with `iotHubRoutingReady=false` (creates `eh-iot-cutover-test-rzsrg`, its private endpoint and Data Sender role), stage 2 with `true`. Both Succeeded. Database `retrofit` stayed Standard 10 DTU, Online.
* IoT Hub now has one route, `all-device-messages` to endpoint `api-telemetry` (identity-based, `eh-iot-cutover-test-rzsrg`). The old route to `evhns-cutover-test-demo` is gone.
* New apps and jobs run in `cae-cutover-test-demo`: `ca-cutover-test-demo-agents`, jobs `job-cutover-test-demo-{load,audit,orch}`.
* Deleted by id after the tests: 2 apps and 8 jobs in `cae-cutover-test`, the environment `cae-cutover-test` (its managed group went with it), private DNS link `link-cutover-test` and zone `jollytree-20e6e99e.uksouth.azurecontainerapps.io`. Ids are in `delete-ids.txt`. No protected resource was touched; `cae-cutover-test-demo` still has static IP 4.159.195.41 and both public URLs return HTTP 200.
* Not deleted: `evhns-cutover-test-demo` (telemetry end to end not shown, see criterion 6), `snet-aca` and `nsg-cutover-test-aca` (optional).

## Tests

| Test | Result |
| --- | --- |
| SQL contained user for `id-cutover-test-internal` (db_datareader, db_datawriter) | Created. SQL is private-only and its Entra admin is an application identity, so `create-sql-users.py` could not run from this host (connection denied). A throwaway job running as `id-cutover-test-init` in `cae-cutover-test-demo` ran the same statements; the job was deleted afterwards. |
| Key Vault secret read from inside the environment | `id-cutover-test-internal` HTTP 403; `id-cutover-test-api` HTTP 200 (`kv-403-test.txt`, no secret values) |
| Employee sign-in on the public API URL | Passed: signed-in workbench, 443 permitted open cases from SQL (`shots/employee-signin.png`) |
| Resident public page on the public URL | Loads (synthetic showcase; `shots/resident-signin.png`); the resident test account sign-in was not separately exercised |
| Telemetry through the new route | Not shown (see criterion 6) |

Role inventory after the change: `id-cutover-test-internal` holds Storage Blob Data Contributor and AcrPull only. `id-cutover-test-api` holds Storage Blob Data Contributor, Storage Queue Data Message Sender, Key Vault Secrets User, Cognitive Services OpenAI User, Foundry User, AcrPull and Azure Event Hubs Data Receiver (scoped to hub `sensor-readings`). A before inventory was not captured.

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | Decision record | Proven (earlier) | ADR 0008, from the previous loop; unchanged here |
| 2 | One external environment, public ingress only on web app and API | Partly proven | One environment remains and runs everything; ingress per app was not re-read in this loop |
| 3 | Reviewed delete list, only those removed | Proven | Runbook list, 0 Delete in what-if, deletions by id, protected resources intact. Optional subnet and NSG, and `evhns-cutover-test-demo`, remain |
| 4 | Entra redirect and logout URIs before/after; employee and resident sign-in | Unproven | Employee sign-in passed on the unchanged public host name. Directory privileges are missing, so redirect URIs cannot be listed or tabled; resident account sign-in not exercised |
| 5 | Separate identities, role inventory, negative test | Proven for the after state | Role inventory above and the 403/200 test. Before inventory not captured |
| 6 | Demo end to end with retained evidence | Unproven | IoT Hub has local auth and public access disabled, so no device can be registered or send from here, and no simulator or receiver job exists in the group. Route, endpoint and role are configured; no message was sent |
| 7 | Production profile builds, tests pass, full gate receipt | Partly proven | `az bicep build` and the infra tests listed below pass. The full gate receipt belongs to the coordinator; `rpi-checks.py --all` was not run |
| 8 | Rollback documented | Proven | Runbook rollback section; note that the old environment is now deleted, so rollback means redeploying with `demoSingleEnvironment=false`, which recreates it empty |

Behaviour changes to know: ACR `networkRuleSet.defaultAction` moved from Deny to Allow (public network access stays Disabled); the Key Vault gained the `secret-rotation-days` tag; the IoT Hub fallback route is disabled; a brief telemetry gap occurred during the route move.
