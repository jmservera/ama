---
title: Project Review and Microsoft Fabric Fit Assessment
description: Component-level assessment of Zava Forward and whether Microsoft Fabric adds justified analytical value or unnecessary platform complexity
ms.date: 2026-10-30
ms.topic: reference
---

## Material Findings

Assessment date: 2026-10-29. Source baseline:
`9b74ac8daaec2a880172e43161b37ac7f2c3f801`.
Scoped evidence corrections dated 2026-10-30 reconcile the 27 October funding
renewal and SQL idle-compute comparison; they are not a fresh whole-platform
assessment or live inventory.
High and Medium below describe platform-decision risks, not newly discovered
exploits or an operational acceptance verdict.

### High: Fabric SQL Is Not an Equivalent Operational Replacement

The current Azure SQL definition enables ledger, and the application explicitly
creates an append-only ledger for audit. Fabric includes a transactional SQL
database, but its current limitations prohibit creating ledger and ledger-history
tables. Moving the system of record there would require changing a deliberate
control, not changing a connection string. A Fabric warehouse or read-only
mirrored endpoint also does not replace the programme's transaction, concurrency,
consent and approval contracts.

Evidence: [SQL configuration](../../../infra/modules/sql.bicep#L38),
[audit creation](../../../src/core/src/zava_forward/core/mssqlstore.py#L277),
[domain store](../../../src/core/src/zava_forward/core/store.py#L44), W5.

### High: Mirroring Would Create a Separate Security and History Obligation

Current role/case/field projections are application controls. Mirroring does not
call those projections; even source SQL row-level security, column permissions,
masking and sensitivity labels are not propagated to OneLake. A whole-table copy
of case bodies, staff data or chat could therefore create an unintended disclosure
path unless separately constrained. Direct Lake on OneLake does not apply SQL
analytics-endpoint row security either.

Mirroring also excludes ledger history tables. Its Delta retention defaults to
one day for newer portal-created mirrors. A current-state replica is not an
automatic historical event model, retained audit archive or independent ledger
verification mechanism. These are integration risks, not evidence that the
current application already exposes data through Fabric.

Evidence: [SQL case bodies](../../../src/core/src/zava_forward/core/mssqlstore.py#L30),
[case-context projection](../../../src/core/src/zava_forward/core/chat_isolation.py#L78),
[history requirement](../../prds/zava-forward-retrofit-programme-demonstrator.md#L1397),
W2, W3, W14.

### Medium: There Is an Analytics Requirement, but Not a Proven Fabric Requirement

PRD FR-020 through FR-024 explicitly require portfolio heatmaps, lifecycle
funnels, historical progression, explainable scenario forecasts and stakeholder
reporting. The current source implements synthetic progress views, exports and
deterministic forecasts. It would be incorrect to dismiss analytics as unnecessary.

What is missing is a demonstrated reason those requirements need a new platform:
an agreed cross-source query, history window, freshness, concurrency or operating
cost that the existing runtime or a smaller reporting solution cannot meet.
Absence of Fabric code is not proof of absence of need.

Evidence: [reporting requirements](../../prds/zava-forward-retrofit-programme-demonstrator.md#L1395),
[current progress reader](../../../src/api/src/zava_forward/api/progress.py#L217),
[forecast implementation](../../../src/core/src/zava_forward/core/progress.py#L539).

### Medium: Historical Volume Is Credible, but Daily Event Rate Is Not a Sizing Test

The later IoT integration record reports a reconciled generated run of 43.8
million daily readings over 730 days. That is a credible analytical-history
candidate. The separate three-observations/day scenario averages only 2.08
records/second across 60,000 fictional homes, but averages do not describe
synchronised bursts, long historical scans or concurrent dashboard queries.
Neither figure proves that SQL is inadequate or that F2 is sufficient.

Evidence: [accounting assumptions](./iot-sensor-analytics-research-plan.md#L239),
[approved integration and generated run](./iot-sensor-analytics-research-plan.md#L414),
W12-W14.

### Medium: Entry-Level Capacity Is Not the Complete Private-Solution Cost

The public pricing view displayed F2 at USD 262.80/month, but did not expose a
selected region. That is not a UK South or agreement-specific quote. Standard
VNet gateway uptime consumes four CU-hours per member-hour; an F2 supplies two
CU-hours/hour. One continuously running member on that meter would exceed F2's
sustained capacity before reports, pipelines or Eventhouse. Other private routes
have different costs and must not automatically be assigned that meter.

The [27 October resident prototype decision](../../architecture/resident-assistant-prototype.md#current-owner-decision-and-implementation-2026-10-27)
records renewed overall USD700 funding through 2026-12-31, with resident USD30
and USD20 inference limits within it. The earlier exercise approval expired on
2026-10-25T16:02Z; that is not the latest overall funding record. All-in actual
spending, forecast and remaining headroom remain unestablished. Neither the
renewal, the resident allocation nor a Bicep budget parameter establishes spare
funds or Fabric-specific purchase permission. Overall funding renewal does not
extend narrower tariff/inference or showcase/session/SQL admission windows.

Evidence: [budget decision](../../case_study_48_addendum.md#L414),
[all-in headroom qualification](../../case_study_48_addendum.md#L592), W4, W6, W15.

### Medium: A New Analytics Service Would Not Close Existing Assurance Gaps

The current agent guide still records an unsupported-claim-with-valid-citation
counterexample as a critical enablement failure. Prior whole-project assurance
also distinguishes engineered controls from qualified human, privacy, accessibility
and operational acceptance. Replicating data or adding analytical AI does not
establish meaningful review, approved retention, resident consent, calibrated
sensor signals, recovery effectiveness or observed housing outcomes.

This is not a statement that every finding in an older review is unchanged:
later employee-chat, briefing and IoT work exists and must be considered at its
own evidence boundary.

Evidence: [current evaluation limit](../../../src/agents/README.md#L66),
[current employee-chat work](../../../src/api/README.md#L207),
[dated RAI assessment boundary](./rai/project-rai-review.md#L8).

## Recommendation

Keep the API, core domain logic and Azure SQL as the operational platform.
Do not make Microsoft Fabric a mandatory dependency or replace operational SQL
on the evidence available.

Fabric has a credible conditional role as a read-only analytical layer for
cross-source portfolio reporting, retained sensor history and reusable business
measures. Evaluate it against a governed SQL/read-model plus Power BI alternative
when a named workload and its economics are established. Existing approved shared
Fabric capacity could make that evaluation worthwhile sooner.

For the current demonstrator, buying a dedicated, always-on Fabric estate and
adding lakehouse, warehouse, Spark, Eventstream and Eventhouse together would
be overengineering. A small analytical implementation for an explicit requirement
is not inherently overengineering. The recommendation is to defer mandatory
platform adoption, not to defer the reporting requirements or reject Fabric
categorically.

This is proposed platform-fit advice. It changes no accepted ADR, requirements,
budget, data authority, operational control or release decision.

## Scope and Method

The review covers all five source distributions, staff and resident interfaces,
business/reporting requirements, data generation and import, IoT, infrastructure,
identity, operations, delivery tooling and assurance/documentation boundaries.
Three independent component investigations were reconciled with direct source
reads. A fourth independent investigation challenged the emerging recommendation.
Current official documentation was researched in Wider, Deeper and Contrarian
waves, including the overview supplied with the request.

Source implementation, existing test definitions, retained observations, proposed
requirements and missing acceptance are distinguished. This was not an exhaustive
line-by-line security audit, fresh UI/conformance review or live Azure/Fabric
inventory. It did not rerun application tests, access private datasets, contact
models, deploy resources or spend money. Context7 was unavailable in the session;
Microsoft Learn search/full-page retrieval and official pricing were used.

The project has prior bounded actual Azure/SQL/model observations. This source
review neither erases them nor freshly verifies the deployed build or complete
authored topology. The 60,000-home stock, retained 980-case lineage and analytical
test cohorts must remain distinct. Generated data is not company evidence.

## Component Review

| Component | Current responsibility and evidence | Fabric fit and disposition |
| --- | --- | --- |
| Business case and requirements | Retrofit flow, accepted handovers, evidence, resident choice and accountable decisions; quantified benefits remain qualified. [Exercise baseline](../../case_study_48_addendum.md#L258) and [portfolio requirements](../../prds/zava-forward-retrofit-programme-demonstrator.md#L1395) | Useful only when a reporting/analysis capability improves an accountable decision. A service count is not business value. No measured Fabric savings or housing outcomes are established. |
| Shared core and persistence | Workflow/quality/finance/grant/resident controls, deterministic ranking, SQL lists and JSON domain records. [Store](../../../src/core/src/zava_forward/core/store.py#L44), [SQL read paths](../../../src/core/src/zava_forward/core/sqlstore.py#L1), [ranking](../../../src/core/src/zava_forward/core/ranking.py#L126) | Retain operational authority. A curated analytical read model is plausible; replicated JSON is not a semantic model. Measure any analytical load on the source. |
| Agents and evaluation | Five bounded domain assistants, task/field allowlists, citations, release and manual-fallback contracts; evaluation lives separately from core runtime logic. [Allowlists](../../../src/core/src/zava_forward/core/assistants.py#L88), [evaluation limit](../../../src/agents/README.md#L66) | Fabric data agents could add analytical Q&A later. They do not replace document/form assistance, deterministic ranking, review or evaluation. No model capability establishes professional or financial authority. |
| API and employee site | Authenticated controlled operations, task queues, native workflow, historical synthetic views, employee chat and briefing. [Reporting](../../../src/api/src/zava_forward/api/progress.py#L217), [chat skills](../../../src/api/README.md#L207), [briefing](../../../src/api/README.md#L9) | Power BI may supplement aggregate views, not replace controlled forms, evidence review, permission checks or accessible manual paths. Do not make case access depend on Fabric availability. |
| Resident service and chat/memory | Own-case guidance, record-use/representative boundaries, separate resident and works decisions, bounded fallback. [Resident design](../../architecture/resident-assistant-prototype.md#L7), [chat isolation](../../../src/core/src/zava_forward/core/chat_isolation.py#L58) | No clear current platform benefit. Do not copy resident narratives, staff chat, opt-in memory or representative grants into general analytics by default. Fabric analytical Q&A is not a replacement resident service. |
| Orchestrator | Token maintenance, ledger digest publish/verification, bounded source monitoring and document-rescan tooling; general autonomous programme supervision is not established. [Job boundary](../../../src/orchestrator/README.md#L9) | Fabric pipelines could orchestrate future data movement. They do not own staff tokens, ledger verification, source approval or operational handoffs. Do not migrate these jobs merely for consolidation. |
| Importer | Bounded XLSX preview, declared mapping, quarantine, lineage and CSV/XLSX export; not a production source-integration platform. [Importer scope](../../../src/importer/README.md#L10), [input bounds](../../../src/importer/src/zava_forward/importer/xlsx.py#L14) | Data Factory becomes useful for recurring heterogeneous integration. It does not replace human resolution of field conflicts, identity authority or accepted imports. |
| Synthetic operating data and climate tools | Multi-CSV discovery pack, seed/hash/version provenance and local climate generation/analysis. Synthetic source-system names do not prove actual company connectors. [Source dictionary](./retrofit-synthetic-data/data-dictionary.md#L113), [climate/backfill record](./iot-sensor-analytics-research-plan.md#L414) | A good non-production analytical exercise input, not a basis for claims about actual source access, data quality, rights, predictive validity or production scale. Do not train a business forecast on constructed outcomes and call it validated. |
| IoT and retained readings | Finite opt-in replay/receiver, exact bindings, SQL admission/replay/DQ, synthetic observation provenance and later canonical-key integration. [Adapter](../../../src/api/src/zava_forward/api/iot_stream.py#L145), [consumer](../../../src/core/src/zava_forward/core/sensor_consumer.py#L196) | Eventstream/Eventhouse are credible for proven time-series questions, long retention or live analytical latency. Current finite replay does not establish a sustained stream need. Raw transport is not accepted/safe/consented analytical truth. |
| Progress, forecast and stakeholder reporting | Coverage-aware synthetic dashboards, exports, historical reconstruction and capacity-based scenarios. [Forecast logic](../../../src/core/src/zava_forward/core/progress.py#L539), [FR-020..024](../../prds/zava-forward-retrofit-programme-demonstrator.md#L1395) | Strongest near-term candidate: reusable definitions, history and cross-source measures. Compare a small semantic model/SQL projection before a whole analytics estate; keep forecast, target, approved plan and actual outcome separate. |
| Infrastructure, identity and operations | SQL, storage, Foundry, Container Apps, monitoring and private/keyless controls are authored, with profile and acceptance qualifications. [SQL controls](../../../infra/modules/sql.bicep#L20), [architecture evidence boundary](../../architecture/README.md#L21) | New tenant/workspace, source-server identity, network, data access, CU monitoring, recovery and retention work remains. Fabric can manage analytics infrastructure but cannot inherit all application controls. |
| CI, developer tools and documentation | Five package boundaries; SQL/browser/container/security and publication gates; research, ADRs, cut-over evidence and qualified business/assurance claims. [Source validation guide](../../../src/README.md#L45), [gate implementation](../../../tools/rpi-checks.py#L30), [prior assurance](./rai/project-rai-review.md#L8) | Fabric items, models, notebooks and connections would need versioning, reproducible deployment, synthetic regression and denial/reconciliation checks. Do not bypass these through untracked portal configuration or imply capstone/product acceptance from adding a service. |

## What Fabric Would Add

Microsoft Fabric is the SaaS data/analytics platform in the supplied overview.
It combines workloads over OneLake; it is not synonymous with a data warehouse,
Power BI alone or a new general-purpose application runtime (W1).

| Capability | Potential project benefit | Necessary qualification |
| --- | --- | --- |
| Data Factory | Repeatable stock/EPC, programme, contractor and finance extracts with shared preparation and lineage | Real source rights, connectors, keys, watermarks and accountable conflict handling are not established by the synthetic discovery pack. |
| OneLake, lakehouse or warehouse | Retained analytical facts and reusable cross-source historical queries; shared preparation for several consumers | Define facts, dimensions, event time, correction and unknowns first. Choose the simplest suitable store rather than create all three. Shortcuts reference supported existing files; SQL database mirroring physically replicates data. |
| Azure SQL mirroring | Managed near-real-time copy of selected eligible tables, reducing bespoke replication plumbing | Source eligibility, load, privacy, history, security and private identity/network configuration remain. It is not zero-copy access to the existing SQL database (W2, W3, W8, W16). |
| Power BI and Direct Lake | Shared KPI definitions, filterable board/assurance views and analytical reads separated from OLTP | Ordinary BI can also use Import or DirectQuery without a lakehouse. Direct Lake requires curated Delta data, capacity sizing and the correct access model (W4, W11, W14). |
| Eventstream and Eventhouse | Time-window joins, retained sensor investigation and event/time-series exploration | Demonstrate a question, history window and latency need. Not all history needs streaming; not every stream needs both Eventhouse and a separate warehouse (W7, W12, W13). |
| Spark and Data Science | Larger batch transformations or later independently evaluated analytical models | Current ranking/scenario logic is deterministic. Synthetic history is not proof of calibrated indoor physics, hazard detection or a useful learned forecast. |
| Fabric data agent | Read-only staff/executive questions over governed tables or a semantic model | Core feature is currently GA, paid F2+ or qualifying P capacity, with feature-specific AI/region settings. It is English-only in the fetched limitations, cannot directly read PDFs/documents or standalone CSV/JSON files, cannot write/action and is not the resident or document-assistance runtime (W10). |
| Fabric SQL database | A transactional database consolidated into Fabric | Ledger is unsupported, so this is not recommended as the current SQL authority's replacement. Do not confuse this limitation with the eligibility of current ledger tables for mirroring (W2, W5). |

Fabric IQ and some adjacent schema, AI, security and networking capabilities
are explicitly preview in current pages. Approval of a core workload does not
approve those surrounding features or cross-geography AI processing (W1, W10).

## Workload Scale

The arithmetic below was checked locally. It is not a benchmark, telemetry
measurement, billable-message count, physical sensor inventory or production
sizing result.

| Evidence class | Scale | Interpretation |
| --- | --- | --- |
| Case-study/fixture scope | 60,000 homes; separate retained 980 programme cases | Homes are not residents, accounts, concurrent users, active cases or monitoring devices. |
| Recorded generated run | 60,000 x 730 daily observations = 43,800,000 rows; 703,111,263 compressed reading bytes | A reconciled synthetic daily history. Gzip bytes are not SQL, Delta or Power BI model size. No new generation or private-data read was performed for this assessment. |
| Declared three/day scenario | 180,000 records/day; 65.7M/365 days; 131.4M/730 days | About 2.0833/s time average. Two scalar measures per paired observation do not double the record count; synchronised slots can burst. |
| Example-payload scaling | 366 bytes x 180,000 = 65.88MB/day; about 24.05GB/365 days | Decimal example JSON payload only. Excludes variable lengths, retries, rejection, transport/security, SQL/index, retention and model overhead; not an upper bound. |
| Hypothetical complete hourly history | 24 x 60,000 x 730 = 1.0512B rows | Shows cadence sensitivity only. Not the executed run or an approved production monitoring requirement. |

The 43.8M-row daily history is below Direct Lake's documented F2 300M-row/table
guardrail, but F2 also has a 10GB model-on-disk guardrail and 3GB model memory,
plus shared CU constraints. No encoded model size, query plan, concurrency or
gateway workload was measured. "Below a row limit" does not mean "fits F2"
or establish interactive performance (W14).

The earlier sensor-ID incompatibility is historical: the later 2026-10-27
continuation adopts canonical home keys and compact collision-checked sensor
keys. Exact case availability, retained length domains, actual transport,
permissions, calibration and operational acceptance still need their own
evidence. Do not present the original identity blocker as unchanged.

## Integration Guardrails

Retain programme writes, deterministic ranking, consent, safety referrals,
professional sign-off, contracts, payments and grant disposition in existing
controlled workflows. Analytics can expose a question or review signal, not
approve a decision or silently alter the operational record.

Use a purpose-limited analytical projection rather than mirror the entire
application database by default. Candidate facts include permitted case/event
keys, stage/return/handoff times, accepted handover, controlled grant states,
capacity assumptions and approved aggregate sensor-quality indicators. Preserve
source/version/as-of, definitions, missingness, exclusions and independent
stock-versus-case denominators. Do not treat award, claim and cash as one measure.

Exclude resident/staff free text, adjustment narratives, conversation content,
memory, representative permissions and raw document bodies unless separately
necessary and approved. Aggregate or pseudonymise identifiers where appropriate;
pseudonymisation is not a claim that data is anonymous. Even synthetic data can
have private geography, provenance or access restrictions.

Check each selected source table and path. In particular:

* The source's case JSON is `NVARCHAR(MAX)`, not native SQL `json`, and its
  field named `rowversion` is `BIGINT`, not SQL's native `rowversion` type.
  Those type-specific mirroring exclusions are not automatic blockers.
* Current mirroring limitations exclude ledger history tables, not every
  current ledger table. Verify actual selected table eligibility; do not
  remove ledger to make an analytical integration easier.
* Values above the documented 1MB LOB limit can truncate in OneLake. Validate
  source sizes/completeness instead of silently turning partial bodies into
  evidence. Native SQL `json`/`vector` tables have separate restrictions (W2).
* Retain business event facts/snapshots explicitly. Mirroring current state
  and short Delta retention does not supply FR-022 history or legal retention.
* Recreate and test permissions at every allowed Fabric/OneLake/semantic-model
  access path. A SQL endpoint filter alone is not protection for Direct Lake
  on OneLake or direct file access (W2, W14).
* Private SQL mirroring has documented gateway options; the tutorial supports
  Entra and workspace identity. The runtime app's managed identity is not the
  logical SQL server's required primary identity. Verify the selected auth kind,
  gateway, tenant, region and permissions together; do not enable SQL passwords
  or public source access as an assumed prerequisite (W8, W9, W16).
* Eventstream has documented private/workspace-identity options. Preserve
  consent/calibration/identity/admission/DQ semantics and source provenance;
  a raw Event Hubs event is not an accepted observation (W7).
* Keep manual case access and urgent human routes independent of capacity
  pausing, a stale analytical copy, an AI outage or failed pipeline.

No live source is mirrored, no approved projection is created and no data
activation follows from these proposed guardrails.

## Costs and Operational Burden

### Capacity, Licensing and Storage

The retrieved public view displayed F2 USD262.80/month, F4 USD525.60/month and
F64 USD8,409.60/month. Its selected region was not exposed. Use these only as
illustrative retail figures, not a UK South, customer-agreement, tax-inclusive
or project-specific quote (W6).

With an explicit illustrative 730 active-hour month, F2's displayed price
corresponds to USD0.36/hour; 40 active hours would be USD14.40 compute only.
A small bounded batch experiment can therefore have different economics from
an always-on analytical service. Storage, licenses, source/gateway work,
other capacity consumption, overages and labour are excluded. Pausing capacity
interrupts mirroring/analytical availability and does not erase retained storage
charges. Do not quote the experiment arithmetic as an operating budget.

Mirroring background replication compute is free and the included replica
storage allowance is one TB per purchased CU, while queries and normal OneLake
operations consume capacity. Active capacity is still required. Mirroring is
not a free analytical platform, and the allowance does not cover every derived
lakehouse, warehouse, cache or semantic model (W3, W6).

F64 is not the minimum Fabric capacity. For ordinary Power BI sharing below
F64, viewers need Pro/PPU/trial; F64+ can serve Free viewers with the appropriate
role. Authors still need suitable licenses. External/app-owned embedding has
distinct rules and must not be used to assume resident authorization. PPU alone
does not supply capacity for non-Power BI Fabric workloads (W4).

### Private and Streaming Paths

A standard VNet gateway consumes four CU-hours/member-hour of uptime. This
is capacity consumption, not a separately established cash charge. It must be
included alongside the workload, and not attributed to every private path.
Self-hosted/on-premises gateways trade that choice for hosting, patching,
availability and operator work; they are not free operations (W15).

At the fetched low-throughput starting rates, Eventstream's active flat meter
plus processor totals about one CU-hour per active hour before traffic and
destinations. It can stop charging those operations after sufficient inactivity,
but continuous events and Eventhouse/BI use change the budget. Retention beyond
24 hours has storage costs. Eventhouse and analytical queries consume capacity
too; their inactivity/scheduling options are not a free always-on safety service
(W12, W13).

Mirroring's source snapshot and replication can add SQL CPU, IO and transaction-log
work. The [authored source baseline](../../../infra/modules/sql.bicep#L51)
is General Purpose serverless with 60-minute auto-pause and 0.5 minimum vCores.
A continuously enabled mirror that prevents idle pause loses those compute
savings even when the application is idle, independently of snapshot/IO load.
Active serverless compute is billed at least at its configured minimum compute
limits; paused compute is zero while storage remains billed (W17).
Conservatively include that no-auto-pause source cost in the comparison until
the selected mirroring path's actual idle behavior is verified.

Evidence qualification (2026-10-30): re-fetched W2/W8 do not state that enabling
mirroring automatically changes the auto-pause setting. Do not present that
mechanism as verified, or equate Fabric mirroring with W18's geo-replication
blocker. Before an authorized trial, record actual settings and idle behavior.
After the trial, verify source mirroring/change-feed cleanup, restoration of the
approved 60-minute auto-pause/0.5-vCore baseline and actual idle pause, disconnecting
diagnostic sessions that would keep SQL awake (W18). Restored settings alone
do not establish resumed savings; no live restoration is claimed here.

Monitor source write/query behavior, log growth, pipeline lag/reseeding,
model freshness, CU contention and failure recovery. A shared capacity can
reduce marginal cash expenditure but still has opportunity cost, throttling
risk and an owner-approved allocation (W3, W8).

### Cost Decision

Compare incremental capacity, licenses, data/storage/network/source effects,
gateway/operations and implementation/review effort against the smallest
equivalent reporting path. Count analyst or staff time savings only after a
like-for-like quality and effort comparison. No cost per accepted housing outcome,
cash saving, headcount saving or positive return is established here.

Current shared capacity, tenant eligibility, regional prices and all-in headroom
are unknown. Any trial activation, paid capacity, identity change or data export
needs its own current scope and approval under the renewed overall envelope.
The recorded renewal is not unspent headroom or Fabric approval, and this
report grants neither.

## Alternatives

| Option | Benefits | Trade-offs | Present disposition |
| --- | --- | --- | --- |
| Existing runtime plus a governed SQL aggregate/history read model | Least new platform surface; reuse domain definitions and transactional source | Source load and analytical history still need design and measurement | Baseline comparator; no unmeasured sufficiency claim |
| Power BI Import over approved views/extracts | Shared measures and staff/board reports without requiring a new lakehouse or F capacity | Licensing, refresh, model limits, permissions and private access remain; Import creates a permitted copy | Prefer appraisal when shared BI is the primary gap |
| Power BI DirectQuery | Keeps most data at source and can query current permitted facts | Per-visual SQL/network load, cache timing, SSO/security and private connectivity; not automatic source-role equivalence | Use only for a demonstrated freshness/governance need; Import is Microsoft's default starting point (W11) |
| Selective Fabric analytics | Managed ingestion/replication, reusable OneLake/semantic layer and optional retained event analysis | New governance/history/security, capacity/connection operating work and evidence | Conditional candidate, especially with approved shared capacity |
| Replace programme SQL with Fabric SQL/warehouse | Consolidation in principle | Ledger mismatch and unproved domain/control/recovery equivalence; migration cost | Not recommended for this baseline |

An approved file-based historical extract in existing storage can also be a
lower-coupling intermediate option. Its export, deletion/hold, privacy, lineage
and refresh rules still need authority; this is not permission to copy private
data into a new store or local analysis tool.

## Adoption Triggers and a Falsifiable Comparison

Reconsider a selective Fabric implementation when all of the following hold:

1. A named decision-user selects a recurring FR-020..024 question, source set,
   history window, freshness, latency/concurrency and quality/reconciliation
   criteria. Identify what the current dashboard/export or smaller SQL/BI path
   cannot provide economically.
2. The capacity owner confirms an active approved capacity/workspace, actual
   spare CU over a representative period, viewer licensing and a named operator,
   or the owner approves a complete dedicated-capacity cost boundary.
3. Accountable data/privacy/security owners approve the minimum fields, audience,
   permissions across all read paths, retention/withdrawal/correction/history and
   recovery behavior, with the selected private identity/network route verified.
4. A bounded synthetic comparison shows Fabric improves preparation/review effort,
   query/refresh behavior or total cost enough to justify its additional operating
   surface, without weakening semantics, accessibility or operational independence.
5. Implementation and publication gates are satisfied separately. An analytical
   experiment is not a live-service, model, privacy or professional approval.

A useful comparison is weekly accepted handovers, stage dwell and returns for
one defined cohort, preserving unknown timestamps and the source denominator.
Use the same permitted synthetic projection for SQL/Power BI and a small Fabric
path. Measure reconciliation, manual review effort, refresh/query latency,
source load, CU/cost, cross-role denial, stopped-capacity behavior and replay/
recovery. Select the least complex configuration that answers that question.
Add Eventstream/Eventhouse only if a separate time-series question needs them.

These are proposed decision criteria, not new approved requirements, a funded
experiment or an implementation plan. Existing approved shared capacity plus a
clear recurring historical decision is the strongest fact pattern that would
make an early Fabric experiment worthwhile. Failure to beat the smaller path is
a valid reason to retain that path rather than expand the Fabric design.

## Priority Before Platform Expansion

* Complete the versioned analytics contract: event definitions, accepted outcomes,
  grant states, missingness, denominators, reconciliation and accountable owners.
* Preserve human/role/consent boundaries and resolve data-copy retention/access
  questions before widening analytical access.
* Obtain actual-model and reviewer-effectiveness evidence for bounded assistants;
  valid citation identifiers alone do not prove that a claim is supported.
* Complete relevant live identity/transport, monitored recovery, assistive-technology
  and human acceptance evidence without presenting earlier local checks as approval.
* Confirm complete cost scope, remaining headroom and task-specific spending
  authority before another paid service, without treating overall renewal as
  approval to spend the resident allocation on Fabric.

Fabric could help deliver an accepted analytical capability. It does not remove
these responsibilities or make the business-case assumptions observed results.

## Validation and Limits

Completed for this assessment: component/source and test-definition inspection,
current official-source retrieval, independent contrarian research, local
arithmetic verification, document diagnostics and the final documentation
diff/whitespace self-check.

Not performed: application test reruns; actual Azure/Fabric/tenant checks;
private-data reads; comparative SQL/Fabric benchmarks; selected-region or
agreement pricing; direct human or assistive-technology research; legal/privacy
approval; deployment; paid inference; complete local RPI publication gate,
hosted checks, independent exact-head acceptance, commit, push or PR creation.
No fresh security, accessibility, legal, pilot or production conformance is claimed.

This is a research deliverable, not a publication-ready RPI implementation
candidate or an architecture decision. No user action is required to complete
the assessment; an experiment or adoption decision would be a separately scoped
owner request.

## Official Sources

W1-W16 were originally retrieved on 2026-10-29; W2/W8 were re-fetched for the
scoped 2026-10-30 cost qualification. W17/W18 were retrieved on 2026-10-30.
Product limits, rates, regional
availability and licensing can change; reverify the selected path before an
approved experiment or purchase. Summaries are paraphrases, not product guarantees.

| ID | Source | Used for |
| --- | --- | --- |
| W1 | [What is Microsoft Fabric?](https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview) | Supplied starting page, SaaS/OneLake and workload scope |
| W2 | [Azure SQL mirroring limitations](https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-limitations) | History, type, LOB, permissions and table constraints |
| W3 | [Mirroring overview](https://learn.microsoft.com/en-us/fabric/mirroring/overview) | Physical versus metadata mirroring, cost allowance, active capacity and Delta retention |
| W4 | [Licenses and capacity](https://learn.microsoft.com/en-us/fabric/enterprise/licenses) | F2/F64, per-user/PPU and embedding distinctions |
| W5 | [Fabric SQL database limitations](https://learn.microsoft.com/en-us/fabric/database/sql/limitations) | Transactional offering, absent ledger and replacement differences |
| W6 | [Microsoft Fabric pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-fabric/) | Displayed retail illustrations, separate storage and purchasing caveats; retrieved region unspecified |
| W7 | [Eventstream Azure Event Hubs source](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-source-azure-event-hubs) | Extended workspace identity and private-network options |
| W8 | [Azure SQL mirroring](https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database) | Source tiers, private gateways and source snapshot/log effects |
| W9 | [Mirrored Azure SQL data security](https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-how-to-data-security) | Server identity, private access and recreated granular security |
| W10 | [Fabric data agent concepts](https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent) | GA read-only analytical Q&A, prerequisites, source/language/permission limits |
| W11 | [Power BI DirectQuery](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about) | Import-first guidance, source load, security, latency and alternatives |
| W12 | [Eventhouse overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse) | Event/time-series analytics and inactive/scheduled compute behavior |
| W13 | [Eventstream capacity consumption](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor-capacity-consumption) | Active meters, destination/retention costs and pause effects |
| W14 | [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview) | Delta/semantic-model fit, F2 guardrails and OneLake versus SQL security |
| W15 | [VNet gateway capacity consumption](https://learn.microsoft.com/en-us/data-integration/vnet/data-gateway-business-model) | Standard four-CU/member uptime meter, route-specific qualification |
| W16 | [Azure SQL mirroring tutorial](https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-database-tutorial) | Entra/workspace identity, source-server primary identity, selected tables and setup permissions |
| W17 | [SQL serverless compute overview](https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-overview?view=azuresql) | Active minimum compute versus zero paused compute; retained storage charges |
| W18 | [SQL serverless auto-pause and auto-resume](https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-auto-pause-resume?view=azuresql) | Idle sessions/CPU conditions, actual-pause verification and distinct documented geo-replication blocker |

The Fabric SQL limitations page contains inconsistent TDE wording between prose
and its feature table. No encryption conclusion relies on that inconsistency;
the ledger restriction is consistent. Some data-agent tutorials retain preview
labels while the current concepts page states GA. The tutorial documents more
authentication choices than the security page's password example. Specific
current feature documentation controls these qualifications, not older search
snippets or generic pricing-page language about Free report viewers.