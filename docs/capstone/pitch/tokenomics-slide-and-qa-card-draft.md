---
title: DRAFT Tokenomics Slide and Q&A Card, AI Inside the Solution
description: Owner-directed draft (2026-11-04) of the Tokenomics slide copy, spoken text and CFO/CIO Q&A card, focused on right-sizing the AI used in the solution; every figure carries a source and evidence label
author: AMA programme
ms.date: 2026-11-04
ms.topic: how-to
---

## Status

DRAFT for owner review, written from existing repository evidence only. It is
not a deck change, a rehearsal, a price, an assessment or a measured result.
The deck is not rebuilt: the Linux working tree has no PowerShell, and the
[source guide](../source/README.md#ai-consumption-evidence-432) requires
approved wording to enter through `slides.json` and a regenerated deck, notes
and question bank, not hand-edited generated files.

Owner direction recorded 2026-11-04: the Tokenomics material covers AI used
in the solution, not AI used to build it. The point to make is that most agent
steps need to understand an input and return a concrete answer, not generate
text, so a typed decision model (or no model) can serve them at lower cost
than a generative model, provided the quality floor holds. That cost
advantage is a hypothesis to test here, not a finding.

Not used on purpose: the 2026-10-24 rubric-scorer model pilot (USD figures)
and any other AI-for-development spend. They describe building the work, not
the solution.

## The Idea in Plain Language

Each step an agent performs has one of three shapes. Pay for the cheapest
shape that clears the quality floor, and say plainly what is unmeasured.

| Step shape | Example in Zava Forward | Tool | Evidence label |
| --- | --- | --- | --- |
| Exact answer from fixed rules | Gates, holds, thresholds, arithmetic, ranking | Rules or a parser; no model call | Observed (historical prototype, PR #19), see figures below |
| Understand an input and pick a concrete answer | Choose a source-bound candidate, classify a document, flag whether evidence supports a claim | Typed decision model (Microsoft Decision 1, optional, under evaluation) | Vendor documentation plus one feasibility observation; benefit unproved |
| Write text a person will read | A cited handover draft or catch-up summary | Generative model (gpt-4.1-mini in the QA exercise) | Observation of five runs; no human acceptance |

The five original responsibilities (stock prioritisation, assessment drafting,
funding, coordination, quality verification) mix these shapes. Most of their
steps are the first two. This is a task-shape hypothesis from the
[model-fit research](../../ideas/typesafe-system-one-agent-fit.md), not a
measured split of calls.

## Figures, Sources and Labels

Every figure that may appear on the slide, in the notes or on the card.

| Figure | Value | Source (date) | Evidence label and limit |
| --- | --- | --- | --- |
| Workflow-only step latency | 0.03 ms | [Prototype learnings](../../reference/research/ux/prototype-learnings-and-simplicity-review.md), PR #19 (2026-10-08) | Observed, historical prototype. Not a production SLO. Do not compute a ratio: the outputs are not equivalent |
| Live generative agent step latency | 12.5 s median, 17.7 s p95 | Same source | Observed, historical prototype. Not a cost figure |
| Decision model output | Closed-set answer with option probabilities; no generated text or rationale | [Typed decision model research](../../ideas/typesafe-system-one-agent-fit.md), model catalog checked 2026-10-10 | Vendor documentation. Not housing evidence |
| Decision model feasibility | One real run selected a source-bound EPC candidate, status Not reviewed | Same document, PR #58 inspected 2026-10-11 | One observation. Held-out accuracy, abstention calibration and net benefit not shown |
| Decision model latency target | p95 at most 10 s warm; generative narrative at most 30 s | [PRD](../../prds/zava-forward-retrofit-programme-demonstrator.md) NFR-009 | Requirement. Not measured |
| Generative tokens in the QA exercise | 6,884 tokens over five runs; mean 1,376.8 per run | [AI Tokenomics note](../../reference/resources/ai-tokenomics.md), infra README record | Observation on `gpt-4.1-mini-2025-04-14`. No human acceptance, so not tokens per accepted proposal and not a cost |
| Price per call, cost per accepted proposal, saving, payback | Unknown | Same note; BRD OD-51, FR-052, NFR-012 | Stated gap. No dated price source, no accepted-outcome count, no authorised held-out batch. No figure is shown |
| Decision model price and speed | Not stated | Vendor announcement (October 2026) | Advertised, not a subscription quote. Keep out |

Kept out of every surface: the modelled USD 0.44 per home and USD 6,873
across 15,600 homes now on S18 and B25. That calculation multiplies one
five-run mean by assumed factors and prices it from a secondary mirror. It
conflicts with acceptance criterion 6 of #435 (no price claim) and with the
rule to show no figure while the gap is open. The owner decides whether S18
keeps it; see the
[placement draft](./tokenomics-placement-draft.md#flagged-tension-for-the-owner).

## Draft Slide (Replaces the S18 Body, Same 50-Second Slot)

Title (58 characters): Right-size the AI: most steps need an answer, not text

| Block | Draft copy |
| --- | --- |
| Lane 1 | Rules and parsers. Exact fields, arithmetic and gates. No model call. |
| Lane 2 | Decision model. Understand the input, return one answer from a closed list, with its probability. No text written. |
| Lane 3 | Generative model. Only where a person needs a cited draft. |
| Cost rule | Cheaper counts only if quality holds on the same held-out cases. |
| Boundary line | Measured: 6,884 tokens over five generative runs. Not measured: price, cost per accepted proposal, saving. |
| Safety line | No price, no call: the case goes to a person. |
| Evidence label | Hypothesis and observation; no price, saving or payback claimed |

Visual: three labelled lanes in reading order, each with a text label and an
icon, so the meaning does not rely on colour. Provide alt text that states the
three step shapes and the boundary line. Use the Fluent 2 tokens already in the
deck, a type size the deck already uses for body text, and plain language
(short sentences, no unexplained term). Spoken text and notes carry the same
claims as the slide, no more.

## Draft Spoken Text (About 20 Seconds Inside the S18 Slot)

"Most agent steps do not need a model to write anything. They need to
understand an input and give a concrete answer. So I use rules for exact
work, a decision model for closed choices, and a text model only when a person
needs a cited draft. Whether that is cheaper I have not measured: I have 6,884
tokens from five runs, no price and no accepted outcomes, so I show no cost
figure. The next gate measures it, and if there is no price, there is no call
and a person takes the case."

About 95 words, roughly 40 seconds spoken: it fits the 50-second S18 slot but
not the issue's 20-second target, which is about 50 words. Trim after
rehearsal. Nothing here is rehearsed or timed.

## Draft Q&A Card (Proposed B28, Appendix, Not on the Spoken Route)

Page and number are proposed; the owner decides whether this is a new card or
an edit to B25 or B26.

Question: Why not use one chat model for every agent step?

Answer first: Because most steps need an answer, not text. A cheaper tool is
only a saving if it clears the same quality floor, and I have not yet measured
that, so I claim no saving.

Strongest evidence and its limit:

* A decision model returns one choice from a supplied list with option
  probabilities and writes no text. Source: model catalog, checked
  2026-10-10 (vendor documentation, not housing evidence).
* One real run selected a source-bound candidate for review. Source: PR #58,
  inspected 2026-10-11. One observation, not accuracy.
* Deterministic gates ran in 0.03 ms against a 12.5 s median for the live
  agent step. Source: PR #19, 2026-10-08. Historical prototype; outputs not
  equivalent, so no speedup claim.
* The test: same held-out cases, three arms (rules or manual, decision model
  with templates, generative), measuring critical misses, unsupported claims,
  overrides, reopened cases, review effort, latency and billing-led cost.
  Source: PRD AC-108 and the parallel experiment protocol. Proposed, Not run.

What the decision model must not do: it is not the sole decision-maker for a
consequential housing decision, it never suppresses or downgrades a hazard
flag, and it does not profile residents. Source: model catalog and
research table (2026-10-10). Processing region needs confirmation: a
GlobalStandard or DataZoneStandard deployment does not establish UK-only
processing.

If the model or price is unavailable: unknown price, an expired allowance or
an unreachable model stops that AI call and keeps the manual or rules route.
Hazard handling does not depend on the scorer. Source: #432 source-only
controls, constructed tests, not live acceptance.

Verdict if the test fails: keep the simpler tool and report the negative
finding. Lower price per call with more critical misses is a failure, not a
saving (PRD AC-108).

On-slide copy for the card (three lines):

* Match the tool to the step: rules, decision model, text model
* Cheaper counts only above the same quality floor
* No price means no call; a person takes the case

CFO follow-up (about 30 seconds): "I do not have a cost per accepted
proposal and I will not estimate one. The method is total attributable cost
divided by human-accepted proposals above the quality floor, reconciled to
billing. Time released is capacity until you confirm where the spend falls."

Classification line for the card: E19 AI Tokenomics note; E21 model-fit
research and PR #58 observation; PRD NFR-009, AC-108, FR-061; BRD OD-51.
Hypothesis and observation; no price, saving or payback.

## Acceptance Criteria Status for #435

| Criterion | Status after this draft |
| --- | --- |
| 1 Owner decides placement; deck rebuilt and revalidated | Unmet. The owner directed a slide and a card be drafted; the placement choice, source-manifest edit, rebuild and PowerPoint validation are not done |
| 2 Mentor confirms what Tokenomics meant and figure or method | Unmet. Needs the mentor |
| 3 Rehearsed inside the timed route; notes stored in the pitch folder | Unmet. Nothing performed or timed |
| 4 Owner decides on a finite measured token batch; spend authority recorded | Unmet. No spend authority is assumed. Until decided, the pitch states the gap and shows no figure |
| 5 Revised deck challenged against the complete assessment guide | Unmet. No revised deck exists. The draft is aimed at A5, A6, B7 and C3 (gap stated unprompted) but no judgement or floor is applied |
| 6 Every Tokenomics statement has a source and label, no price, saving or payback claim | Partly drafted. The new copy is labelled and claims no price. The existing S18 and B25 figure and the rest of the deck and notes are not audited or changed |

Nothing here changes resident consent, professional review, human approval or
Finance authority. AI is optional in every lane: the manual path remains.
