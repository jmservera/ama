---
title: ADR commission input — optional resident portal and communication agent
date: 2026-10-23
status: unsigned-prd-draft-input
---

## Commission boundary

**For the parent to commission after the PRD draft. No ADR was authored,
accepted or delegated here.** This is not an architecture decision record,
security approval, tenant instruction or implementation plan.

Read `amendment.md`, `amendment.patch`, `id-traceability.md`,
`quality-review.md`, `validation.json`, and the six upstream BRD input files.
Base is `140d8f494482c78e84d15f3d46b9223d3c487af0`; PRD v0.18.0
to candidate v0.19.0, BRD v0.19.0 to candidate v0.20.0. Exact hashes
are in `validation.json`; recheck if the parent rebases. Upstream Define is
BLOCKED, Govern NOT_EVALUATED. No approved handoff or signoff exists.

Preserve existing ADR 0001/0002/0003 production-path/exercise distinctions,
staff ADR 0004 scope/acceptance and ADR 0005 regulatory assistant no-send.
Do not infer resident membership in a staff Entra directory, broaden the five
staff assistants or introduce resident persistent memory by reusing staff
chat. The new resident-answer task needs its own registry/release/evaluation
contract; its existence does not select a separate hosted “agent platform”.

## Decision inventory, candidates and drivers

All recommendations below are candidates. ADR author chooses record grouping
and identifiers only after inspecting the current ADR registry.

| Decision needed | Options to compare | Drivers and acceptance evidence | PRD / residual gate |
| --- | --- | --- | --- |
| Resident identity and recovery | Supported managed external/customer identity candidate with local username/password-style sign-in; managed federation where genuinely usable; assisted enrolment/recovery into the same entitlement checks | Simple mobile UX, account enumeration/rate/session controls, shared devices, proportionate step-up, recovery proof, support effort, residency/terms/cost. Exclude homegrown password storage and emailed credentials. Do not select a provider from training knowledge alone. | FR-069, AC-126 to AC-128; OQ-030 / BRD OD-54 |
| Case/field/task entitlement and representatives | API-owned versioned scoped grants with deterministic checks; central managed policy evaluation backed by explicit case grants; compare operational complexity and invalidation | Multiple occupants/homes, task-limited interpreter/representative, source/review/expiry/dispute/revocation, next-request denial and delivery-time recheck. Login/address/relationship is not consent or rights. Define authoritative grant owner and recovery separation. | FR-062/069/070; OD-42/54 |
| Published documents and requested files | Controlled existing Blob path with separate quarantine/clean/publication scopes; conditional governed SharePoint only if independently evidenced; proxy delivery versus short-lived scoped references | No direct broad store/model access, type/size/malware validation, safe failed/unknown scan, reviewer acceptance separate from publication, source/version trace, revocation/cache effects, encrypted transport, rights/retention, dependency/cost. Existing staff document approval does not authorise resident publication. | FR-062/063, NFR-019/020; OD-54 |
| Omnichannel event reconciliation | SQL case-event ledger and transactional/outbox patterns; configured connector adapters where real inventory exists; manual assisted capture for absent connectors | Stable event IDs, occurrence versus recorded time, retries/idempotency, ambiguous identity matching, protected originals, delivery/receipt/accepted/review states, owned exceptions. No exactly-once delivery/billing claim. Avoid duplicate entry without assuming M365/telephony integrations. | FR-065/066, AC-118 to AC-120; OD-52 |
| Grounding, runtime and evaluation | Deterministic status/process views only; retrieval plus existing bounded model adapter for a separate registered task; managed agent runtime only if requirements justify extra tooling/cost | Authorised source projection before retrieval/model call and every turn, version/as-of/stale/conflict semantics, citations plus semantic correctness, injection tests, explicit unknown and independent human/hazard route. One bounded call/no delegation is proposed initial exercise configuration, not a reason to add agents. | FR-067, AC-121 to AC-123, NFR-017; OD-49/54/55 |
| Communication autonomy/release | Per-message reviewed reply/outbox (default); later narrowly versioned policy for routine factual replies/acknowledgements/reminders; reject broad autonomous messaging | Activation authority, permitted task/channel/audience/content/expiry, changed-access/evidence/contact recheck at dispatch, quality/control evaluation, human sensitive/consequential/uncertain gate, stop/incident/restart, audit with policy rather than fake reviewer. Simulated outbox is not live sending. | FR-070, AC-129 to AC-131; OD-53 and upstream FR-044/AC-084 contradiction |
| Service operation, support and resilience | Staff-owned manual exception queues first; later accepted connector/notification automation; staged task disable independent of portal reads | Named service/source/queue/support owners, chase until accepted handoff, ordinary versus urgent update commitments, outages/lost acknowledgement/replay, finite retry, accessible recovery, incident escalation, deployment rollback and retention recovery. Proposed one/two-working-day exercise queue ages are not operational SLAs. | FR-066/068, NFR-020; OD-25/35/36/52/54/55 |
| Privacy, records and observability | Minimum case-event/handoff records with separate file/conversation/audit retention classes; diagnostic telemetry separate from protected audit | Data minimisation, actual lawful basis/DPIA/processor/rights/retention decisions before real data, no persistent resident memory. OTel/shared telemetry vocabulary, bounded cardinality, no credentials/raw prompts/documents/contact content, auditable access without broad diagnostic copying. Use proposed-additions process if genuinely new names are needed. | NFR-019, AC-135/136; OD-45/46/54 |
| Capacity, cost and sequencing | Reuse lean accepted-exercise Azure/SQL/model baseline; isolated resident projection/task with scoped limits; add topology only for verified requirements | Five-session proposed exercise workload is not 60,000 users. Validate upload/scan/model/session/rate limits and whole service/support costs, retain financial source/budget gates, compare portal-only versus agent. No build/paid action now. Record any proven shared staff-auth dependency rather than delaying staff landing for speculative infrastructure. | NFR-021, FR-071; OD-51/55 |

## Security and agent-authority needs

The ADR should record boundaries rather than promise “secure by design”:

1. Resident client, identity provider, case API, programme state, file
   quarantine/clean/publication stores, model context, staff queue and
   diagnostics each have explicit permitted reads/writes and failure handling.
2. The browser or model cannot grant identity, change entitlement, issue
   direct SQL writes, publish a file or supply legal/consent/contract approval.
   A resident event is an attributed report, not verified business truth.
3. Deny content and existence-revealing metadata across case/field/task scope
   for lists, identifiers, links, search, files, export and model retrieval.
   Recheck grants after recovery/household changes and at dispatch; revoke
   cached/link access according to an explicit tested mechanism.
4. Hold unsafe/unvalidated uploads away from all readers/models; unavailable
   scanning fails closed. A pending receipt does not accept evidence. Bound
   file/rate/model use and prove timeout/replay recovery.
5. Safety/distress/help/referral must remain independent of inference;
   uncertainty must not generate a confident answer or delay urgent action.
   Sensitive or consequential communication remains human-reviewed.
6. Audit identity/grant/policy/source/action/version/outcome without claiming
   a person reviewed each policy-approved routine message. Keep diagnostic
   PII/credentials out by default; enforce access and separate retention.
7. Demonstrate logout/shared-device behaviour, revocation mid-session/turn,
   injection, malformed/unsafe files, stale/missing facts, model failure,
   duplicate/lost acknowledgements and kill-switch operation.

These are requirements for later design/evidence, not a vulnerability finding,
completed threat model or claim that existing code satisfies them.

## Blocking upstream wording and authorisation

Parent must reconcile BRD FR-044's universal human-review body with AC-084's
policy-disposition exception. Do not use an ADR to overrule that requirement
or manufacture an OD-53 approval. Per-message review remains default.
Architectural options can be evaluated while this is open, but the routine
exception cannot be activated. OD-52 staffing/channel inventory, OD-54 real
identity/privacy/files/recovery and OD-55 validated limits/benefit assumptions
also remain unresolved. Role-agent hypotheses cannot supply those signatures.

## Desired ADR output and non-goals

Return a proposed decision/options comparison with drivers, consequences,
security/service/agent-authority contracts, reversible migration/slice path,
required evidence, accountable decision owners and residual open gates.
Separate provisional exercise configuration from actual operational limits.
Cross-link the exact PRD candidate and BRD authority boundary. Include a
diagram only if useful, using the architecture-diagrams authoring contract.

Do not deploy, procure, mutate a tenant, select production topology without
evidence, claim legal approval, infer residents from homes, re-run broad
company research or absorb unrelated inherited BRD repairs. Implementation,
backlog, tests and repository integration are later parent-scoped native RPI
work; this handoff ends at decision readiness, not accepted architecture.
