---
title: ADR 0001 Azure Architecture for the Zava Forward Demonstrator
description: Proposed Azure hosting, agent placement, data, model and security architecture for the non-production Zava Forward retrofit workbench demonstrator
author: AMA programme
ms.date: 2026-10-14
ms.topic: reference
---

## Status

Proposed. This is a design for a non-production demonstrator using constructed,
non-identifying data. It is not an approved production architecture. Service
availability, quotas, model versions and regional capacity are target-specific
and must be checked before deployment. The dated UK South exercise observations
below do not establish availability in a new subscription or production region.

### Exercise Applicability (2026-10-11)

The owner's [subsequent-build direction](../case_study_48_addendum.md#subsequent-application-exercise-builds-2026-10-11)
requires real AI, real SQL state and actual Azure hosting for every accepted
application exercise build (delivered AMA prototype/PoC/MVP or update).
BRD CON-007/AC-086 and PRD CON-009/AC-057 define version-linked
workflow, SQL write/read/restart and real inference proof on the continuing
generated stock/programme. Local/mock checks remain tests, not delivery.
Per-task Decision placement stays conditional; manual access is independent.

The historical full topology below remains proposed, not all deployed.
[Pinned #58 learning](../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11)
records a lean Azure SQL/Blob/AI MVP, not production Entra user login or
private-only isolation. Keep source/image/revision claims distinct.
No premium estate, new app rewrite, production option selection, deployment
authorization or blanket spend override follows from this note. Missing
effective budget/authorization/evidence blocks acceptance, not mock substitution.

### Current Exercise Handover (2026-10-13)

The later [#65](https://github.com/jmservera/ama/pull/65) rebuild ran the real
MVP image, SQL and both model tiers in `ama` / `uksouth`; subsequent initialization
and owner-reported sign-in are recorded in the
[current operator handover](../../infra/README.md#current-exercise-handover-2026-10-13)
and [dated addendum](../case_study_48_addendum.md#observed-deployment-and-identity-learning-2026-10-1213).
This supplements the historical deployments and proposed topology below.
Separate workers remain placeholders; the owner-requested shared five-assistant
MVP runtime is specified in
[ADR 0002](./0002-pilot-readiness-architecture.md#five-assistant-exercise-runtime-2026-10-13),
not evidence that this proposed queue/worker estate was deployed.
Development public-network exceptions, token
storage, full M365 integration, human acceptance and production authority
remain explicitly scoped. Merge of documentation is not approval of the ADR.

## Supersedes/amends

[ADR 0002](./0002-pilot-readiness-architecture.md) (proposed, 2026-10-08)
amends this ADR for the working MVP. It keeps Azure SQL, Blob, `uksouth` and
Entra-only access, and adds proposals for keeping audit entries in full for the
legal retention period (it replaces the earlier idea of audit events without
personal content, per owner direction and DH-007), field-level role visibility,
deterministic home ranking, map scale for about 60,000 homes, replicas and
image hardening, and DPIA-gated staff time capture. Where the two differ for
the MVP, ADR 0002 applies once approved.

## Context

The [Zava Forward Workbench PRD](../prds/zava-forward-retrofit-programme-demonstrator.md)
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

## Responsible AI Architecture Boundary (2026-10-14)

Proposed amendment, not adoption or deployment. The future separate-worker
estate must enforce the same [PRD RAI release contract](../prds/zava-forward-retrofit-programme-demonstrator.md#responsible-ai-release-and-oversight-contract-2026-10-14)
as the [current shared-API realization](./0002-pilot-readiness-architecture.md#responsible-ai-control-plane-2026-10-14).
Do not infer an implemented identity boundary from this proposed topology.

The API owns task release/impact records, permission-filtered evidence,
validated proposals, meaningful review and incident/suspension state. Workers
receive only task-scoped authorized inputs and cannot activate a task, approve
risk, change a policy or commit a domain decision. Recheck task release and
material dependencies before dispatch, proposal publication and human review;
queued work from a superseded release cannot bypass suspension by retrying.

Bind provenance to task, provider/deployment/model, prompt, policy, evidence,
permissions and release versions. Protect retained prompts, explanations and
review/incident records under the same minimum-necessary access and approved
retention rules as their sources. Observability defaults to identifiers and
redacted metrics, not resident/source text. Processor, inference-transfer and
immutable-audit/erasure questions remain DPO/Legal approval gates.

The [failed assessment attempt](../case_study_48_addendum.md#assessment-attempt-and-evidence-limits)
is retained alongside the [validated recovery](../case_study_48_addendum.md#verified-recovery-and-open-dispositions-2026-10-14)
and [baseline RAI report](../../.copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md).
Its 11 PARTIAL residuals (8 MEDIUM, 3 LOW) remain open; proposal-only authority,
source verification and manual routes reduced nine original severity claims.
The report does not prove this amendment implemented or accepted. Current
staff/tenant identity processing needs explicit privacy scope review despite
constructed resident content; restart persistence does not prove recovery.

Reuse the existing API, SQL records and operator disable path before adding a
new governance service. This is simpler and preserves one authority, but
requires explicit server-side gates and tested version invalidation; a separate
worker identity is not available in the current MVP. Always-on assistance and
an AI-ranked queue are rejected: neither adds evidence of fair or safe
outcomes. The cost is evaluation, monitoring and human review capacity, which
must be included in the value comparison rather than hidden as model savings.

Before operational activation, evidence must satisfy PRD AC-062 to AC-066,
including cohort/missing-data evaluation, oversight error detection, accessible
challenge and a suspend/manual-fallback/restart drill. Framework coverage is
not certification; geography and intended use need independent legal scope
review. No new infrastructure or paid inference is authorized by this amendment.

## Hybrid M365 and Excel transition

Review on 2026-10-08 by web research (cited below) and the Neighbourhood Housing
Officer, Data and Performance Lead and Executive Director Assets role agents.
No design-thinking coach agent exists in this repository, so the challenge was
synthesised here. Role views are research instruments, not company facts. The
company's tenant, licences, workbook formats and owners are unknown.

### Is the hybrid feasible and convenient

Feasible, with conditions. Convenient only if staff do not carry double entry.

* Feasible: Graph can read a workbook in place on SharePoint (Graph Excel API, `workbook/tables`), and `Sites.Selected` scopes the app to one site. Source: Microsoft Graph Excel API and permissions reference on learn.microsoft.com, accessed 2026-10-08.
* Convenient: staff keep a familiar surface during transition, and Excel ends as a read-only report fed from the API (Power Query or an export), not a write surface.
* Hazard: Excel co-authoring has no record locking or audit trail, so a workbook and the API both being writable (dual write) is the highest-risk state.
* Constraint: Microsoft Graph has no Private Link. The private-only design needs controlled egress to `graph.microsoft.com` and `*.sharepoint.com` for the import job (Azure Firewall or NAT gateway with FQDN rules) or the import falls back to uploaded files in Blob. Not yet built; an open item.
* Teams: Office 365 connector webhooks are retired (Microsoft 365 Dev Blog, 2026), so alerts use a Teams Workflows webhook, which posts under a generic bot identity.
* Licensing: manual labels, basic DLP and retention are expected to be covered by M365 E3 (Microsoft compliance licensing comparison); auto-labelling and Teams DLP need E5 or add-ons. Unverified for the tenant (OQ-012).

### Staged transition (proposed, thresholds to be set by owners)

| Stage | Excel | Workbench | Exit criteria |
|---|---|---|---|
| 0 Shadow | Unchanged, still the working record | One-way, repeated, idempotent snapshot imports keyed by file hash and row business key. Imported values tagged unverified source assertions | Workbook structures profiled, owners named, quarantine owner and age limit set |
| 1 Parallel run, short and fixed | Named import owners edit; others read-only through SharePoint permissions | Staff record new decisions, handoffs and hazards in the workbench; frontline views show appointments, contractor and flags | Reconciliation, quarantine and drift measures below meet owner-set targets for N consecutive cycles |
| 2 Read-only | Stamped superseded; exceptions through a named owner | System of record | Staff sign-off, tested out-of-hours route, rollback defined, data protection approval for real data |
| 3 Retire | Workbooks become API-fed reports | Sole write path | No post-cut-over workbook edits |

Rules from the role challenge: imports are one-way (no write back to Excel); a
decision, approval or hazard recorded only in Excel is invalid; hazard and
safeguarding cases never rely on Teams nudges and need a named owner and
out-of-hours route; vulnerability data goes to SharePoint only after data
protection and access review.

### Transition measures

* Reconciliation rate by field and batch, with stratified and sampled manual audit so a high rate cannot hide a systematic mapping error.
* Quarantine rate, age and reason mix, with a named owner.
* Post-snapshot source edits, as the drift indicator.
* Unmatched or duplicate property identifiers.
* Evidence reference resolution to the expected version or hash.
* Teams nudge to recorded workbench action conversion and time.
* Time to update a case and handoff acceptance time against the workbook baseline.

### Options still to compare (Executive challenge)

Excel-only improvement, M365-only (SharePoint lists and Power Platform), full
Azure with hard cut-over and the hybrid have not been costed on the same basis.
A board-level approval would need that appraisal, Excel baselines (volume,
quality, error rate), measured demonstrator cost per assessed home, written exit
criteria and confirmation that Awaab's Law clocks hold throughout transition.
Hard cut-over is rejected here because a failed switch could breach statutory
timescales. These remain open (OQ-012).

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

## Provisional options appraisal

This is a worked illustration of the PRD Options Gate, not an approved
decision. The weights below are architect proposals pending sponsor approval,
and the scores are architect judgements on a 1 to 5 scale (5 is best). The
only measured evidence at that comparison date is the `warm-test` deployment and the `prototype/`
tests, so every score for cost, support and company fit stays provisional.
A high aggregate cannot offset a failed mandatory control gate.

| Criterion | Weight | A Azure custom, hard cut-over | B Greenfield business apps | C Azure-led hybrid, staged | D Excel hardening only |
| --- | --- | --- | --- | --- | --- |
| Control and workflow coverage | 25 | 5 | 3 | 5 | 1 |
| Whole-life cost and affordability | 20 | 2 | 3 | 2 | 5 |
| Supportability and recovery | 15 | 2 | 3 | 3 | 4 |
| Data and integration fit | 15 | 3 | 3 | 4 | 2 |
| Resident and accessibility readiness | 10 | 3 | 3 | 3 | 2 |
| Evidence confidence | 15 | 4 | 2 | 3 | 4 |
| Weighted score (out of 5) | 100 | 3.30 | 2.85 | 3.45 | 2.95 |

Reading the result:

* C leads A mainly on data fit, because staff keep their workbooks during a
  transition, and on supportability, because a hard cut-over has no manual
  fallback. The margin (0.15) is small and sensitive to the cost weight.
* D fails the mandatory control gate (no server-enforced approval authority),
  so its score is not eligible regardless of the aggregate.
* B is scored with low evidence confidence because no tenant, licence or
  Power Platform capability has been verified (OQ-012).
* Cost scores rest on retail list prices only. The deployed stack runs a
  Premium registry, a private-endpoint-heavy network and a Container Apps
  environment, so it is not a cheap option. A sponsor affordability envelope
  is still missing.

## Observed deployment measurements

Observed on 2026-08-26 from the `warm-test` deployment in `uksouth` (single
run, not a statistical sample, no load applied):

| Observation | Value |
| --- | --- |
| Full deployment duration | 12 min 38 s |
| Slowest module | containerapps, 6 min 9 s |
| Next slowest | monitoring 3 min 36 s, sql 2 min 46 s, network 1 min 47 s |
| SQL database | GP_S_Gen5 serverless, 0.5 to 2 vCores, auto-pause 60 min |
| Container registry | Premium (needed for private endpoints), about 1.67 per day list price |
| Container Apps environment | list price shows a 0.125 per hour management and private endpoint meter |

These are observations, not SLO attainment. Targets in the operational
section remain proposals until a load and failure test is run.

## Architecture challenge and data store review

On 2026-10-08 the architecture reviewer and Design Thinking coach agents challenged the design. Their views are hypotheses and judgement, not company facts, and pricing and feature limits were not verified.

Data store decision:

* Keep Azure SQL serverless for case state. The domain needs ACID transitions, row-version concurrency, unique idempotency keys and joins over Excel-origin tabular data.
* PostgreSQL Flexible Server is a credible alternative (row-level security, pgaudit, portability) but has no native ledger, so switching is not justified now. Cosmos DB and Table/Blob-only are rejected for the system of record because strict multi-entity rules and reporting joins would move into application code. Blob stays for evidence.
* Ledger gives tamper evidence, not prevention. The Bicep does not yet configure ledger digest upload to an immutable container or a scheduled verify run, so the claim is not yet substantiated. Planned change: digest storage plus scheduled verification, and append-only ledger tables only for audit, approvals and transitions.
* Reconsider if per-row RLS or portability becomes a requirement, or if measured serverless resume latency breaches the API latency target (then disable auto-pause).

Region split:

* North Europe refused new SQL servers (`RegionDoesNotAllowProvisioning`, observed 2026-10-08, re-probed the same day), so `sqlLocation=uksouth` places SQL in the UK with its private endpoint in the North Europe VNet. This adds cross-region latency, a second failure domain and cross-region traffic cost, and is acceptable for the demonstrator only. The reviewer recommends co-locating the whole stack in one region where capacity allows. Round-trip latency is not yet measured.
* Residency: UK South is UK, North Europe is EU. Do not claim a single residency position until OQ-012 is resolved.

Additional services:

* Azure AI Search: defer until a held-out evaluation shows retrieval is the failure mode (fixed cost, extra private endpoint, security trimming risk).
* Azure AI Document Intelligence: add later as a narrow import-job step for scanned surveys and EPC PDFs (pay per page); the coach rates document handling a likely real pain point worth a trial.
* Content Understanding: not now. Storage Queues stay; move to Service Bus if per-case ordering or richer dead-lettering is needed. Container Apps stay, with region as a parameter.

Design Thinking challenge:

* The private-only controls are heavy for a constructed-data demonstrator and are invisible to staff. The riskiest assumption is value and desirability (do role views over one case model reduce coordination effort), not Azure feasibility.
* Keep the store, model tiers, evidence store, hardening level and import route reversible. Validate the Excel read-only rule and the identifier and ownership model with users first.
* Proposed cheap experiments: one-week Excel shadowing with 3 to 5 staff; a role-view task test on constructed cases against their current Excel method; a Document Intelligence trial on 20 to 30 redacted or synthetic documents with an accuracy threshold agreed with staff beforehand.
* Open question for the sponsor: is the controls story itself part of what the demonstrator must show? That answer decides what counts as over-engineering.

## Development deployment in North Europe

Deployed 2026-10-08 as `warm-dev` in resource group `amaFY27` (`northeurope`) with `allowPublicNetworkAccess=true`. Findings:

* `gpt-4.1` and `gpt-4.1-mini` have no pay-as-you-go SKU in `northeurope`, so the tiers were overridden to `gpt-5.4-nano` (standard) and `gpt-5.4` (capable) with `DataZoneStandard`. Both provisioned.
* ACR requires its export policy enabled when public access is on.
* The MCAPS subscription policy reverted SQL public access to `Disabled` until the resource group carried the tag `SecurityControl=Ignore`.
* Both Container Apps run (placeholder images), with a public API FQDN in this mode.

## Region selection

Checked 2026-10-08 from `az cognitiveservices model list`; capacity and quota in untested regions were not verified.

* Recommended target: `uksouth` for the whole stack. The full stack deployed there end to end on 2026-08-26 (SQL, Container Apps, `gpt-4.1` and `gpt-4.1-mini` at `GlobalStandard`), UK data at rest suits a UK customer, and it removes the SQL cross-region split. North Europe refused new SQL servers and `swedencentral` lacked Container Apps capacity on the dates observed.
* Caveat: `uksouth` has no `DataZoneStandard` model option, so inference may be processed outside the UK. Acceptable for constructed data only; revisit before real resident data (OQ-012).
* Fallback if an EU inference boundary is required: `westeurope` or `francecentral` list `DataZoneStandard` for both models. SQL and Container Apps capacity there is untested, so probe before committing. `germanywestcentral`, `polandcentral`, `italynorth` and `spaincentral` list data-zone models but have no pay-as-you-go `gpt-4.1-mini` data-zone evidence beyond the model list and were not tested further.
* The `warm-dev` stack in `northeurope` with SQL in `uksouth` is a development stack only.

## Staff data trust and control

The owner's position (2026-10-08): staff value is the top goal, technical excellence must still be shown, and staff used to on-prem Excel will feel they lose control of their data in the cloud. The design must therefore make staff confident their data is safe, secure and compliant with their own rules (BRD Business Rule Enforcement, RULE-001 to RULE-024). The architect, product advisor and the Housing Officer, Data and Performance, Building Safety and Resident Engagement role agents were consulted. Their views are judgement and sector hypotheses, not company facts; staff rules, retention schedules, workbook owners and the DPIA status are unknown.

Staff concern to control mapping:

| Staff concern | Control in the design | Gap |
| --- | --- | --- |
| Loss of control | Named rules enforced by server-side gates and an authority matrix (FR-036); Excel is an import source and source workbooks are never modified (FR-029, DD-004). | Transition path is a hypothesis pending OQ-012. |
| Where is my data | `uksouth` recommended for the whole stack; constructed data only (NFR-005). | No single residency claim until OQ-012; `uksouth` has no data-zone model so inference may be processed outside the UK. |
| Who can see it | Server-side role, record and field rules (NFR-003); Entra-only access; per-workload identities. | Entra roles, SQL contained users and cross-role denial are unexercised. |
| Can I get it back | FR-030, NFR-006, NFR-010 export with history; SQL point-in-time restore. | AC-032 not started; no restore drill; no Excel-shaped export. |
| Can it be changed silently | SQL ledger, immutable `audit-archive`, versioned rules. | Ledger digest upload and scheduled verification are not configured. |
| Does AI touch it | Agents have no data-store role and only post proposals; AI output labelled and needs human approval. | Not yet visible to staff. |
| Am I being watched | Audit records decisions and handoffs. | Staff need a written statement of who may read logs and for what, agreed with staff and HR (unknown). |
| System down | Tested out-of-hours route and rollback required before Excel retirement. | An offline break-glass list for hazard and vulnerable cases is needed; clocks do not pause for outages. |

Make visible to staff (proposed, MVP unless stated):

* A plain-language "your data" page: what is held, where, who holds which role, what AI can and cannot do, and the rule that governs each point. Each compliance statement carries a status of verified, designed or unknown.
* Per-case history showing who viewed or changed a record and why, including imports and exports.
* Export of a user's caseload to Excel or CSV with source, version and history, usable without the workbench or an AI provider.
* A read-only Excel mirror and an import preview showing every row disposition with the source file untouched.
* "AI-drafted, human-approved" labels and explanation records.
* A verify-integrity action that runs the ledger check and shows the result (later, after digest storage exists).

Keep invisible: private endpoints, managed identities, NSGs and cost controls, summarised in one line.

Gaps to close first, in order:

1. Ledger digest storage to an immutable container and scheduled verification.
2. Exit and export path (AC-032) and a round-trip test.
3. One point-in-time restore drill with the date, recovery time and record-count match recorded.
4. Residency decision (OQ-012): record `uksouth` with the inference caveat and remove stale split-region wording.
5. Exercise the identity path: Entra roles, SQL user script and a cross-role denial test.
6. A staff-facing surface for items 1 to 4.
7. Defer Front Door and WAF, Graph egress and AI Search until real personal data is planned.

Claims not to make without named human legal, compliance or DPO approval: "compliant" with UK GDPR, Awaab's Law or the RSH standard; "tamper-proof" or "immutable" audit (the ledger is tamper-evident); "UK-resident" or "private-only"; "DPIA done", "consent managed" or "AI is overseen"; "Excel retired" before staff sign-off, a rehearsed fallback and data protection approval. Use "designed to support" instead.

Adoption red lines raised by the role views: double entry, dual write with no source of truth, audit logs used for individual performance management without agreement, silent AI edits to staff or vulnerability records, and no tested fallback. Staff messaging hypothesis: the spreadsheet becomes a read-only view of one governed record, and the audit trail protects residents and staff. This needs testing with staff.

Trust measures to observe in the demonstrator (thresholds need owner approval): task completion on the export, history and provenance tasks against the current Excel method; whether staff can state where data lives and who sees it; reconciliation rate and unmatched counts; audit completeness; restore-test age and result; parallel-run divergence; export round-trip result; residency attestation per service. A synthetic dataset can test that these measures detect problems; it cannot show the organisation's own rules are met.

Demonstration plan (about 15 minutes, no new services): import a constructed workbook with a preview and an untouched source; edit a case and show its history; show one case under two roles with a denied attempt and log entry; raise an AI draft that a human accepts or rejects; trigger a business rule (RULE-006 or RULE-008); tamper with a scratch copy and show the integrity check fail; export to Excel with no AI involved; show the restore drill result; close with the data page and the residency statement.

## Data handling and retention alignment

The addendum Data Handling and Retention Baseline (proposed, 2026-10-08) turns into these architecture rules. All remain proposals for DPO and Legal approval.

| Baseline rule | Architecture response | Status |
| --- | --- | --- |
| Storage limitation, deletion and erasure | A scheduled retention job per data class with owner approval and a log of deletions only; SQL ledger tables record history, so deletion of personal content needs a design that keeps the hash chain valid, such as storing personal content outside the ledger and hashing references. | Not built. Open design item |
| Audit survives deletion without personal content | Audit events hold identifiers and hashes, not free text. | Prototype follows this; needs verification |
| Backups and restore | SQL point-in-time restore window set to the approved period; restores re-apply deletions. | Window not set from an approved schedule |
| Logs and telemetry | Log Analytics and Application Insights retention set to a short operational default; the immutable `audit-archive` container carries the longer security and audit record. Immutable storage conflicts with erasure, so it must hold no personal content. | Retention values need owner approval |
| Transfers and residency | Region recorded per service in this ADR; inference may process outside the UK in `uksouth`, so no personal data goes to model deployments until approved (DH-006). | Constructed data only |
| Processors | Microsoft and any model or contractor service needs a written processor agreement before real data. | Not evidenced |
| Evidence a reviewer expects | Approved schedule, record of processing, DPIA, processor and transfer records, deletion and restore tests. | None exist yet |

Deployment note (2026-10-08): the first `uksouth` deployment into the recreated `ama` resource group failed with `VaultAlreadyExists`. The Key Vault name was derived from the resource group ID, which is identical when a group is recreated, and an earlier purge-protected vault held the name. The name now also hashes the location and a version salt.

Result: the redeploy `warm-dev2` into `ama` (`uksouth`, `allowPublicNetworkAccess=true`, default gpt-4.1 and gpt-4.1-mini at GlobalStandard) succeeded in 9 min 13 s.

## Open items

* RAI task/impact inventory, named residual-risk and incident owners, version-bound release evidence and PRD AC-062 to AC-066 before operational activation.

* Approve the retention schedule and resolve how ledger tables and immutable audit storage coexist with erasure.
* Azure Policy assignments and subscription-level Defender plans.
* Add Front Door Premium, WAF and the Private Link origin to the internal environment, plus an Entra app registration, once a public edge is needed.
* Confirm the Foundry model names, versions, SKUs and quotas in the chosen region, and set `modelDeployments` from the PRD evaluation results.
* Container hardening (non-root user, read-only root file system, dropped capabilities) is an application image requirement; Container Apps does not expose these settings, so enforce them in the Dockerfile and scan images in CI.
* Build the application images; the default placeholder image only proves the infrastructure.
* Consider Azure Policy assignments, Defender for Containers and cost budgets at subscription level.
* A multi-region or zone-redundant design is not included (`zoneRedundant` is a parameter).

## Validation performed

* `az bicep build` and `az bicep lint` are clean on `main.bicep` and every module.
* `az deployment group what-if` reported 93 creates, then the stack was deployed to resource group `ama` as `warm-test` in `uksouth`: all modules succeeded, both Container Apps are running, and both model deployments (`gpt-4.1-mini`, `gpt-4.1`) provisioned.
* Deployment findings fixed in the template: Foundry project and model deployments conflicted when created in parallel (now serialised); the SQL admin principal type is a parameter. The Container Apps environment failed with `AKSCapacityHeavyUsage` twice in `swedencentral`, so the validated region is `uksouth`. Region capacity is therefore a real deployment risk.
* The container images are the placeholder quickstart image, so no application behaviour, load, latency or cost has been measured. A4 and A5 evidence remains design and deployment only.
* The SQL contained-user script, the Entra app registration, the SharePoint site and the Teams webhook have not been exercised.
