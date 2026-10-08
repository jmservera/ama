---
title: ADR 0001 Azure Architecture for the Proper Warm Demonstrator
description: Proposed Azure hosting, agent placement, data, model and security architecture for the non-production Proper Warm retrofit workbench demonstrator
author: AMA programme
ms.date: 2026-10-08
ms.topic: reference
---

## Status

Proposed. This is a design for a non-production demonstrator using constructed,
non-identifying data. It is not an approved production architecture. Service
availability, quotas, model versions and regional capacity are unverified and
must be checked in the target subscription before deployment.

## Context

The [Proper Warm Workbench PRD](../prds/proper-warm-retrofit-programme-demonstrator.md)
requires one workbench API as the only write path, bounded AI tasks that return
typed proposals with citations and hold no write credentials, a deterministic
workflow orchestrator with idempotency keys, a quarantining import service,
audit and telemetry (NFR-004), evidence-based model selection and portability
(NFR-010). It names Container Apps, Azure SQL, Durable Functions, Azure AI
Foundry and Blob storage as candidates. No Dataverse or Dynamics dependency is
assumed.

## Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Hosting | Azure Container Apps, VNet-integrated, internal environment | Several small workloads (API, agents, orchestrator, import), queue-driven scale to zero, jobs, per-workload identity and mTLS. App Service would suit one web app but gives weaker per-workload isolation and no native event-driven jobs. Containers keep the design portable (NFR-010) |
| Agents | One `agents` Container App scaled by the `agent-tasks` queue (KEDA, 0 to 5) | Bounded task service. Its identity can call Foundry and read and write the task queue, and has no database, blob or Key Vault access. It posts proposals to the API, which validates and stores them |
| Orchestrator | Container Apps job on a 5 minute schedule | Deterministic, idempotent, checkpointed in SQL through the API. Durable Functions remains an option if replay semantics are needed |
| Import | Event-triggered Container Apps job on `import-jobs` queue | Writes bad rows to the quarantine container, good rows through its own limited SQL role |
| Database | Azure SQL Database serverless with ledger enabled, Entra-only authentication | Relational workflow state, tamper-evident history for auditability, auto-pause for demonstrator cost |
| Evidence store | Blob storage (the PRD fallback), with immutable audit archive container | SharePoint stays conditional |
| Models | Microsoft Foundry account with a project and two deployments, `standard` (gpt-4.1-mini) and `capable` (gpt-4.1) | PRD requires choosing the smallest model that meets task thresholds on held-out cases. The tier per task is configuration, not code. Versions are placeholders pending the evaluation harness |
| Registry | ACR Premium, private, no admin user, identity pull | Private endpoint support and quarantine and retention policies |
| Secrets | Key Vault, RBAC, purge protection, private | No secret is needed by default (all access is by managed identity) |
| Edge | Internal environment only. Front Door Premium with WAF and Private Link is the intended public edge but is not deployed yet | Avoids public exposure of a demonstrator. See open items |

## Identities and access

| Identity | Access granted | Not granted |
|---|---|---|
| `api` | SQL read and write, blob contributor, queue sender, Key Vault secrets user, ACR pull | Foundry |
| `agents` | Foundry OpenAI User and AI User, queue data contributor, ACR pull | SQL, blob, Key Vault, any write path |
| `orchestrator` | Queue sender, ACR pull | SQL, blob, Foundry |
| `import` | SQL read and write, blob contributor, queue contributor, ACR pull | Foundry |

The API additionally accepts calls only from the agents, orchestrator and import
client IDs (Entra app authentication on the Container App when `entraClientId`
is set). SQL contained users are created with
[`infra/scripts/create-sql-users.sql`](../../infra/scripts/create-sql-users.sql).

## Security and audit controls

* Private endpoints for SQL, Blob, Queue, Key Vault, ACR, Foundry and Azure Monitor (AMPLS, private-only), with private DNS zones linked to the VNet.
* Local authentication disabled on Foundry, Log Analytics, Application Insights and storage shared keys; SQL is Entra-only; ACR admin user off.
* NSGs deny by default on the private endpoint subnet; the Container Apps subnet only admits Front Door and VNet traffic.
* Container Apps environment mTLS, HTTPS-only ingress, health probes, single-revision mode, images pulled by identity.
* Diagnostic settings from every service to one Log Analytics workspace; SQL auditing to Azure Monitor; ledger tables; immutable `audit-archive` blob container.
* Defender alert policy on SQL, metric alerts for Foundry client errors and SQL CPU to the action group, optional `CanNotDelete` locks.
* Constructed, non-identifying data only. Production would need a data protection impact assessment and a new approval, which this record does not provide.

## Failure domains and scaling

| Component | Scales by | Failure behaviour |
|---|---|---|
| `api` | HTTP concurrency, 1 to 4 replicas | Writes fail closed; reads may degrade. Two or more replicas need `zoneRedundant` |
| `agents` | `agent-tasks` queue length, 0 to 5 replicas | Failed tasks go to `agent-tasks-poison`; case proceeds as a workflow-only task, never auto-advances |
| `orchestrator` | Single scheduled execution | Resumes from SQL checkpoint with idempotency keys; exhausted retries raise an owned exception |
| `import` | `import-jobs` queue, 0 to 2 executions | Bad rows to `quarantine`; no partial batch commit |
| SQL | Serverless vCore range, auto-pause | Point-in-time restore; ledger digest verifies history |
| Foundry | Per-deployment capacity (tokens per minute) | Throttle alert; the task degrades to workflow-only |

## Threat model mapping

| PRD threat | Control in this design |
|---|---|
| Prompt injection or ungrounded output causes a transition | Agents identity has no data role; output is a typed proposal posted to the API, which enforces gates and human acceptance |
| Data leakage through AI context | Foundry private, no public endpoint, default content filter, constructed data only, local auth off |
| Credential theft | No keys, shared keys, SQL logins or ACR admin; managed identities only |
| Lateral movement | Per-workload identity, NSG deny-by-default, private endpoints, API accepts only named caller identities |
| Tampering with the audit trail | SQL ledger, immutable `audit-archive` container, diagnostics to Log Analytics |
| Supply chain | Digest-pinned images pulled from private ACR with quarantine policy; scan in CI (open item) |

## Operational targets and cost model

* Targets (proposed, unmeasured): API availability 99.5 percent monthly, p95 API latency under 500 ms excluding AI tasks, AI task completion p95 under 30 s. Alerts exist for API 5xx and restarts, Foundry client errors and SQL CPU; the SLO method is in the PRD observability section.
* Cost drivers in dev: Azure SQL serverless (auto-pause), Container Apps consumption (scale to zero for agents and jobs, one API replica), ACR Premium (needed for private endpoint), private endpoints and Log Analytics ingestion, and Foundry tokens. A monthly budget resource alerts at 80 percent actual and 100 percent forecast.
* Cost per unit of business value (for example per assessed home or per accepted AI proposal) cannot be stated until a deployment produces measured usage. This is an explicit gap, not an estimate.

## M365 configuration, integration and use

M365 is optional and secondary to Azure. It is used for three purposes and never
as a system of record or an approval path (PRD CON-005, OQ-012).

| Capability | Configuration | Integration | Use |
|---|---|---|---|
| Entra ID | One app registration for the workbench API (audience `api://<client id>`), app roles per workbench role, a SQL admin security group, group-based role assignment | Container App built-in authentication validates tokens; the API maps roles to permissions and field rules; managed identities call the API as service callers | Sign-in, roles, conditional access, audit of sign-ins |
| SharePoint Online (optional) | A dedicated site for exercise evidence only, no tenant-wide access, retention label and sensitivity label on the library | The API identity gets Microsoft Graph `Sites.Selected` on that one site through `infra/scripts/grant-sharepoint-access.sh`; set `evidenceStore=sharepoint` and `sharePointSiteId`. SQL keeps only stable references and versions | Collaboration documents that housing teams already use. Blob remains the fallback |
| Teams | One channel with a Workflows webhook passed as `teamsWebhookUrl` | The ops action group posts alerts; the API may post links to cases awaiting human review | Notifications and a review nudge. Decisions are always made and recorded in the workbench |

Prerequisites to confirm first: M365 licences and tenant, SharePoint admin
and Global or Privileged Role Administrator consent for Graph permissions,
data residency, and a named owner for the site. Constructed, non-identifying
data only until those checks and a data protection review pass. The Entra app
registration, Teams webhook and SharePoint site are created manually or by
script, not by this Bicep, because they live in the tenant and not in the
resource group.

## Open items

* Azure Policy assignments and subscription-level Defender plans.
* Add Front Door Premium, WAF and the Private Link origin to the internal environment, plus an Entra app registration, once a public edge is needed.
* Confirm the Foundry model names, versions, SKUs and quotas in the chosen region, and set `modelDeployments` from the PRD evaluation results.
* Container hardening (non-root user, read-only root file system, dropped capabilities) is an application image requirement; Container Apps does not expose these settings, so enforce them in the Dockerfile and scan images in CI.
* Build the application images; the default placeholder image only proves the infrastructure.
* Consider Azure Policy assignments, Defender for Containers and cost budgets at subscription level.
* A multi-region or zone-redundant design is not included (`zoneRedundant` is a parameter).

## Validation performed

* `az bicep build` and `az bicep lint` are clean on `main.bicep` and every module; `main.bicepparam` compiles.
* `az deployment group validate` (ARM preflight) succeeded and `what-if` reported 91 creates against the only resource group the available service principal can write to.
* The deployment was not applied. That principal can write only to the unrelated `squadscope-podcaster` resource group, and `what-if` showed the template would modify its existing `privatelink.blob` and `privatelink.queue` private DNS zones. Deploying there would alter another project, so a deployment needs a dedicated subscription or resource group, plus Entra permissions to resolve the SQL admin group.
* Design consequence: the private DNS zones should become parameters so a landing zone can reuse existing zones instead of creating them.
* No runtime, load or cost measurement exists, so A4 and A5 evidence remains design-only.
