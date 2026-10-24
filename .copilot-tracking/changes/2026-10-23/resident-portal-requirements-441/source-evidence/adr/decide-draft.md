# Decide — owner-confirmed Option B (proposed exercise architecture)

**Status:** The owner explicitly confirmed Option B for a proposed synthetic exercise architecture only. It is not an accepted architecture. The session-only draft is not a registered ADR; no identifier allocation, implementation, deployment, procurement, live sending, or paid operation is authorized.

## Decision question

For the optional synthetic resident portal and distinct resident-answer/communication task, which architecture boundary best preserves one current case authority, separate resident identity and entitlement, safe evidence handling, accessible assisted service, and reversible delivery alongside the existing staff path, without prematurely committing to a provider, live processing, or a second platform?

## Evaluation basis

Compare against the confirmed Frame drivers and constraints. Hard boundaries apply to every option: no homegrown password storage; do not assume resident membership in staff Entra; authentication is not case/field/task or representative permission; no persistent resident memory; no inference-based legal, consent, works, safety or contract decisions; unsafe uploads fail closed; resident replies remain individually human-reviewed by default; routine policy remains OFF until the FR-044/AC-084 conflict and OD-53/release authority are resolved. Assisted and non-digital routes remain available without detriment. These are proposed controls for later evidence, not proof of implementation or approval.

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

## Owner-confirmed decision

**Chosen option: B — shared case/API authority with a separately gated resident-answer task.** Owner-confirmed rationale: “Reuse existing case authority to avoid duplicate platforms; deliver the portal/workflow first and independently gate the bounded resident-answer task.” The choice is for a proposed exercise architecture only, with no production, spending, deployment or implementation authority. Assisted channels remain; routine autonomous messaging stays OFF pending FR-044/AC-084 reconciliation.

The recommendation does not select an identity vendor, a managed-agent product, production topology, document service, connector, database implementation, service objective, cost ceiling, retention period, policy exception, or rollout date. If service evidence shows shared API/store cannot meet a resident trust or operating boundary, revisit Option C; if the answer task cannot pass separate evaluation or staffing gates, retain Option A without blocking independent staff delivery.

## Candidate consequences if Option B is selected later

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
