---
title: Epic 113 live recheck, 2026-11-21 (Refs #113)
description: Per-criterion proven or unproven result for the three unticked epic 113 criteria, with a read-only live Azure posture probe of resource group ama; nothing is ticked or closed
ms.date: 2026-11-21
---

Refs #113. Scope is the synthetic demo, desktop only, under the owner decisions of 2026-11-18 (live Azure authorised in resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive technology testing not needed for the demo). Tier: FOCUSED; no `src/` file changed and no defect was found. No Azure resource was created, changed or deleted, so nothing needed cleanup. No credential was read and no browser was needed: the criteria are about GitHub state and platform posture, not a signed-in journey.

## Method

* `gh issue view` on #113, #114, #116, #117, #118, #119, #120, #121, #122, #440, #1906, #2116, #2136 and #2147 on 2026-11-21 at about 03:09Z. Observed; raw output not retained.
* Read-only Azure CLI calls (`az resource list`, `az containerapp show`, `az sql server/db show`, `az storage account show`, `az keyvault show`, `az containerapp env show`, `az sql server ad-only-auth get`) against resource group `ama`, plus unauthenticated `GET /` and `GET /healthz` on both demo apps. Observed; output below is trimmed to the fields quoted and contains no secret.
* The 2026-11-20 [child disposition note](./issue-113-child-disposition-live-2026-11-20.md), the [2026-11-19 recheck](./issue-113-first-unmet-demo-criterion-2026-11-19.md) and the [2026-11-18 audit](./issue-113-epic-audit-live-2026-11-18.md) are the prior baseline.

## Live posture observed on 2026-11-21 (Azure observed)

| Probe | Observed |
| --- | --- |
| `ca-cutover-test-demo-api` | revision `ca-cutover-test-demo-api--0000038`, image pinned by digest `sha256:bc5cb9ae...a937da`, user-assigned managed identity, external ingress, replicas 0 to 4; `GET /` and `GET /healthz` returned 200 |
| `ca-resident-demo` | revision `ca-resident-demo--0000015`, image pinned by digest `sha256:65481780...bbd19`, user-assigned managed identity, replicas 0 to 1; `GET /` and `GET /healthz` returned 200 |
| SQL server | public network access Disabled, minimum TLS 1.2, Microsoft Entra-only authentication true; database `retrofit` Standard S0 (per the 2026-11-20 estate note), earliest restore point 2026-11-07 |
| Storage `stcutovertestrzsrg` | blob public access false, TLS 1.2 minimum, shared key access false |
| Key Vault `kv-cutovertest-rzsrg` | soft delete true, public network access Disabled, RBAC authorization true; purge protection not set |
| Network | 9 private endpoints, 14 private DNS zones, one virtual network |
| Monitoring | 13 metric alerts and 8 scheduled query alerts, including ledger digest mismatch and ledger verify missing alerts |
| Defender for Storage | not readable: the signed-in principal lacks `Microsoft.Security/pricings/read` |

## Per-criterion table

| # | Criterion | Result | Proven or unproven | Why |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 completed with residuals and owner decisions recorded | Not met | Unproven | #440 is OPEN with two unticked criteria: triage of findings into owner-approved issues (owner approval is required for deferrals and pivots), and delivery of research, plan, changes and independent review artifacts in its PR. Both are owner and process gates and cannot be self-ticked. Merged children do not satisfy it. |
| 2 | All child features closed or deferred | Not met | Unproven | Four children are CLOSED (#118, #119, #120, #122; #119, #120 and #122 moved remaining criteria to deferred issues #2147, #2136 and #2116). #114, #116, #117 and #121 are OPEN. #114 has all criteria ticked and waits only for the #440 checkpoint and the owner tick. #116 has one unticked criterion (provider-boundary allowlists). #117 has one (uploads scanned by a real scanner; fake-transport scanning does not count). #121 has six unticked RAI-delta criteria, mostly DPO, Legal and record-owner approvals routed to #1906. |
| 3 | No production claim without measured load, recovery and DPO or Legal approvals | Holds as a negative guard | Proven for the demo as an absence; positive production readiness unprovable | No repository or live surface claims production readiness: the posture above is a synthetic demo estate at Standard S0 with scale-to-zero apps, and ADR 0002 states no production resilience claim. Production load, restore timing and DPO or Legal approvals sit in #1906 and are out of demo scope by owner decision. |

## Findings

* No defect was found: both apps respond, are digest-pinned, use managed identity, and the data plane has no public SQL or blob access. No `src/` change was warranted.
* Key Vault purge protection is not enabled. This is a demo posture observation, not a defect for the demo; enabling it is irreversible and is a production-hardening item, so it was not changed.
* The Defender for Storage state could not be read with the available role, so no real malware scanner can be evidenced for #117. A scanner is a demo-buildable feature, but enabling Defender for Storage changes subscription-level billing and posture and was outside the authorised "no production changes" boundary for this pass.

## Residual actions

* Owner: decide #440 triage and the closure or deferral of #114, #116, #117 and #121.
* Engineering, demo-buildable: a real upload scanner gating availability (#117), and provider-boundary allowlists (#116).
* Routing: production-only items remain with #1906, #2116, #2136 and #2147.

## Evidence limits

* GitHub and Azure reads are point-in-time on 2026-11-21; raw output was not retained.
* No signed-in browser journey was run on this pass; role-by-endpoint and field-level visibility proofs are those recorded under #116 earlier, not re-observed here.
* Earliest SQL restore point and Standard tier are carried from earlier notes and one `az sql db show` read; no restore was performed (no drills).
