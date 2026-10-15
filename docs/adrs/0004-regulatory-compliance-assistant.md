---
title: ADR 0004 Regulatory Compliance Assistant
description: Proposed design for an AI-assisted regulatory checking system with a versioned law store, proactive step checks and a home-specific chat, built on the existing Azure SQL, Foundry and five-assistant runtime
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

## Status

Proposed. This is a design proposal by the AMA programme. It records no
approval by the owner, Legal, Compliance, the DPO or any control owner, and
it does not decide which duties apply to Zava North Homes. It builds on
[ADR 0001](./0001-azure-architecture.md), [ADR 0002](./0002-pilot-readiness-architecture.md)
and the [regulatory literacy synthesis](../reference/research/ux/regulatory-literacy-for-journeys.md).

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

Compare against a non-AI baseline: deterministic rule cards with links to the
provision. If chat adds no measured value over that, ship the rule cards
alone.

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

* Chat only, no rule engine: weak on clocks and silent failure; rejected.
* Fine-tune a model on law: stale, uncitable, hard to roll back; rejected.
* Separate regulatory product: duplicates identity, audit and hosting; rejected
  for the exercise, but the law store has a clean boundary if one is wanted.

## Open items

* Named Legal, Compliance and DPO owners and their approval capacity are
  unknown company details.
* Which sources Zava is actually bound by (grant award, contracts, leases) is
  unverified and needs the real documents.
* Licensed PAS 2035 text and official sources for the gaps are not yet held.
* Cost of Azure AI Search and monitoring jobs is not estimated.
* Phase 2 commencement on 30 November 2026 is planned, not confirmed here.
* Whether staff want alerts at these steps needs validation with real users.
