---
title: Demo single-environment migration and teardown runbook
description: Deploy, verify, delete and roll back steps for the demoSingleEnvironment profile, with the resources to delete once the second Container Apps environment is retired
ms.date: 2026-11-20
ms.topic: how-to
---

Refs #2061. Demo only (synthetic, desktop). Production is unchanged: the profile
is off by default and its guard rejects production, the public edge and public
backing stores. See [ADR 0008](../docs/adrs/0008-single-external-demo-environment.md).

## Profile

Deploy `main.bicep` with `deploymentProfile=development`, `demoDirectIngress=true`,
`demoSingleEnvironment=true`, `enablePublicEdge=false`,
`allowPublicNetworkAccess=false` and `sqlTier=dtu`. The guard `singleEnvironmentRequiresDirectDemo`
rejects any other combination.

* `sqlTier=dtu` keeps the demo database on Standard S0 (10 DTU) with no
  serverless settings; the default tier is unchanged and the guard
  `dtuTierRequiresDevelopmentProfile` rejects it outside `development`.
* The template creates its own Event Hubs namespace `eh-<iot hub name>` and, with
  `iotHubRoutingReady=true`, the IoT Hub route points at it. Deploy first with
  `false` so the sender role can propagate, then with `true`.
* One external environment `cae-<prefix>-demo` on `snet-aca-demo`.
* Public ingress (`external: true`) only on the API app, which serves the web
  app and the employee and resident API. `ca-resident-demo` keeps its own
  external ingress through `resident-demo.bicep`.
* Agents, orchestrator, importer and all jobs have no ingress.
* The existing public hostname and the Entra registrations stay (option A).

## Managed identities and role assignments

| Identity | Used by | Roles (scope) |
| --- | --- | --- |
| `id-<prefix>-api` | public API app | Blob Data Contributor and Queue Data Message Sender (storage), Key Vault Secrets User (vault), AcrPull (registry), OpenAI User (AI account), SQL reader and writer |
| `id-<prefix>-internal` (new) | ledger-verify and rank-publish jobs | Blob Data Contributor (storage), AcrPull (registry), SQL reader and writer |
| `id-<prefix>-agents`, `-import`, `-orchestrator`, `-init` | internal apps and jobs | unchanged, see `role-assignments.json` |
| `id-resident-demo` | `ca-resident-demo` | AcrPull, Key Vault Secrets User on two named secrets, OpenAI User on its own account |

The internal identity holds no Key Vault, Queue sender or OpenAI role. When
`demoSingleEnvironment` is false the internal key falls back to the API identity
and no role is added, so production is unchanged. Event Hubs receiver roles stay
with owner decision #1818.

## Deploy order

1. Record the current role assignments and the redirect and logout URIs of the
   public Entra registration (needs a login with directory read access).
2. Run `az deployment group what-if` and confirm no Delete lines.
3. Deploy with the profile parameters above (owner approval required).
4. Run `python3 infra/scripts/create-sql-users.py` so `id-<prefix>-internal`
   receives its SQL grants.
5. Move the jobs and apps that still run in the old environment. Re-point
   `live-receiver-job.bicep` and `live-simulator-job.bicep`, which already target
   `cae-<prefix>-demo`.
6. Sign in as employee and resident at the public URLs and run the demo flow.
7. Negative test: with `id-<prefix>-internal`, a Key Vault secret read must
   return 403; the same call with the API identity succeeds.

## Delete list (after step 6 passes and the owner approves by resource id)

| Resource | Name in group `ama` (live, 2026-11-20) | Note |
| --- | --- | --- |
| Container Apps environment | `cae-cutover-test` | the internal second environment |
| Managed group, internal load balancer and its frontend IP | `ME_cae-cutover-test_ama_uksouth` | ids not readable with the current login; delete with the environment and confirm the group is gone |
| Private DNS zone | `jollytree-20e6e99e.uksouth.azurecontainerapps.io` | plus link `link-cutover-test` |
| Event Hubs namespace | `evhns-cutover-test-demo` (`/subscriptions/<subscription-id>/resourceGroups/ama/providers/Microsoft.EventHub/namespaces/evhns-cutover-test-demo`) | Basic tier, public. Delete only after the IoT Hub route targets `eh-<iot hub name>` and telemetry reaches it |
| Subnet (optional) | `snet-aca` | only after the environment is gone |
| NSG (optional) | `nsg-cutover-test-aca` | only after the subnet is gone |

Never delete resource group `ama`, SQL, storage, Key Vault, IoT Hub or the
external environment `cae-cutover-test-demo` and its managed group
(`ME_cae-cutover-test-demo_ama_uksouth`, public IP `4.159.195.41`).

## Rollback

Redeploy with `demoSingleEnvironment=false` (or without the parameter). The
identity module then drops `id-<prefix>-internal` and the jobs return to the API
identity. If the old environment has not been deleted, re-point the jobs to it.
After deletion, restore it by redeploying the two-environment parameters and
re-creating the private DNS zone link. Restore the recorded redirect URIs if
they were changed.
