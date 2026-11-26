---
title: Research for issue 435 cost-per-home versus value evidence
ms.date: 2026-11-26
---

## Scope

Issue 435, mentor Tokenomics question. Goal: a cited cost-per-home versus value document for the pitch using only existing repository evidence. Synthetic demo, focused tier, no src change.

Research disposition: `reused` (the repository already holds the evidence; no new investigation or live call). Planning Readiness: Ready. The mentor's reference is https://en.wikipedia.org/wiki/Tokenomics; the mentor's meaning is unconfirmed.

## Findings (read 2026-11-26)

| Item | Finding | Source |
| --- | --- | --- |
| Metered usage | One measured held-out batch: 12 synthetic proposals, 2,522 tokens (882 input, 1,640 output), 210.17 mean per proposal, USD 0.000744 at list price (0.10 input, 0.40 output per 1M, Azure Retail Prices API, retrieved 2026-11-18), usage only, no accepted outcomes | docs/reference/research/ai-heldout-batch-432-live-2026-11-18.md |
| Cost ledger | `ai_consumption.py` records calls, tokens, price and authority events; price, cost and liability stay `Unknown` until settled and approved. No settled ledger export is in the repository; billing reconciliation is waived for the demo | src/core/src/zava_forward/core/ai_consumption.py; docs/capstone/tokenomics-qa-brief.md |
| Per-home cost | Labelled planning scenario only: 275,360 tokens per home at an assumed USD 1.60 per 1M gives USD 0.440576; times 15,600 modelled homes gives USD 6,872.9856 (arithmetic re-run 2026-11-26). The batch unit is a proposal, not a home, so no measured per-home cost exists | tokenomics-qa-brief.md; slides.json S18 |
| Value, funding | Conditional grant potential min(50% of GBP 6,082, GBP 7,500) = GBP 3,041 per home, GBP 47,439,600 over 15,600 homes, assuming eligibility, allocation, award and claims. Not secured funding | slides.json S05, S10, B09 |
| Value, time | Pilot targets (25 percent fewer coordination hours per home, 20 percent shorter cycle time) are targets, not results. Time capture is built but off, so no measured time saved. Released time is capacity, not cash | slides.json S20; timecapture.py; docs/reference/resources/ai-tokenomics.md |
| Currency | USD cost and GBP value are separate; no approved dated FX exists, so no ratio | slides.json S18, B05, B09 |

## Gaps that stay Unknown

Settled cost per home, full project cost, accepted-proposal count, secured funding, measured time saved, FX rate.

## Criteria

Only the mentor-confirmation criterion is unticked on the issue; it needs the mentor and cannot be proven from the repository.
