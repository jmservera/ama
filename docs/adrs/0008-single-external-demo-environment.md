---
title: ADR 0008 Single external Container Apps environment for the synthetic demo
description: Proposed demo-only design that hosts public and non-public apps in one external Container Apps environment, with the Entra option, the managed-identity split and the untouched production profile
author: AMA programme
ms.date: 2026-11-20
ms.topic: reference
---

## Status

Proposed, demo only. Refs #2061. This record is a proposal by the AMA programme.
It does not record owner approval of the delete list, of any Entra change or of
a redeploy, and it does not tick any other acceptance criterion of #2061. The
synthetic demo is desktop only and uses live Azure in resource group `ama` under
the owner decisions of 2026-11-18 (USD 700 cap, no drills, no Key Vault
rotation, no production changes).

## Context

Container Apps ingress is set per app: `external: true` is public and
`external: false` is reachable only inside the environment. Whether a public
endpoint can exist is set per environment (`vnetConfiguration.internal`); an
internal environment cannot host a public app, an external one can host both.

Read-only inventory of resource group `ama` on 2026-11-19 (research note
`.copilot-tracking/research/2026-11-19/issue-2061-live-research.md`):

| Environment | Internal | Contents |
| --- | --- | --- |
| `cae-cutover-test` | yes | API (external ingress), agents (no ingress), eight jobs |
| `cae-cutover-test-demo` | no | `ca-cutover-test-demo-api` and `ca-resident-demo`, both external |

`infra/modules/containerapps.bicep` already selects the mode with
`externalEnvironment = demoDirectIngress || allowPublicNetworkAccess`, so a
demo profile with one external environment needs no new module, only a
re-pointing of the helper templates.

## Decision

* Demo profile: one external environment. Public ingress only on the web app
  and the employee/resident API. Agents, orchestrator, importer, IoT readers and
  jobs use internal ingress (`external: false`) or no ingress.
* `infra/resident-demo.bicep`, `infra/live-receiver-job.bicep`,
  `infra/live-simulator-job.bicep` and `infra/public-edge-existing.bicep` reference
  the single environment instead of an `existing` second one.
* Entra: option A, reuse the public environment. The public app registrations and
  URLs stay, so employee and resident sign-in keep working at every step; only
  the private apps' redirect URIs and ingress settings change. Option B (recreate
  every registration) is rejected because it changes every redirect, logout and
  callback URL at once and widens the outage window for no demo benefit. Secrets
  stay in Key Vault and are never printed or committed.
* Managed identities: public-facing containers use a dedicated least-privilege
  identity and internal containers use their own. `id-resident-demo` already
  follows this pattern: AcrPull, Key Vault Secrets User on two named secrets and
  Cognitive Services OpenAI User on its own account. The public demo API still
  shares `id-cutover-test-api`, which holds vault-wide Key Vault Secrets User and
  storage data roles; it needs its own identity with only the roles sign-in and
  its read paths require. Role assignments are re-created per identity in
  `infra/role-assignments.json`, and hub-scope Event Hubs receiver roles stay
  with owner decision #1818.
* Production profile: unchanged. The internal environment with Front Door
  Premium and Private Link (ADR 0002 decision 6) remains deployable and covered
  by its existing infra tests.

## Implementation 2026-11-20 (owner option A, Refs #2061)

The Bicep profile is built: `demoSingleEnvironment` in `infra/main.bicep` (guarded,
default off) and a conditional `id-<prefix>-internal` identity for the ledger-verify
and rank-publish jobs. The public API keeps its identity because it legitimately
needs SQL, storage, queue, Key Vault and registry access; the split only moves the
internal jobs off it. Delete list and rollback are in the
[runbook](../../infra/demo-single-environment-runbook.md); evidence and unproven
criteria are in the
[research note](../reference/research/issue-2061-demo-single-environment-profile-2026-11-20.md).
Nothing is deployed and the owner approvals above remain open.

## Rollback outline

Keep the previous Bicep parameters and the old redirect URIs recorded before
deploy. To roll back, redeploy the two-environment parameters, restore the old
redirect and logout URIs and re-assign the previous identity to the demo API. The
`ama` group, SQL, storage, Key Vault and IoT Hub are never touched by the delete
step. The verified rollback runbook is still to be written.

## Consequences

* One environment removes the second environment, its internal load balancer,
  public IP and private DNS zones and links, but only after the owner approves a
  delete list by resource id.
* Entra registrations are not readable with the current login (Graph returned
  insufficient privileges on 2026-11-19), so the before/after URI table needs an
  identity with directory read access.

## Open items

* Owner approval of the delete list and of the Entra changes.
* What-if on the real group and the FULL validation tier for the infra change.
* Negative access test for the public identity and the end-to-end demo evidence.
