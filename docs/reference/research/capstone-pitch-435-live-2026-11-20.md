---
title: Capstone pitch Tokenomics preparation, fourth per-criterion pass (Refs #435)
description: Retained deck and batch evidence for the three unticked acceptance criteria of issue 435 on the synthetic demo, with what cannot be proven stated precisely
ms.date: 2026-11-20
---

Scope: synthetic demo, desktop only, documentation only. Owner decisions of 2026-11-18 apply. No source, deck, SQL or Azure change was made, no Azure resource was created and no credential was read. Earlier passes ([first](./tokenomics-pitch-criteria-435-live-2026-11-18.md), [second](./capstone-pitch-435-live-2026-11-18.md); the [third](./capstone-pitch-435-live-r3-2026-11-18.md) retained outputs) disagreed on criterion 1 and the first two left deck observations unretained; this pass re-reads the deck and resolves the disagreement.

## Retained observations (2026-11-20)

`python-pptx` read of [the v2 deck](../../capstone/deck/zava-forward-cowork-v2-draft.pptx), which has 55 slides and was last changed by commit 05e94d303 (not by any Tokenomics work):

* Slide 22: title "Model inference. Measure accepted value."; footer "E21: assumed workload; secondary price, 23 Oct 2026, not current verified price. E19: usage only. E05: controls coded; #435 not accepted."
* Slide 53 (B25): "What is your Tokenomics unit and can the AI bill run away?"; "#435 not accepted; no saving, payback or full-project price established."
* Slide 55 (B27): "What stops chat and agent sprawl multiplying hidden calls?"

Batch records in [evaluation/heldout-batch-432-live-2026-11-18](./evaluation/heldout-batch-432-live-2026-11-18/): `report-live.json` states approver and spend reference "Owner decision 2026-11-18 on #432", 12 calls, budget USD 0.50, accrued USD 0.000744, outcome completed, label `measured held-out batch`; `authorization.json` carries expiry 2026-11-19T00:00:00Z and the list-price source retrieved 2026-11-18.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt and revalidated if changed | Proven: decision recorded and deck needs no rebuild | The owner chose slide 22 on the main route plus B25 and B27 cards (placement draft, 2026-11-13). The retained read shows those slides already carry it, so the deck does not change; the criterion's rebuild clause is conditional and does not fire. Residual: the issue text names slide 16 and a 15-minute route, so the format question stays with the owner |
| 2 | Mentor confirms meaning and whether a figure or method is expected | Unproven; cannot be proven for the demo | Needs a statement from the mentor; the repository holds only the owner's report of the 2026-10-22 review. Nothing was assumed |
| 4 | Owner decides on a finite measured batch; spend authority recorded | Proven for the synthetic demo | Decision 2026-11-13 (up to USD 5) and executed authorisation 2026-11-18 (USD 0.50, 12 calls) with a completed batch: 12 synthetic proposals, 2,522 tokens. Caveats: synthetic, usage only, no accepted-proposal count so no cost per accepted outcome, list-price estimate not a billing record. The pitch therefore still states the gap and shows no cost-per-accepted figure |

## Inconsistency found and fixed

[Rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) still described the held-out batch as "not run live" and "awaiting" execution after it had run. The figures table now cites the #432 result. The spoken line was left unchanged because its timing is unrehearsed.

## Flag for the owner

Criterion 3 is ticked in the issue, but the rehearsal notes record no performed timing ("rehearsal record blank"). On the evidence in the repository it is not proven; the tick should be reviewed. Criteria 5 and 6 rest on offline documents ([challenge](../../capstone/pitch/capstone-assessment-challenge.md), [audit](../../capstone/pitch/current-deck-assessment-2026-11-12.md)) and were not re-proven.

## Limits

No browser or live Azure proof applies: these criteria are about decisions and the deck, and no web file changed.
