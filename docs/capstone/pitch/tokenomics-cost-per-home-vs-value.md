---
title: Cost per home versus value, evidence for the Tokenomics pitch answer
description: Cited table of what the repository can and cannot say about AI token cost per home against secured funding and time saved, with Unknown wherever no price or outcome source exists; supports #435
author: AMA programme
ms.date: 2026-11-26
ms.topic: how-to
---

## Status

Presenter evidence for [#435](https://github.com/jmservera/ama/issues/435), the mentor's request to show how the solution cost was calculated. The mentor pointed to [Tokenomics](https://en.wikipedia.org/wiki/Tokenomics); the mentor's exact meaning is unconfirmed, so this page offers a method and its gaps, not a verdict. It uses only existing repository evidence on the synthetic demo. It adds no measurement, price, saving or payback. Evidence labels: measured held-out batch, labelled planning scenario, modelled conditional grant, pilot target, Unknown.

## Unit

Tokenomics here means cost per accepted outcome above a quality floor, with the numerator counting every attributable cost and the denominator counting only human-accepted work ([B25 in the question bank](./questions-and-answers.md), [Q&A brief](../tokenomics-qa-brief.md)). The pitch also needs a per-home view, because funding and effort are per home.

## Cost per home

| Item | Figure | Label | Source |
| --- | --- | --- | --- |
| Measured tokens per proposal | 210.17 mean (min 180, p50 214.5, max 225); 2,522 tokens over 12 synthetic proposals | Measured held-out batch, usage only | [#432 note](../../reference/research/ai-heldout-batch-432-live-2026-11-18.md) |
| Measured cost of that batch | USD 0.000744 in total, about USD 0.000062 per proposal, at list price (input 0.10, output 0.40 per 1M tokens, Azure Retail Prices API, retrieved 2026-11-18) | Measured tokens at a dated list price; not a billing record | same note |
| Measured cost per home | Unknown | The batch unit is a proposal; no proposals-per-home count is measured | none |
| Planning cost per home | USD 0.440576 (275,360 tokens at an assumed USD 1.60 per 1M); USD 6,872.9856 for 15,600 modelled homes; USD 0.881152 per home if the workload doubles | Labelled planning scenario; inference only; rate is a secondary source dated 2026-10-23 | [Q&A brief](../tokenomics-qa-brief.md), S18 in [slides.json](../source/slides.json) |
| Settled cost per home from the ledger | Unknown | The ledger records calls and tokens; price, cost and liability stay Unknown until settled and approved; no settled export exists | [ai_consumption.py](../../../src/core/src/zava_forward/core/ai_consumption.py), [Q&A brief](../tokenomics-qa-brief.md) |
| Full project cost per home (hosting, review, correction, assurance, support) | Unknown | Not priced | [AI cost evidence](../history/cowork-main-presentation/evidence/ai-cost-evidence.md) |

The measured and planning figures do not agree, and they should not be reconciled. The scenario assumes 13,768 tokens per task; the batch measured 210.17 tokens per proposal on a different model (`gpt-4.1-nano`) with short synthetic prompts. Neither extrapolates to the other.

## Value per home

| Item | Figure | Label | Source |
| --- | --- | --- | --- |
| Secured funding | Unknown (none evidenced) | No award, allocation or claim exists in the demo data | S05, B09 in [slides.json](../source/slides.json) |
| Conditional grant potential | GBP 3,041 per home; GBP 47,439,600 over 15,600 homes (50 percent of the GBP 6,082 national housing association average, capped at GBP 7,500) | Modelled; assumes every home and full cost is eligible, with allocation, award and successful claims | S05, S10, B09 in [slides.json](../source/slides.json) |
| Time saved | Unknown | Time capture is built but off; no measured effort exists. The pilot target of 25 percent fewer coordination hours per home is a target, not a result | [timecapture.py](../../../src/api/src/zava_forward/api/timecapture.py), S20 in [slides.json](../source/slides.json) |
| Value of time saved in money | Unknown | Released time is capacity, not cash, until Finance books where it falls | [ai-tokenomics.md](../../reference/resources/ai-tokenomics.md) |
| Accepted proposals | Unknown (zero counted) | The batch has no acceptance step | [#432 note](../../reference/research/ai-heldout-batch-432-live-2026-11-18.md) |

## Reading cost against value

| Per home | Cost | Value | Ratio |
| --- | --- | --- | --- |
| Funding | USD 0.440576 planning scenario (inference only) | GBP 3,041 modelled, conditional | Unknown: no approved dated exchange rate, and the grant is not secured |
| Time | Unknown | Unknown | Unknown |

The honest reading is that the inference scenario is small beside the modelled grant, but both are assumptions, they sit in different currencies, and the cost excludes everything except inference. No saving, payback or return can be stated.

## What to say

"The cost per home is a planning scenario of about 44 US cents for inference only. The real measure is cost per accepted outcome, and for that we have a measured token batch on 12 synthetic proposals, but no price settled by Finance, no accepted-outcome count and no measured time saved. Where we have no source, we say Unknown."

## What not to say

* USD 0.44 as the cost of the project, or as a measured cost.
* The conditional grant as secured funding, or any cost-to-grant ratio.
* Any time or money saving, payback or return.
* That the batch figure scales to a home.

## What would close the gaps

Settled provider cost for a defined period, a count of human-accepted proposals above an agreed quality floor, a proposals-per-home count, measured effort from time capture, a Finance-approved exchange rate and the mentor's confirmation of what they expect (a figure or a method). Each needs an owner decision or outside input; none can be produced from the repository.
