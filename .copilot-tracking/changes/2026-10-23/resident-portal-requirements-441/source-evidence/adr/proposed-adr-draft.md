---
id: null
title: Optional Resident Service Architecture Boundary
status: proposed
proposed_date: 2026-10-23
deciders:
  - Programme owner (exercise architecture decision only)
consulted:
  - Digital service owner
  - Programme Manager
  - Resident Engagement
  - Data and Performance
  - Housing Building Safety
  - Privacy and security reviewers
  - Accessibility representatives
informed:
  - Delivery and operations teams
  - Staff and resident-representation stakeholders
tags: [resident-portal, identity, case-entitlement, documents, omnichannel, bounded-ai]
supersedes: null
superseded-by: null
related:
  - path: docs/adrs/0001-azure-architecture.md
    relation: influenced-by
  - path: docs/adrs/0002-pilot-readiness-architecture.md
    relation: influenced-by
  - path: docs/adrs/0003-journey-derived-capabilities-runtime-fit.md
    relation: influenced-by
  - path: docs/adrs/0004-per-user-agent-chat-and-memory.md
    relation: informational
    note: Staff-only chat and memory remain unchanged.
  - path: docs/adrs/0005-regulatory-compliance-assistant.md
    relation: informational
    note: Regulatory assistant no-send boundary remains unchanged.
  - path: docs/adrs/0006-src-layout-and-cutover.md
    relation: influenced-by
affected_components: [resident portal, identity and recovery, case grants, document lifecycle, event reconciliation, resident-answer task, human queues]
asr_triggers:
  - kind: security
    evidence: PRD FR-069/FR-070, NFR-019; BRD OD-54
    note: Resident identity, grants, revocation, documents and model access create a trust boundary.
  - kind: compliance
    evidence: PRD NFR-019, AC-135/136; BRD OD-54; ADR 0004 OD-45 to OD-49
    note: Privacy, retention and real-data authority remain unresolved; no legal conclusion is made.
  - kind: cost
    evidence: PRD NFR-021/OD-55 and BRD illustrative capacity model
    note: Identity, support, storage, scanning, model and operations affect whole-service cost; no quote or budget exists.
  - kind: performance
    evidence: PRD AC-139 and NFR-021; OD-55
    note: Proposed exercise response measures require validation and are not operational SLOs.
  - kind: availability
    evidence: PRD FR-066/068 and NFR-020; BRD OD-52/55
    note: Outage, retries, lost acknowledgements and manual fallback affect continuity; targets remain open.
  - kind: scalability
    evidence: PRD NFR-021/OD-55; draft workload assumptions
    note: Validate workload limits; 60,000 homes are not accounts or concurrent sessions.
  - kind: maintainability
    evidence: ADR 0001 to 0004; PRD DD-009
    note: Reuse versus added services/connectors changes operating complexity and support.
  - kind: evolvability
    evidence: PRD DD-009/OD-54/55; ADR 0001 to 0004
    note: Keep choices replaceable where evidence is absent without preselecting future topology.
effort: L
success_criteria:
  - metric: Current grants enforced across view, list, search, files, export, retrieval and dispatch; revocation denies the next protected request
    target: Seeded authorized and unauthorized cases return expected allow/deny result
    measurement_window: Before resident activation
    source: PRD AC-111 to AC-128; BRD AC-104 to AC-117; OD-54
  - metric: Unsafe documents remain isolated and review, acceptance and publication are distinct
    target: Invalid, scanner-unavailable, pending, unpublished and revoked cases fail closed
    measurement_window: Before upload/publication enablement
    source: PRD AC-114/115 and AC-135/136; BRD AC-106/107; OD-54
  - metric: Resident answers use current authorized sources, abstain on missing/stale/conflict and require review
    target: Separate task registration and release evidence; per-message review; no live send path
    measurement_window: Before synthetic task activation and after material version changes
    source: PRD AC-121 to AC-131; BRD AC-113/114/118/119; OD-53/54
  - metric: Portal and assisted events recover through owned queues and independent help survives model outage
    target: Duplicate, ambiguous and lost-ack scenarios reach safe owned resolution
    measurement_window: Before exercise acceptance
    source: PRD AC-118 to AC-120 and AC-137/138; BRD AC-110 to AC-112; OD-52
---

# Optional Resident Service Architecture Boundary

**Status:** Owner-confirmed Option B for a proposed synthetic exercise architecture only. It is not an accepted production architecture. No registered or repository ADR, identifier allocation, implementation, deployment, procurement, live sending, or paid operation is authorized.

## Context

For the optional synthetic resident portal and distinct resident-answer/communication task, which architecture boundary best preserves one current case authority, separate resident identity and entitlement, safe evidence handling, accessible assisted service, and reversible delivery alongside the existing staff path, without prematurely committing to a provider, live processing, or a second platform?


> Source: PRD candidate v0.19.0, FR-062 to FR-071, AC-111 to AC-140; unsigned draft, Validate BLOCKED and Finalize NOT_EVALUATED.
>
> Source: BRD candidate v0.20.0, FR-053 to FR-062, RULE-027/028 and OD-52 to OD-55; unsigned draft, Define BLOCKED and Govern NOT_EVALUATED.
>
> Source: Pinned ADRs 0001 to 0005: preserve exercise/production distinctions, staff-only ADR 0004 and regulatory no-send ADR 0005; no supersession.

## Evaluation basis

Compare against the confirmed Frame drivers and constraints. Hard boundaries apply to every option: no homegrown password storage; do not assume resident membership in staff Entra; authentication is not case/field/task or representative permission; no persistent resident memory; no inference-based legal, consent, works, safety or contract decisions; unsafe uploads fail closed; resident replies remain individually human-reviewed by default; routine autonomous messaging remains OFF until the FR-044/AC-084 conflict and OD-53/release authority are resolved. Assisted and non-digital routes remain available without detriment. These are proposed controls for later evidence, not proof of implementation or approval.

## Considered options

### A — Portal and deterministic workflow first; agent deferred

Use a resident-specific interface over an API-authorized case projection, with explicit current grants and revocation. Provide requested document intake and appointment response as attributed events, shared with staff and assisted-channel capture. Keep answers to deterministic status/process views and human assistance; do not introduce the resident-answer model task in the first slice. Identity remains a supported managed external/customer identity capability with a local username/password-style experience as a candidate, not a selected provider. A mediated document lifecycle separates quarantine, scan, human review, and publication. Do not assume that telephone, email, SMS, letter or housing-system connectors already exist.

**Benefits:** Smallest resident-facing AI risk; portal/workflow value can be compared with the AI increment; simpler evaluation, disablement, and explanation; aligns with existing case API authority and keeps answers available through a person.

**Costs and limits:** Does not exercise the requested distinct resident-answer task until a later increment; human service capacity may dominate; deterministic answers still require current permissions and source freshness; identity, file safety, privacy, service ownership and accessibility remain substantial unresolved work.

### B — Shared case authority plus a separately registered, bounded resident-answer task

Keep the API as the only resident-facing authorization and write boundary and the existing SQL case/event authority as the candidate shared record, rather than introducing another case store. Use a resident-only projection and explicit versioned grants for case, field, task and representative scope. Record portal and assisted-channel activity with source and time provenance in the shared case workflow, using idempotent event/outbox handling and owned exception queues; treat delivery, receipt, review, acceptance, and receiver handoff as distinct states. Use controlled quarantine, clean, and published document states (or an equivalently isolated design) with fail-closed scanning, reviewer acceptance separate from publication, and tested revocation behavior.

Register the resident-answer capability as a distinct task under the existing task governance, not as an extension of staff chat or a new autonomous agent platform. For the proposed synthetic exercise only, consider one bounded model call over an API-produced, currently authorized source projection, with no delegated tool/agent loop and no persistent resident memory. It may give a cited status/process explanation or abstain and create a human handoff. Every reply is held for per-message human review and sent only through a labelled simulated outbox in this scope. No automated dispatch is enabled. Keep the portal/workflow stage deliverable independently; agent activation would require its own registry, evaluation, approval, limit, monitoring, stop and fallback evidence.

Identity remains a provider-neutral decision: a supported managed external/customer identity service offering local username/password-style sign-in is the leading candidate shape, but provider, federation, recovery proof, residency, terms, cost, and account-support model require evidence. Versioned API-owned grants remain distinct from identity proof; a relationship or address never grants access, and recovery must not silently broaden entitlement.

**Benefits:** Reuses the existing authority and task-control principles instead of creating split case truth; covers the requested answer/handoff task while containing it; allows portal-only comparison before attributing any benefit to AI; preserves staff and regulatory task boundaries.

**Costs and risks:** Adds a new resident trust boundary and higher security, privacy, accessibility, evaluation, support, and recovery burden than Option A. Shared-store isolation and revocation must be demonstrated across list, search, document, export, model context, and dispatch paths. Human review adds workload and may erase modeled capacity savings. A shared event ledger requires disciplined reconciliation and does not guarantee exactly-once delivery. No operating capability or throughput is yet validated.

### C — Separate managed resident service, agent platform, stores, and integrations

Adopt a separately hosted resident portal/agent platform with its own identity setup, service/data stores, and connector layer, integrating to the staff case authority through explicit APIs or events. This could provide a more isolated resident release boundary or managed channel features if verified product capabilities and service ownership support them. No product, provider, connectors, region, or data residency is selected by this option description.

**Benefits:** Potentially independent release and scale; may offer managed identity, channel or isolation capabilities; reduces direct coupling of the resident UI runtime to staff surfaces.

**Costs and risks:** Adds another source of truth or projection to synchronize, more identity and entitlement edges, duplicate audit/retention and support responsibilities, connector failure and reconciliation work, and likely additional vendor/licence/operating cost. Provider functionality, terms, accessibility, export, outage and real integration evidence are absent. It is premature without a verified isolation, capability, or ownership requirement that Options A/B cannot meet.

## Cross-cutting decision criteria and unresolved evidence

| Concern | Minimum boundary for any option | Evidence or owner decision still needed |
|---|---|---|
| Identity and recovery | Managed credential lifecycle; resident sign-in separate from staff identity; current authorization checked on every request; recovery cannot grant case rights | OD-54: supported service, accessible enrollment/recovery, abuse controls, terms, residency, costs, support owner, lawful processing and recovery assurance |
| Case, task, and representative authority | Server-side versioned scoped grants; default deny; deny existence-revealing metadata; recheck after household/recovery changes and before every retrieval and dispatch | Identify authoritative grant issuer, proof/approval, dispute and revocation owners; validate access denial and next-request behavior; do not infer these from a login or address |
| Documents | Isolate unvalidated intake from readers and models; unavailable scan is fail-closed; clean is not accepted; human review and publication are separate; demonstrate revocation and cached/link behavior | OD-54: permitted types/limits, scanner capability/owner, retention and rights, publication authority, download/revocation behavior, recovery and cost |
| Omnichannel events | Preserve source, actor, occurred/recorded time, delivery/receipt/review/accepted states, stable event identity and owned ambiguity/replay queues; no exactly-once claim | OD-52: actual channel/system inventory, source ownership, receiving queue, staffed service and connector evidence; manual/assisted capture is labelled as such |
| Resident-answer task | Separate task registration and release/evaluation; current authorized projection before model context; cited source/as-of or abstention; human/help/hazard path independent of model; no persistent memory or delegated agent | OD-53 and OD-54/55: policy authority, versioned evaluation and release, source freshness/conflict rules, review capacity, disable/restart ownership, privacy and operating limits |
| Communication | Per-message human review is the default for every resident reply, including in-portal output. No actual dispatch in this commission | Requirements owner reconciles universal FR-044 with AC-084; no exception unless separately authorized under OD-53 and proven release gate. Simulated outbox is not sending authority |
| Service and accessibility | Assisted and non-digital parity, safe shared-device behavior, accessible recovery, ordinary and urgent routes, manual fallback, and named owners for exceptions | OD-52 plus direct accessible research, service response/capacity commitments, incident and lost-acknowledgement recovery; exercise aging examples are not SLAs |
| Privacy, audit, telemetry | Minimize processing; keep protected case audit distinct from diagnostic telemetry; no credentials, raw prompts, document text, or resident contact/address content in diagnostics; retention remains unselected | OD-54 and appropriate privacy/security review, purpose and retention/rights decisions, access model, transfer/provider terms. Follow shared telemetry-foundations vocabulary and OpenTelemetry semantic conventions; do not coin custom names here. |
| Cost and scale | Cost full identity, support, storage, scan, model, network and service operation; stage reversible and avoid an unnecessary platform | OD-55: verified limits and cost inputs. 60,000 homes is not accounts or concurrency; five sessions are only a proposed exercise workload. |

Telemetry alignment for a later design: use the shared telemetry-foundations skill and the applicable OpenTelemetry semantic conventions for traces, metrics, logs, and resource attributes; bound metric cardinality and apply the skill denylist/redaction rules. This draft does not name a new telemetry attribute or assert that an audit/observability implementation exists. Protected business audit and diagnostic telemetry remain separate with independently governed access and retention.

## Decision Outcome

**Chosen option: B — Shared case authority with a separately gated resident-answer task.** The owner confirmed: “Reuse existing case authority to avoid duplicate platforms; deliver the portal/workflow first and independently gate the bounded resident-answer task.” This is a proposed synthetic exercise architecture only, not production, spending, deployment, procurement or implementation authority. Per-message human review remains the default for every reply; routine autonomous messaging remains OFF pending FR-044/AC-084 reconciliation and OD-53/release gates.

| Driver | A: portal only | B: shared authority + gated task | C: separate platform |
|---|---|---|---|
| Platform duplication | Lowest | Low; shared API candidate | Highest |
| Resident-answer task | Deferred | Included only after independent gates | Included with extra platform |
| Operating complexity | Lower initially | Moderate; review and reconciliation required | Highest; additional ownership and integration |
| Evidence fit | Safe fallback if agent is not ready | Matches request without unconditional release | No verified platform need yet |

The recommendation does not select an identity vendor, a managed-agent product, production topology, document service, connector, database implementation, service objective, cost ceiling, retention period, policy exception, or rollout date. If service evidence shows shared API/store cannot meet a resident trust or operating boundary, revisit Option C; if the answer task cannot pass separate evaluation or staffing gates, retain Option A without blocking independent staff delivery.

### Consequences

* **Positive:** One case authority reduces competing decision state; resident and staff events can be reconciled; the agent remains a distinct registered, inspectable task; portal and model value can be measured separately; infrastructure additions are not justified by assumption.
* **Negative:** A public resident surface increases attack and support exposure; API authorization and document isolation become critical and require independent evidence; per-message review and human handoffs require staffing; shared data creates privacy and retention obligations; added review/reconciliation can make the illustrative low scenario net-negative.
* **Neutral/accepted uncertainty:** Managed identity candidate, connector availability, actual provider/model, workload capacity, support volumes, telemetry backend, retention, real legal basis, benefits and costs remain unknown until evidence and accountable decisions exist.

## Exact upstream traceability

| Architecture question | Unsigned PRD candidate | Unsigned BRD candidate | Boundary carried into this analysis |
|---|---|---|---|
| Resident case projection and safe access | FR-062; AC-111–113 | FR-053; AC-104/105 | Current case/field/task scope, approved version only, deny cross-case disclosure |
| Upload and publication | FR-063; AC-114/115; NFR-019 | FR-054; AC-106/107; NFR-014 | Quarantine and safe scan; review is not acceptance/publication |
| Appointment response | FR-064; AC-116/117 | FR-055; AC-108/109 | Response is not works consent or autonomous confirmation; retain capacity/human gates |
| Omnichannel history and exceptions | FR-065/066; AC-118–120; NFR-020 | FR-056/057; AC-110–112 | Provenance, replay/ambiguity handling, delivery distinct from accepted handoff, owned queues |
| Grounded resident-answer task | FR-067; AC-121–123 | FR-058; AC-113/114 | Authorized sources, citation/as-of, abstention, independent help/hazard route |
| Non-digital parity and assistance | FR-068; AC-124/125 | FR-059 and RULE-027; AC-115/125 | Optional channel, no detriment, safe contact and person route |
| Identity, entitlement, representative | FR-069; AC-126–128; NFR-019 | FR-060; AC-116/117 | Separate identity and versioned grant/recovery/revocation; OD-54 unresolved |
| Message policy and review | FR-070; AC-129–131; DD-009 | FR-061 and RULE-028; AC-118/119/126; FR-044/AC-084 | Default per-message review; conflict explicitly unresolved; OD-53 and activation OFF |
| Value, effort, and sizing | FR-071; AC-132/133; NFR-021; AC-139 | FR-062; AC-123/124; OD-55 | Hypothesis only; compare portal-only and answer-task; no uptake, cash or capacity assertion |
| Six-script exercise and controls | GOAL-005; AC-140; NFR-018–020 | FR-053–062; NFR-013/014; RULE-027/028 | Proposed synthetic exercise only; all new criteria remain unrun |

Candidate PRD hashes as supplied in its validation record: document SHA-256 bfe93dc2cb68ec18c76d10794305ee1667c5ecc1937c0c28cd876dae77195f8d; patch SHA-256 37e35e478f49165d787c475afed46d94eb5bff7eb8348925b68e8c43e1aed97c. These upstream bytes were not recomputed in this Decide turn. The BRD and PRD candidate packages remain unsigned; BRD Define is BLOCKED / Govern NOT_EVALUATED; PRD Validate is BLOCKED / Finalize NOT_EVALUATED. Neither package is an approved handoff.

## Owner decision needed to exit Decide

Choose Option A, B, C, or revise the options. If choosing B, confirm whether the staged boundary is right: portal/workflow slice first; distinct resident-answer task only after separate registry, evaluation, human-review capacity, privacy/security, service-owner and release gates; routine dispatch remains OFF. State the rationale or tradeoff you want recorded. The Decide phase remains open until you explicitly confirm the resulting option and rationale; no Govern or repository integration follows automatically.


## Diagram

The ADR workflow diagramFormat remains the closed-enum value **mermaid**. The owner requested an editable Excalidraw illustration instead of a Mermaid-only visual. Installed ADR and architecture-diagrams contracts permit only ASCII or Mermaid as the selected primary diagram format. To avoid changing or mislabeling the enum, this draft keeps Mermaid as the declared format and adds a supplementary Excalidraw source and PNG preview. The PNG is a local Chrome screenshot of an SVG generated from the same editable element model; it is not an Excalidraw application export.

~~~mermaid
flowchart TB
    resident[Resident / representative portal] --> identity[Managed external identity candidate]
    identity --> api[Resident API boundary: current authorization and validated writes]
    assisted[Assisted phone / email / visit] --> api
    help[Independent person / urgent-help route] --> humans[Human review and owned queues]
    api --> grants[Current case / field / task / representative grants]
    grants --> case[(Existing case authority candidate)]
    case --> events[Shared event / outbox and exceptions]
    case --> task[Separately registered resident-answer task]
    upload[Resident upload] --> quarantine[Quarantine and fail-closed scan]
    quarantine --> review[Human review; clean is not published]
    task --> humans
    events --> humans
    humans --> simulated[Simulated outbox only; no live send]
~~~

Rendered preview: ![Resident service boundary diagram](./resident-service-boundary.png). Editable Excalidraw source: [resident-service-boundary.excalidraw](./resident-service-boundary.excalidraw). Companion SVG: [resident-service-boundary.svg](./resident-service-boundary.svg).

## Risks and Mitigations

* Cross-case or representative disclosure: default-deny API grants, recheck every protected request and turn, separate recovery from entitlement, and test lists, search, files, export, model retrieval, dispatch and revocation.
* Unsafe or unpublished document exposure: isolate quarantine; unavailable scanning fails closed; clean, human acceptance and publication are separate; test cache and link revocation.
* Incorrect or manipulated answer: use current authorized source projection, treat prompts and file content as untrusted data, cite source/as-of, abstain on missing/stale/conflicting facts, and keep help/hazard handling independent.
* Unreviewed communication: per-message review remains default; routine exception stays OFF until FR-044/AC-084 wording and OD-53/release authority are resolved. No live send path is selected.
* Service exclusion or lost handoff: preserve assisted/non-digital routes and named queue ownership; test outage, duplicate, ambiguity and lost-ack recovery. Delivery is not receipt or accepted handoff.
* Privacy or telemetry leakage: separate protected audit from diagnostic telemetry; use shared telemetry-foundations and applicable OpenTelemetry semantic conventions; apply denylist/redaction; no credentials, raw prompts, file text or resident contact/address content in diagnostics. No new telemetry names are coined.
* Unsupported scale/value assertion: validate actual costs and limits under OD-55; homes are not accounts; five sessions are only proposed exercise load.

## Rollback / Exit Strategy

Keep the portal and resident-answer task independently disableable. If the answer task fails evaluation, privacy/security, human-review capacity or ownership gates, disable it and retain only portal, deterministic status and human/assisted routes whose own gates pass. If resident authorization, document controls or service recovery cannot be demonstrated, disable resident access without delaying independent staff landing/auth. Reconcile uncertain events rather than replaying them as accepted facts. Do not delete records as a rollback shortcut; retention and deletion decisions remain open. Restart requires current versioned evidence, authorization and human approval; no automatic restart or live operation is implied.

## Affected Components

* Resident and representative portal and access journeys.
* Managed external identity candidate and separate recovery.
* API-owned resident projection and case/field/task/representative grants.
* Existing case authority, subject to resident-isolation evidence.
* Document quarantine, scan, review, publication and revocation.
* Separately registered resident-answer task and human-review queue.
* Shared portal/assisted-channel event and exception reconciliation.
* Human help, urgent/hazard routing, diagnostics and operational ownership.

## Confirmation

This proposal records the owner-confirmed exercise decision, not an accepted ADR or implementation evidence. Before adoption or activation, the requirements owner must resolve FR-044/AC-084; Programme/service owners must close OD-52; authorized domain owners must decide OD-53; Digital/privacy/security owners must close OD-54; Programme/Data and Performance must validate OD-55. Independent integrated-byte quality review and applicable accessibility, privacy, security and service evidence remain required. Revisit if evidence shows shared authority cannot meet a verified boundary or the bounded task fails its independent gates.

## Registry and placement gate

No ADR identifier is allocated. Pinned repository ADRs 0001–0006 are in docs/adrs; no .adr-config.yml was found in the inspected pinned tree. The installed authoring skill expects an allocator-issued four-digit ID and final path under docs/planning/adrs. This draft does not create a synthetic registry, infer 0007, update existing lineage, or resolve the repository-versus-plugin placement mismatch. Native RPI integration must choose the authoritative path and allocator before a registered ADR is created.
