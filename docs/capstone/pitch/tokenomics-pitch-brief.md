---
title: Tokenomics Pitch Brief for the Capstone Presentation
description: "How to carry AI Tokenomics into the 15-minute capstone pitch - placement options, draft slide copy and notes, evidence to bring, executive questions and claims to keep out"
author: AMA programme
ms.date: 2026-10-22
ms.topic: reference
---

## Status

This is a proposal for the owner, not a change to the deck. The
[24-slide council deck](../deck/zava-forward-executive-draft.pptx) is
unchanged, its 795-second main route has not been rehearsed against this
material, and the owner has not decided where Tokenomics sits. The
[AI Tokenomics resource note](../../reference/resources/ai-tokenomics.md) holds
the sources and the evidence labels used here. Confirm with the mentor what
they meant before freezing the slide.

## The Argument in One Line

I do not count tokens. I count what each accepted proposal costs, above a
quality floor, and I can show how the design bounds that cost. Today I can state
the method and the measured gap, not a price.

Say the gap yourself. The assessment guide rewards surfacing risk unprompted
(C3) and caps unevidenced claims at 3 on B7, so a stated gap with a plan scores
better than an invented figure.

## Why the Panel Will Care

| Criterion | What the panel looks for | What Tokenomics lets you show | Gap today |
| --- | --- | --- | --- |
| A5 Operations | Cost modelled per unit of business value | Finite allowances and partial token capture exist; method for cost per accepted proposal | No price source, no denominator, no accepted-outcome volume |
| A6 AI design | Model choice justified on cost, latency and quality | Smallest-model-that-meets-thresholds rule (#108) | Cost per accepted proposal not reported |
| B7 Evidence | Numbers the audience can act on | Token counts from the operator exercise, limits, call bounds | No cost-per-transaction figure |
| C1 Business framing | Value at stake and cost of inaction | Value claims separated from capacity and cash | AI running cost absent from the investment case |
| C3 Honesty | Risk surfaced unprompted; credible "I don't know" | The stated unmeasured items below | Needs rehearsal |

This table is a preparation aid, not a score. Apply the full
[Capstone Assessment Guide](../../reference/method/ama-capstone-assessment-guide.md),
including section and individual floors, to the final deck before treating it
as ready.

## Placement Options

| Option | Change | Time effect | Risk |
| --- | --- | --- | --- |
| A (recommended) | Strengthen slide 16 ("Prove the programme. Test the AI separately.") with the cost-per-accepted-proposal line, add one Q&A card to slide 20 and one optional appendix slide (draft copy below) | About 20 seconds on slide 16; recover from slide 14 or 17 | Smallest structural change; keeps the argument inside the existing value test |
| B | New main-route slide after slide 16 | About 45 seconds; recover from two slides | Splits the story and adds a slide to a dense route |
| C | Spoken only, in the 75-second question window | None | Weakest on B6 (slides stand alone) and B7 |

Adding or reordering main-route slides is a structural change that needs the
owner's decision. Slide 14 already says that five calls and token limits "do not
establish a currency cap or cost per accepted home", so option A extends an
existing honest statement instead of adding a new claim.

## Draft Slide Copy (Appendix or Slide 16 Insert)

Title (54 characters): Count outcomes, not tokens: cost per accepted proposal

| Block | Draft copy |
| --- | --- |
| Peer 1 | Tokens are one line. Total Cost of AI adds hosting, human review, correction, assurance, support and exit. |
| Peer 2 | Meter and bound. Finite call and token allowances today; monetary, per-task and per-request bounds proposed; a stop means the workflow-only path. |
| Peer 3 | Report per outcome. Cost per accepted proposal beside critical misses, overrides and reopened cases. |
| Boundary line | Measured: 6,884 tokens over five operator runs. Not measured: price, cost per accepted home, value. |
| Evidence label | Observation and proposal; no price, saving or benefit claimed |

Draft speaker notes (about 110 words, first person):

"Before I ask you to endorse the next gate, here is how I treat AI cost. A
token invoice is one line of the cost of AI. Review, correction, hosting,
assurance and support usually cost more, so I report the total, per accepted
proposal, beside the quality it has to clear. The design already bounds it with
finite call and token allowances and expiry, no open-ended agent loop, and a
stop that sends the case to people. Those allowances are not a currency cap.
Monetary, per-task and per-request limits are proposed and not yet tested.
What I have not measured is the price or the cost per accepted home. One
operator exercise used 6,884 tokens across five runs; that is an observation,
not an estimate. The next gate measures it."

Keep within the slide's evidence label. Do not read the notes as a promise of
savings.

## Numbers to Bring

| Figure | Value | Evidence class and limit |
| --- | --- | --- |
| Operator exercise tokens | 6,884 over five runs, about 1,377 per proposal | Repository observation on `gpt-4.1-mini-2025-04-14`; five samples, no human acceptance; not a cost, throughput or quality estimate |
| Calls and tokens bounded | Finite call and token allowances and expiry per authority reference; proactive generation off | Repository design and operator authority (ADR 0002, agents README); not a currency guarantee, not independent task or period budgets, not a production budget |
| Exercise technology ceiling | USD 450 a month including USD 200 for inference and comparators | Historical owner-approved exercise ceiling (EXA-012), not a vendor quote; the recorded override for the #58 rebuild means it is not today's cap |
| Cost per accepted proposal | Unknown | No dated price source and no human-accepted outcome count; do not estimate on stage |
| Value above the quality floor | Unknown | Value claims remain hypotheses; 20% and 25% targets remain unratified (BRD OD-18) |

## Executive Questions

| Executive | Likely question | Answer stem | Evidence label |
| --- | --- | --- | --- |
| CFO | What does the AI cost per accepted home, and when does it pay back? | I do not have that number and I will not estimate one. The method is cost per accepted proposal beside the quality floor, reconciled to billing; value counts only when you confirm where the spend falls | Gap stated; BRD FR-052, OD-51 |
| CFO | Can the bill run away? | Today calls and tokens are finite per authority reference and expire, and an exhausted allowance stops that AI path; these are not a currency cap, and the budget alert is a notification, not a hard cap. Monetary, per-task and per-request limits are proposed and not yet tested | Design (ADR 0002, agents README, ADR 0001); proposal NFR-012, AC-109 (Not run) |
| CIO | Why not use the cheapest model, or cache everything? | Cheaper counts only if critical misses, unsupported claims and overrides do not worsen on the same held-out cases; a cache must prove one stored answer is valid for similar questions | Proposal; PRD AC-108 |
| CIO | What stops agent sprawl multiplying calls? | The orchestration is a deterministic state graph, not an agent loop, and calls are finite per authorisation; per-request call and depth bounds are proposed and tested by AC-109. Chat is the capability to watch because it multiplies calls per request | Design; PRD NFR-017, AC-109 (Not run) |
| CEO | Is the AI worth it? | Not claimed yet. Time saved is capacity until booked; the next gate produces the comparison against manual and rules-based routes | Value hypothesis; BRD RULE-016, RULE-019 |
| Panel | What is your cost per transaction? | Stated gap with the plan and the date it closes | A5, B7 |

## Claims to Keep Out

* Any price, saving, payback or "cost per home" figure.
* The 10 to 25 percent token share as fact. It is a Tokenomics Foundation host's
  claim from one audit and one podcast; if mentioned, attribute it and call it
  indicative.
* "Microsoft standard" or "industry standard" for Tokenomics. It is a draft
  community practice (definition v0.5.2).
* Any slide, quote or figure from the internal Microsoft deck found through
  WorkIQ.
* The word "savings" for released staff time.

## Actions Before the Pitch

* Ask the mentor to confirm what they meant by Tokenomics, and whether they
  expect a figure or a method.
* Owner decision: a finite, authorised measured batch on held-out cases to record
  tokens per proposal and the spread, with a dated regional price retrieved and
  stored. Spending needs the owner's explicit authority; none is assumed here.
* Decide the denominator and quality floor for the pitch (BRD OD-51).
* Choose placement (option A, B or C), then rebuild the deck through the
  `powerpoint` skill and re-run its validators; this brief does not.
* Rehearse the 20 seconds and the CFO answer aloud, then record timing and the
  rehearsal in this folder.
* Challenge the revised deck against the complete Capstone Assessment Guide.

## Evidence Boundary

Nothing in this brief is a score, an approved target or a rehearsed script. The
sources are public draft Tokenomics material retrieved on 2026-10-22, the BRD
v0.19.0 and PRD v0.18.0 proposals, ADR 0001 and ADR 0002, and repository
observations cited above.
