---
title: Capstone Rubric Review of the Agentic Retrofit Programme BRD
description: Evidence-based readiness assessment of the Proper Warm BRD against the FY27 AMA capstone criteria
ms.date: 2026-09-30
ms.topic: reference
---

## Review Scope

This review assesses the
[Agentic Retrofit Programme BRD](../../../brds/agentic-retrofit-programme-brd.md)
against the complete
[Capstone Assessment Guide](../../method/ama-capstone-assessment-guide.md).
It records what the BRD can evidence today and what still requires a working
implementation, measured operation, live presentation or dissemination.

The scores are a readiness estimate, not a prediction of the panel result.
Sections A to C are scored live by the panel. A document cannot prove demo
performance, Q&A behaviour, delivery craft or working implementation.

## Readiness Result

| Section | Provisional score | Floor | Readiness |
| --- | ---: | ---: | --- |
| A. Technical Excellence | 21/35 | 21/35 | Section floor reached, but A4 scores 1 |
| B. Communication and Executive Presence | 19/35 | 21/35 | Section floor not reached |
| C. Consultative and Stakeholder Skills | 12/15 | 9/15 | Section floor reached |
| D. Thought Leadership Artifact | 9/15 | 9/15 | Section floor reached, but D3 scores 1 |
| Total | 61/100 | 66/100 pass threshold | Not Yet Met |

The floor check fails before the total is considered:

* Section B is below 60%.
* A4, B3, B5 and D3 are scored 1 on current evidence.
* The rubric does not permit a total score to offset an individual score of 1.
* A thought leadership submission and dissemination route are not yet
  evidenced by the BRD.

## Criterion Review

| Criterion | Score | Evidence in the BRD | Gap to excellent |
| --- | ---: | --- | --- |
| A1. Architecture, modularity and scalability | 4 | Clear separation of deterministic controls, bounded agent capabilities, authoritative systems, human authorities and tranche gates | Add a documented component and data-flow architecture, interface contracts, scaling limits and explicit failure domains |
| A2. Trade-off reasoning and design patterns | 5 | The BRD challenges the original five-agent request, evaluates non-agent alternatives and records speed, safety, breadth, standardisation, supplier and lock-in trade-offs | Preserve the rejected options and make them visible in the live architecture argument |
| A3. Security, compliance and responsible AI | 4 | Strong legal, data-protection, authority, provenance, fail-closed and human-review controls | Add a stated threat model covering identity, isolation, prompt injection, malicious evidence, grounding failure, leakage and cross-agent trust boundaries |
| A4. Implementation completeness | 1 | The BRD defines an end-to-end target and acceptance criteria but provides no working implementation evidence | Build all core demonstration paths end to end and disclose any non-working or simulated boundary |
| A5. Operations, observability, reliability, performance and cost | 2 | Reliability, continuity, audit, cost treatment and measures are specified as requirements | Produce structured logs, metrics and traces; set and measure latency, reliability and recovery targets; report cost per demonstrated journey and per accepted handover |
| A6. AI solution design and evaluation | 3 | Comparison 2 defines accuracy, review effort, error severity, unsupported claims, explanation fidelity and automation-bias measures | Justify model and non-model choices against cost, latency and quality; implement a repeatable evaluation harness with documented failure modes |
| A7. Agentic autonomy and orchestration | 2 | Boundaries, handoffs, state, escalation and human authority are well defined | Demonstrate meaningful bounded autonomy, deliberate state-graph or handoff patterns, tool selection, retry or reflection, and safe stop behaviour |
| B1. Narrative structure and argument | 4 | The BRD connects problem, evidence, options, recommendation, controls and value | Use the Board narrative as the live argument and remove detail that does not advance the decision |
| B2. Audience calibration and register | 3 | Executive and technical material are both present | Separate the Board story from the requirement detail and rehearse deliberate movement between business and architecture registers |
| B3. Demo and executive hook | 1 | The document names a value-bearing end-to-end demonstration but contains no proven two-minute demo | Script and rehearse an outcome-led demo that lands the user and business value in under two minutes, with a tested recovery path |
| B4. Q&A composure and depth | 2 | The open decisions, caveats and evidence classifications provide strong preparation material | Create an executive challenge bank and practise concise answers that distinguish facts, assumptions, unknowns and verification steps |
| B5. Delivery craft, pace, presence and time discipline | 1 | No timed delivery evidence can be inferred from the BRD | Rehearse the 15-minute session, protect the recommendation and leave time for questions |
| B6. Written communication, deck and documentation | 4 | The BRD is extensive, navigable, traceable and explicit about uncertainty | Reduce duplication, add a navigable architecture pack and ensure each presentation slide carries one decision-relevant idea |
| B7. Use of evidence and data storytelling | 4 | The BRD uses quantified scenarios, sensitivities, baselines and evidence classifications without presenting them as company facts | Turn the key numbers into decision visuals and add measured demo results rather than relying on planning scenarios |
| C1. Discovery and business framing | 5 | Stakeholders, constraints, value hypotheses, cost of inaction, discovery questions and success measures are explicit | Replace sector assumptions with real engagement evidence as it becomes available |
| C2. Active listening and disagreement navigation | 2 | The BRD accurately records competing perspectives, but live behaviour cannot be assessed | Rehearse restating challenges before answering, conceding valid points and adapting the recommendation without abandoning controls |
| C3. Influence and intellectual honesty | 5 | The BRD makes a clear recommendation, rejects premature autonomy and surfaces material unknowns and downside risk unprompted | Keep the same candour in the live pitch and avoid allowing the demo to imply validated business outcomes |
| D1. Substance and originality | 4 | The synthesis of retrofit delivery, resident authority, professional controls, agent boundaries and evaluation is substantial and reusable | Add real user and sponsor engagement evidence so the artifact is not grounded mainly in sector research and modelled role perspectives |
| D2. Craft and publish-readiness | 4 | The BRD is structured, sourced and traceable | Edit a standalone 2,000-word architecture guidance artifact that another architect can use without navigating the full BRD |
| D3. Dissemination and reach | 1 | No publication, filing, delivery or approval path beyond the cohort is recorded | Choose an audience and channel, submit or schedule the artifact, and preserve proof of dissemination |

## Priority Remediation Plan

### Gate 1: Build evidence

Build a complete non-production demonstrator using synthetic or approved
de-identified cases. It must exercise the shared property record, lifecycle
state, deterministic gates, bounded agents, human approvals, exception routing,
audit trail and portfolio view.

The demonstration should include:

* at least one successful journey and representative safety, consent,
  eligibility, missing-evidence and integration-failure paths;
* explicit component contracts and a state model;
* one genuinely autonomous but bounded agent path that can select approved
  tools, evaluate evidence, update working state and pause or hand off;
* model, prompt, rule and evidence versions attached to every AI output; and
* disclosed simulations and known gaps.

This evidence targets A1, A4 and A7.

### Gate 2: Operate and evaluate

Instrument the demonstrator with correlated logs, metrics and traces. Define
targets for response time, task completion, recovery, quality and cost. Measure
model and workflow alternatives through the existing Comparison 2 design.

The evaluation pack should show:

* model and non-model choices by quality, latency and cost;
* test datasets and expected outcomes;
* error severity, unsupported claims, missed critical exceptions and human
  review time;
* prompt-injection, malicious-document, leakage and grounding tests;
* failure recovery and manual-continuity evidence; and
* cost per completed demonstration journey and projected cost per accepted
  handover, with assumptions separated from measured values.

This evidence targets A3, A5 and A6.

### Gate 3: Land the argument

Use the BRD's Board Decision Narrative as the spine of the 15-minute session:

1. customer and mission;
2. delivery-control problem and stakes;
3. alternatives considered;
4. bounded recommendation;
5. two-minute outcome demo;
6. measured evidence, risks and economics; and
7. the decision requested.

Prepare a prerecorded recovery path or equivalent deterministic fallback for
the demo. Build a challenge bank for CEO, CIO and CFO questions and rehearse
inside the time limit.

This evidence targets B1 to B7 and C2.

### Gate 4: Publish the reusable learning

Extract a standalone architecture guidance artifact from the BRD. A suitable
working topic is: "Designing bounded agents for regulated property retrofit:
separating deterministic controls, professional authority and agentic work."
Identify the intended audience and publication channel before drafting, then
submit, schedule or deliver it with evidence of reach.

This evidence targets D1 to D3.

## Decision

The BRD is a strong design and governance foundation, but it is not yet a
capstone-ready submission. The immediate priority is not more requirements
detail. It is working, observable and evaluated implementation evidence,
followed by a concise executive argument and a real dissemination path.
