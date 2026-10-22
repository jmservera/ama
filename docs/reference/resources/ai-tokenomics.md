---
title: AI Tokenomics (Total Cost of AI and Value Realised)
description: What the mentor clue on Tokenomics points to, the public Tokenomics Foundation framing, how it maps to the capstone rubric and the Zava Forward evidence, and what remains unmeasured
ms.date: 2026-10-22
ms.topic: reference
---

## Purpose

On 2026-10-22 a mentor mentioned Tokenomics during the mentor progress review.
The owner reported this as a clue about what the capstone panel will probe. The
mentor's exact words are not in the repository, so the link between the remark
and the sources below is an owner-reported inference, not a recorded finding.
Ask the mentor to confirm what they meant before the final deck is frozen.

This page records the retrieved external framing, maps it to the
[Capstone Assessment Guide](../method/ama-capstone-assessment-guide.md) and to
what Zava Forward can already show, and names the gaps. It is a resource
pointer with retrieved findings, not regulatory evidence, a company fact or a
validated benefit.

## Access and Retrieval

| Item | Detail |
| --- | --- |
| Public source | [Tokenomics Foundation](https://www.tokeneconomics.com/), pages on the definition, Total Cost of AI and projects; retrieved 2026-10-22 |
| Source status | Draft working-group output. The definition is labelled draft v0.5.2, dated 2026-09-01. The Foundation runs alongside the FinOps Foundation. Treat every item as an emerging practice, not an accepted standard |
| Internal pointer | A Microsoft internal slide deck, "FinOps for AI & Tokenomics on Microsoft" (Ali Mazaheri and Patrick Vangoedsenhoven, modified 2026-10-22), found through WorkIQ. Internal Microsoft material: paraphrase, do not quote or show it to a customer or panel |
| Not confirmed | That this deck, or any named speaker, is the source of the mentor's remark. A WorkIQ check found no evidence that the deck itself was presented on 2026-10-22, only a same-day team meeting that discussed AI spend, model selection and prompt return on investment |
| Foundation events | The site lists a Tokenomics event on 22 to 23 October 2026; the relationship to the mentor's remark is unknown |

## What Tokenomics Says (Public Framing)

Evidence class: community and practitioner framing, draft.

| Idea | Statement | Source |
| --- | --- | --- |
| Definition | AI Tokenomics is the discipline of converting energy and capital into AI capabilities and consuming that intelligence efficiently across the organisation to realise measurable business value | Definition page, draft v0.5.2 |
| Three questions | Production (energy and capital into capability), Consumption (using it well: model selection, routing, caching, forecasting, licences) and Value (what the output is worth: pricing, labour, revenue, business processes) | Home and definition pages |
| Total Cost of AI (TCA) | Tokens are not the AI bill. TCA adds energy, capital, platform, software, licensing, labour and process change. The Foundation's host claims token and API cost is 10 to 25 percent of total AI spend and cites one enterprise audit at about 25 percent | Episode 17, 2026-09-07. An assertion from one podcast and one audit, not a benchmark |
| Unit economics | TCA divided by realised, finance-defensible value delivered above a quality floor | Episode 17 |
| Value destinations | A booked value claim needs one of five destinations: new revenue won, revenue retained, spend removed, spend avoided or capital freed | Episode 17 |
| Labour claims | Split into capacity gain, augmentation and automation, each with its own baseline | Episode 17 |
| Big-T notation | Big-O for AI consumption: T(1) cache or precompute, T(log n) filter before inference, T(n) one call per request, T(n.k) k hidden calls per request, T(n.k.a) agent depth multiplies calls, T(infinity) loops with no termination. Remedies: cache, filter, trim, bound depth, add budgets, hard termination | Projects page, release due December 2026 |
| Seven-layer stack | What AI costs is decided in the lower layers; how much is spent is decided in the upper ones | Projects page |
| Gateway and routing | A gateway holds policy, observability and failover; routing is one decision inside it | Episode 17 |

The internal Microsoft deck, paraphrased, adds three practical points. First,
choose the denominator deliberately: cost per token suits infrastructure, cost
per agent run suits workflows and cost per business outcome is the finance
metric. Second, time saved is not value until it is booked somewhere. Third,
change one lever (routing, caching, context), measure again and keep or revert,
so that cost per acceptable outcome improves, not only the average token price.
Also treat gateway token limits as operational guardrails and billing records as
the financial source of truth.

## Why It Matters for the Capstone

The rubric already asks for this, in different words.

| Criterion | Descriptor that Tokenomics answers | Current position |
| --- | --- | --- |
| A5 Operations | "cost modelled per unit of business value" for the top band; "cost or performance evidenced, but not both" below it | [ADR 0001](../../adrs/0001-azure-architecture.md) states cost per unit of business value "cannot be stated until a deployment produces measured usage" and calls this an explicit gap. This is the clearest named gap |
| A6 AI solution design | Model choice justified against alternatives "on cost, latency and quality" | Offline evaluation harness and a smallest-model rule exist (#108). Cost per accepted proposal is not reported |
| B7 Evidence | "Bring numbers. Cost per transaction, latency, evaluation scores, the value at stake. Assertions without evidence cap you at a 3" | Token counts exist for one operator exercise; no cost-per-transaction figure exists |
| C1 Business framing | Quantify the value at stake and the cost of inaction | [BRD](../../brds/agentic-retrofit-programme-brd.md) value claims remain hypotheses; AI running cost is not in the investment case |
| C3 Intellectual honesty | Surface risk unprompted; say "I don't know" credibly | Stating the gap before the panel asks is the scored behaviour |

## What Zava Forward Can Already Show

Evidence class: repository observation, not a benchmark.

* Every model call returns a validated usage envelope of prompt, completion and
  total tokens, kept with the append-only ledger event
  ([core `ai.py`](../../../src/core/src/zava_forward/core/ai.py) and
  [assistants](../../../src/core/src/zava_forward/core/assistants.py)).
* Operator-authorised exercises carry finite call, token, budget and expiry
  limits, and proactive generation is off by default
  ([ADR 0002](../../adrs/0002-pilot-readiness-architecture.md)). In Big-T terms
  the design already bounds k (calls per request) and a (agent depth) and
  forbids unbounded loops.
* One renewed QA exercise ran five assistant tasks on Azure OpenAI
  `gpt-4.1-mini-2025-04-14` using 6,884 tokens in five attempts, an arithmetic
  mean of about 1,377 tokens per proposal. This is a five-sample operational
  check with no human acceptance, so it is not a throughput, quality or cost
  estimate.
* ADR 0001 names the Azure cost drivers and a monthly budget alert at 80 percent
  actual and 100 percent forecast, and records the Foundry tokens-per-minute
  throttle that degrades a task to workflow-only.
* The BRD already treats time saved as capacity and not cash unless a budget
  owner confirms spend will fall (RULE-016, RULE-019), which matches the
  Tokenomics "booked value" test.

## Gaps

| Gap | Why it matters | Where it is tracked |
| --- | --- | --- |
| No price table, so no money figure per token | A cost per accepted proposal needs the regional price for the deployed model on a recorded date. None is stored, and none is invented here | BRD OD-51; NFR-012 |
| No denominator defined | Cost per token, per assistant run, per accepted proposal and per accepted handover answer different questions | BRD OD-51; FR-052 |
| TCA components not enumerated for Zava Forward | The investment case lists technology cost lines but not as a Total Cost of AI with a token share | BRD FR-025, RULE-016, NFR-012 |
| No quality floor in cost reporting | A cheaper model that raises critical misses is not cheaper | BRD NFR-012; backlog #108 |
| Review effort is the largest hidden cost | Human review, correction and re-review are likely larger than tokens, which the existing comparative-effort design already measures | BRD RULE-019; PRD effort comparison |
| Chat is a consumption driver | Per-user threads and memory multiply calls per request | Backlog #157 and #159 |

## Backlog

Created #432 (metering, limits and cost per accepted outcome) under epic #104.
Added Tokenomics delta sections with unticked criteria to #100, #104, #107,
#108, #126, #144, #146, #157, #159, #214, #225 and #226 on 2026-10-22. No
existing criterion was changed or ticked.

## Pitch Use

See the [Tokenomics pitch brief](../../capstone/pitch/tokenomics-pitch-brief.md)
for the slide option, speaker notes, executive questions and the claims that
must stay out of the pitch.

## Review Triggers

* Tokenomics definition moves beyond draft v0.5.2, or the Big-T notation
  release (December 2026) changes the notation.
* The mentor clarifies what they meant.
* A deployed run produces a measured token total tied to accepted outcomes.
* A regional price for the deployed model is retrieved and dated.
