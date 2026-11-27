---
title: Tokenomics Q&A Brief for the Capstone Presenter
description: Presenter answer separating the full Azure planning envelope, protected AI budget proposal, historical inference scenario and measured synthetic usage
author: AMA programme
ms.date: 2026-11-27
ms.topic: how-to
---

## Status

Presenter aid for [#435](https://github.com/jmservera/ama/issues/435) criterion 1.
It adds no measurement, rehearsal or acceptance. Owner decision of
2026-11-13: Slide 22 (S18) keeps Tokenomics brief on the main route, B25 and B27
are the prepared Q&A cards, and a held-out batch of up to USD 5.00 is
authorised. That batch ran live on 2026-11-18 under #432 (12 synthetic
proposals, 2,522 tokens, USD 0.000744 at list price; usage only, no accepted
outcomes). The module named in the decision is
`zava_forward.agents.heldout_batch` (merged in #1525 and #1531).

## Where to Point

| Moment | Page | Use |
| --- | --- | --- |
| Pitch, 60 s slot | 56 (B28) | Full Azure planning envelope, scale-to-zero limits, allowances and retained measured-batch evidence |
| Pitch, 45 s slot | 55 (B27) | Protected recommendation/document pools, chat limits and theoretical AI bounds |
| Pitch, 35 s slot | 22 (S18) | Distinguish the older inference planning scenario from measured usage and full project cost |
| Cost or runaway-bill question | 53 (B25) | Workings, accepted-outcome method, controls and limits |
| Priority, hidden calls or agent sprawl question | 55 (B27) | Class/period budget proposal, bounded attempts and existing admission mechanisms |

Pages are in the [question bank](./pitch/questions-and-answers.md) and the
[speaker script](./pitch/speaker-script.md). Return to the interrupted page
deliberately; native buttons use fixed jumps. The historical S18 notes cite B25 and B27
as slides 52 and 54 (earlier numbering); use pages 53 and 55. S18 says controls
"remain proposed"; B27 corrects that to source-coded but not live-proved, so
prefer the B27 wording if asked.

## 30-Second Answer

"The full illustrative Azure envelope is about USD 435-1,260 a month, with AI
included. Scaling apps to zero removes their replica charges; provisioned SQL
and scheduled jobs remain. The AI example has a USD 50 monthly ceiling and
protects recommendations and document judging from chat exhaustion. Those
allocations aren't activated spending authority. We have measured synthetic
tokens, but no reconciled bill or cost per accepted outcome."

## Full Azure Planning, Not the Token Bill

The [dated cost model](./source/azure-cost-model-2026-11-27.json) gives exact
units, meters and assumptions. UK South public prices were retrieved
2026-11-27; the scenario uses 30 days/720 hours, USD and no negotiated rate,
tax, FX conversion or shared free allowance.

| Cost component | Low USD/month | High USD/month |
| --- | ---: | ---: |
| Identified persistent services | 334.838 | 334.838 |
| App compute | 37.422 | 517.104 |
| Job compute | 0.756 | 151.200 |
| Blob capacity | 0.192 | 1.920 |
| Log ingestion and billable retention | 3.140 | 62.800 |
| Monitoring allowance | 6 | 20 |
| Security allowance | 50 | 100 |
| Operations and transfer allowance | 2 | 20 |
| Model usage | 0 | 50 |
| Full scenario | 434.348 | 1257.862 |

The subtotal includes current S3 SQL, Premium registry, IoT B1, Event Hubs,
nine private endpoints and fourteen private DNS zones. SQL is not currently
serverless or auto-paused. Low-demand app compute assumes one of each replica
for 176 working hours plus 22 one-hour cooldowns; high load assumes every
configured maximum replica for 720 hours. Jobs, logs and storage have separate
volume assumptions. Monitoring/security/operation amounts are planning
allowances, not measured charges or enforced limits.

Zero app replicas do not stop scheduled audit, orchestration, simulator or
intake jobs. Five temporary S0 QA databases would add USD 90.75 if retained
for all 30 days, before their other charges; outside the core scenario.
Production redundancy, future Fabric, exceptional traffic, other resources
and human work need separate costing. The range is not a maximum invoice or
permission to exceed an earlier technology ceiling.

## Protect the Business Tasks

The following allocations illustrate the requested policy; they are not
approved spend or current live configuration.

| Pool | Daily USD | Monthly USD |
| --- | ---: | ---: |
| Recommendations | 1 | 20 |
| Document judging | 0.50 | 10 |
| Chat | 1 | 20 |
| Absolute aggregate ceiling | 2.50 | 50 |

Chat cannot borrow the USD 30/month and USD 1.50/day priority allocations.
Each attempted model call needs class and aggregate day/month admission.
Budget IDs remain stable within UTC calendar periods; renewal must preserve
spent history and unresolved liability. The source already supports atomic
worst-case money reservations, but configure and test this isolation under
named authority before relying on it.

The configuration point is `Consumption.authorize` in the
[core admission source](../../src/core/src/zava_forward/core/ai_consumption.py).
Assign each capability its class-day, class-month, aggregate-day and
aggregate-month budget IDs. Set each budget's `amount` to the corresponding
USD limit alongside finite `calls` and `tokens`; record the price, owner,
approval evidence, validity period and alert owner. This is an operator
configuration mechanism, not a shipped self-service budget screen. Changes
must respect immutable budget identities and unresolved reservations.

Deterministic missing-field/state/evidence checks use no model tokens.
Interpretation may need a bounded model; professional acceptance stays
separate. For a single attempt with at most 4,000 total provider-input tokens
and 1,000 output tokens, public prices give these upper estimates:

| Observed deployment SKU | Input/output USD per million | Attempt ceiling USD |
| --- | --- | ---: |
| GPT-4.1-nano GlobalStandard | 0.10 / 0.40 | 0.0008 |
| GPT-4.1-mini regional Standard | 0.484 / 1.936 | 0.003872 |

No model call means zero model charge. If the proposed policy is enforced,
the maximum is USD 2.50/day and USD 50/month across these paths, regardless
of model mix; model changes require valid prices and re-authorisation.
Retrieval/system context, retries and additional passes must be included or
separately reserved. Unknown price, liability, authority, safety or aggregate
holds can still stop every model pool. Manual and independent hazard paths
continue. Azure budget alerts notify after delayed cost evaluation; they
don't stop consumption or implement these caps.

## Three Things Not to Mix

| Item | What it is | What it is not |
| --- | --- | --- |
| Planning scenario | Labelled estimate: 6,884 historical tokens over five runs is 1,376.8 per run; assumed 10 times that per task (13,768) and 20 tasks per home (275,360 tokens) at an assumed USD 1.60 per million tokens (GPT-4.1-mini output-rate, secondary source dated 2026-10-23) gives USD 0.440576 per home and USD 6,872.9856 across 15,600 modelled homes. Doubling the workload gives USD 0.881152 per home | A verified deployment price, a measured workload, an accepted-outcome cost or the full project cost |
| Live consumption ledger | Source supports calls/tokens and monetary reservation, settlement and holds; actual attributable cost requires valid prices, usage and Finance billing reconciliation | Proof that the illustrated pools are configured, complete attribution or evidence of saving |
| Held-out measurement runner | Owner-authorised finite batch, at most USD 5.00, to measure tokens per proposal on held-out cases; implemented on main (`zava_forward.agents.heldout_batch`); ran live 2026-11-18 under #432: 12 synthetic proposals, 2,522 tokens, USD 0.000744 at list price | Usage only: no accepted-outcome count, so no cost per accepted outcome, saving or permission |

## If Pressed

* Accepted-outcome cost is total attributable cost divided by human-accepted proposals above an agreed quality floor. A zero or unknown denominator means not measurable (B25).
* Finite calls, tokens and expiry are not money caps and budget alerts are not hard stops. Task, period and call-depth limits exist in source; live activation and billing reconciliation are unproved (B25, B27).
* Value counts only when Finance confirms where the spend falls.

## Do Not Say

* Any price, saving or payback as fact, or USD 0.44 as the cost of the project.
* That the held-out batch proved quality, acceptance or reconciled billing.
* That Tokenomics has been rehearsed or timed; no rehearsal is recorded.

## Sources

* [Slide manifest](./source/slides.json), Slide 22 notes and workings
* [Full Azure and AI budget model](./source/azure-cost-model-2026-11-27.json)
* [Current Tokenomics synthesis](../reference/resources/ai-tokenomics.md#full-azure-planning-and-protected-ai-pools-2026-11-27)
* [B25 and B27 answers](./pitch/questions-and-answers.md)
* [Placement draft and decisions](./pitch/tokenomics-placement-draft.md)
* [Core consumption ledger](../../src/core/README.md) and [API consumption report](../../src/api/README.md)
* [Cost per home versus value evidence](./pitch/tokenomics-cost-per-home-vs-value.md)
