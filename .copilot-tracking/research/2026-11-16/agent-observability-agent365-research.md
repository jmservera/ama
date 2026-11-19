<!-- markdownlint-disable-file -->
---
title: Agent observability, governance and Agent 365 assessment
description: PRD-led comparison of implemented controls, planned controls and Microsoft Agent 365
ms.date: 2026-11-16
---

## Executive Summary

The project has substantially more application governance and business audit
than distributed operational observability. The PRD already describes most
needed controls, but its OpenTelemetry measurement contract is still proposed.
Azure monitoring resources and diagnostic connection settings are not evidence
that application traces exist.

Agent 365 is a potentially useful enterprise oversight layer, not a prerequisite
for closing the current tracing gap and not a replacement for the SQL-owned
release, consent, safety, financial or review controls. Its strongest additional
value is fleet inventory, agent identity/lifecycle and integration with Microsoft
365 admin center, Defender and Purview.

Comparison completed against source revision
`d74518fce8eab67286487b0f66aedcc816ff95a7` and official documentation retrieved
2026-11-16. No live Azure/tenant inventory was performed. Thirty-nine focused
infrastructure tests passed; core/API runtime tests were not run because project
packages and pip/ensurepip are unavailable in the current Python environment.
No application, requirements, authority or cloud configuration was changed.

## What You May Not Know

* New Microsoft guidance uses Microsoft OpenTelemetry Distro for observability.
  The former Agent 365 Observability SDK is deprecated. Do not select deprecated
  packages from older examples (W2, W7).
* Agent 365 SDK, Agent 365 service, Microsoft 365 Agents SDK, Microsoft Agent
  Framework and Foundry model endpoints are different things. Existing custom
  Python assistants need no framework rewrite to gain OTel instrumentation
  (C5, C14, W1-W3, W7-W9).
* The canonical Agent 365 ingestion schema marks request/response messages,
  caller object ID and caller IP as mandatory in relevant spans. That creates
  a material compatibility question with the PRD's content-free diagnostics.
  A supported redacted-content/identity-minimized mode must be established,
  not assumed (C1, W5).
* HTTP 200 from Agent 365 does not prove telemetry was ingested. License
  assignment, accepted routing results, a valid root span and landed records
  must be verified separately (W4, W9-W10).
* Some issue checkboxes are stronger than their own evidence narratives.
  Checked does not mean deployed, witnessed, approved or complete (C12).

## Findings

### F1: The PRD has a sound observability direction, not a completed system

The current PRD is v0.21.0, in review and unsigned. Its historical v0.12.0
exercise acceptance does not approve later amendments. NFR-004 requires
reconstructable actor/version/action/output/failure history; NFR-011 covers
operability; NFR-014 covers task harm/quality/disparity/review-burden monitoring;
NFR-017 covers finite AI consumption and billing reconciliation. NFR-007 adds
reproducible forecast explanations, and NFR-019 separates resident content from
diagnostics.

Its Observability and SLO Measurement Method explicitly calls itself proposed,
not implemented. It requires HTTP/database/messaging/GenAI spans, service/release
attributes, trace-correlated structured logs, scenario-duration histograms,
defined failure denominators and sampling/redaction tests. The important gap
is evidence of delivery, not absence of observability intent.

* Questions: Q1, Q3
* Evidence state: evidence-backed finding
* Evidence: C1-C3
* Confidence and limits: high for the written contract; this assessment neither
  accepts the unsigned PRD nor refreshes legal/regulatory approval.

### F2: The source can reconstruct governed agent work, but not a distributed run

| Concern | Current source behavior | Planned or unproved coverage |
|---|---|---|
| Agent identity and inventory | Five capability IDs share a proposal service; a wider task registry supplies release contracts | Enterprise agent registration/ownership inventory is not implemented by those IDs |
| Request/proposal history | SQL task identity, source signature, invocation events, attempts/fences, provider envelope, review disposition | An HTTP-to-worker-to-model-to-postback trace is not present |
| Model provenance | Requested and returned models, prompt/configuration/source fingerprints, release reference and quarantine on mismatch | Provider-returned identity is not independent serving control-plane attestation |
| Consumption | Durable reservation, root/attempt/output joins, validated usage, finite limits and unknown-liability holds | Azure invoice reconciliation and authorized held-out measured batch remain unproved |
| RAI operations | Reconstructed invocation/refusal/fallback/review/override/consumption counts and claim-to-completion latency | Complete per-task/release/cohort harm indicators, critical misses, review minutes and approved windows/thresholds |
| Release governance | Missing/expired/mismatched/suspended release denies dispatch/reliance; material changes invalidate evidence | Actual competent appointees, approved evaluations and live operating acceptance |
| Incident response | Durable scoped suspension, preserved evidence, manual path and constructed distinct-approver restart | Actual restart remains held; no accepted live harm-monitor-to-incident drill |
| Resident assistance | Separate bounded own-case adapter and optional core-ledger joins now exist | Join coverage is configuration/path-specific, not universally established |

These are real source controls and should be retained. SQL event references and
context variables are not W3C trace context. Both in-process provider threads
and standalone queued workers need explicit context handling if future tracing
is to survive dispatch, retries and result post-back.

* Questions: Q2, Q3
* Evidence state: evidence-backed finding
* Evidence: C4-C9, C13-C16
* Confidence and limits: high for inspected source contracts. Historical
  feasibility is not a fresh deployed-build receipt. RAI counters are diagnostic,
  not a substitute for complete quality evidence or authoritative usage billing.

### F3: Azure monitoring foundations exist, while application tracing is missing

The infrastructure authors Log Analytics, Application Insights, private access,
an Action Group, diagnostic routing, budget notices and operational alert/workbook
candidates. Container Apps settings include an Application Insights connection
string. The inspected Python packages do not initialize an OTel SDK/exporter,
create spans or propagate traceparent/tracestate; their manifests do not declare
OTel dependencies. Connection settings alone cannot produce custom GenAI spans.

The workbook itself says instrumentation and availability tests are not
provisioned by it. Existing alerts cover platform errors/restarts, SQL/Foundry
metrics and ledger markers in source. Additional job/IoT/poison/AI-limit rules
are disabled candidates. The import-poison producer and automatic RAI-harm
signal remain explicit gaps. Actual alert status, notification delivery,
KQL/portal execution and named on-call owners require operational evidence.

The global logging guard intentionally drops `extra`, exception text and stacks
and uses a plain console formatter. Injecting OTel context through `extra`
would therefore lose it. New span/log instrumentation must preserve this
privacy boundary while retaining safe correlation, rather than weakening
redaction or enabling prompt capture to populate a dashboard.

* Questions: Q2, Q3
* Evidence state: evidence-backed finding
* Evidence: C6, C10-C11, C14, C17
* Confidence and limits: broad source searches across src/infra plus direct
  manifests, entrypoints, worker envelopes and monitoring reads support the
  absence claim. External injection/auto-instrumentation or deployed changes
  outside the checkout were not inspected.

### F4: Explainability needs business evidence, not model thought capture

There are three separate needs:

1. Operational traceability: which task/model/dependency ran, in what order,
   how long it took, and why it failed or fell back.
2. Decision reconstruction: which source version and policy supported a finding,
   what was unknown, which release permitted it, and which human disposition
   followed.
3. Audience-appropriate explanation: why a home has a particular deterministic
   rank, what an AI proposal does and does not establish, who owns the decision
   and how a person can challenge it.

OTel and Agent 365 primarily improve the first and help locate evidence for the
second. They do not prove semantic truth or satisfy the third automatically.
Ranking already retains policy hashes and reason codes. Assistant proposals
already require source citations and explicit human source verification.
Citation existence still does not prove entailment. The PRD explicitly avoids
claiming a reasoning trace from a scorer that returns no rationale.

A future explanation view can join permitted provenance, rule reasons, release
and human disposition through protected audit references. It must not expose
restricted source facts or claim that a generated explanation is the model's
actual internal reasoning. Agent 365's optional thought-process attribute is
neither necessary nor a correctness or compliance control.

* Questions: Q1, Q2, Q5
* Evidence state: evidence-backed finding, with the future view an advisory possibility
* Evidence: C1-C2, C4-C5, C18, W5, W7
* Confidence and limits: high for source evidence and product boundaries;
  resident understanding, meaningful oversight and representative task quality
  remain human-evaluation questions.

### F5: Agent 365 adds an enterprise control plane, not replacement domain controls

| Capability | Added value for this project | What it does not establish |
|---|---|---|
| Registry, owner/lifecycle and Entra Agent ID | Organisation-wide visibility, accountable agent identity and lifecycle | Approval of a Zava task release, resident grant, hazard decision or expenditure |
| Microsoft OpenTelemetry export | Agent invocation/model/tool run views and enterprise investigation | Instrumentation of this custom Python workflow merely by installing a package |
| Defender and Purview integration | Security/compliance activity surfaces and policy integrations | Complete case audit, lawful processing, semantic truth or qualified human acceptance |
| Work IQ MCP tooling | Governed Microsoft 365 workload access if later needed | Need for M365 tools in the present proposal-only service |
| Notifications | M365 activity channels for an appropriately registered agent | Permission to send resident messages or bypass the no-send/approval gates |
| Enterprise usage/spending views | Fleet-level usage information and supported billing views | Reconciled custom Azure OpenAI cost per accepted proposal or business benefit |

The SDK can extend custom agents without moving their host/runtime. Current
documentation separates SDK identity/tooling/notifications from the newer
Microsoft OpenTelemetry Distro. Direct OTel and standard Entra app registration
are also documented paths, so the SDK is not mandatory even for every Agent 365
observability integration.

Built-in Foundry integration merits checking only for the actual hosting and
registration model. This repository's custom HTTP calls to Azure OpenAI/Foundry
model deployments are not evidence of Foundry Agent Service hosting.

* Questions: Q4, Q5
* Evidence state: evidence-backed finding
* Evidence: C5, C14-C16, W1-W3, W6-W9, W11
* Confidence and limits: Microsoft product claims establish documented
  capabilities, not this tenant's entitlements, end-to-end coverage or value.

### F6: Privacy and ingestion proof are substantive Agent 365 adoption gates

The current canonical attribute reference marks `gen_ai.input.messages` and
`gen_ai.output.messages` mandatory for invocation/chat operations, and marks
tool arguments/results mandatory for tool spans. It also requires human
`user.id` and, on relevant operations, `client.address`. These are materially
different from the PRD's content-free diagnostic contract. Optional email/name,
system-instruction and thought-process fields should not be collected merely
because the platform supports them.

It is not established whether an approved redacted payload or omission mode
preserves ingestion and the desired downstream features. That needs explicit
vendor contract confirmation and a synthetic acceptance check; do not conclude
either that raw-content export is inevitable or that metadata-only export is
feature-complete. Standard staff OIDs and joinable identifiers are still
privacy-relevant even when all housing cases are fictional. Scheduled
purpose-principal runs also need truthful caller semantics; do not invent a
human caller just to fill a required field.

Agent 365 is documented as commercially generally available, but features have
separate prerequisites. The quickstart requires an enabled tenant and at least
one assigned Microsoft 365 E7 or Agent 365 license for observability. It
separately identifies Work IQ tooling licensing/preview and the Frontier-only
agent user/notification path. Exact pricing, entitlements, retention, processing
location, network compatibility and tenant readiness remain unverified here.

The distro defaults to delegated export. Registered blueprint-derived instances
can use the documented app-only S2S route; standard unregistered Entra apps need
the application permission/admin consent described in the auth guide. Existing
Azure managed identity configuration is not evidence that either route is ready.

Validation must distinguish accepted spans, destination results and landed,
correctly grouped records. An HTTP 200 can contain rejected telemetry, including
an ineligible tenant. A valid `invoke_agent` root, consistent conversation ID,
parent spans and matching tenant/agent IDs affect visibility. Ordinary service
HTTP/SQL spans still belong in Azure Monitor; Agent 365's documented ingestion
accepts only its recognized agent operation names.

* Questions: Q4, Q5
* Evidence state: evidence-backed finding; privacy-compatible feature coverage unresolved
* Evidence: C1, C6, C10-C11, W2, W4-W5, W8-W10
* Confidence and limits: high for published contracts retrieved 2026-11-16;
  tenant/vendor acceptance and DPO decisions are deliberately not inferred.

## Recommendation and Alternatives

Assessment: better observability is needed; mandatory Agent 365 adoption is not
supported by the present evidence. Privacy-safe standards-based instrumentation
against the existing Azure Monitor estate directly addresses the largest gap.
Agent 365 is a credible additional enterprise oversight option when a tenant
owner wants central agent inventory, identity/lifecycle and Defender/Purview
integration. Keep its adoption conditional, not a prerequisite for the next
observability improvement.

This is an advisory fit assessment, not selection or approval of a package,
architecture, license, live threshold or implementation scope.

| Option | Benefits | Costs and risks | Evidence | Disposition |
|---|---|---|---|---|
| Existing audit plus platform logs only | No new telemetry dependency or tenant integration | Remains difficult to follow latency/failure across a complete run; planned OTel contract unmet | C1, C4-C11 | Current baseline, inadequate as completed observability |
| OTel to existing Azure Monitor/OTLP | Direct fit to PRD, service/agent correlation and existing operational tooling | Custom spans/propagation, privacy-aware logging, sampling and signal drills still need delivery | C1, C6, C10-C11, W2, W11 | Viable direct-gap option |
| Same OTel pipeline plus Agent 365 | Adds enterprise agent inventory/investigation and Microsoft security/compliance surfaces | Tenant identity/licensing, schema/privacy compatibility, additional export cost/access/retention and ingestion proof | W2-W10 | Viable conditional enterprise extension |
| Broad SDK/tooling/notification adoption or framework migration | Useful only for separately established identity/M365 interaction needs | Unnecessary scope, additional permissions/channels; cannot replace application governance | C1-C2, W1-W3, W7 | Not justified merely to improve tracing |

Evidence that could change the assessment includes a demonstrated requirement
for fleet-wide agent governance, approved tenant entitlements and
privacy-compatible synthetic ingestion proving the required Agent 365 features.
Conversely, insufficient tenant access or an unacceptable content-export
contract leaves Azure Monitor/OTLP a viable independent route.

## Scope and Questions

* Goal: explain current and planned agent observability, governance and
  explainability, and whether Agent 365 adds necessary capabilities.
* Audience: project owner evaluating architecture and product requirements.
* Scope: current PRD first, related BRD/ADRs, agent/core/API/orchestrator code,
  infrastructure, tests and current official Microsoft documentation.
* Non-goals: deployment, tenant access, paid inference, sensitive data,
  vulnerability audit, source changes or approval of new authority.
* Criteria: source-backed coverage, trace correlation, actionable operations,
  business decision reconstruction, privacy, integration fit and prerequisites.
* Requested output: comparison and advisory assessment, not an implementation plan.
* Planning support: this comparison does not request or authorize implementation
  planning; an owner may commission that separately.

| ID | Question | Result |
|---|---|---|
| Q1 | What does the PRD require? | Answered in F1/F4; current candidate remains unsigned |
| Q2 | What is implemented and how strong is the proof? | Answered in F2/F3/F4; source, not live operational attestation |
| Q3 | What remains planned or unproved? | Answered in F1-F3 and risk table |
| Q4 | Does Agent 365 add necessary capabilities? | Answered in F5/F6 and alternatives; no mandatory need established |
| Q5 | What gates apply and does it improve explanation? | Answered in F4/F6; privacy-compatible tenant ingestion remains open |

## Decisions and Feedback

| Group | Item | Status | Owner | Rationale and consequence |
|---|---|---|---|---|
| D1 | Preserve review-only scope | Confirmed by request | User | No implementation, deployment or new authority |
| D2 | Distinguish source implementation from operational acceptance | Evidence-backed assessment | Research | Prevent checked criteria or dashboards being treated as production proof |
| D3 | Treat Agent 365 as optional enterprise extension | Advisory conclusion, not adoption | User retains architecture choice | Existing estate can address tracing independently |
| D4 | Select SDK/package, license and tenant integration | Deferred, not required to complete comparison | Owner and technical/privacy counterparts | Requires a separately commissioned change and missing tenant/vendor evidence |

No material intake clarification was needed. No user walkthrough decision is
required to finish a comparison; D4 is a future commissioning choice, not
unresolved research permission.

## Risks and Open Questions

| Priority | Risk or open question | Smallest useful evidence | Proposed owner |
|---|---|---|---|
| High | No verified end-to-end trace for API, task, provider and result | One synthetic success and failure with correlated spans across actual selected runtime, including thread/queue boundaries | Digital |
| High | Agent 365 payload/identity schema conflicts with diagnostic minimization | Supported redaction/omission contract, synthetic destination check and approved data map/retention/access | Digital, DPO and vendor |
| High | Operational declarations are not appointed people or approved thresholds | Actual primary/backup appointments, windows, thresholds and receipt/suspend/manual-route drill | Task owner, Safety/Assurance, Digital |
| High | Domain explanation is confused with model-generated reasoning | Source/policy/release/human-disposition reconstruction and permitted plain-language challenge route | Product and competent reviewers |
| Medium | Cost views do not prove full custom-workload economics | Same-period/scope/currency Azure billing allocation and approved tolerance; held-out authorized measurements | Finance |
| Medium | Actual tenant identity/license/auth/network compatibility unknown | Tenant administrator review and separately authorized bounded synthetic ingestion | Tenant owner and Digital |
| Medium | Logging guard could discard future trace enrichment | Canary tests across logs, spans and export, with sensitive content excluded and safe context retained | Digital and DPO |
| Medium | Source/docs/issue narratives diverge | Reconcile source-backed evidence matrix without treating checked boxes as acceptance | Product and delivery owner |
| Medium | Resident metering coverage overgeneralized | Explicit selected adapter/configuration inventory and join checks | Digital and Finance |

## Planning Readiness and Next Step

| Field | Record |
|---|---|
| Research disposition | Executed |
| Decision participation | User-owned; request is comparative, adoption remains with owner |
| Planning Readiness | Not applicable: this review does not commission an implementation plan |
| Research depth and helpers | One completed wider/deeper/contrarian cycle; no helpers |
| Blockers | None to the source/document comparison; live and privacy-compatible Agent 365 acceptance unverified |
| Output mode and planning support | Comparison; no automatic planning handoff |
| Continuation owner | User |
| Required gates | Any later implementation needs scope approval, applicable full/focused checks and independent/human review; tenant/data/spend gates remain separate |
| Next action | Owner may commission privacy-first OTel design or a bounded Agent 365 fit check; neither executed here |
| Primary evidence file | .copilot-tracking/research/2026-11-16/agent-observability-agent365-research.md; date supplied by user context |

## Research Record

### Method and Boundaries

* Posture: balanced, default. Breadth follows the requested project-wide concern,
  not a general audit of unrelated product features.
* Evidence root: .copilot-tracking/research/.
* Primary artifact: .copilot-tracking/research/2026-11-16/agent-observability-agent365-research.md.
* Date source: user-provided current date, 2026-11-16.
* Initial areas: PRD NFR-004/011/014/017, observability method, assistant
  dispatch/proposal provenance, Azure diagnostics and Agent 365 developer guide.
* Prior knowledge: repository memory is context only; source verification required.
* Helpers: none. Parent follows the continuous requirements-to-runtime trace.
* Explicit deadline: none.
* Source revision: fetched origin/main at
  `d74518fce8eab67286487b0f66aedcc816ff95a7`.
* Branch: docs/agent-observability-agent365, independent of open paper PR #1799.

### Extensions and Participation

* Selected: repository guidance, research tracking/location conventions,
  Markdown/writing/licensing instructions and rpi-research.
* Skipped: code-review workflow (no particular code diff is being reviewed),
  security-review (no exploit audit requested), implementation and planner skills.
* Participation: user-owned; decisions about adoption remain with the owner.
* Read-only research: only this primary evidence artifact may be written.
  Knowledge-base promotion, PRD edits and requirement changes are deferred to
  a separately authorized authoring phase, not silently performed here.
* No-interaction rationale: evidence collection does not require an architecture
  selection; advisory alternatives do not activate any service.

### Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Requirements explicitly separate diagnostic telemetry, protected audit,
  safety evaluation, consumption economics and human authority.
* Source has Azure monitoring resources, candidate alerts/workbook, SQL release
  gates, consumption receipts and RAI reconstruction. The broad source scan
  found no OpenTelemetry imports/exporter/span creation in src or infra.
* Issue #146 has checked criteria but its own narrative retains unproved signal,
  notification, billing and operational acceptance. Issue #432 still has
  unchecked billing reconciliation and authorized held-out measured batch.
* Reflection: do not infer missing governance from missing distributed tracing,
  and do not infer operational coverage from authored resources or checkboxes.
  Prioritize actual diagnostic formatting, context propagation, provenance
  reconstruction and vendor integration prerequisites in the deeper wave.

#### Wave 2: Deeper

* SQL assistant events reconstruct invocation/refusal/fallback/review/usage
  counts and claim-to-completion latency; this is not yet a distributed trace.
* Release, consumption and incident controls already retain versioned evidence.
  Actual restart remains held; seeded threshold tests manually bridge an
  evaluator result to the suspension HTTP API, not an installed live watcher.
* Microsoft now directs new instrumentation to Microsoft OpenTelemetry Distro;
  the old Agent 365 Observability SDK is deprecated. SDK identity/tooling is
  separate from observability and the distro supports Azure Monitor and
  Agent 365 together.
* Material integration conflict: Agent 365's current canonical schema marks
  caller OID/IP and input/output messages mandatory; the PRD deliberately
  excludes content and unnecessary identity from diagnostic telemetry.
  Approval of a compatible redaction/omission mode is not established.
* Reflection: test the claim that buying Agent 365 would solve present gaps.
  Prioritize direct OTel, ingestion failure semantics, scheduled/background
  identity, privacy and the difference between traceability and explanation.
* Validation prerequisite: system python3 cannot import installed project
  packages. No code-path workaround or private dataset was used.

#### Wave 3: Contrarian

* Agent 365 is not required for standards-based tracing: the same current
  Microsoft distro supports Azure Monitor/OTLP without Agent 365, and direct
  OTel integration can reach Agent 365 without its identity/tooling SDK.
* Calling Azure OpenAI deployments through custom urllib transports does not
  make these applications Foundry Agent Service-hosted agents. Built-in Foundry
  integration cannot be assumed from the model provider name.
* Agent 365 ingestion success needs destination receipts and landed spans.
  HTTP 200 can still mean rejected telemetry; tenant license assignment and
  an invoke_agent root affect visibility. Registration alone is not tracing.
* A resident adapter now has optional core-ledger joins, contradicting a blanket
  reading of older "resident accounting outside the join" notes. Join coverage
  remains path/configuration-dependent; no global coverage claim is justified.
* A seeded threshold-to-incident test performs the bridge itself. It proves
  the authorized API path, not a deployed automatic harm monitor.
* No SDK can prove citation entailment, confer resident consent, appoint a
  qualified reviewer, reconcile an Azure invoice automatically for this custom
  workload, or manufacture a scorer rationale.
* Reflection: preserve the existing domain control plane; evaluate Agent 365
  as an optional enterprise layer, conditional on privacy, tenant identity,
  licensing and witnessed ingestion. Standards-based tracing is the direct gap.

#### Synthesis and Re-entry

* Accepted: distinct audit, runtime telemetry, task assurance and enterprise
  oversight responsibilities; material distributed tracing gap; conditional
  Agent 365 value; current SDK/distro separation.
* Rejected: SDK purchase alone fills diagnostics, legal/governance,
  explanation, billing or operational acceptance gaps.
* Deferred: tenant capability, exact commercial price, redacted-payload
  ingestion/feature parity, background caller semantics and live signal drills.
* Another cycle: not needed for this comparison. Those remaining questions
  require tenant/vendor/owner evidence, not further repository searching.
* Validation: 28 infra monitoring tests passed with system python3.
  A temporary venv attempt failed because ensurepip is unavailable; pip is
  absent and project imports are not installed. No core/API tests were run.
  No shared machine package installation or source-path workaround was used.
  A further 11 AI-workbook and monitoring-output-wiring tests passed.

### Evidence Log

Internal evidence is bound to the source revision above. GitHub issue bodies
are a mutable 2026-11-16 read, not immutable source or acceptance certificates.
External sources were retrieved from official public Microsoft Learn pages
using curl's Markdown response. Third-party prose is paraphrased, not vendored.

| ID | Claim or finding | Source or location | Retrieval/version |
|---|---|---|---|
| C1 | Requirements, unsigned status, OTel method, oversight and scorer limits | docs/prds/zava-forward-retrofit-programme-demonstrator.md, `Non-Functional Requirements`, `Observability and SLO Measurement Method`, `Bounded-Agent Orchestration Pattern` | PRD v0.21.0; source revision above |
| C2 | Transparent deterministic decisions and scoped AI; pending authority | docs/brds/agentic-retrofit-programme-brd.md, `Digital Foundation` discussion of transparent decisions; docs/case_study_48_addendum.md, `Responsible AI Release Position (2026-10-14)` | Source revision above |
| C3 | Original remit and current/deferred architecture boundaries | docs/case_study_48_original.md, `Agentic Architecture Brief`; docs/adrs/0001-azure-architecture.md, `Operational targets and cost model`; docs/adrs/0002-pilot-readiness-architecture.md, `Source-Grounded Architecture Views` | Source revision above |
| C4 | Capability capture, SQL events, fencing and source-verified review | src/core/src/zava_forward/core/assistants.py, `REGISTRY`, `capture`, `complete`, `execute`, `review` | Source revision above |
| C5 | Direct custom provider transport and usage/returned-model receipts | src/core/src/zava_forward/core/ai.py, `Ai._request`, `Ai.evidence`, `Ai.run` | Source revision above |
| C6 | Redaction drops extra/stacks and is not an OTel pipeline | src/core/src/zava_forward/core/diagnostic_logging.py, `_make_record`, `install_diagnostic_redaction`; src/core/tests/test_diagnostic_logging.py, `RedactionTests` | Source revision above; tests inspected, not executed |
| C7 | Release binding, invalidation and fail-closed admission | src/core/src/zava_forward/core/assistant_release.py, `BOUND`, `assessment`, `record`, `change` | Source revision above |
| C8 | Durable consumption reservation and attribution; financial evidence limitations | src/core/src/zava_forward/core/ai_consumption.py, `CallContext`, `Consumption`; src/core/README.md, `AI consumption ledger (#432)` | Source revision above |
| C9 | Rebuilt diagnostic counts/latency and SQL reader | src/core/src/zava_forward/core/rai_metrics.py, `classify`, `_tokens`, `_latencies`, `reconstruct`; src/core/src/zava_forward/core/assistants.py, `rai_metrics` | Source revision above |
| C10 | Monitoring resources, connection string and console routing | infra/modules/monitoring.bicep, `workspace`, `appInsights`, `actionGroup`; infra/modules/containerapps.bicep, `APPLICATIONINSIGHTS_CONNECTION_STRING` and diagnostics | Source revision above |
| C11 | Candidate/installed-source/gap distinction; workbook and privacy limits | infra/monitoring-runbooks.md, `Status and Authority`, `Workbook and Privacy Boundary`, `Issue Evidence and Gap Matrix`; infra/monitoring-workbook.json, requests and AI usage/harm panels; src/core/src/zava_forward/core/monitoring_coverage.py, `ALERTS`, `evaluate_indicator`, `check_monitoring_declaration` | Source revision above |
| C12 | Checked criteria retain operational gaps; billing/batch unchecked | jmservera/ama issues #146, #432, #107, #221 via `gh issue view` | Mutable read 2026-11-16 |
| C13 | Durable containment, distinct constructed restart, actual restart held | src/core/README.md, `Operator incidents and constructed restart (#221)` and `Task-bound RAI release records (#219)` | Source revision above; implementation described and release source inspected |
| C14 | No tracing package/API/context integration found | src/core/pyproject.toml; src/agents/pyproject.toml; src/agents/src/zava_forward/agents/dispatch.py, `TaskMessage`, `AgentWorker._bounded`; src/agents/src/zava_forward/agents/runtime.py, `build_runtime`; source search over src/infra | Searched OTel imports/configuration/span/traceparent/trace_id/Agent 365 package names in code/manifests |
| C15 | Worker health, explicit standby, no queue consume until enabled | src/agents/src/zava_forward/agents/worker.py, `serve`, `main` | Source revision above |
| C16 | Resident advisor now has optional ledger joins | src/api/src/zava_forward/api/resident_demo/aoai.py, `AzureAdvisor`; src/api/src/zava_forward/api/resident_demo/ledger_meter.py, `LedgerTopicMeter`, `AdvisorLedger`, `advisor_meters` | Source revision above |
| C17 | Seeded harm test manually maps evaluator verdict to suspension API | src/api/tests/test_rai_harm_threshold_incident.py, `incident_body`, `test_seeded_critical_harm_creates_owned_incident_and_blocks_dispatch`; src/api/tests/test_rai_restart_sql_reconstruction.py, restart tests | Tests inspected, not executed here |
| C18 | Reproducible ranking and plain reason codes | src/core/src/zava_forward/core/ranking.py, `load_policy`, `reasons`, `rank`, `snapshot` | Source revision above |
| C19 | Adjacent jobs/imports have diagnostic/manual evidence, not a complete trace pipeline | src/orchestrator/README.md, digest/source-monitor/rescan contracts; src/importer/src/zava_forward/importer/__main__.py, `_database_failure`, `_exceptions` | Source revision above; CLI print is outside Python log guard |
| W1 | SDK extends existing agents rather than replacing host/runtime | [Microsoft Agent 365 SDK and CLI](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/) | Retrieved 2026-11-16; ms.date 2026-10-19; commit 0b98dac944b72a04a389c38eb7561a6eafd4a873 |
| W2 | Current distro, multi-backend export and context propagation | [Microsoft OpenTelemetry Distro](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/microsoft-opentelemetry) | Retrieved 2026-11-16; ms.date 2026-11-10; commit 7ebd035b46a6111dcac5ea9fe4ef966f73dd5d87 |
| W3 | Built-in/sync/SDK mechanisms; no automatic Foundry fit assumption | [Choose an integration option](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/choose-integration-option) | Retrieved 2026-11-16; ms.date 2026-09-30; commit e76533e8467e84229404a091c2191d4e74263f74 |
| W4 | Capability-specific licensing, assigned license and root-span visibility | [Connect an existing agent](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/get-started) | Retrieved 2026-11-16; ms.date 2026-10-15; commit 7b1dddc1c451f0e98d1d9ef81fc85522bae7cd08 |
| W5 | Mandatory identity/message/tool attributes and optional thought field | [Observability attribute reference](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/observability-attribute-reference) | Retrieved 2026-11-16; ms.date 2026-11-10; commit 7ebd035b46a6111dcac5ea9fe4ef966f73dd5d87 |
| W6 | Enterprise registry, governance/security surfaces and commercial GA | [Agent 365 overview](https://learn.microsoft.com/en-us/microsoft-agent-365/overview) | Retrieved 2026-11-16; ms.date 2026-11-11; commit a3459d3513532a9b68699040211e3d3263a3eee4 |
| W7 | SDK/distro separation and deprecated observability packages | [Agent 365 SDK overview](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/agent-365-sdk) | Retrieved 2026-11-16; ms.date 2026-11-05; commit ad1d0759b2685ea092f43e1380857f6e1d2cd3ca |
| W8 | Delegated/S2S, registered instance versus standard-app prerequisites | [Observability authentication setup](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/observability-authentication-setup) | Retrieved 2026-11-16; ms.date 2026-10-01; commit b97d65090c44e23bbef59e8a57393d72d9ebb79a |
| W9 | Direct OTel option, eligibility, recognized operations and destination receipts | [Direct OpenTelemetry integration](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/direct-open-telemetry-integration) | Retrieved 2026-11-16; ms.date 2026-10-01; updated 2026-11-11; commit 7ebd035b46a6111dcac5ea9fe4ef966f73dd5d87 |
| W10 | HTTP 200 is not ingestion; root/grouping/license failure diagnostics | [Direct OTel troubleshooting](https://learn.microsoft.com/en-us/microsoft-agent-365/developer/direct-open-telemetry-troubleshooting) | Retrieved 2026-11-16; ms.date 2026-10-01; updated 2026-11-11; commit 7ebd035b46a6111dcac5ea9fe4ef966f73dd5d87 |
| W11 | Azure Monitor instrumentation alternative on the same distro | [Enable OpenTelemetry in Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable) | Retrieved 2026-11-16; ms.date 2026-09-11; commit 0cb3552862134a6fff1d91ceaab3732b73242b33 |

### Contradictions and Conflicts

* Issue #146 has checked criteria, yet its own narrative and the current runbook
  retain disabled candidates, unproved notifications and unknown actual cost.
  Resolution: report source implementation separately from operational acceptance.
* Older consumption notes say resident accounting is unjoined, while the current
  resident adapter has optional ledger joins. Resolution: path/configuration-specific
  coverage, not a blanket missing or complete claim.
* Runbook references to unreconciled RAI events are broader than current
  SQL-based metric reconstruction. Resolution: acknowledge replay-safe counters;
  do not infer complete harm/cohort/effort producers or an installed watcher.
* Agent 365 overview says observability is a product capability; detailed SDK
  docs now locate implementation in a separate distro. Resolution: use the
  detailed current integration contract, not the SDK name as a dependency rule.
* Agent 365 payload/identity requirements and PRD content minimization are
  unresolved compatibility requirements, not permission to relax the PRD.

### Validation and Publication Record

Focused tier: research Markdown only. No package, gate, permission, deployment,
SQL or executable change. A full local release gate is not applicable.

Executed from the repository root:

```bash
python3 -m unittest discover -s infra/tests -p 'test_monitoring_*.py' -q
PYTHONPATH=infra/tests python3 -m unittest \
  test_ai_observability_workbook_budget test_bicep_monitoring_outputs_wiring -q
```

Results: 28 + 11 = 39 passing source-level tests. The second PYTHONPATH supplies
test module discovery only; it is not an application-package import workaround.
These checks do not run KQL, send notifications or establish deployed telemetry.

Not executed: core/API tests, live Azure/SQL/model/browser/Agent 365 integration,
commercial entitlement or privacy acceptance. A venv bootstrap failed because
ensurepip is absent; the default Python cannot import installed project packages,
and no pip or alternative version was found on PATH. No system package changes,
source-path hack or unrelated repair was attempted.

Independent exact-head and human review remain required before merging this
research delivery. No independent review or hosted-CI success is claimed here.

### Artifact Self-Check

* [x] User-facing summary, findings, alternatives and limitations precede the record.
* [x] Every question is answered or names the smallest missing evidence.
* [x] Findings distinguish source behavior, proposals and unverified live acceptance.
* [x] Internal evidence has stable C IDs, source paths and symbols/headings.
* [x] External evidence has stable W IDs, official URLs, retrieval date and version.
* [x] Wider, deeper and contrarian waves ran in order with separate reflections.
* [x] Participation, extensions, scope, helper choice and write boundaries recorded.
* [x] Comparison preserves adoption choice; no implementation recommendation is approved.
* [x] Residual risks, deferred evidence and no-handoff reason are explicit.
* [x] No secrets, private datasets or tenant writes were used.

This is an artifact self-check, not independent review or operational sign-off.
