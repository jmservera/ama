---
title: Cost per home versus value evidence and per-criterion status (Refs #435)
description: Evidence that the repository supports a cited cost-versus-value answer for the mentor Tokenomics question only as a method with Unknown gaps, and a per-criterion status for issue 435 on the synthetic demo
ms.date: 2026-11-26
---

Scope: synthetic demo, desktop only. Owner decisions of 2026-11-18 apply (live Azure authorised, billing reconciliation, DPO and Legal approval and person-run assistive technology testing not needed). No Azure call, no credential read, no source under `src/` changed (focused tier, documentation only).

## What changed

* Added [the pitch evidence page](../../capstone/pitch/tokenomics-cost-per-home-vs-value.md): cost per home (measured batch, labelled planning scenario, ledger, full project) against value per home (secured funding, conditional grant, time saved), each with source and label, and Unknown where no price or outcome source exists.
* Linked it from the [pitch folder README](../../capstone/pitch/README.md) and the [Q&A brief](../../capstone/tokenomics-qa-brief.md), and indexed it in the knowledge base.

## Commands and results (2026-11-26)

```text
python3 arithmetic re-run: 6884/5 = 1376.8; x10 = 13768; x20 = 275360 tokens per home
275360/1e6 x 1.60 = 0.440576 USD per home; x15600 = 6872.9856 USD
2522/12 = 210.17 tokens per proposal; 882 input x 0.10 + 1640 output x 0.40 per 1M = USD 0.0007442
min(0.5 x 6082, 7500) = 3041 GBP per home; x15600 = 47,439,600 GBP
```

The figures match the existing Q&A brief, the #432 note and the deck notes. No new figure was invented. The wording check forbids any price, saving, payback or cost-to-grant ratio.

## Limits

* The measured batch has no accepted outcomes, no proposals-per-home count and no billing record; the planning scenario and the batch disagree and are not reconciled.
* Secured funding and measured time saved do not exist in the demo data; the conditional grant is modelled.
* No settled ledger export is in the repository; none was queried live because a settled figure needs Finance and billing reconciliation, which the owner waived for the demo.
* The deck was not changed; the page is presenter backup.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt if changed | Ticked in the issue; not re-proven here | [2026-11-25 note](./capstone-pitch-435-live-2026-11-25.md) |
| 2 | Mentor confirms what Tokenomics meant, figure or method | Unproven; cannot be proven for the demo | Needs the mentor. The new page offers a method plus a labelled scenario and states that the meaning is unconfirmed. Left unticked |
| 3 | Segment rehearsed in the timed route | Ticked in the issue; not re-proven | [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) |
| 4 | Owner decides on finite measured batch, spend authority recorded | Ticked; proven for the synthetic demo | [#432 note](./ai-heldout-batch-432-live-2026-11-18.md) |
| 5 | Deck challenged against the assessment guide | Ticked; not re-proven | [challenge](../../capstone/pitch/capstone-assessment-challenge.md) |
| 6 | Every Tokenomics statement sourced and labelled, no price, saving or payback claim | Ticked; the new page applies the same rule: every row has a source and label, Unknown elsewhere, no ratio | Pitch evidence page |
