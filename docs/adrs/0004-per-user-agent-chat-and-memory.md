---
title: ADR 0004 Per-User Agent Chat and Memory
description: Accepted decision on whether and how staff users could hold case-linked conversations with the existing assistants and keep opt-in per-user memory, within the existing single-API, Azure SQL and proposal-only runtime
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

## Status

Accepted as written by the owner, Juan Manuel Servera, on 2026-10-15 (GitHub
#158; BRD OD-44 decided). Acceptance adopts option C, staged, as the direction
and registers conversational tasks as a registry change under FR-036. It does
not activate the capability for live personal data: lawful basis, staff notice,
DPIA, retention and access (BRD OD-45, OD-46, OD-48, OD-49) remain open items
below, and no DPO, Legal, HR or control-owner approval is recorded here. It
applies the runtime of
[ADR 0001](./0001-azure-architecture.md),
[ADR 0002](./0002-pilot-readiness-architecture.md) and
[ADR 0003](./0003-journey-derived-capabilities-runtime-fit.md) to the proposal
in [BRD v0.18.0](../brds/agentic-retrofit-programme-brd.md) and
[PRD v0.17.0](../prds/zava-forward-retrofit-programme-demonstrator.md). It is
tracked as GitHub backlog epic #157 and children #158 to #164.

## Context

The five assistants return one typed proposal per request. They keep no thread
and no memory, there is no resident-facing screen, and contractors cannot use
the shared staff proposals. The capability appears in no earlier BRD, PRD or
ADR.

Evidence available:

* The customer journey atlas is desk research with 28 journeys and 24
  opportunity hypotheses. It does not show that staff want a conversation
  (BRD OD-41).
* The assistants and role projection in the MVP code are proposal-only and
  server-side default-deny (ADR 0001, ADR 0002).
* FR-036 requires registration of every AI-assisted task, and ADR 0003
  decision 3 forbids a new assistant without a registry change.
* Microsoft Learn documentation, retrieved 2026-10-14, describes Foundry Agent
  Service memory as a preview with user-profile and chat-summary types,
  automatic extraction enabled by default, a scope parameter, item-level
  create, read, update and delete, and a store-level default expiry. Preview
  status and features may change; this is not a verified design for Zava.

Assumptions and unknowns:

* Whether staff would use a chat panel is a hypothesis.
* Retention, lawful basis, staff notice and DPIA are Unknown until the DPO and
  Legal decide (BRD OD-45, OD-46).
* Whether memory is needed at all, or only thread history, is undecided (BRD
  OD-48).

## Decision drivers

* Do not add authority. Humans approve; the channel drafts, recommends,
  reconciles and flags only (RULE-018, RULE-025).
* Do not multiply agents (FR-036, ADR 0003 decision 3).
* Keep one API, one store and one audit approach (ADR 0001, ADR 0002).
* Isolate each user and role; no cross-user leakage (NFR-010).
* Consent, inspection, edit, deletion and expiry for any memory (FR-050).
* Memory is context, not evidence and not a system of record (RULE-025).
* No use for performance rating without a separate decision (RULE-026).
* Keep the case usable when the model is unavailable (FR-044).

## Options considered

* A. No chat. Keep stateless one-shot proposals.
* B. Per-user threads over the existing assistants, with no memory.
* C. Per-user threads plus opt-in per-user memory in Azure SQL, staged.
* D. Shared case memory visible to every user on a case.
* E. Managed Foundry Agent Service memory.

## Decision

The owner accepted option C, staged, as written on 2026-10-15. The options
compared above (A no chat, B threads over existing proposals, C threads plus
opt-in per-user memory in Azure SQL, D and E rejected or deferred) are
confirmed unamended. Option B is the fallback if the DPO and Legal later
reject memory (BRD OD-48). Option A remains the default comparator and is
rejected only if the owner wants follow-up questions. If the owner chooses A or
B, the BRD and PRD rows stay inactive or are reduced.

Authority: chat may recommend, draft, reconcile and flag only. It can never
approve, decide, certify, record consent, diagnose, contact a resident, change a
record without independent human review, or act as a system of record (decision
6, RULE-018, RULE-025).

Registry: a conversational task is a registry change under FR-036. It needs
registration with thresholds and a named accountable reviewer (BRD OD-49 names
the approver of thresholds) before it is enabled. No new assistant is created.

Storage: Azure SQL behind the `Store` interface (decision 3). No new store is
justified; Foundry Agent Service memory is not used.

Deployment: Azure only, region `uksouth`. Fixtures in tests and
demonstrations are labelled synthetic (ADR 0005 permits labelled synthetic-demo
fixtures only).

1. Chat extends the five existing assistants. It adds no sixth agent. A
   conversational task is registered under FR-036 with its thresholds and
   accountable reviewer, and can be enabled, disabled and have memory switched
   off without redeploying.
2. The first slice is staff only, embedded as a panel in the role workbench case
   view (PRD FR-055). Resident, representative, provider and installer chat is
   deferred to BRD OD-47. The journey, agent and UI mapping is in PRD section
   Per-user agent chat and memory.
3. Threads are stored in the existing Azure SQL store behind the `Store`
   interface through additive idempotent migrations (PRD FR-056). A thread is
   owned by a server-derived user key, tied to a case and task, and deletable by
   its owner. Thread content is separate from the append-only audit ledger,
   which holds event metadata only, so deletion does not break tamper evidence.
4. Memory is a later gate. It is off by default, per user and per role,
   inspectable, editable, deletable and expiring, and never holds resident
   health, safeguarding, vulnerability, special-category or consent data
   (PRD FR-057). Retention is Unknown until the DPO approves it.
5. Every turn re-authorises the user's current role and case and applies the
   same server-side field projection as the case view, so a changed or revoked
   role takes effect on the next turn (PRD NFR-015).
6. The channel cannot approve, decide, certify, record consent, diagnose or
   contact a resident. Case text and memory are untrusted input. Any
   record-changing output is a proposal that goes through the existing
   independent review (PRD FR-058).
7. Runtime stays direct Azure OpenAI calls through the existing Foundry
   deployments (`standard`, `capable`) in `uksouth`, as in ADR 0001 to
   ADR 0003. No Foundry Agent Service orchestrator is deployed.
8. Activation needs a multi-turn evaluation harness with approved thresholds
   (PRD FR-059, BRD OD-49).

## Isolation model

* Identity: the user key comes from the authenticated Entra principal on the
  server, never from a client-supplied value.
* Storage: every thread and memory row carries the user key and role; every
  query filters on it; there is no shared memory table across users.
* Per-turn checks: role, case scope and projection are re-evaluated on each turn
  and on each export or deletion.
* Prompt assembly: only the owner's own thread and memory plus the projected
  case data enter the prompt. Other users' content is never retrievable.
* Injection: case text and memory are treated as inert data, as in the existing
  proposal service.
* Administration: administrator or break-glass access is rare, reasoned,
  time-limited and audited, and its policy is a BRD OD-46 decision.

## Consequences

* Positive: follow-up questions stay inside the case view, the registry, the
  review and the audit that already exist; no new store or agent runtime.
* Negative: personal data of staff, and resident data inside case text, enter a
  new data class that needs a DPIA, notice, retention and rights handling.
* Risk: users may treat chat as authority or memory as evidence. Mitigation is
  the refusal rules, citations from the case record only and review of every
  proposal.
* Risk: memory could be used for staff monitoring. Mitigation is RULE-026 and
  no management view of content.
* Risk: Azure SQL row-level isolation depends on application filters. A
  database-level control such as row-level security could be evaluated; this ADR
  does not decide it.
* Cost and latency: unknown. No estimate is made without measurement.

## Alternatives considered and rejected

* A. No chat. Rejected only if the owner wants follow-up questions; it remains
  the default and the comparator. It costs nothing and adds no risk.
* B. Threads without memory. Not rejected: it is the smaller first step and the
  fallback if the DPO rejects memory (BRD OD-48).
* D. Shared case memory. Rejected: it exposes one user's notes to others, blurs
  authority, and turns memory into a de facto record.
* E. Managed Foundry Agent Service memory. Not chosen for the first slice: it is
  a preview, automatic extraction conflicts with opt-in consent and inspection
  by default, it adds a second store beyond Azure SQL, and ADR 0001 to ADR 0003
  use direct calls. Revisit after general availability and a DPIA.

## Open items

Decided 2026-10-15 by the owner:

* OD-44: adopted as written; staff only, embedded in the case view; registry
  change under FR-036.

Owner:

* OD-48: memory in scope or thread history only; staff memory versus any later
  resident memory.

DPO and Legal:

* OD-45: lawful basis, staff notice, DPIA, model provider and region terms,
  rights handling and treatment of resident data in case text.
* OD-46: retention per class (Unknown), access including break-glass, aggregate
  use and the performance-use prohibition, with HR if named.

Others:

* OD-47: any non-staff chat, depending on OD-41, OD-42 and FR-045. Resident
  Engagement, DPO and Legal.
* OD-49: grounding, abstention and injection thresholds and accountable
  reviewer.

The owner is also the named owner for DPO and Legal decisions, but no lawful
basis, DPIA, retention, access or threshold decision has been recorded, so
OD-45 to OD-49 stay open and are not invented here. Live personal data stays
excluded until they are recorded.

Not decided here: storage hardening such as row-level security, a retention
number, model choice per task and any cost target.

## Related documents

* [BRD v0.18.0](../brds/agentic-retrofit-programme-brd.md): BG-013, FR-049,
  FR-050, RULE-025, RULE-026, NFR-010, NFR-011, AC-091 to AC-098, OD-44 to OD-49
* [PRD v0.17.0](../prds/zava-forward-retrofit-programme-demonstrator.md): FR-055
  to FR-059, NFR-015, NFR-016, AC-091 to AC-103, OQ-020 to OQ-025
* [Customer journey atlas](../reference/research/ux/customer-journeys/customer-journey-atlas.md)
* [ADR 0001](./0001-azure-architecture.md),
  [ADR 0002](./0002-pilot-readiness-architecture.md) and
  [ADR 0003](./0003-journey-derived-capabilities-runtime-fit.md)
* GitHub backlog: epic #157, #158 (decision), #159 (panel), #160 (threads), #161
  (memory), #162 (isolation), #163 (privacy and retention), #164 (registry and
  evaluation)

## Implementation status

The original acceptance did not itself implement or activate the capability.
Subsequent source delivery exists under `src/` (threads, isolated memory,
privacy, cited panel and scripted evaluation). The
[2026-10-27 engineering boundary](../reference/research/chat-memory-dpia.md#staff-chat-engineering-boundary-2026-10-27-refs-157162159164163)
records current bounded staff HTTP turns, warning and consumption evidence.
It does not amend this decision or supply a conversational registry/release,
privacy/access policy, thresholds, serving-model/human effectiveness or a named
screen-reader exercise. General staff model dispatch and HTTP memory prompting
remain denied; #159 to #164 and parent #157 are not accepted in full.
