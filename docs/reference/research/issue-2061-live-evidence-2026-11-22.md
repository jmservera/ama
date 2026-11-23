---
title: Issue 2061 live evidence pass 2026-11-22
description: Read-mostly live check of the one-environment demo against each unticked criterion, with a throwaway negative access probe; Entra URIs, sign-in, telemetry and identity findings
ms.date: 2026-11-22
---

Refs #2061. Synthetic demo, desktop, resource group `ama`. Evidence files sit outside the repository in
`/home/azureuser/.local/share/ama/phase-witness/2061-live-20261122T233323Z/live/`. Earlier notes:
[2026-11-20 live move](./issue-2061-live-single-environment-2026-11-20.md),
[profile](./issue-2061-demo-single-environment-profile-2026-11-20.md). No source file or Azure estate change was made;
one throwaway job was created and deleted (see the negative probe).

## Findings

### Environment and ingress (criteria 2 and 3)

Read with `az containerapp env list`, `az containerapp list` and `az containerapp job list` on 2026-11-22.

| Item | State |
| --- | --- |
| Managed environments | One: `cae-cutover-test-demo`, `vnetConfiguration.internal=false`, domain `happyriver-ace49996.uksouth.azurecontainerapps.io` |
| `ca-cutover-test-demo-api` | external ingress (employee and API) |
| `ca-resident-demo` | external ingress (resident front door) |
| `ca-cutover-test-demo-agents` | no ingress configured at all (not reachable even inside the environment by name; tighter than the internal ingress the criterion asks for) |
| Jobs | `job-cutover-test-demo-{load,audit,orch}`, `job-live-simulator`, `job-live-receiver`; jobs have no ingress |
| Event Hubs namespaces | Only `eh-iot-cutover-test-rzsrg`; `evhns-cutover-test-demo` is gone |
| IoT Hub | one route `all-device-messages` to identity-based endpoint `api-telemetry`; local auth disabled, public access disabled |

### Entra app registration (criterion 4)

The signed-in Azure CLI can now read the directory. Registration `zava-forward-api` (`0dbb6baf-c8af-414f-ad0b-5daa7695cbc9`, audience `AzureADMyOrg`, token version 2, no logout URL, no SPA URIs) holds three web redirect URIs. The Container Apps authentication config of `ca-cutover-test-demo-api` uses this client id with `RedirectToLoginPage`. `ca-resident-demo` has no Container Apps authentication; it uses the shared demo password form, so no resident registration exists.

| URI | State |
| --- | --- |
| `https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/.auth/login/aad/callback` | current, used |
| `https://ep-cutover-test-esdrcphsarcahhde.b01.azurefd.net/.auth/login/aad/callback` | stale (Front Door, not in the demo profile) |
| `https://ca-cutover-test-api.jollytree-20e6e99e.uksouth.azurecontainerapps.io/.auth/login/aad/callback` | stale (host of the deleted environment `cae-cutover-test`) |

This is the before and after table: Option A was taken, so the current URI did not change and the registration was not edited in this pass. Removing the two stale URIs is an Entra change on a production-shaped registration and still needs owner approval, so it was not done.

### Sign-in (criterion 4)

Playwright (Chromium, 1366x900) with credentials read at runtime and never printed.

| Account | Result |
| --- | --- |
| Employee (Entra, existing test account) | Landing page, "Sign in to the workbench", Microsoft sign-in, redirect back to `/app` on the new host, workbench shows "My cases" and perspective `Retrofit Programme Manager` with 133 assigned cases. Screenshot `shots/employee-signin-2061.png` |
| Resident (shared demo password form) | Public page loads; after sign-in the page states "You are signed in" with read-only progress. Screenshot `shots/resident-signin-2061.png` |

### Identities (criterion 5)

Role inventory read on 2026-11-22 with `az role assignment list --all`.

| Identity | Roles |
| --- | --- |
| `id-cutover-test-internal` | Storage Blob Data Contributor, AcrPull |
| `id-cutover-test-api` | Storage Blob Data Contributor, Storage Queue Data Message Sender, Key Vault Secrets User, Cognitive Services OpenAI User, Foundry User, AcrPull, Event Hubs Data Receiver (hub `sensor-readings`), custom ZF Blob Index Tag Reader |
| `id-resident-demo` | AcrPull, Key Vault Secrets User on two named secrets only (`resident-demo-password-verifier`, `resident-demo-session-key`), Cognitive Services OpenAI User |

Negative access test: a throwaway manual job `job-tmp-probe-2061` ran as `id-resident-demo` inside `cae-cutover-test-demo`, requested its own tokens and printed HTTP status codes only (script `probe.py`, output `negative-probe-id-resident-demo.txt`). The job was deleted afterwards and no copy remains in the group.

| Probe | Status | Reading |
| --- | --- | --- |
| Key Vault list secrets | 403 | no vault-wide access |
| Key Vault read its own session-key secret | 200 | scoped grant works (value not printed) |
| Blob list on `stcutovertestrzsrg` | 403 | no storage data access |
| Queue list on `stcutovertestrzsrg` | 403 | no queue access |
| Event Hubs read on `sensor-readings` partition 0 | 401 | no hub access (REST probe returns 401 for a missing role) |

Finding to know: `ca-resident-demo` is also assigned `id-cutover-test-api`, and its `ZF_DEMO_SENSOR_CONSENT_SQL_CLIENT_ID` is that identity's client id (its main `ZF_SQL_CLIENT_ID` is `id-resident-demo`). The public resident app therefore still carries the API identity for the sensor-consent read. The split is real for the API and internal containers but not total for the public resident app. A full before inventory was never captured; the 2026-11-20 `pre-apps.json` shows only the pre-move identity assignment per app (API and resident demo apps used `id-cutover-test-api` and `id-resident-demo`).

### Telemetry end to end (criterion 6)

Log Analytics workspace `log-cutover-test` and Azure Monitor metrics.

* `job-live-simulator` (every 7 to 8 minutes) last slot `2026-11-22T23:20Z` log: `homes=288 sent=249 failed=0 skipped=39 retries=0`; recent executions all Succeeded.
* IoT Hub route to `eh-iot-cutover-test-rzsrg`: namespace `IncomingMessages` about 2,050 to 2,090 per hour for the six hours to 22:36 UTC.
* `job-live-receiver` (every 30 minutes) logged `receipts=1032` (23:25), 1038, 1058, 1032, 1027, 1059 over the prior five runs, each Succeeded.
* Employee view of the signed-in workbench loads from SQL (above). Device registration from this host is not possible (IoT Hub local auth disabled, `az iot hub device-identity list` returns 401002), which is expected and not needed because the simulator job runs inside the environment.
* Import workbook flow: `job-cutover-test-demo-load` has no execution in the retained log window and no console log rows, so a fresh import was not exercised or proven. Triggering it needs a blob upload to the shared store, which this pass did not do.

### Other estate observation

`nsg-cutover-test-aca`, an unused `snet-aca` subnet and `alert-cutover-test-api-5xx`, `alert-cutover-test-api-restarts` (for the deleted `ca-cutover-test-api`) remain. They are optional delete-list items awaiting owner approval; nothing was removed.

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | Decision record | Proven | ADR 0008 ([docs/adrs/0008-single-external-demo-environment.md](../../adrs/0008-single-external-demo-environment.md)), status Proposed, covers design, Entra option A, identity split and production profile; unchanged |
| 2 | One external environment, public ingress only on web and API, internal elsewhere | Proven live; what-if attachment from 2026-11-20 only | One environment, two external apps, agents without ingress, jobs without ingress. Fresh what-if not run: no infra change |
| 3 | Reviewed delete list, only those removed, protected resources kept | Proven | 2026-11-20 delete ids, 0 Delete in what-if; SQL, storage, Key Vault, IoT Hub, `ama` present. Optional leftovers listed above |
| 4 | Entra URIs before/after; employee and resident sign-in | Proven for sign-in and URI table; stale URI removal unproven | Table above; both sign-ins pass. Stale URIs not removed (owner approval) |
| 5 | Separate identities, role inventory, negative test | Partly proven | After-inventory and a 403/401 negative probe for `id-resident-demo` and (2026-11-20) `id-cutover-test-internal`; no before inventory; resident app still carries the API identity |
| 6 | Demo end to end with retained evidence | Mostly proven | Simulator, IoT Hub route, receiver, employee sign-in and resident sign-in shown; import workbook flow and map interaction not re-exercised |
| 7 | Production profile builds, infra tests pass, full gate receipt verifies | Unproven here | No source change and the coordinator owns the full gate; `rpi-checks.py --all` was not run |
| 8 | Rollback documented | Proven | Runbook rollback section (`infra/demo-single-environment-runbook.md`); the old environment is deleted so rollback means redeploying with `demoSingleEnvironment=false` |
