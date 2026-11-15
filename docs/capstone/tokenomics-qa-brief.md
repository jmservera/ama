---
title: Tokenomics Q&A Brief for the Capstone Presenter
description: Concise presenter answer separating the labelled USD 0.44 per home planning scenario, the live consumption ledger and the authorised held-out measurement batch; supports #435 AC1 without a deck change
author: AMA programme
ms.date: 2026-11-13
ms.topic: how-to
---

## Status

Presenter aid for [#435](https://github.com/jmservera/ama/issues/435) criterion 1.
It adds no measurement, rehearsal, deck rebuild or acceptance. Owner decision of
2026-11-13: Slide 22 (S18) keeps Tokenomics brief on the main route, B25 and B27
are the prepared Q&A cards, and a held-out batch of up to USD 5.00 is
authorised. That batch has not run. The module named in the decision,
`zava_forward.agents.heldout_batch`, is implemented on main (merged in #1525
and #1531) but not yet run live; it awaits owner-authorised live provider
execution.

## Where to Point

| Moment | Page | Use |
| --- | --- | --- |
| Pitch, 50 s slot | 22 (S18) | Say the labelled planning scenario and the gap; do not expand |
| Cost or runaway-bill question | 53 (B25) | Workings, accepted-outcome method, controls and limits |
| Hidden calls or agent sprawl question | 55 (B27) | One selected skill, one bounded call, admission limits |

Pages are in the [question bank](./pitch/questions-and-answers.md) and the
[speaker script](./pitch/speaker-script.md). Return to the interrupted page
deliberately; native buttons use fixed jumps. The S18 notes cite B25 and B27
as slides 52 and 54 (earlier numbering); use pages 53 and 55. S18 says controls
"remain proposed"; B27 corrects that to source-coded but not live-proved, so
prefer the B27 wording if asked.

## 30-Second Answer

"There is no verified cost per outcome yet. Three things are different. First, a
labelled planning scenario: about USD 0.44 per home for inference only. Second,
the live consumption ledger records usage, and cost stays Unknown until it is
settled and approved. Third, a held-out measurement, capped at USD 5.00, is
authorised but not run. Until it runs and Finance reconciles billing, I will not
claim a price, a saving or a payback."

## Three Things Not to Mix

| Item | What it is | What it is not |
| --- | --- | --- |
| Planning scenario | Labelled estimate: 6,884 historical tokens over five runs is 1,376.8 per run; assumed 10 times that per task (13,768) and 20 tasks per home (275,360 tokens) at an assumed USD 1.60 per million tokens (GPT-4.1-mini output-rate, secondary source dated 2026-10-23) gives USD 0.440576 per home and USD 6,872.9856 across 15,600 modelled homes. Doubling the workload gives USD 0.881152 per home | A verified deployment price, a measured workload, an accepted-outcome cost or the full project cost |
| Live consumption ledger | Records calls and tokens in the core ledger; price, cost and liability are `Unknown` until the spend is settled and approved by Finance | A billing reconciliation, a currency cap on finite token allowances or evidence of saving |
| Held-out measurement runner | Owner-authorised finite batch, at most USD 5.00, to measure tokens per proposal on held-out cases; implemented on main (`zava_forward.agents.heldout_batch`), not yet run live; awaiting owner-authorised live provider execution | A result: it has not run live, and a bounded test would not prove savings or permission |

## If Pressed

* Accepted-outcome cost is total attributable cost divided by human-accepted proposals above an agreed quality floor. A zero or unknown denominator means not measurable (B25).
* Finite calls, tokens and expiry are not money caps and budget alerts are not hard stops. Task, period and call-depth limits exist in source; live activation and billing reconciliation are unproved (B25, B27).
* Value counts only when Finance confirms where the spend falls.

## Do Not Say

* Any price, saving or payback as fact, or USD 0.44 as the cost of the project.
* That the held-out batch has run, passed or reconciled to an invoice.
* That Tokenomics has been rehearsed or timed; no rehearsal is recorded.

## Sources

* [Slide manifest](./source/slides.json), Slide 22 notes and workings
* [B25 and B27 answers](./pitch/questions-and-answers.md)
* [Placement draft and decisions](./pitch/tokenomics-placement-draft.md)
* [Core consumption ledger](../../src/core/README.md) and [API consumption report](../../src/api/README.md)
