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

## Open items

* Add Front Door Premium, WAF and the Private Link origin to the internal environment, plus an Entra app registration, once a public edge is needed.
* Confirm the Foundry model names, versions, SKUs and quotas in the chosen region, and set `modelDeployments` from the PRD evaluation results.
* Container hardening (non-root user, read-only root file system, dropped capabilities) is an application image requirement; Container Apps does not expose these settings, so enforce them in the Dockerfile and scan images in CI.
* Build the application images; the default placeholder image only proves the infrastructure.
* Consider Azure Policy assignments, Defender for Containers and cost budgets at subscription level.
* A multi-region or zone-redundant design is not included (`zoneRedundant` is a parameter).

## Validation performed

`az bicep build` and `az bicep lint` run clean on `main.bicep` and every module,
and `main.bicepparam` compiles. No deployment, `what-if` or runtime test has
been performed.
