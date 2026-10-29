<!-- markdownlint-disable-file -->

# Task Research: Microsoft Fabric Project Fit

| Field | Value |
|---|---|
| Date | 2026-10-29 |
| Researcher / agent | GitHub Copilot; rpi-research |
| Status | Complete; source/public-documentation assessment, not live acceptance |
| Artifact path | .copilot-tracking/research/2026-10-29/microsoft-fabric-project-fit-research.md |
| Source baseline | 9b74ac8daaec2a880172e43161b37ac7f2c3f801 |
| Branch | jmservera/fabric-research; clean at intake; tracking origin/jmservera/fabric-research; no PR found |

## Research Brief

* What to research: review Zava Forward's major components and determine whether Microsoft Fabric provides justified value or avoidable complexity.
* Why it matters: choose capabilities for demonstrated housing-programme needs rather than increase the service count for its own sake.
* Audience or intended use: project owner and executive, architecture, data and engineering reviewers.
* Scope: business requirements; core workflow and SQL persistence; agents; API and staff/resident sites; orchestration; importer and synthetic/IoT data; infrastructure, identity and operations; analytics, reporting, evaluation and delivery evidence.
* Non-goals: no application or infrastructure changes, deployment, paid trial, data export, purchases, issue creation, commit, push or approval. No private datasets or private support/cohort material. A whole-project architecture and capability assessment is not an exhaustive line-by-line security audit or operational acceptance.
* Criteria: unmet need, workflow authority, workload scale and latency, cross-system integration, analytical history, privacy and authorization, reliability, cost and team overhead, evidence maturity and simpler alternatives.
* Requested outputs: evidence-backed project/component review, current Fabric research, alternatives, conditional recommendation and reversal criteria.
* Output mode: convergence, limited to an advisory platform-fit recommendation; no implementation handoff is requested.

## Research Parameters

| Field | Value |
|---|---|
| Research questions | Q1-Q7 below |
| Codebase scope | c:/src/ama; current src/, infra/, tools/ and relevant docs/ |
| External scope | Official Microsoft Learn, Fabric pricing/licensing and service documentation |
| Initial internal candidate areas | README.md; src/README.md; component READMEs and controlling implementations; ADR 0001-0006; BRD/PRD; data, IoT, UX, RAI and pilot evidence |
| Initial external candidate areas | Fabric overview; OneLake; Azure SQL mirroring; Data Factory; Power BI and Direct Lake; Real-Time Intelligence; capacity, licensing, security and regional support |
| Research posture | balanced |
| Posture provenance | Default: thorough breadth across a bounded platform-fit decision, with adjacent research where it could change the answer |
| Explicit limits / deadline | None supplied; research-only and no spending or live-data access |
| Completion basis | Component coverage and adequate evidence for material claims; preserve tenant, price and live-workload unknowns rather than infer them |
| Edits allowed during research | Evidence only; no application or infrastructure edits |
| Resolved evidence root | .copilot-tracking/research/ |
| Known constraints | Azure SQL is the documented programme-state authority; current budget and acceptance status must be verified; generated data is not company evidence |

## Extension Registry and Provenance

* Precedence: host safety; explicit caller scope; repository instructions; research contract; scoped domain skills.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
|---|---|---|---|---|
| Instruction | .github/copilot-instructions.md | Repository-wide, supplied in context | Required project entry reading, knowledge-base durability, branch and evidence safeguards | Selected; no commit/push requested |
| Instruction | context7.md and context7-mcp | Cloud-service documentation question | Prefer current retrieved documentation | Selected; Context7 tools not exposed by tool discovery; use Microsoft Learn MCP and disclose fallback |
| Instruction | copilot-tracking.instructions.md | Research artifact path | Dated primary and independent lane artifacts; parent owns synthesis | Selected |
| Instruction | markdown.instructions.md; writing-style.instructions.md; licensing-posture.instructions.md | Markdown and tracking evidence | Plain-language, ASCII, paraphrase with provenance; tracking template exception | Selected |
| Skill | rpi-research | Evidence, alternatives and platform-fit research | Ordered Wider, Deeper and Contrarian waves; no implementation | Selected |
| Skill | code-review | User requests a thorough project review | Evidence-first risk framing | Entry read; diff-review workflow skipped because no change set was supplied and this is a project/platform assessment |
| Research specialist | RPI Researcher | Registered general internal/external research agent | Independently owned bounded component evidence; no final platform decision | Selected for independent repository lanes |
| Research specialist | System Architecture Reviewer | Registered architecture trade-off specialist | Potential independent architecture review | Skipped: a bounded RPI Researcher contrarian lane answered the independent uncertainty without invoking a formal review/ADR phase |
| Skill | web-design-guidelines and accessibility | Web changes or standalone UI/accessibility audit | Current source and defined interaction evidence | Skipped as an audit workflow: no web changes or conformance claim; inspect existing UX evidence for platform relevance |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
|---|---|---|---|
| Intake | Request names the project, desired depth, decision and starting source; no blocking clarification needed | No questions asked | Review all major components; investigate current Fabric and simpler alternatives |
| Direction change | No material direction change yet | Not applicable | Preserve research-only boundary |
| Convergence | Component evidence, full official sources and independent contrarian challenge support conditional advice without a tenant query | No further user question needed to answer the current request | Advise retaining operational authority and deferring mandatory dedicated Fabric; preserve conditional analytics evaluation and owner decision |

## Scope and Success Criteria

* Scope: breadth across every major component, with detailed reads at the data/authority boundaries that control the Fabric decision.
* Assumption to test: Fabric may help shared analytical history but is unlikely to replace transactional approvals or solve the project's existing acceptance gaps.
* Cheap discriminating check: inspect the SQL schema/store, reporting implementation and declared IoT throughput for a concrete unmet historical, cross-system or stream-analysis requirement; verify Fabric's supported ingestion against that actual schema.
* Success criteria: every question answered or its smallest missing evidence named; material facts linked to code locations or current official sources; distinguish documented intent, source implementation, local tests and live acceptance; compare simpler alternatives and record conditions that could reverse the advice.

## Task Research Requests

* Explicit requests: thorough project review, research Microsoft Fabric, determine benefits versus overengineering, starting with the supplied Microsoft Learn overview.
* Inferred questions: whether Fabric should replace any current service, whether an optional analytical sidecar makes sense, and which scale, governance or economics would justify it.
* Caller constraints and non-goals: no implementation or billable action was requested.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
|---|---|---|---|
| add | Review all major project parts and Fabric fit | User request, 2026-10-29 | Component coverage is required; avoid deciding from the overview alone |
| exclude | No private data, live changes, spending or approval | Repository instructions and research scope | Source and public-documentation assessment only |
| narrow | Distinguish project assessment from exhaustive security/conformance audit | Evidence discipline | Do not imply unperformed runtime, human or acceptance checks |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|---|---|---|---|---|
| Q1 | What do the project and its major parts actually implement, versus propose or leave unaccepted? | breadth | H | answered at component/source level; live state not established |
| Q2 | What data, reporting, analytical history and IoT workloads require a new platform, if any? | depth | H | answered conditionally; production workload/query pain unavailable |
| Q3 | Which current Fabric capabilities fit those requirements, and what are their product limits? | breadth | H | answered from current official documentation |
| Q4 | Can actual Azure SQL and event schemas be ingested without breaking authority or duplicating sensitive data unnecessarily? | depth | H | supported options identified; exact selected tables/tenant path untested |
| Q5 | What licensing, capacity, regional, security, operational and cost burdens would adoption introduce? | breadth | H | model and constraints answered; tenant/agreement quote unavailable |
| Q6 | Which smaller alternatives and strongest pro-Fabric arguments challenge the initial hypothesis? | depth | H | answered; independent contrarian evidence reconciled |
| Q7 | What is the recommendation now, and what measurable future conditions would reverse it? | depth | H | answered; advisory only, no implementation authority |

## Prior Knowledge Gate

* Reviewed at intake: docs/case_study_48_original.md; opening and exercise-baseline sections of docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md.
* Starting claims to verify: 60,000 generated stock records and a distinct retained 980-case lineage; SQL programme-state authority; bounded advisory agents; IoT evidence and human/operational gates remain distinct.
* Reused verified findings: clean dedicated research branch and exact source commit, observed through read-only Git commands.
* Superseded or stale: earlier USD450 exercise budget is historical; current budget must be read before any affordability claim. Memory is context, not evidence.

## Research Cycle Log

### Cycle 1

* Active controls: project-wide component coverage, current official sources, read-only/no-spend boundaries.
* Active posture and completion basis: balanced; adequate evidence across all material platform-fit criteria.
* Explicit limit effect: no live tenant, private workload or paid experiment will be assumed.

#### Wave 1: Wider

* Plan: independent internal lanes for transactional/API/agent architecture; data/IoT/analytics; and infrastructure/operations/evidence. Parent investigates current official Fabric capabilities.
* Worker evidence relationships: all three RPI Researcher lanes completed. Operational evidence locates authority in API/core/SQL and role-projected advisory paths; data evidence distinguishes 60,000 stock from 980 cases, finite streaming from historical generation and actual imports from simulated source-system labels; infrastructure evidence distinguishes authored topology, bounded provider observations and unmet operational acceptance.
* Available lane artifacts: .copilot-tracking/research/subagents/2026-10-29/fabric-operational-architecture-subagent-research.md; .copilot-tracking/research/subagents/2026-10-29/fabric-data-analytics-subagent-research.md; .copilot-tracking/research/subagents/2026-10-29/fabric-infrastructure-governance-subagent-research.md.
* Reflection: Wider completed through the three component lanes, direct SQL inspection and official Fabric workload/replication/licensing discovery. The SQL schema is relational-plus-JSON, not an already curated analytical model. Historical synthetic sensor generation is material counter-evidence to dismissing analytics on average events/second alone. Current Fabric documentation and actual Azure SQL ledger/schema restrictions control Deeper; no adoption verdict yet.

#### Wave 2: Deeper

* Parent-prioritized material: actual SQL schema and ledger/history support; minimum-field analytical projection; source permission propagation; source/private connectivity; historical versus stream scale; licensing and active-capacity economics.
* Plan and evidence: parent inspected mssqlstore.py:1-305, infra/modules/sql.bicep:1-150 and the current cost decision at addendum:414-605; retrieved and read full official overview, Azure SQL mirroring limitations, mirroring overview, licensing and Fabric SQL limitations.
* Reflection: Deeper completed. The current case body is NVARCHAR(MAX), not native SQL json; the rowversion-named field is BIGINT, not native rowversion. Mirroring excludes ledger history tables, not all ledger current tables. Fabric SQL database cannot create ledger tables, so it is not an equivalent replacement for the existing authority. Source permissions/masks do not propagate to OneLake and mirror history is not durable business history by default. Private SQL gateways, Entra/workspace identity and private/keyless Eventstream options are documented. Exact selected gateway/auth/region support still needs tenant verification. Later IoT integration resolves historical identity owner blockers prospectively. PRD portfolio analytics is an explicit requirement. VNet gateway uptime, Eventstream processing, Eventhouse consumption and Direct Lake guardrails/security mean F2 retail price alone is not a solution quote. Contrarian now tests whether shared capacity and existing historical scale make a bounded Fabric option worthwhile immediately.

#### Wave 3: Contrarian

* Challenge targets: existing shared capacity, low-cost mirroring, explicit portfolio requirements, already generated historical sensor series and managed SaaS integration as a possible reduction in net complexity.
* Plan: one independent bounded RPI Researcher lane tests the strongest case for using Fabric now, false objections, smaller alternatives and whether the proposed defer-operational/add-optional-analytics framing survives.
* Evidence: .copilot-tracking/research/subagents/2026-10-29/fabric-contrarian-fit-subagent-research.md; independent lane K1-K14, read in full by parent.
* Reflection: a blanket no-value/overengineering verdict is not supported. Explicit reporting requirements, generated historical scale, managed replication and potential shared capacity justify a selective analytics evaluation. They do not prove a dedicated capacity is necessary or that it beats SQL/read models plus Power BI. Retain the source/API authority and test one curated KPI before adding a mandatory runtime dependency. Corrected objections and historical chronology are preserved above.

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Parent disposition | Rationale | Treatment |
|---|---|---|---|---|
| Keep API/core/Azure SQL as programme authority | C1-C4, C10-C11, W5 | accepted | Existing controlled ledger/domain behavior and no like-for-like Fabric SQL ledger | Selected advisory architecture boundary |
| Make Fabric mandatory now | C5-C13, W1-W16 | rejected | Reporting need is real but incremental platform necessity, capacity, comparative value and live authority are not established | Defer dedicated mandatory adoption, not analytics |
| Fabric is inherently overengineering or has no present value | C12-C13, W3-W4, W10-W14; contrarian K1-K6 | rejected | Historical analytics and reusable semantics are credible; managed/shared capacity can reduce plumbing and marginal cost | Conditional analytical option retained |
| A selective Fabric analytical sidecar can be evaluated | C12-C13, W2-W4, W7-W16 | accepted | Plausible fit if governed scope, economics and one workload are verified | Advisory option, not approved implementation |
| SQL/read models plus Power BI must be sufficient/free | C3, C13, W4, W11 | rejected | Source load, semantics, private access, licensing and latency still need measurement | Smaller comparator, not an asserted winner |
| Any mirroring is impossible because of ledger, JSON, rowversion or private networking | C10-C11, W2, W7-W9, W16 | rejected | Restrictions are narrower than those blanket claims | Preserve exact compatibility conditions |
| Tenant-specific capacity, cost, data approvals and performance | C9, W3-W4, W6-W16 | deferred | No tenant/live/private-data query or experiment was requested | Explicit decision-changing evidence, not assumed zero |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no for the current advisory decision.
* Stop basis: all major components, material product constraints, simpler alternatives and strongest counterarguments are covered. Further public-source retrieval cannot establish tenant capacity, operating demand, agreement prices, governance approval or comparative performance. These remain conditional triggers, not hidden facts.
* Revised brief: none; no scope expansion, implementation or billable action.
* Readiness effect: research complete; implementation Planning Readiness Not applicable because the requested output is platform-fit advice, not a delivery plan.

## Evidence Log

* Delegation: three completed Cycle 1/Wider RPI Researcher lanes and one completed Cycle 1/Contrarian lane, named above. Deeper ran inline to reconcile the controlling source/product boundaries. Source observations and existing test definitions were inspected; application tests and live services were not rerun.

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
|---|---|---|---|---|---|
| C1 | Original case requests agent-supported retrofit prioritisation, assessments, funding, coordination and quality with human/resident boundaries | docs/case_study_48_original.md:19 | read_file | high | Problem specification, not delivered capability |
| C2 | Subsequent application builds require real AI, real SQL and Azure; SQL remains programme-state authority | docs/case_study_48_addendum.md:258; docs/case_study_48_addendum.md:274 | read_file and grep, parent | high | Exercise acceptance, not production approval |
| C3 | Indexed SQL case lists coexist with JSON case bodies and in-memory detail/statistics/export paths | src/core/src/zava_forward/core/sqlstore.py:1 | read_file, parent | high | Actual implementation; no performance measurement inferred |
| C4 | Operational approvals, deterministic ranking, chat ownership and bounded proposals remain core/API responsibilities | src/core/src/zava_forward/core/store.py:44; src/core/src/zava_forward/core/ranking.py:45; src/core/src/zava_forward/core/chat_isolation.py:58 | delegated read and neighboring tests | high | Operational lane I2/I4/I5/I11; test definitions read, not rerun |
| C5 | Synthetic source labels and 14-CSV discovery pack do not establish production-system integrations | docs/reference/research/retrofit-synthetic-data/data-dictionary.md:113 | delegated read | high | Data lane L1/L2; current reporting demand still unvalidated |
| C6 | Declared stream cadence is three paired observations/home/day; historical generated runs use distinct parameters | docs/reference/research/iot-sensor-analytics-research-plan.md:239 | delegated read | high | Data lane arithmetic: 180,000/day, about 2.08/s average; 43.8M-row generated history is separate |
| C7 | API replay/receiver is finite, opt-in and SQL-backed, not measured continuous production streaming | src/api/src/zava_forward/api/iot_stream.py:145 | delegated read and neighboring tests | high | Data lane L8/L9; actual transport and device evidence not established |
| C8 | Current architecture and delivery evidence separate proposed topology, local checks and observed provider components | docs/architecture/README.md:21; src/README.md:45 | delegated read | high | Infrastructure lane: no total-product acceptance claim |
| C9 | Later owner budget authority expired; actual all-in headroom remains Unknown/Blocked | docs/case_study_48_addendum.md:414; docs/case_study_48_addendum.md:592 | read_file, parent, corroborating infrastructure lane | high | Expiry 2026-10-25T16:02Z; no new spending authority |
| C10 | Bicep specifies private-only Entra SQL, serverless auto-pause and a ledger-enabled database | infra/modules/sql.bicep:20; infra/modules/sql.bicep:38 | read_file, parent | high | Authored configuration, not a fresh live inventory |
| C11 | SQL case body is NVARCHAR(MAX), named rowversion is BIGINT, and audit explicitly becomes append-only ledger in ledger-enabled databases | src/core/src/zava_forward/core/mssqlstore.py:30; src/core/src/zava_forward/core/mssqlstore.py:277 | read_file, parent | high | Must distinguish types and current rows from ledger history |
| C12 | Later approved IoT integration adopts canonical home and compact collision-checked sensor keys; a daily 730-day generated exercise reconciled 43.8M readings | docs/reference/research/iot-sensor-analytics-research-plan.md:414 | read_file, parent | high | Supersedes historical source/identity blockers prospectively; not live device, full-hourly scale or physical calibration acceptance |
| C13 | Portfolio heatmap, funnel, historical reporting and explainable scenario forecasts are explicit PRD requirements | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1395; docs/prds/zava-forward-retrofit-programme-demonstrator.md:409 | grep, parent | high | No claim that analytics is unnecessary; need to establish platform-specific incremental value |
| C14 | Importer is a bounded XLSX preview/mapping/quarantine/export library rather than a production multi-system integration platform | src/importer/src/zava_forward/importer/xlsx.py:14; src/importer/README.md:10 | delegated read and tests; parent grep of bounds | high | Source lineage is useful; real connectors/schedules/merge authority not established |
| C15 | Orchestrator includes token maintenance, ledger digest jobs and bounded source-monitor/rescan tooling; no general autonomous programme supervisor is established | src/orchestrator/README.md:9; src/orchestrator/README.md:21 | read_file, parent, and operational lane | high | Do not omit token job or equate pipeline orchestration with domain authority |
| C16 | Current API has historical/closed synthetic reporting and employee chat skills; workload/source labels and local-test limits remain explicit | src/api/README.md:150; src/api/README.md:207; src/api/src/zava_forward/api/progress.py:217 | read/grep, parent, and operational/data lanes | high | Old lane README line 154 is dashboard evidence, not current employee-chat heading; corrected here |
| C17 | Current agent guide retains unsupported-claim-with-valid-citation as a critical enablement failure despite scripted poisoning/injection coverage | src/agents/README.md:66 | read_file, parent | high | No evaluation rerun; not an invented actual-model failure or proof every old RAI issue remains open |
| C18 | Prior whole-project RAI review separates engineered controls from qualified human/legal/operational acceptance and identifies sensitive cross-store retention/access questions | docs/reference/research/rai/project-rai-review.md:8; docs/reference/research/rai/project-rai-review.md:105 | read_file, parent | high for the dated assessment | Earlier baseline 9bfed5; later #530/#531 work must not be described as still wholly undelivered |
| C19 | Five-package CI/local gates include SQL/browser/container/security checks; source definitions do not themselves establish full deployment/acceptance | src/README.md:45; .github/workflows/src-ci.yml:49; tools/rpi-checks.py:30 | delegated read | high | No full gate or publication performed in this research |

### External Evidence

| ID | Claim / finding | Source title | URL | Retrieved | Version/date | Confidence |
|---|---|---|---|---|---|---|
| W1 | Fabric is an integrated SaaS analytics/data platform with OneLake, Data Factory, Power BI, engineering/science, real-time and SQL database workloads; IQ is labelled preview | What is Microsoft Fabric? | https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview | 2026-10-29 | Current fetched page | high |
| W2 | Azure SQL mirroring does not propagate source RLS/object permissions/masking/labels; excludes ledger/temporal history, supports eligible current tables, truncates LOB values above 1 MB, and excludes native json/vector tables | Limitations in Microsoft Fabric mirrored databases from Azure SQL Database | https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-limitations | 2026-10-29 | Current fetched page | high |
| W3 | Database mirroring copies into OneLake; background replication compute and a capacity-linked storage allowance are free, queries are not; running capacity is required and mirror retention defaults to one day for newer portal-created items | What is Mirroring in Fabric? | https://learn.microsoft.com/en-us/fabric/mirroring/overview | 2026-10-29 | Current fetched page | high |
| W4 | F capacities start at F2; below F64 ordinary Power BI viewers need Pro/PPU/trial; PPU does not provide non-Power BI Fabric capacity; embedding has distinct rules | Understand Microsoft Fabric licenses and capacity | https://learn.microsoft.com/en-us/fabric/enterprise/licenses | 2026-10-29 | Current fetched page | high |
| W5 | Fabric includes a transactional SQL database, but ledger/ledger-history tables cannot be created there; it is not Azure SQL feature-equivalent | Limitations in SQL database in Microsoft Fabric | https://learn.microsoft.com/en-us/fabric/database/sql/limitations | 2026-10-29 | Current fetched page | high |
| W6 | Public pricing view displays F2 USD262.80/month, F64 USD8409.60/month and separate storage; displayed region is unspecified, so these are illustrative retail figures rather than UK South/agreement quotes | Microsoft Fabric pricing | https://azure.microsoft.com/en-us/pricing/details/microsoft-fabric/ | 2026-10-29 | Current retrieved pricing view | high for displayed figures; not a regional quote |
| W7 | Eventstream can ingest Event Hubs; its extended connection supports workspace identity and private-network options, unlike the basic shared-key setup | Add an Azure Event Hubs source to an eventstream | https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-source-azure-event-hubs | 2026-10-29 | Current fetched page; feature-level distinctions apply | high |
| W8 | Azure SQL mirroring supports private-source gateways and vCore service tiers; initial snapshot and replication can add source CPU/IO/log work | Mirroring Azure SQL Database | https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database | 2026-10-29 | Current fetched page | high |
| W9 | Private SQL mirroring needs a gateway/reachable endpoint and a primary SQL-server identity; granular source security must be configured anew in Fabric | How to secure mirrored data from Azure SQL Database | https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-how-to-data-security | 2026-10-29 | Current fetched page; UAMI preview and documented password path require exact verification | high |
| W10 | Fabric data agents are GA read-only conversational analytics, not domain action agents; use configured tables/user permissions, do not read unstructured files, require paid F2+ and feature-specific AI settings | Fabric data agent concepts | https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent | 2026-10-29 | Current concept page says GA; some tutorials/integrations still say preview | high |
| W11 | Power BI recommends Import by default; DirectQuery is for justified latency/size/governance requirements and adds per-visual source load and its own security/gateway obligations | DirectQuery in Power BI | https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about | 2026-10-29 | Current fetched page | high |
| W12 | Eventhouse is a managed KQL/event/time-series analytical engine, can expose data in OneLake and can suspend when unused; useful capabilities are not project performance evidence | Eventhouse overview | https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse | 2026-10-29 | Current fetched page | high |
| W13 | Eventstream has active processing/traffic/flat CU meters, separate retention costs and pause effects; at low throughput documented flat plus starting processor meters total about one CU-hour per active hour before traffic/destinations | Capacity consumption for Microsoft Fabric eventstreams | https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor-capacity-consumption | 2026-10-29 | Current fetched rates; subject to change | high |
| W14 | Direct Lake consumes curated Delta tables and capacity; F2 guardrails include 300M rows/table, 10GB model disk and 3GB memory; OneLake mode does not enforce SQL-endpoint RLS | Direct Lake overview | https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview | 2026-10-29 | Current fetched page | high |
| W15 | Standard VNet gateway consumption is 4 CU-hours per member-hour of uptime, in addition to analytical workload usage | Virtual network data gateways capacity consumption | https://learn.microsoft.com/en-us/data-integration/vnet/data-gateway-business-model | 2026-10-29 | Current fetched rate; chosen route applicability must be verified | high |
| W16 | Azure SQL mirroring tutorial documents Entra, service-principal and workspace-identity authentication, explicit table selection, source-server identity and permissions | Configure mirrored databases from Azure SQL Database | https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-tutorial | 2026-10-29 | Current fetched page; Entra server principal/UAMI preview notes retained | high |

### Contradictions / Conflicts

* Earlier budget figures and historical acceptance reports must not be presented as the current baseline; reconcile dated owner decisions before conclusions.
* Mirroring's detailed limitations do not justify saying every ledger current table is unmirrorable. Only ledger history is explicitly excluded in W2; base-table eligibility requires the actual schema check. Fabric SQL's absence of ledger support is a distinct replacement constraint (W5).
* The source has JSON text and a BIGINT field named rowversion. W2 restrictions on native json and native rowversion must not be falsely applied to those source fields (C11).
* W5's encryption prose and feature matrix differ on TDE. No encryption conclusion is drawn from that inconsistency; the ledger restriction is consistent and sufficient for this comparison.
* Search excerpts include older and newer connectivity/authentication descriptions. Use the full current source-specific page, not an older claim that all Event Hubs ingestion requires a public endpoint or shared keys. W7 documents private options and extended workspace identity; actual region/feature/tenant support remains a verification gate.
* W6's generic marketing prose suggests Free viewers suffice without stating the F64 threshold. Use the more specific licensing matrix in W4: smaller ordinary Power BI capacity workspaces still require viewer Pro/PPU/trial licenses, with separate embedding exceptions.
* Older IoT paragraphs and lane summaries emphasize producer identity incompatibility. The later approved integration at C12 resolves the historical source/identity owner blockers prospectively. It does not erase the old failed review or prove live identity/transport/actual case availability; do not report the old blocker as an unchanged current defect.
* Existing requirements explicitly include portfolio reporting and forecasts (C13). Statements that no analytics requirement exists would be false; what is not demonstrated is a requirement for this additional platform or measured inadequacy of the current/smaller path.
* Data-agent examples/search snippets retain preview labels, while the full concepts page states GA. Treat the core read-only feature as GA per W10 and retain preview/region/AI-policy verification for selected surrounding features.
* W9's security guide describes a password credential path, but the complete tutorial W16 also documents Entra, service principal and workspace identity. Do not claim mirroring requires enabling SQL password authentication. Do not assume the runtime workload identity is the separate logical-server primary identity or that every authentication kind works with every gateway.
* Four CU-hours/member-hour in W15 is a capacity-consumption rate, not a quoted cash fee and not proof that every private Fabric path uses that meter. An F2 provides two CU-hours/hour, so a continuously running member on that meter cannot fit its sustained budget by itself. Smoothing may accommodate bursts, not remove steady-state demand; on-premises gateways and Eventstream private endpoint paths need their own full costing.
* Direct Lake on OneLake and Direct Lake on SQL have different security/fallback behavior. SQL-endpoint RLS alone is not a security boundary for OneLake direct file access (W14); semantic-model/OneLake permissions and every allowed read path must be tested.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision implication |
|---|---|---|---|---|
| Q1 | Programme transactions and human/resident decisions have existing API/core/SQL authority; analytics would be derivative | C1-C4 | high | Do not treat a data platform as a workflow/approval replacement |
| Q2 | Portfolio reporting/forecasting is required and partly source-implemented; source inputs are synthetic and platform-specific query pain is not established | C5-C7, C12-C13 | high | Compare measured alternatives without denying the analytics requirement or inflating synthetic scale into production demand |
| Q5 | Source topology, funding authority and operational acceptance cannot be assumed from existing infrastructure definitions | C8-C9 | high | A platform addition needs separate economics and acceptance evidence |
| Q3-Q4 | Fabric SQL is a real OLTP offering, but its lack of ledger support makes it an unsuitable like-for-like replacement here | C10-C11, W1, W5 | high | Reject operational replacement, not the whole platform |
| Q4 | Mirroring requires new security and history semantics; it is not a governed, complete historical model by default | C3-C4, C10-C11, W2-W3 | high | Prefer a purpose-limited derived feed if a future analytical need is proven |
| Q5 | Free replication does not mean free analytical use; capacity and report-sharing licensing need a full marginal-cost comparison | W3-W4, C9 | high | Avoid both zero-cost claims and the false claim that F64 is mandatory for all Fabric use |
| Q3-Q6 | Fabric data agents can offer read-only executive analytical Q&A after semantics/security exist; they do not replace document-grounded domain assistants, resident chat/memory or approvals | C4, C13, W10 | high | Keep as a later optional analytical consumer, not an implementation prerequisite |
| Q5-Q6 | Private/keyless analytical ingestion is possible but requires explicit integration and operating work; a SQL/Power BI alternative also needs measured source load, security and private access | C10-C11, W7-W9, W11 | high | Compare complete operating costs and failure behavior, not service prices alone |
| Q2-Q6 | Historical sensor scale is a credible future lakehouse/Eventhouse use case; average daily event rate alone does not establish a streaming need, nor do row counts prove F2 model fit | C6, C12-C13, W12-W15 | high | Evaluate actual query/window/latency/concurrency plus encoded model and gateway load |
| Q1-Q7 | Import, domain AI, scheduled maintenance, frontends and delivery controls each retain work not replaced by a shared analytical platform | C4, C14-C19, W1, W10 | high | Component-specific platform fit, no service-count rationale |
| Q7 | Do not make Fabric mandatory or replace operational SQL; conditionally evaluate a curated analytical sidecar against the smaller SQL/Power BI path | C1-C19, W1-W16, contrarian K1-K14 | high for present boundary; conditional for future economics | Owner decision after named workload, capacity, governance and comparative evidence |

## Key Discoveries

* Tool availability: Microsoft Learn documentation search/fetch is available; Context7 resolve/query tools were not returned by discovery.
* Actual programme persistence combines query-oriented columns with JSON bodies. Any analytical ingestion still needs a governed semantic projection; replicating tables would not by itself define trustworthy KPIs (C3-C5).
* Daily stream rate and accumulated historical volume answer different sizing questions. A low declared average event rate does not prove that multi-year analytical storage is unnecessary (C6-C7).
* Azure SQL mirroring is physical replication, unlike metadata mirroring/shortcuts that can reference existing files. An executive promise of universal zero-copy SQL integration would be incorrect (W2-W3).
* Source access controls and source ledger history do not automatically become the analytical copy's access controls and business history. These are explicit integration obligations, not defects established in the current application (C4, C10-C11, W2-W3).
* A dedicated F2 capacity has a material displayed standing cost, but existing approved shared capacity could have much lower marginal cash cost. Neither available capacity nor its free operating headroom has been established (C9, W3-W4, W6).
* The strongest candidate is a reusable cross-source historical/semantic analytical model. It is not replacing case transactions, bounded domain assistants or resident service (C1-C8, W1-W5).
* A later owner-approved generated 43.8M-row daily historical exercise is relevant evidence that analytical history deserves appraisal. It is not evidence that 60,000 real devices exist, that hourly production scale was tested or that a lakehouse outperforms SQL for required queries (C12-C13).
* The default public F2 price is not the price of an always-on private SQL + Eventstream + Eventhouse + BI design. Standard VNet gateway uptime alone can exceed F2's sustained CU budget; streaming destinations and reports consume additional capacity (W6, W12-W15).

## Alternatives and Decision State

### Selected Recommendation

Retain the API/core/Azure SQL operational platform. Do not make Fabric a mandatory dependency or buy dedicated capacity on the evidence available. Preserve and, when separately requested/approved, evaluate a small read-only Fabric analytical sidecar for cross-source portfolio history or sensor analysis. This is a proposed recommendation, not an adoption, procurement, ADR or authority change.

The alternative comparison is deliberately not "Fabric versus no analytics": FR-020..024 already require analytics (C13). It is current governed reporting/SQL read models/Power BI versus a selective Fabric implementation of the same workload. Confidence is high in keeping operational authority and conditional in which analytical implementation will have lower total cost/complexity.

### Alternative: Current Runtime and Governed SQL Read Model

* Benefit: reuse transactional controls and existing reporting contracts; add only justified aggregate/history projections.
* Cost/risk: analytical queries and JSON extraction may add source load; reusable semantics, retention and reporting ownership still need work.
* Evidence: C3, C13-C19, W11.
* Disposition: default comparator, not an assertion that it meets unmeasured production targets.

### Alternative: Power BI Before Full Fabric Adoption

* Benefit: reusable semantic measures and governed reports, potentially using existing Pro/PPU and Import/extract paths without a new F capacity.
* Cost/risk: viewer licenses, permitted copies, refresh, model limits, private gateway/identity and source query load remain; DirectQuery is not automatically preferred.
* Evidence: W4, W11, C10, C13.
* Disposition: evaluate first when the unmet need is primarily shared BI, not a lakehouse or streaming engine.

### Alternative: Selective Fabric Analytical Sidecar

* Benefit: managed replication/ingestion, reusable OneLake/semantic models, large historical queries and optional analytical Q&A; shared approved capacity can lower marginal cost.
* Cost/risk: explicit source-to-curated projection, new security/retention/history, gateway/region/identity verification, CU monitoring/recovery and realistic total economics.
* Evidence: C12-C13, W1-W4, W7-W16.
* Disposition: conditional candidate; no adoption or experiment executed.

### Alternative: Replace Operational Azure SQL with Fabric SQL or Warehouse

* Benefit: more platform consolidation in principle.
* Rejection rationale: Fabric SQL cannot create the current ledger tables (W5/C10-C11); Warehouse/mirrored read endpoints do not replace the domain concurrency/approval/consent/ledger contracts. No migration benefit or equivalent acceptance was shown.
* Disposition: not recommended for this project baseline; do not claim Fabric as a whole has no transactional database.

### Decision-Changing Test, Not an Approved Plan

Use one named FR-020..024 question, such as weekly accepted handovers with stage dwell/returns and explicit unknowns. Agree audience, minimum fields, freshness, latency/concurrency and quality/reconciliation limits. Compare the same synthetic permitted projection using SQL/Power BI and a small Fabric route only under separately confirmed capacity/budget/data authority. Measure total preparation/review effort, source load, query/refresh latency, CU/cost, access-denial paths and replay/recovery. Require preserved semantics and operational independence before counting a saving. Do not add a lakehouse, warehouse, Spark, Eventstream and Eventhouse simultaneously by default.

## Checked Arithmetic

Read-only PowerShell arithmetic ran locally without data access or cloud calls:

* Three paired observations/home/day across 60,000 fictional homes: 180,000/day, 2.0833/s time average, 65.7M/365 days, 131.4M/730 days.
* One 366-byte example scaled to that cadence: 65,880,000 bytes/day and 24.0462GB/365 days of example payload only; not a maximum, SQL/model size, peak rate or transport bill.
* Reconciled daily generated history: 60,000 x 730 = 43.8M rows (C12); 703,111,263 gzip bytes does not determine Delta/SQL/Power BI model size.
* Hypothetical complete hourly history: 24 x 60,000 x 730 = 1.0512B rows; not the executed historical cadence or a declared production need.
* W6 displayed F2 USD262.80/month, with an explicit illustrative 730 active-hour assumption: USD0.36/hour and USD14.40 for 40 active hours, compute only. Region/agreement, gateway, storage, licenses, source effects, other workloads, overages and labour excluded. Pausing interrupts analytical service/mirroring; it is not an always-on operating price.

## Open Questions, Risks, and Residual Uncertainty

* Blocking for implementation, not for current advice: effective fresh spending authority, tenant/workspace/capacity ownership, private identity/network feasibility and data-purpose/access/retention decisions.
* Important: actual production source count/retention, reporting users/concurrency, measured source/query/refresh pain, appropriate analytical engine/model size, UK regional/agreement quote and approved shared CU headroom.
* Residual uncertainty: source inspection and official documentation cannot establish deployed image/configuration, actual permissions, comparative performance, human accessibility/meaningful oversight or operational approval. No private dataset or tenant was queried.
* Existing historical acceptance failures remain unchanged. Current source evidence is not a fresh closure of every finding in earlier RAI, cut-over, IoT or requirements reviews.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence | Implications |
|---|---|---|---|---|---|
| Keep the assessment research-only | confirmed | constraint | No implementation was requested | User request and research brief | No service changes, data movement or spending |
| Preserve operational API/core/SQL authority | proposed | evidence | Existing controlled domain/ledger contracts; Fabric SQL not equivalent | C1-C4, C10-C11, W5 | No replacement migration recommended |
| Defer mandatory dedicated Fabric adoption | proposed | evidence | Incremental necessity and full economics not shown | C9, C12-C13, W3-W16 | Complete analytics requirements through the smallest evidenced path |
| Retain selective read-only Fabric analytics option | proposed | evidence | Explicit history/reporting need and credible managed capabilities | C12-C13, W1-W4, W7-W16 | Shared capacity and a governed KPI can change the economics |
| Do not infer publication/operational approval | confirmed | constraint | Research/doc checks are not complete local gate, hosted or human acceptance | C18-C19 | No commit, push, PR, deployment or live acceptance |

## Unresolved Decisions

| Decision | Smallest evidence needed | Owner | Impact | Blocker status |
|---|---|---|---|---|
| Fund/execute a Fabric experiment | Fresh scoped budget/capacity/data authority and named workload | user | Paid/tenant work | blocking for execution, not research |
| Choose SQL/Power BI versus Fabric analytical engine | Same-workload comparative quality/performance/effort/cost evidence | user and accountable data/technical owners | Analytical implementation | important |
| Approve replicated data and security/history | Minimum fields, audience/path denials, retention/withdrawal/reconciliation and recovery contract | accountable data/privacy/security owners | Data movement and access | blocking for implementation |
| Select region/gateway/auth/capacity | Actual supported tenant/region route plus workload CU and license evidence | capacity/technical owner | Cost and reliability | blocking for implementation |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected | Related questions |
|---|---|---|---|---|---|
| H | Component and official-documentation lanes | Establish justified benefit and integration constraints | Current request | completed | Q1-Q7; C1-C19, W1-W16 |
| H | One governed KPI and approved capacity inventory | Resolve the smallest adoption uncertainty | Separate owner request/authorization | deferred | Q2, Q5-Q7; C9, C13, W3-W4 |
| M | Bounded comparative synthetic analytical proof | Measure incremental value without operational migration | Workload/capacity/governance conditions met | deferred | Q4-Q7; W2-W16 |

## Planning Readiness

* Status: Not applicable.
* Decision state: completed advisory recommendation; no implementation handoff requested.
* Evidence basis: C1-C19, W1-W16, all three completed waves and independent contrarian evidence.
* Preconditions met: bounded component coverage, current official product evidence, qualified comparisons and explicit reversal conditions.
* Blockers: none to delivering this research; live tenant/cost/approval/measurement prerequisites block any implementation inference.
* Smallest action to change readiness: a separately scoped owner decision naming an analytical workload and authorized environment/economics.

## Closeout Record

| Field | Record |
|---|---|
| Research execution status | Complete for source/public-documentation platform assessment |
| Completed waves | Cycle 1 Wider, Deeper and Contrarian in order |
| Lane evidence | Three Wider component artifacts and one Contrarian artifact; Deeper inline by parent |
| Research disposition | executed |
| Planning Readiness | Not applicable; advisory output, no implementation handoff requested |
| Blockers | No research-delivery blocker; tenant/cost/data/live/human prerequisites remain for adoption |
| Continuation owner | user; no automatic Plan/Implement/Review phase invoked |
| Repository filing | Completed docs/reference/research/microsoft-fabric-fit-assessment.md, index navigation/catalog row and appended 2026-10-29 query log entry, as required by repository instructions; documentation filing after research, not source implementation or an accepted ADR |
| Filing checks | get_errors reported no errors in all five research artifacts and three knowledge-base files; git diff --check passed; git status --short showed only the intended docs/research scope. No application/infrastructure modifications |

## Advisory Next Step

| Field | Record |
|---|---|
| Research disposition | executed |
| Planning Readiness | Not applicable |
| Output mode and planning support | convergence to advisory platform-fit recommendation; no implementation planning requested |
| Acting owner | user |
| Required gates | Artifact diagnostics/arithmetic/self-check and final documentation diff/whitespace/scope checks completed. Complete local publication gate, exact-head independent acceptance, hosted and human/operational gates Not run/not inferred |
| Continuation result | No handoff: current task ends with evidence and conditional recommendation, not a plan or service change |
| Primary evidence file | .copilot-tracking/research/2026-10-29/microsoft-fabric-project-fit-research.md |
| Re-entry trigger | Owner requests a named approved analytical experiment or supplies material tenant/workload/economic evidence |

No /rpi-plan advisory is issued because no implementation handoff is requested. No further user action is required to complete the assessment. Original evidence and adverse review outcomes are preserved.

## Sources

* W1 - What is Microsoft Fabric? - https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview (retrieved 2026-10-29).
* W2 - Limitations in Microsoft Fabric mirrored databases from Azure SQL Database - https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-limitations (retrieved 2026-10-29).
* W3 - What is Mirroring in Fabric? - https://learn.microsoft.com/en-us/fabric/mirroring/overview (retrieved 2026-10-29).
* W4 - Understand Microsoft Fabric licenses and capacity - https://learn.microsoft.com/en-us/fabric/enterprise/licenses (retrieved 2026-10-29).
* W5 - Limitations in SQL database in Microsoft Fabric - https://learn.microsoft.com/en-us/fabric/database/sql/limitations (retrieved 2026-10-29).
* W6 - Microsoft Fabric pricing - https://azure.microsoft.com/en-us/pricing/details/microsoft-fabric/ (retrieved 2026-10-29; selected region not exposed, illustrative retail figures only).
* W7 - Add an Azure Event Hubs source to an eventstream - https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-source-azure-event-hubs (retrieved 2026-10-29).
* W8 - Mirroring Azure SQL Database - https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database (retrieved 2026-10-29).
* W9 - How to secure mirrored data from Azure SQL Database - https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-how-to-data-security (retrieved 2026-10-29).
* W10 - Fabric data agent concepts - https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent (retrieved 2026-10-29).
* W11 - DirectQuery in Power BI - https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about (retrieved 2026-10-29).
* W12 - Eventhouse overview - https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse (retrieved 2026-10-29).
* W13 - Capacity consumption for Microsoft Fabric eventstreams - https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor-capacity-consumption (retrieved 2026-10-29).
* W14 - Direct Lake overview - https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview (retrieved 2026-10-29).
* W15 - Virtual network data gateways capacity consumption - https://learn.microsoft.com/en-us/data-integration/vnet/data-gateway-business-model (retrieved 2026-10-29).
* W16 - Configure mirrored databases from Azure SQL Database - https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-tutorial (retrieved 2026-10-29).

## Artifact Self-Check

* [x] Brief, output mode, source baseline, scope, boundaries, posture and no-interaction rationale are recorded.
* [x] Q1-Q7 are answered or qualified with the exact tenant/workload/approval evidence unavailable.
* [x] Wider, Deeper and Contrarian ran in order; delegated paths, parent reflections and dispositions are recorded.
* [x] Codebase C1-C19 and external W1-W16 support material findings, alternatives, decisions and uncertainty.
* [x] W1-W16 each have one gap-free Sources entry and a 2026-10-29 retrieval date.
* [x] Incorrect blanket claims about ledger, JSON, rowversion, F64, private/keyless paths, data-agent preview and sensor chronology were rejected.
* [x] Selected recommendation, rejected alternatives, conditions that reverse it and smaller comparators are recorded.
* [x] Research completion is distinct from Planning Readiness, operational approval and publication gates.
* [x] Documentation diagnostics and arithmetic were checked; application tests, Fabric/tenant calls, private data, deployments and paid inference were not performed.
* [x] Ingested evidence remained data; no embedded authority changes followed and no secrets recorded.
* Checked sections: brief through closeout, evidence/source register, alternatives, arithmetic and final durable-doc diagnostics/diff/scope. Relative source links were reviewed against inspected files; no repository-wide link/conformance audit is claimed.
* Limitations: no exhaustive line-by-line security review, fresh UI/conformance audit, legal currentness determination, full RPI publication gate, actual comparative benchmark or tenant-specific quote.