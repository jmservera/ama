---
title: Capstone pitch Tokenomics preparation, fifth per-criterion pass (Refs #435)
description: Fresh deck and demo API observations for the three unticked acceptance criteria of issue 435 on the synthetic demo, with what cannot be proven stated precisely
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only, documentation only. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, cap USD 700; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed). No source, deck, SQL or Azure change was made, no Azure resource was created (none to delete) and no credential was read. Earlier passes: [first](./tokenomics-pitch-criteria-435-live-2026-11-18.md), [second](./capstone-pitch-435-live-2026-11-18.md), [third](./capstone-pitch-435-live-r3-2026-11-18.md), [fourth](./capstone-pitch-435-live-2026-11-20.md).

## Observations (2026-11-22)

* `python-pptx` read of [the v2 deck](../../capstone/deck/zava-forward-cowork-v2-draft.pptx): 55 slides, last changed by commit 05e94d3036. Slide 16 is "Adopt without a big-bang replacement." (S14, adoption, not Tokenomics). Slide 22 is "Model inference. Measure accepted value." (S18; footer "E21: assumed workload; secondary price, 23 Oct 2026, not current verified price. E19: usage only. E05: controls coded; #435 not accepted."). Slide 53 is B25 (CFO card, "no saving, payback or full-project price established") and slide 55 is B27.
* `az containerapp show -g ama -n ca-cutover-test-demo-api` (existing login, read-only): provisioning `Succeeded`, running status `Running`, latest revision `ca-cutover-test-demo-api--0000053`. This shows the demo API is up; it adds no Tokenomics evidence. Raw output is not retained beyond these values.
* #432 batch records in [evaluation/heldout-batch-432-live-2026-11-18](./evaluation/heldout-batch-432-live-2026-11-18/): `authorization.json`, `report-live.json` (12 calls, USD 0.000744 at list price, 2,522 tokens).

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt and revalidated if changed | Proven for the decision; no rebuild needed | Owner decision 2026-11-13 (slide 22 on the main route, B25 and B27 cards, USD 0.44 per home kept as a labelled scenario) in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md); the deck read above shows those slides already carry it, so the rebuild clause does not fire. Correction: the issue text says slide 16, but slide 16 is S14; Tokenomics sits on slide 22. The format (15 versus 30 minutes) stays with the owner |
| 2 | Mentor confirms meaning and whether a figure or method is expected | Unproven; cannot be proven for the demo | Needs a mentor statement; the repository holds only the owner's report of the 2026-10-22 review. Nothing was assumed |
| 4 | Owner decides on a finite measured batch; spend authority recorded | Proven for the synthetic demo | Decision 2026-11-13 (up to USD 5) and executed authorisation under #432 (USD 0.50, 12 calls) with a completed batch, see the [#432 note](./ai-heldout-batch-432-live-2026-11-18.md). Caveats: synthetic, usage only, no accepted-proposal count so no cost per accepted outcome, list-price estimate not a billing record |

## Flags for the owner

* Criterion 3 is ticked but the [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) hold no performed timing; the tick is not supported by repository evidence.
* The #432 figures are not yet on slide 22 or B25; adding them is a deck rebuild through the PowerPoint workflow.
* Issue 435 is referenced, not closed.
