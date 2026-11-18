---
title: Tokenomics pitch, status of unticked criteria for the demo (Refs #435)
description: Per-criterion proven or unproven record for the three unticked acceptance criteria of issue 435, checked on 2026-11-18 against repository decisions, the 55-slide deck and the measured batch of issue 432
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Owner decision 2026-11-18 authorises live Azure in resource group `ama` (cap USD 700) and waives billing reconciliation, DPO and Legal approval and person-run assistive technology testing. These three criteria are about the pitch and owner or mentor decisions, so no live Azure probe of the demo apps could prove them, and none was run. No Azure resource was created, so none needed deletion. No source code changed.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt and revalidated if changed | Decision proven; rebuild and revalidation not evidenced | The owner decision of 2026-11-13 (slide 22 on the main route, B25 and B27 question cards, USD 0.44 per home kept as a labelled scenario) is recorded in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md). A python-pptx read on 2026-11-18 of [the v2 deck](../../capstone/deck/zava-forward-cowork-v2-draft.pptx) shows 55 slides: slide 22 "Model inference. Measure accepted value." (E21), slide 53 B25 CFO card, slide 55 B27. This run did not rebuild or revalidate the deck through the PowerPoint workflow, and slide 53 still says "#435 not accepted", so the criterion stays unticked |
| 2 | Mentor confirms what Tokenomics meant, and figure or method | Unproven; cannot be proven for the demo | Needs a statement from the mentor. The repository has none: the placement draft records it as unmet and the meaning stays owner-reported. Nothing was assumed |
| 3 | Owner decides on a finite measured batch, spend authority recorded | Proven for the synthetic demo | Owner decision of 2026-11-13 authorised up to USD 5 (placement draft). Issue 432 then ran the batch on 2026-11-18 under a recorded `authorization.json` (approver owner, cap USD 0.50, 12 calls): 12 synthetic proposals, 180 to 225 tokens each, 2,522 in total, USD 0.000744 at list price, see [the #432 note](./ai-heldout-batch-432-live-2026-11-18.md). Caveats: synthetic and not independently labelled, usage only with no quality or accepted-proposal count, and a list-price estimate rather than a billing record |

## Already ticked, not re-examined

The rehearsal, assessment challenge and statement-audit criteria are ticked in the issue. Their records are the [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md), the [assessment challenge](../../capstone/pitch/capstone-assessment-challenge.md) and the [deck assessment](../../capstone/pitch/current-deck-assessment-2026-11-12.md). This note does not change them.

## Open items for the owner

* Quote the #432 figures on the Tokenomics slide or card only with their label (`measured held-out batch`, synthetic, no cost per accepted proposal), then rebuild and revalidate the deck to close criterion 1.
* Ask the mentor the meaning question to close criterion 2.
* Issue 435 is referenced, not closed.
