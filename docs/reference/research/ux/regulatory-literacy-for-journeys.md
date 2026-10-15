---
title: Regulatory literacy for journey users and agents
description: What each journey role should know about current law and regulation, and how agents can surface it so people make safe decisions when in doubt
ms.date: 2026-10-15
ms.topic: reference
status: Research synthesis and design proposal; not legal advice, validated user need or approved requirement
---

## Main finding

Users do not need to know the law. They need to recognise when a situation
may carry a legal duty, know who owns the interpretation, and act safely
while waiting. Agents should therefore carry a small, dated regulatory
knowledge layer and use it to prompt, cite and route. They must not decide
that a duty is satisfied, interpret law or activate a rule.

This is a sector-informed proposal built from the
[Customer Journey Atlas](./customer-journeys/customer-journey-atlas.md) and the
[regulatory register](../../regulatory/README.md). Which duties apply to
Zava North Homes, and its delegations, are unknown company details.

## Knowledge levels

| Level | Meaning | Who |
| --- | --- | --- |
| Recognise | Spot a trigger and use the human route immediately | Everyone who hears a report or handles resident data |
| Apply | Follow an approved procedure and clock without interpreting | Repairs, housing officers, schedulers, preparers |
| Interpret | Decide what a provision requires for a case | Named Legal, Compliance, DPO, Building Safety and funding owners only |

Awareness is the right target for most roles. Interpretation stays with
named owners under the register's authority hierarchy.

## Needs by journey role

Dated status is from the local snapshots (retrieved 2026-09-19; register
2026-09-25). Check the official source before a consequential use.

| Journey role | Know at least | Source and status | Doubt trigger and human owner |
| --- | --- | --- | --- |
| Repairs and hazard intake, contact centre, housing officers | A damp, mould or emergency hazard report starts statutory clocks on awareness; Phase 1 in force since 27 Oct 2025. Do not delay human intake. Phase 2 hazards planned from 30 Nov 2026 | [Awaab's Law regulations 2025](../../regulatory/social-housing-regulation/awaabs-law-hazards-in-social-housing-regulations-2025.md), [Phase 1](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md) and [Phase 2](../../regulatory/social-housing-regulation/awaabs-law-phase-2-guidance-2026.md) guidance (guidance is non-statutory) | Any possible hazard, vulnerability or unclear awareness date goes to the safety/repairs owner |
| Building Safety lead | Safety and Quality Standard (from 1 Apr 2024) and Awaab's Law timeframes; completion is not assurance | [Standard](../../regulatory/social-housing-regulation/social-housing-safety-and-quality-standard-2024.md), [Act 2023](../../regulatory/social-housing-regulation/social-housing-regulation-act-2023.md) | Owns hazard categorisation and holds |
| Surveyor, designer, coordinator, QA inspector | PAS 2035 roles, risk path and independent evidence. Only an overview is held locally; the licensed standard and contract incorporation are unverified | [PAS 2035 overview](../../regulatory/retrofit-standards-and-funding/pas-2035-2023-bsi-overview.md) | Appointed retrofit coordinator and Compliance |
| Programme, Assets, Finance, grant preparer | Target direction: EPC C by 1 Apr 2030 under the 2026 government response (policy, commencement of duty unresolved); grant terms come from the award letter, not the allocation annex | [Government response](../../regulatory/energy-efficiency/social-rented-sector-mees-government-response-2026.md), [Warm Homes annex](../../regulatory/retrofit-standards-and-funding/warm-homes-social-housing-fund-technical-annex-2025.md) | Funding owner and Finance approver; no claim without the actual grant agreement |
| Everyone handling resident data | Purpose limits, special-category data (health, vulnerability), consent versus other lawful bases, and that significant decisions need meaningful human involvement (UK GDPR Art. 22A-22C as currently consolidated) | [UK GDPR current text](../../regulatory/data-protection/uk-gdpr-current-text.md), [DPA 2018](../../regulatory/data-protection/data-protection-act-2018.md) | DPO adviser |
| Leasehold-service staff | Lease terms decide responsibility; no local lease or landlord-tenant statute is held in the knowledge base | Gap: no source held | Legal review before any explanation |
| Residents and representatives | Plain explanation of their choices, complaint and redress routes, and safe contact; not legal duties | Same sources, rendered in plain language | Resident-facing owner, human-reviewed |
| Suppliers, installers | Contract and scheme requirements, not statute | Gap: contract and TrustMark terms not held | Contracts manager |

## Integration design for agents

The MVP already restricts the five assistants to proposal-only output with
captured source IDs and mandatory citations
(`mvp/zavaforward_mvp/assistants.py`). A regulatory layer fits the same
pattern.

1. A regulatory source register as data: ID, authority type, status
   (in force, guidance, consultation, historical), effective, retrieval and
   review dates, content hash, change likelihood, owner. This is the
   register already described in the regulatory README.
2. Approved rule cards, not raw law. Each card has a trigger, the cited
   provision, the clock, the safe default action, the escalation owner,
   approver, effective date and version. Only cards approved by the named
   owner are active; candidate changes stay in review.
3. Deterministic clocks and holds in the service. An agent may flag that a
   report may start a clock. The service owns the awareness timestamp and
   deadlines; a model result never sets, screens out or rewrites them.
4. A cited "doubt" output. Every regulatory answer returns source,
   provision, status, retrieval and effective dates, then states the
   uncertainty and routes to the named owner. Agents refuse to turn missing
   evidence into compliance or an announcement into commenced law.
5. Currency gate. If the cited source is past its monitoring cadence, the
   answer is labelled possibly stale and the owner check is prompted.
6. Role-shaped presentation. Recognise-level roles see a short prompt with
   an action; interpret-level owners see the provisions and diffs.
7. Change path: detect, preserve, classify, route to owner, approve, test,
   activate on effective date, notify. Detection never overwrites an
   approved rule; an authorised owner can place a hold.

## When in doubt: expected agent behaviour

| Situation | Agent does | Agent does not |
| --- | --- | --- |
| Possible hazard in a resident message | Points to the human emergency or hazard route first, shows the cited trigger, drafts a case note for the owner | Decide it is not significant, delay intake or send resident messages |
| Question about a duty or deadline | Quotes cited provision with status and dates, says what is unknown | Say the duty is met or give legal advice |
| Rule differs between sources or is historical | Shows both, flags the conflict, escalates | Pick the latest-looking source |
| Planned law (Phase 2 or 3, MEES) | Marks it future, with the date and status | Apply it as active |
| Automated recommendation affecting a resident | Requires a named human decision with reasons | Make a significant decision solely by automation |
| Lease, grant or contract term needed | Lists the missing document and holds the decision | Infer terms from archetypes |

## Gaps and risks

* Awaab's Law Phase 2 hazards guidance is only introductory in the local
  copy and its commencement is unresolved (register: high change).
* No local source for leasehold, building safety beyond the standard,
  consumer-standard detail, complaints handling or TrustMark rules.
* The local PAS 2035 item is an overview; the licensed text is unread.
* Rule cards need owner approval Zava does not yet have; the exercise uses
  synthetic fixtures, and fictional elapsed-hour fixtures are not statutory
  periods.
* Over-reliance: prompts can create false comfort. Measure whether users
  escalate correctly, and test with real staff before any claim of benefit.
* Cost and timing of monitoring are unknown.

## Suggested next steps

1. Owner decision on whether the first build adds a read-only rule-card and
   citation capability to the existing assistants.
2. Draft rule cards for Awaab's Law Phase 1 and UK GDPR Art. 22 as
   proposals for named human review.
3. Add retrieval of the official sources for the gaps above, as dated
   snapshots in the regulatory folder.
4. Validate the "recognise" prompts with repairs, housing and resident
   engagement staff.
