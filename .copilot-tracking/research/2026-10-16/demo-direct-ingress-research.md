# Demo direct ingress research

Task ID: issue-360. Task slug: demo-direct-ingress. Date: 2026-10-16.

## Brief and Controls

Focused internal research for offline criteria a, b, f and a proposed migration
for c. No Azure operations, deployments, tenant changes or deletion. User supplied
live network facts are evidence inputs, not independently observed here.
Repository instructions and ADR 0006 apply; existing infra patterns selected.
No UI implementation or legal currentness research is needed.

## Questions and Three-Wave Cycle

1. Wider: inspected issue 360, related 349/351, PR 359 lifecycle, main template,
   network, Container Apps, setup script and cut-over evidence.
2. Deeper: traced exposure coupling and guard parameters, auth forwarding,
   tagged API discovery, private proof runner and historical MVP callbacks.
3. Contrarian: rejected allowPublicNetworkAccess because it opens dependencies;
   rejected in-place environment mutation and renaming the entire main prefix
   because these risk immutable replacement or duplicated stateful services.
   A new workload-only suffix and dedicated subnet preserve existing identities
   and private service references. Existing Front Door remains an optional edge.

## Evidence

* C1: infra/main.bicep:120 derives publicAccess from the development opt-in;
  backing modules consume that value. Keep this expression independent.
* C2: infra/modules/containerapps.bicep:49 couples external environment and
  private DNS to allowPublicNetworkAccess; default NoProxy already exists.
* C3: infra/modules/network.bicep:66 has the old ACA NSG and embedded subnets.
  Add a separate conditional demo subnet and NSG without replacing snet-aca.
* C4: infra/scripts/setup-entra.py:108 isolates CLI extension storage; discovery
  must branch before any afd call, and direct mode needs actionable tool checks.
* C5: docs/architecture/cutover-evidence-pack.md:36 records historical Front Door
  proof, explicitly blocked real-user sign-in and browser API 302 gap.
* C6: git history 15e8158:infra/modules/containerapps.bicep:49-52 used the broad
  development public switch; ingress:104 was external and EasyAuth:190 redirected.
  That commit's initialize-api-auth.py:95 derived callbacks from the app FQDN.
  Prior art is history-only; no MVP files restored or read from the working tree.
* C7: PR 359 was open at intake. git fetch origin and git merge origin/main
  completed before setup edits (already up to date). Do not duplicate or
  overwrite its separate device-code changes.
* W1: https://learn.microsoft.com/en-us/azure/container-apps/billing,
  retrieved 2026-10-16: Consumption bills allocated compute and requests;
  private endpoints/planned maintenance can add Dedicated Plan Management fees
  even on Consumption. Empty Consumption environment is not running replicas.
* W2: https://azure.microsoft.com/en-us/pricing/details/container-apps/,
  retrieved 2026-10-16: shared monthly grants and job/replica billing confirmed,
  but public rendering returns no numeric regional rates. Runbook estimates
  must be clearly labelled illustrative assumptions pending account quote.

## Synthesis

Use explicit development-only demoDirectIngress, forbid public backing access,
edge coexistence and bearer-only/unauthenticated demo workloads. New suffixed
apps/jobs/environment share existing dependency names and identities. Preserve
old workloads until owner-approved verification and retirement.
Direct setup selects a tagged API and its public FQDN; no edge discovery.
Probe strict status/redirect/role outcomes without persisting URLs or identity
material. Browser sign-in, real roles, SQL/AI and approvals remain live gaps.

Research disposition: executed. Planning Readiness: Ready for offline scope.
No additional cycle needed: remaining unknowns are deliberately live acceptance.
