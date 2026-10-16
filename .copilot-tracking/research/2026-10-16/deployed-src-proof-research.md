---
title: Deployed src proof research
description: Private-network continuation of issues 200 and 201
ms.date: 2026-10-16
---

## Research Brief and Parameters

Task identity: issues-200-201-deployed-src-proof; slug: deployed-src-proof.
Focused convergence for the owner's requested Azure proof. Evidence root:
`.copilot-tracking/research/2026-10-16/`. Audience: cut-over reviewer.
Only ama resources may change; no tenant writes, network peering, policy bypass,
SQL firewall attempts, private datasets, local Docker or legacy-directory edits.
The user explicitly requests the entire lifecycle, deployment, push and PR.

## Extension Registry and Participation

Repository instructions and ADR 0006 selected. RPI phase skills selected.
No independent research specialist needed: this is one continuous deployment
trace. Interaction unavailable; explicit owner constraints resolve scope.
Existing clean topic branch `feat/deployed-from-src-proof-200` has no PR and
continues this workstream from `3c2d9e9`.

## Questions and Evidence

* C1: `infra/main.bicep:106` computes public access as development OR the
  explicit switch. Thus development cannot actually opt into private networking.
* C2: `infra/modules/sql.bicep:30` and `:149` use the switch for server access
  and conditional firewall creation. A false effective switch avoids both
  prohibited public access and firewall requests.
* C3: `infra/modules/containerapps.bicep:84` enables trusted-proxy auth only
  when Entra client ID exists; current configuration also requires a vault
  client secret. No secret or tenant roster was supplied.
* C4: `src/core/src/zava_forward/core/sqlstore.py:371` requires an input seed
  on an empty database. An explicitly labelled tiny synthetic fixture can
  prove infrastructure, not continuing 60k/980-case acceptance.
* C5: `infra/scripts/initialize-workbench-staff.py:84` requires a private
  human roster and Graph permission. Do not substitute a managed identity
  for a human staff member.
* W1: Azure CLI on 2026-10-16 reports Microsoft.Devices Registered and SQL
  publicNetworkAccess Disabled. Existing ACR is public, quarantine disabled.
  No Container Apps environment exists. All listed resources are in ama.
* W2: `az ad app list --filter "startswith(displayName,'Zava')"` fails with
  Insufficient privileges. RG ownership does not confer Graph privileges.

## Research Cycle Log

1. Wider: reviewed both issue bodies/comments, evidence pack, ADR, infra
   deployment and image recipe. Provider registration is fixed.
2. Deeper: traced network switch, SQL grants/schema initialization, image
   package boundaries, staff initializer and EasyAuth dependency.
3. Contrarian: rejected public SQL/tag bypass and VM data-plane access.
   Rejected inventing tenant staff or calling synthetic proof product acceptance.
   A fully private development profile needs an explicit-switch correction;
   an authenticated production application still needs tenant prerequisites.

## Findings, Alternatives and Decisions

Accept private development switch correction with regression coverage, remote
ACR builds before registry isolation, dedicated initialization MI and in-VNet
job. Bootstrap with repository deploy wrapper, retaining existing resources.
Attempt application deployment only with real fail-closed ingress authentication;
otherwise record the exact auth blocker and continue SQL/image proof.
No tenant change or owner sign-off is authorized by this execution.

## Readiness

Research disposition: executed. Planning Readiness: Ready.
Unknown runtime outcomes are execution questions, not missing owner decisions.
Stop affected steps on permissions or unavailable prerequisites, continue others.
No further research cycle is warranted before testing Azure behavior.
