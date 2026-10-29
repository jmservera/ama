<!-- markdownlint-disable-file -->

# Microsoft Fabric Project Fit: Infrastructure and Governance Lane

| Field | Value |
| --- | --- |
| Status | Complete |
| Cycle / wave | 1 / Wider |
| Lane | Internal: infrastructure, operations, governance, maturity evidence |
| Source baseline | 9b74ac8daaec2a880172e43161b37ac7f2c3f801 |
| Parent artifact | .copilot-tracking/research/2026-10-29/microsoft-fabric-project-fit-research.md |
| Approved artifact | .copilot-tracking/research/subagents/2026-10-29/fabric-infrastructure-governance-subagent-research.md |
| Research posture | Balanced, bounded platform-fit evidence review |
| Limits | Read-only source and evidence inspection. No cloud, private-data, secret, install, deployment, spending, git, or gate execution. |

## Delegated Questions and Criteria

Investigate actual implementation rather than assume diagrams describe deployment. Establish the Azure services and profiles represented in source and evidence; demonstrated versus source-only topology; deployment and operational overhead; availability, recovery and monitoring; identity and resident/staff boundaries; budget and unknown headroom; operational, RAI and accessibility acceptance gaps; development tooling complexity; and whether a further SaaS analytics platform would fill an evidenced need or duplicate current capability.

Permitted source scope: README.md, src/README.md, component package overview, infra/README.md, main.bicep and controlling modules/SQL/readiness contracts, identity/secrets/network/recovery/diagnostic contracts, .github/workflows, tools/rpi-checks.py, docs/architecture cut-over evidence, docs/case_study_48_addendum.md budget decision, latest project RAI and relevant security/UX acceptance evidence, and capstone/documentation evidence only for architecture/business maturity.

Non-goals: exhaustive security, legal, or conformance audit; platform selection or recommendation; source/documentation modification; live validation. The parent owns synthesis and platform decision.

## Initial Evidence Goal

For this Wider wave, map credible infrastructure and governance evidence that supports, weakens, or leaves unresolved the platform-fit assumptions. Preserve the difference between design intent, offline source/test evidence, and observed cloud or human acceptance.

## Research Log

* Preflight: approved path is under .copilot-tracking/research/subagents/2026-10-29/ and differs from the parent primary artifact. Passed before this write.
* Intake evidence: README.md identifies the repository as a research-backed proposal and points to source, infrastructure, architecture and case-study evidence. src/README.md records five isolated PEP 420 distributions, dependency boundaries, container images and a substantial local validation matrix. infra/README.md explicitly labels its Bicep architecture proposed/non-production and distinguishes offline-tested pipeline definitions from observed Azure deployment.
* Finalized: controlling Bicep, operational evidence, CI gates, budget decision and RAI/accessibility evidence inspected. No source, cloud, gate or environment operation was performed.

## Findings

### Component inventory and maturity

| Component | Source evidence | Maturity relevant to platform fit |
| --- | --- | --- |
| Five Python distributions | src/README.md:11-27 | Core, API, agents, orchestrator and importer are isolated PEP 420 packages. API may still import agents; workers/importer are separate images but not evidence of an integrated analytical platform. |
| Azure SQL database | infra/main.bicep:274-292; infra/modules/sql.bicep:38-106 | Private, Entra-only serverless SQL database with ledger, audit, threat protection, 14-day short-term retention and Log Analytics diagnostics. It is the implemented programme-state/controlled-record store, not an analytical replacement candidate. |
| Storage, identity, registry, Container Apps and Foundry | infra/main.bicep:183-312; docs/architecture/README.md:130-147 | Per-workload identities and private-oriented components are authored. The current API directly hosts workflow and five assistants; workers/queues/importer are explicitly deferred/proposed. |
| IoT | infra/main.bicep:31-44,313-333; src/core/README.md:44-166 | B1 Hub settings and a private endpoint/routing design exist. The executable consumer/replay is deliberately finite constructed SQL processing, capped at 100 homes and 100,000 original home-slot combinations, not production throughput proof. |
| Operations | infra/modules/monitoring.bicep:14-103; infra/main.bicep:530-615 | Log Analytics, Application Insights, AMPLS/private endpoints, email/optional Teams action group, model/SQL/API alerts, ledger-mismatch/missing-verification alerts and budget notifications are declared. Architecture evidence states full structured application tracing is not established. |
| Delivery and validation | .github/workflows/src-ci.yml:1-360; .github/workflows/src-deploy.yml:1-300; .github/workflows/infra-plan.yml:1-109; tools/rpi-checks.py:30-62,152-172,336-360 | CI exercises unit/dependency/lint/type, browser/axe, SQL Server, Bicep, container, Trivy and SBOM contracts. Release/what-if deployments require protected environments, private runners and OIDC. These are source/pipeline contracts, not evidence that the releases or target Fabric tenant ran. |

### Strongest observations

1. **Existing Azure service set is already broad and purpose-specific.** The Bicep entry point wires identity, VNet/DNS/NSGs, monitoring, Key Vault, storage, registry, SQL, Foundry, IoT and Container Apps (infra/main.bicep:183-359). A Fabric addition would introduce a further SaaS/security/cost/operating boundary rather than replace an absent data platform. This supports a high bar for a separate analytics need.
2. **SQL is a controlled transactional ledger, not spare analytical storage.** SQL is private and Entra-only; it uses ledger, short-term backup retention, audit and threat-protection declarations (infra/modules/sql.bicep:20-106). The architecture identifies SQL as controlled workflow/audit/proposal state and explicitly says append-only/hash-chain evidence is not external immutable anchoring proof (docs/architecture/README.md:124-145,230-231). A future replica/analytics sink must preserve SQL as authority and separately resolve retention, audit and data-minimisation consequences.
3. **The implemented analytical demand is bounded and synthetic.** The core sensor consumer/replay has finite, constructed, SQL-only scopes and specifically disclaims throughput/sizing and live IoT acceptance (src/core/README.md:44-166). Bicep's B1 Hub and 1-7-day retention are an authored exercise profile, not demonstrated continuous telemetry needing a real-time analytics estate (infra/main.bicep:31-44,313-333).
4. **Source topology is not deployment proof.** infra/README.md:7-20 labels the infrastructure proposed/non-production. Architecture documentation distinguishes current single API/SQL proposal service from deferred queues/workers, and states the visual topology is not a fresh Azure inventory (docs/architecture/README.md:21-35,145-147,197-231). The cut-over pack has some bounded provider observations, but records no successful publication/deployment record for the private publisher path and unresolved browser/role/SQL/AI acceptance (docs/architecture/cutover-evidence-pack.md:43-71).
5. **Exercise and pilot/production profiles have materially different gates.** `main.bicep` defaults to a production profile but supports explicit development exceptions, scale-to-zero, direct demo ingress and placeholder images; guard conditions require region/quota evidence, private backing, pilot locks and role/auth constraints (infra/main.bicep:1-177). A platform addition would need to define its own equivalent profile, capacity, network, identity and operating acceptance, not inherit Bicep's generic tags or alerts.
6. **Observability and recovery are engineered foundations, not accepted operations.** Monitoring resources use private-only telemetry endpoints and action groups (infra/modules/monitoring.bicep:14-103); alerts cover throttle, SQL CPU, API failure/restarts and ledger job signals (infra/main.bicep:402-582). However full structured traces are not established (docs/architecture/README.md:145), SQL backup retention/zone settings are configuration rather than restored-service evidence (infra/modules/sql.bicep:51-63), and the RAI review marks witnessed restore/restart, response ownership and thresholds unknown (docs/reference/research/rai/project-rai-review.md:88-99,115-116,174-182).
7. **Identity boundaries are deliberately workload- and audience-specific.** Four user-assigned managed identities are created per workload (infra/modules/identity.bicep:6-35); architecture evidence distinguishes Entra staff authentication, case scope, resident record-use permission, Graph own-photo and token renewal boundaries (docs/architecture/README.md:119-144). A wider analytical service would require a separately evidenced access model; it cannot safely assume staff, resident, token-store or system identities can share a workspace.
8. **Current budget capacity for a new paid service is unknown, not USD 700.** The current owner decision states USD 700 was an October all-in ceiling whose authority expired on 2026-10-25; the 2026-10-23 refresh says all-in actual, month-end forecast and comparable headroom are Unknown/Blocked due to incomplete scope (docs/case_study_48_addendum.md:414-421,523-599). Bicep's default `monthlyBudget=300` and 80%/100% notifications are local alerts, not a confirmed funding envelope or hard stop (infra/main.bicep:25-26,584-615).
9. **Operational, RAI and accessibility gaps dominate the next maturity constraint.** The latest whole-project RAI review reports substantial synthetic controls but no qualified whole-project operational acceptance, and no model authority beyond recommend/draft/flag (docs/reference/research/rai/project-rai-review.md:7-33,67-99). It records unverified effective least privilege/retention and unrun assistive-technology/human acceptance, with contrast and unfixed-image concerns (docs/reference/research/rai/project-rai-review.md:115-116). Fabric would not itself discharge these gaps.
10. **Delivery tooling is intentionally substantial.** CI and the local RPI runner combine five package suites, SQL Server selectors, Bicep/actionlint, browser/axe, Docker/hardening, Trivy/SBOM, requirements and dirty-tree/base checks (src/README.md:45-167; .github/workflows/src-ci.yml:49-360; tools/rpi-checks.py:30-62,152-172). Any platform integration needs a tested contract and protected-environment/OIDC route; a workbook-only or tenant-side configuration would be outside present reproducibility evidence.
11. **Current source does not establish a missing SaaS analytics workload.** The existing staff dashboard is explicitly synthetic demonstration data and provides semantic-table alternatives (src/api/README.md:90-171). The architecture describes intended metrics/operations but lacks demonstrated cross-system historical reporting, data-lake scale, BI audience, real-time query SLA, tenant capacity or capacity economics. This leaves an analytical sidecar unresolved, not justified by source evidence.

## Contradictions and Clarifications

* **Proposed versus observed:** infra/README.md:7-20 calls the entire Bicep estate proposed/non-production, while docs/architecture/cutover-evidence-pack.md:43-71 preserves limited real-provider inspection and synthetic proof activity. They are compatible only when provider observations are treated as bounded component evidence, not proof of the authored full topology or user acceptance.
* **Historical versus current budget:** older USD 500/535.41 illustrations are explicitly superseded; the current local source says the USD 700 authority expired and all-in headroom remains Unknown/Blocked (docs/case_study_48_addendum.md:414-421,592-599). The Bicep USD 300 budget parameter is an alert default, not contradictory funding approval.
* **Historical RAI acceptance versus latest review:** the 2026-10-14 report has planning-only owner acceptance and operational approval NOT_GRANTED (docs/reference/research/reports/2026-10-14/rai-report-ama-20261014.md:1-41); the newer 2026-10-28 review confirms synthetic controls but not qualified operational, accessibility or human acceptance (docs/reference/research/rai/project-rai-review.md:7-33,115-116). Neither establishes readiness for another data platform.
* **Profile intent versus exercised deployment:** Bicep defaults to production guards (infra/main.bicep:93-177), but exercise evidence includes development/direct-ingress/placeholder and deferred-worker paths (docs/architecture/README.md:145-147,197-231). A claim that these settings demonstrate pilot resilience or Fabric connectivity would be contradicted by the source.

## Evidence Relationships for Parent Synthesis

| Delegated question | Relationship | Confidence | Provenance |
| --- | --- | --- | --- |
| Existing services and purpose | Supports: current estate already supplies transactional storage, files, AI, IoT ingestion design, runtime, security and operations primitives | High for source presence; medium for deployed state | infra/main.bicep:183-359; src/README.md:11-39 |
| Demonstrated versus source-only topology | Weakens any claim of a fully deployed analytics-ready platform | High | infra/README.md:7-20; docs/architecture/README.md:21-35,145-147,197-231; docs/architecture/cutover-evidence-pack.md:43-71 |
| SQL authority and system-of-record constraints | Supports: retain SQL controlled state; treat external analytics as derivative with new governance | High for configuration/design; low for production effectiveness | infra/modules/sql.bicep:20-106; docs/architecture/README.md:124-145,230-231 |
| Operational overhead and recovery | Supports: an additional platform would need separate network, identity, CI, monitoring, recovery and acceptance integration | High for existing burden; medium for incremental burden inference | infra/modules/monitoring.bicep:14-103; .github/workflows/src-deploy.yml:1-300; tools/rpi-checks.py:30-62 |
| Identity/resident/staff boundaries | Supports: identities and human/consent boundary are distinct; a shared analytics access model is unproven | High | infra/modules/identity.bicep:6-35; docs/architecture/README.md:119-144; docs/reference/research/rai/project-rai-review.md:67-99 |
| Cost headroom | Disproves: USD 700 is available headroom for a Fabric purchase | High | docs/case_study_48_addendum.md:414-421,523-599 |
| Existing acceptance gaps | Supports: analytics platform adoption cannot close operational/RAI/accessibility acceptance independently | High | docs/reference/research/rai/project-rai-review.md:7-33,115-116,174-197 |
| Current need for SaaS analytics | Leaves unresolved: source shows synthetic dashboard/sensor exercises but no demonstrated cross-system BI or scale requirement | Medium | src/api/README.md:90-171; src/core/README.md:44-166; docs/architecture/README.md:145-147 |

## Disconfirming Evidence Needed

* An owner-approved, non-sensitive workload inventory showing multiple governed source systems, material historical/reporting latency pain, user audiences and a recurring BI/stream-analysis decision that SQL/dashboard exports cannot meet.
* Tenant evidence of approved Fabric capacity/licensing, region, account-effective cost and all-in headroom, with a named operating/identity/access model.
* A bounded proof that a derivative pipeline can read permitted SQL/IoT data without changing SQL authority, duplicating resident/staff data unnecessarily, or weakening retention/consent/audit controls.
* Observed operating evidence: monitored pipeline/semantic-model recovery, alert ownership, accessibility and human acceptance, plus RAI/DPO/security decisions for the added data copies.

## Gaps and Stop Decision

* Not inspected or established: live tenant Fabric availability/capacity/license/region; live Azure inventory beyond retained evidence; actual query volumes, BI consumers, source-system count, reporting latency, service SLOs, agreement pricing or current spend headroom; deployment/recovery operation; human accessibility, DPO/security and operational acceptance.
* No external Fabric-product research is included in this internal lane; the parent owns external capability comparison.
* Stop decision: delegated internal Wider criteria met. Further source reads are likely redundant for the bounded infrastructure/governance question. Parent synthesis must not convert source/pipeline contracts into deployed or accepted service claims.