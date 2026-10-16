---
title: ADR 0005 Regulatory Compliance Assistant
description: Accepted synthetic-development design for a regulatory compliance assistant with human authority boundaries and a measured chat-value ship gate; operational reliance remains unapproved
author: AMA programme
ms.date: 2026-10-16
ms.topic: reference
---

## Status

Accepted for synthetic development only by the exercise owner, Juan Manuel
Servera, on 2026-10-16 (Refs #209). Operational use remains proposed and
unapproved. This accepts development of the regulatory compliance assistant,
not a finding that chat adds value or that any legal duty is satisfied. Chat
must pass the [ship test](#evaluation) before it is shipped.

The 2026-10-15 permission for clearly labelled fictional demo assumptions
remains bounded below. Neither decision supplies real company Legal,
Compliance, DPO or control-owner approval or decides which duties apply to
Zava North Homes. It builds on
[ADR 0001](./0001-azure-architecture.md), [ADR 0002](./0002-pilot-readiness-architecture.md)
and the [regulatory literacy synthesis](../reference/research/ux/regulatory-literacy-for-journeys.md).

## Owner Decision: Acceptance and Authority (2026-10-16)

ACCEPT the regulatory compliance assistant for synthetic development only.
Develop the full assistant, including chat, subject to measured value over
deterministic rule cards with provision links as the chat ship test. Accepting
this design does not approve operational reliance, paid deployment or actual
staff/resident processing; their existing authorization gates remain.

The assistant's authority is **retrieve, compare, cite, flag and route only**.
It may summarise retrieved evidence as a cited proposal; it has no independent
legal, approval or action authority. It can never:

* Give legal advice, make an authoritative legal interpretation, decide that a
  duty applies or is satisfied, certify compliance or replace professional
  judgement.
* Approve, activate, amend or retire rule cards or live controls; remove a
  hold; approve its own output; or promote a simulated approval to a real one.
* Set or alter hazard awareness dates or statutory clocks, screen out a
  report, suppress a deterministic alert, delay emergency/hazard intake,
  decide safety acceptance or close a compliance check.
* Infer, grant or override resident consent, representative authority,
  privacy permissions or significant decisions affecting a resident.
* Make financial commitments, approve expenditure, submit a real grant claim,
  bind Zava to terms or automatically send resident communications.
* Invent binding grant, contract or lease terms, fabricate official or licensed
  sources, treat future/consulted law as active, or silently resolve conflicting,
  missing, incomplete or stale evidence as clear.

Legal interpretation, rule activation, resident consent, safety decisions and
financial commitments remain under the relevant named human approval and
resident decision rights. A deterministic engine executes only human-approved
contracts; it does not confer any of those powers on the assistant.

### Exercise Owners and Approval Capacity

| Capacity | Named exercise owner | Permitted synthetic-demo capacity |
| --- | --- | --- |
| Legal | Juan Manuel Servera | Review cited interpretations and record simulated legal review of fictional rule cards and source-change proposals |
| Compliance | Juan Manuel Servera | Review synthetic applicability, card approval and activation/hold/restart proposals; record simulated control-owner decisions |
| DPO | Juan Manuel Servera | Review synthetic purpose, minimisation, access and retention assumptions; record simulated privacy review |

These are exercise capacities, not actual company appointments, qualified legal
sign-off, completed reviews or permission for real processing. Fictional role
accounts represent those capacities; they are not additional named approvers.
Holding all three capacities does not waive author/approver separation: Juan
Manuel Servera cannot approve a card he authored by switching roles. If that
separation is unavailable, keep the card unapproved.

The real company Legal, Compliance and DPO owners, their delegations and
approval capacity remain an unknown-company-details gap. Close it with named
accountable owners and evidenced authority before operational reliance. Do not
invent appointments or transfer synthetic approvals into operational use.

## Owner Decision: Synthetic Demo Development (2026-10-15)

The owner directed that missing real approval delegates and source documents
must not block synthetic development: use made-up demo details and record the
decision. This authorizes development fixtures and simulated review workflows,
not invented evidence of legal compliance or permission for real processing.

* Use fictional role accounts such as `demo-compliance-reviewer`,
  `demo-legal-reviewer` and `demo-privacy-reviewer`. Label their identity and
  authority records `synthetic-demo`; they are not real delegates or signatories.
* Simulated card approvals, acknowledgements and incident/restart decisions may
  exercise the complete demo flow. Label each as simulated and bind it only to
  the synthetic exercise; it cannot approve an operational release or a real
  person's data processing.
* Missing grants, contracts and leases may have wholly original fictional
  fixtures labelled `synthetic-demo`, with no claim of company provenance,
  legal force or real retrieval. Example: a fictional demo grant requires an
  evidence checklist before a simulated claim can be submitted. This is a test
  condition, not a funding condition imposed on Zava.
* Missing official or licensed standards remain gap records. Do not fabricate
  statutory provisions, official publication/retrieval dates, commencement
  dates or licensed PAS text to fill them. Separate synthetic rule cards from
  cited official sources and never display fixture conditions as law.
* Safe offline development and synthetic demonstrations can proceed despite
  these gaps. Keep fixture identities, approvals, source records and outputs
  visibly distinguishable from actual evidence, including in exports and logs.
  Synthetic approval records cannot be promoted to operational approvals.
* Actual staff identities, live provider processing, paid calls, participant
  exercises and deployment retain their separate existing authorization gates.
  Synthetic resident records do not remove actual staff privacy obligations.
* Before operational reliance, replace fictional assumptions with verified
  applicable sources, actual accountable delegates and their qualified approval
  evidence, and rerun affected tests. Until then, report the operational result
  as unassessed or blocked, never compliant or approved.

The chosen option is to unblock synthetic development using explicit fixtures,
rather than wait for real company delegates/documents or silently portray
invented details as genuine. The benefit is a demonstrable end-to-end workflow;
the cost is later replacement, revalidation and the risk of fixture assumptions
leaking into real use. Visible labelling and non-transferable exercise authority
are required to reduce that risk. This decision records no completed
implementation, model evaluation, human trial or operational approval.

## Requirements traceability

| Requirement | Document |
| --- | --- |
| FR-051, AC-099, OD-50 | [BRD](../brds/agentic-retrofit-programme-brd.md) |
| FR-060, AC-104 to AC-106, OQ-026 | [PRD](../prds/zava-forward-retrofit-programme-demonstrator.md) |
| Proposal summary | [Case Study 48 Addendum](../case_study_48_addendum.md) |

It extends BRD FR-038 to FR-040 and RULE-021, which already require a source
register, monitoring and human-approved change. BRD and PRD numbers differ, so
cite the document.

## Context

Journey roles meet legal duties at many steps: hazard intake clocks, PAS 2035
roles, grant conditions, resident data and automated decisions. Most users
should recognise a trigger and act safely, not interpret law. The knowledge
base holds dated snapshots and a register but nothing the product can query,
and the MVP assistants have no regulatory source.

Requested capabilities:

* A store for laws, standards and guidance.
* Proactive checks that alert users in specific situations.
* A chat for questions about a specific home.

## Principles

* The system retrieves, compares, cites, flags and routes. Named humans
  interpret law, approve rule cards and decide that a duty is met.
* Authority order follows the regulatory README: legislation, regulatory
  standards, grant and contract terms, guidance, then consultation material.
* Planned or consulted law is labelled future and never fires as active.
* Deterministic code owns clocks, rule evaluation and holds. A model never
  sets an awareness date, screens out a report or closes a check.
* Safety routes (emergency and hazard intake) work with the system down.
* Every output cites source, provision, status, effective date and
  retrieval date, or says the source is missing.

## Architecture

```text
Official sources -> Ingest job -> Law store (Azure SQL + Blob + AI Search index)
                                        |
        Home, case and step events -> Rule engine (deterministic) -> Alerts
                                        |
User chat -> Chat service -> Retrieval (law + home facts, role scoped) -> Foundry model
                                        |
                          Cited, proposal-only answer -> human owner on doubt
```

All components reuse the existing runtime: `api` (SQL authority), `agents`
(Foundry only, no database), `orchestrator` (schedule) and `import`.

### 1. Law store

Azure SQL (ledger enabled) is the system of record. Blob holds immutable
source snapshots. An Azure AI Search index (hybrid keyword and vector) holds
provision-level chunks for retrieval only; it is rebuildable from SQL.

| Table | Purpose |
| --- | --- |
| `reg_source` | Stable ID, title, official URL, authority type, jurisdiction, owner, change likelihood, monitoring cadence |
| `reg_version` | Source version: publication, effective, retrieval and supersession dates, content hash, blob path, parse result, completeness, current-use status (in force, guidance, consultation, historical) |
| `reg_provision` | Provision ID within a version (for example Article 22A, Phase 1 regulation 5), text, heading path, hash, embedding reference |
| `reg_rule_card` | Versioned approved card: trigger, applicability conditions, provisions cited, clock, safe default action, escalation owner role, approver, approval date, effective and retirement dates, status (draft, approved, active, held, retired) |
| `reg_change` | Detected difference, classification, affected cards, journeys, tests and templates, reviewer, decision |
| `reg_check` | One evaluation: card version, home or case, step, inputs hash, result, evidence IDs, time |
| `reg_alert` | Alert raised from a check, audience role, acknowledgement, owner action, outcome |
| `reg_chat_turn` | Question, home scope, retrieved provision IDs, answer, citations, model tier, reviewer if escalated |

Seed it from `docs/reference/regulatory/` snapshots. Snapshots stay
immutable; a new retrieval becomes a new `reg_version`. Local sources that
are overviews or incomplete (PAS 2035, Phase 2 hazards guidance) carry
`completeness = partial` and the chat says so. Missing sources (leasehold,
complaints handling, TrustMark, licensed PAS 2035) are registered as
`gap` records so the system can say "no source held".

### 2. Change monitoring

The orchestrator job fetches official publication metadata, legislation.gov.uk
data and GOV.UK feeds on each source's cadence (weekly for Awaab's Law
Phase 2 until commencement; monthly for UK GDPR and the grant scheme). Scraping
is discovery only. On a difference it:

1. Stores the candidate beside the approved version.
2. Classifies the change and lists affected cards, journeys, tests and
   communications (an assistant may draft this as a proposal).
3. Routes to the named owner. An approved card is never overwritten by
   detection; an authorised owner may place a hold.
4. After approval, runs regression tests, then activates on the effective
   date with rollback.

### 3. Rule cards and the rule engine

A rule card turns an approved interpretation into data. Example (illustrative,
needs Compliance approval):

| Field | Example |
| --- | --- |
| Trigger | Case record contains a damp, mould or emergency hazard report |
| Cited provisions | Hazards in Social Housing Regulations 2025; Phase 1 guidance, status in force from 27 Oct 2025 |
| Clock | Per the approved card, starting from the recorded awareness time |
| Safe default | Use the human emergency or hazard route now; open an investigation task |
| Escalation | Repairs and hazard owner, then Building Safety lead |
| Approver | Named compliance owner |

The engine is plain code over SQL facts. It is idempotent and checkpointed,
and runs on three triggers: workflow step transition, data change on a home
or case, and a schedule for clocks. It emits a check result of `clear`,
`attention`, `breach risk`, `unknown (missing evidence)` or `not applicable`.
Missing evidence is `unknown`, never `clear`.

### 4. Proactive alerts

Alerts attach to the journey step where the user already works, not a new
portal. Each alert states what was noticed, the cited source and status, the
safe action, who owns the decision, and the clock if one applies.

| Step | Example check | Audience |
| --- | --- | --- |
| Report or nominate | Possible hazard in free text or call note | Intake, repairs owner |
| Understand home | Vulnerability or health data captured without a recorded purpose | Officer, DPO adviser |
| Scope and feasibility | Measure set changed after a PAS 2035 review | Coordinator |
| Funding | Claim lacks grant agreement terms or evidence | Grants officer, Finance |
| Coordinate and deliver | Hazard hold open on a home being scheduled | Scheduler, Programme |
| Inspect | Completion recorded without independent acceptance | QA, Programme |
| Handover | Complaint or defect still open at closure | Housing, resident owner |
| Any automated recommendation | Significant decision affecting a resident lacks named human decision | Decision owner |

Alert hygiene: group per home, rank by clock and harm, require an owner
acknowledgement and outcome for `breach risk`, rate-limit `attention`, and
track false-positive rates so fatigue is measured, not assumed. The model may
draft the explanation text, but the trigger is deterministic. No alert
sends resident messages automatically.

### 5. Home-specific chat

A chat panel on the home and case view, available to roles by purpose.

Flow:

1. The API builds a scoped fact snapshot for the home using the existing
   capture pattern: only categories the user's role may read, with source IDs.
2. Retrieval pulls matching provisions and approved rule cards. Filters
   exclude historical and consultation material unless the user asks, and
   label it when used.
3. The `agents` service calls Foundry with the facts, provisions and a fixed
   system instruction; it has no database access and no write path.
4. Output is validated: every statement cites a provision or fact ID, status
   and dates are shown, and unsupported claims are dropped.
5. The turn is stored with its sources. The user can send it to the named
   owner with one action when in doubt.

Answer template: what the sources say, what applies to this home according
to its recorded facts, what is unknown or missing, safe next action, and who
decides. The chat refuses to conclude compliance, give legal advice, treat a
policy announcement as commenced law, or infer lease, grant or contract terms.
When sources conflict it shows both and escalates. A model-negative result
never suppresses a rule-engine alert.

### 6. Security, privacy and governance

* Role-scoped facts only; the resident's health and vulnerability data
  follow existing purpose controls. Queries to Foundry exclude fields not
  needed for the question.
* Chat and check records are retained under the existing retention
  alignment; DPO review decides periods.
* Source text is untrusted data: retrieved law and imported documents are
  never executed as instructions, and prompt-injection tests are included.
* Entra roles: rule-card authors, approvers and chat users are separate; an
  author cannot approve their own card.
* UK GDPR Art. 22A to 22C: the system proposes and flags; consequential
  decisions have a named human with recorded reasons.
* Accessibility: alerts and chat meet WCAG 2.2 AA, no colour-only status,
  keyboard operable, plain-language mode.

## Evaluation

Use the existing real-AI proof discipline. Acceptance needs evidence from
the continuing synthetic 60,000-home stock, not unit tests alone.

| Measure | Gate to set with owners |
| --- | --- |
| Citation validity: every cited provision exists and supports the claim | Target 100 percent on a graded set |
| Refusal accuracy: no compliance conclusions, no future law applied as active | Target 100 percent on adversarial prompts |
| Rule recall on seeded hazard, evidence and automated decision cases | Set after a baseline run; hazard misses are critical |
| Alert precision and acknowledgement time | Measured in a staff trial |
| Stale source handling | Cards using an out-of-cadence source are labelled |
| Staff comprehension | Validated with repairs, housing and grants staff, not assumed |

The owner accepted the chat ship test on 2026-10-16: compare against a non-AI
baseline of deterministic rule cards with provision links. On the same
role-scoped tasks and source versions, record answer/citation correctness,
safe escalation and refusal, task completion, comprehension, elapsed time,
human review effort and attributable service cost. Agree the graded tasks and
benefit thresholds before running the comparison; do not choose them after
seeing the results.

Ship chat only when the evidence shows added value over that baseline without
weakening safety, privacy or citation gates. If chat adds no measured value,
fails those gates, or lacks comparison evidence, ship the rule cards and law
store without chat, subject to their own approval gates. Synthetic results do
not establish real staff benefit or authorize operational use. The comparison,
thresholds and staff validation remain unexecuted or unset here; this records
the accepted test, not a passing result.

## Phasing

1. Law store and source register loaded from the existing snapshots, with
   gap records and a read-only provision viewer (SQL, Blob, no AI).
2. Rule cards and engine for two approved cards (hazard awareness
   clocks, automated decision safeguard), alerts in the workbench.
3. Chat over the law store and one home's facts, proposal only, with
   evaluation gate.
4. Change monitoring and the approval workflow with regression tests.
5. Broaden cards by journey step, guided by alert precision data.

## Alternatives considered

The following comparison records the options for the owner's 2026-10-16
decision. Benefits and costs are design expectations, not measured outcomes
or service quotes.

| Option | Expected value and trade-off | Decision |
| --- | --- | --- |
| No assistant | Avoids new store, monitoring and chat costs, but leaves users to navigate snapshots and route questions manually; no new proactive step checks | Not selected for the synthetic exercise: it does not demonstrate the requested source-to-journey workflow |
| Rule cards and law store without chat | Versioned sources, deterministic checks, alerts and provision links provide an auditable baseline without model-answer risk or chat inference cost; users still navigate explanations themselves and store/monitoring costs remain | Required comparator and shipping fallback if chat does not demonstrate added value; simplest acceptable outcome under its own approval gates |
| Full assistant with chat | Adds home-specific, role-scoped cited explanations and routing; potential comprehension/effort benefit is unproved, with added retrieval, inference, privacy, evaluation and review costs | ACCEPT for synthetic development only; chat shipment is conditional on the accepted value and safety gates |

Additional architectural alternatives retained from the proposal:

* Chat only, no rule engine: weak on clocks and silent failure; rejected.
* Fine-tune a model on law: stale, uncitable, hard to roll back; rejected.
* Separate regulatory product: duplicates identity, audit and hosting; rejected
  for the exercise, but the law store has a clean boundary if one is wanted.

## Cost Position (2026-10-16)

| Component | Estimate status | Evidence needed before billable deployment |
| --- | --- | --- |
| Azure AI Search | Unknown; no monthly estimate or verified incremental cost | Region, tier, partitions/replicas, index/vector size, query/indexing load, billable features, approved run duration and current pricing |
| Source-monitoring jobs and diagnostics | Unknown; no monthly estimate or verified incremental cost | Source count/cadence, job duration/compute, retrieval and storage traffic, log volume/retention, alerting charges and current pricing |

Reuse of existing services does not mean zero cost. Attribute both incremental
and shared costs without double counting; include chat inference and human
review effort in the comparator. Before paid deployment, document sizing,
usage assumptions, current price evidence, budget fit and the relevant human
spending approval. This decision is not spending authorization.

## Open items

* The synthetic-development decision and exercise Legal, Compliance and DPO
  owner are recorded above. Real company owners, delegations and approval
  capacity remain unknown company details and must be verified before
  operational reliance; no real legal or privacy approval is recorded here.
* Which sources Zava is actually bound by remains unverified:
  * Grant award: obtain the actual award letter, agreement, conditions and
    variations; a scheme overview does not establish an award or its terms.
  * Contracts: obtain executed contracts/call-offs and incorporated standards
    and variations; do not infer obligations from sector practice.
  * Leases: obtain the applicable lease and variations for each relevant home;
    do not infer repair, access, consent or cost responsibilities.
  Original fictional demo fixtures do not establish applicability or fill
  official gaps. Named real owners must review the actual documents before
  operational reliance.
* Licensed PAS 2035 text and official sources for the gaps are not yet held.
* Azure AI Search and monitoring-job/diagnostics costs are explicitly unknown;
  sizing, pricing and spending approval remain open as set out above.
* Chat comparison tasks, pre-agreed benefit thresholds and measured results
  are outstanding. Acceptance of the ship test is not evidence that it passed.
* Phase 2 commencement on 30 November 2026 is planned, not confirmed here.
* Whether staff want alerts at these steps needs validation with real users.
