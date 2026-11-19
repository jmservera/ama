---
title: Capstone pitch Tokenomics preparation, per-criterion status (Refs #435)
description: Evidence for the unticked acceptance criteria of issue 435 on the synthetic demo, with what cannot be proven stated precisely
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, documentation only. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, cap USD 700; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed for the demo). No source, deck, SQL or infrastructure change was made and no Azure resource was created.

This is a second pass over the same criteria as [tokenomics-pitch-criteria-435-live-2026-11-18.md](./tokenomics-pitch-criteria-435-live-2026-11-18.md), which stays as recorded. The one difference: that note kept criterion 1 as rebuild and revalidation not evidenced; this pass reads criterion 1 as decided with no rebuild needed because the deck is unchanged. The owner should pick between the two readings.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt if it changes | Proven for the decision; no rebuild required (an earlier note recorded this criterion as not evidenced; this note supersedes it from the repository records and an unretained deck inspection) | Owner decision 2026-11-13 (slide 22 on the main route, question cards B25 at slide 53 and B27 at slide 55, USD 0.44 per home kept as a labelled scenario) is recorded in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md). Observed; raw output not retained: inspection of the [55-slide v2 deck](../../capstone/deck/zava-forward-cowork-v2-draft.pptx) on 2026-11-18 found slide 22 (S18, "Model inference. Measure accepted value."), slide 53 (B25, "accepted-outcome TCA unknown") and slide 55 (B27) already carry the placement, so the deck is unchanged and needs no rebuild. The issue text still names slide 16 and a 15-minute route; the format question stays with the owner. |
| 2 | Mentor confirms what Tokenomics meant and whether a figure or method is expected | Cannot be proven for the demo | Needs the mentor. The repository holds only the owner's report of the 2026-10-22 review; the meaning is unconfirmed. The pitch keeps stating the unit as a method with gaps and shows no figure that implies the mentor asked for one. |
| 3 | Segment rehearsed in the timed route | Ticked in the issue; not re-proven | The [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) still say no performed timing is recorded. This note does not claim one. |
| 4 | Owner decides on a finite measured batch; spend authority recorded | Proven for the synthetic demo | Authority recorded in `authorization.json` (approved by the owner, reference "Owner decision 2026-11-18 on #432", 12 calls, 24,000 tokens, USD 0.50, expiry 2026-11-19T00:00:00Z) and the batch ran: 12 proposals, 2,522 tokens, 180 to 225 per proposal. See the [#432 note](./ai-heldout-batch-432-live-2026-11-18.md) and its [evidence folder](./evaluation/heldout-batch-432-live-2026-11-18/). Label `measured held-out batch`; cases are synthetic and labelled by demo roles, not independent people. |
| 5 | Deck challenged against the complete assessment guide | Ticked in the issue; not re-proven | [capstone-assessment-challenge.md](../../capstone/pitch/capstone-assessment-challenge.md) (offline, not an assessor score). |
| 6 | Every Tokenomics statement sourced and labelled; no price, saving or payback claim | Ticked in the issue; not re-proven | [current-deck-assessment-2026-11-12.md](../../capstone/pitch/current-deck-assessment-2026-11-12.md). |

## Live check

Read-only, 2026-11-18: `az containerapp show -g ama -n ca-cutover-test-demo-api` reported (Observed; raw output not retained) provisioning state `Succeeded`, running status `Running`, latest revision `ca-cutover-test-demo-api--0000031`. This confirms the demo API that produced the batch is up; it adds no Tokenomics evidence. No credentials were read or printed and no browser proof was needed because no web file changed.

## Limits and follow-up

* The measured figures are not yet on slide 22 or the B25 and B27 cards, which still carry the USD 0.44 per home planning scenario and "accepted-outcome TCA unknown". Adding them is a deck rebuild through the PowerPoint workflow and is left to a later owner-directed change.
* No cost per accepted proposal exists: the batch has no accepted-proposal count or quality rates. The USD figure is a list-price estimate, not a billing record.
* Criterion 2 stays open until the mentor answers; criterion 3 stays unperformed until a presenter times a run.

## Evidence limits

* The deck inspection and the `az containerapp show` result are "Observed; raw output not retained"; they cannot be re-checked from this repository.
* The decision for criterion 1 rests on the placement draft; the deck coverage is the unretained observation.
