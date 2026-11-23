---
title: Issue 2061 live evidence pass 2026-11-23
description: Re-verification of every unticked criterion of issue 2061 on revisions 0000054 and 0000026, closing the import workbook and map gaps; stale URI removal, fresh what-if and the resident identity drift stay open
ms.date: 2026-11-23
---

Refs #2061. Synthetic demo, desktop, resource group `ama`, base 342fad401d. Evidence files sit outside the repository in
`/home/azureuser/.local/share/ama/phase-witness/2061-live-20261123T005026Z/live/` (scripts, JSON, screenshots). This pass
extends [the 2026-11-22 pass](./issue-2061-live-evidence-2026-11-22.md). No source, infra or Azure estate change was
made and no throwaway resource was created. Credentials were read at runtime and never printed.

## Findings

### Environment and ingress (criteria 2, 3)

Read with `az containerapp env list`, `az containerapp list` and `az containerapp job list`.

* One managed environment, `cae-cutover-test-demo`, `vnetConfiguration.internal=false`, domain `happyriver-ace49996.uksouth.azurecontainerapps.io`.
* `ca-cutover-test-demo-api` (revision `--0000054`) and `ca-resident-demo` (revision `--0000026`) have external ingress; `ca-cutover-test-demo-agents` has no ingress; the five jobs have none.
* One Event Hubs namespace remains, `eh-iot-cutover-test-rzsrg`; the second environment and `evhns-cutover-test-demo` are gone.

### Entra URIs and sign-in (criterion 4)

Registration `zava-forward-api` (audience `AzureADMyOrg`, token version 2, no logout URL, no SPA URIs) holds the same
three redirect URIs as on 2026-11-22: the current API callback plus two stale ones (the retired Front Door endpoint and
the deleted `cae-cutover-test` host). Option A kept the current URI, so before and after are identical for it. The two
stale URIs are not removed; changing a production-shaped registration needs owner approval.

Playwright, Chromium 1366x900:

* Employee: Microsoft sign-in with the existing test account redirects back to `/app` on the new host; the workbench shows "My cases", perspective Retrofit Programme Manager, 133 assigned cases. Screenshot `shots/employee-signin-2061-r2.png`.
* Resident: the shared-password form on `ca-resident-demo` shows "You are signed in". Screenshot `shots/resident-signin-2061-r2.png`.

### Identities (criterion 5)

Role inventory read with `az role assignment list --all` (file `role-inventory-2026-11-23.txt`); identical to 2026-11-22.

| Identity | Roles |
| --- | --- |
| `id-resident-demo` (public resident app) | AcrPull; Key Vault Secrets User on two named secrets; Cognitive Services OpenAI User |
| `id-cutover-test-api` (API app, receiver job) | storage blob, queue sender, Key Vault Secrets User, OpenAI and Foundry User, AcrPull, Event Hubs Data Receiver on `sensor-readings`, blob index tag reader |
| `id-cutover-test-internal` (audit job, simulator job) | Storage Blob Data Contributor, AcrPull |
| `id-cutover-test-agents` | queue contributor, AcrPull, Foundry and OpenAI User |

The negative access test of 2026-11-22 (HTTP 403 vault list, blob and queue, 401 Event Hubs for `id-resident-demo`, 200 only
for its two scoped secrets) was not rerun because the identities and assignments are unchanged. No before inventory exists
from the pre-move estate; only the 2026-11-20 and later after states were recorded.

Drift found: `ca-resident-demo` carries both `id-resident-demo` and `id-cutover-test-api`, and live env vars
`ZF_DEMO_SENSOR_CONSENT*` (SQL client id of the API identity) exist, but `infra/resident-demo.bicep` assigns only its own
identity and no committed Bicep or script sets those variables (grep of `infra/` and `src/` finds them only in
`src/api/src/zava_forward/api/resident_demo/sensor_consent.py`). A redeploy of the committed Bicep would therefore drop
the sensor-consent wiring, and the live public app holds the API identity. Closing this is an infra change (FULL tier,
owner decision on whether the public app may read consent through a narrower identity); it was not made here.

### Demo end to end (criterion 6)

* Import workbook flow: at `/app#/import` a synthetic two-row `.xlsx` (Reference, Address, Postcode, Stage, Status, Owner) was uploaded as the employee. The page returned "Your file has not been changed", sheet "Homes": 1 row ready, 1 needing fixing, columns matched by name. Screenshot `shots/import-workbook-2061-r2.png`. This proves the workbook check path on the new endpoint; it is a dry run, so the blob-triggered `job-cutover-test-demo-load` execution is not proven.
* Map and telemetry: `GET /api/map?zoom=15` as the employee returned 443 homes; sensor states 59 `fresh`, 22 `consent-withheld`, 19 `no-readings`, 343 `not-loaded`. A fresh sample read `observed_at 2026-11-23T00:50:00Z`, age 314 seconds, source "Synthetic simulator reading", so simulator, IoT Hub, receiver and SQL work end to end. Screenshot `shots/employee-map-2061-r2.png` (map loaded).
* Resident view: signed in as above.

### Production profile and tests (criterion 7)

On this worktree (no source change): `az bicep build --file infra/main.bicep` exit 0, no errors; `python3 -m pytest infra/tests -q` gives 759 passed, 4 skipped, 1461 subtests passed. The full local gate and an external receipt were not run (the brief reserves `rpi-checks.py --all` to the coordinator).

### Rollback (criterion 8)

`infra/demo-single-environment-runbook.md` holds the rollback section, unchanged.

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Decision record | Proven | ADR 0008 (Proposed), unchanged |
| 2 | One external environment, public ingress only on web and API | Proven live; fresh what-if not run | live reads above; 2026-11-20 what-if retained |
| 3 | Reviewed delete list, only those removed | Proven | 2026-11-20 delete ids; protected stores present; optional NSG, subnet, two alerts remain, owner-gated |
| 4 | Entra URI table; employee and resident sign-in | Proven for table and both sign-ins; stale URI removal owner-gated | above |
| 5 | Separate identities, role inventory, negative test | Partly proven | after inventory, negative probe from 2026-11-22; no before inventory; resident app holds API identity (drift) |
| 6 | Demo end to end | Proven except blob-triggered load job | import check, map with fresh readings, both sign-ins |
| 7 | Production build, infra tests, full gate receipt | Build and infra tests proven; full gate receipt unproven here | coordinator owns the gate |
| 8 | Rollback documented | Proven | runbook |
