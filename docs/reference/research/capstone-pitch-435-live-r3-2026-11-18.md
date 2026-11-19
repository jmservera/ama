---
title: Capstone pitch Tokenomics preparation, third pass with retained evidence (Refs #435)
description: Per-criterion proven or unproven table for the unticked and contested acceptance criteria of issue 435 on the synthetic demo, with raw deck and Azure read-only outputs retained
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, documentation only. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, cap USD 700; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed for the demo). No source, deck, SQL or infrastructure change was made and no Azure resource was created. Credential files were not read.

This extends two earlier passes, [tokenomics-pitch-criteria-435-live-2026-11-18.md](./tokenomics-pitch-criteria-435-live-2026-11-18.md) and [capstone-pitch-435-live-2026-11-18.md](./capstone-pitch-435-live-2026-11-18.md), which stay as recorded. Those passes kept their deck and Azure observations without raw output; this one retains them in [pitch-435-live-r3-2026-11-18](./evaluation/pitch-435-live-r3-2026-11-18/).

## Per-criterion status

| # | Criterion (issue state) | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt and revalidated if it changes (unticked) | Decision proven; rebuild clause not applicable | The 2026-11-13 owner decision (slide 22 on the main route, cards B25 and B27, USD 0.44 per home kept as a labelled scenario) is in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md). [deck-inspection.txt](./evaluation/pitch-435-live-r3-2026-11-18/deck-inspection.txt) (python-pptx, deck sha256 `949e2077...fa7fca`, 55 slides) shows slide 22 carries the labelled scenario with its E21 caveat, slide 53 carries "accepted-outcome TCA unknown" and slide 55 the bounded-call controls. The deck is unchanged, so no rebuild is owed. The issue text still names slide 16 and a 15-minute route; the format is still an owner question. |
| 2 | Mentor confirms what Tokenomics meant and whether a figure or method is expected (unticked) | Cannot be proven for the demo | It needs a statement from the mentor. The repository holds only the owner's report of the 2026-10-22 review. The deck stays safe without it: it shows no figure presented as asked for and states the method and the gap. |
| 3 | Segment rehearsed inside the timed route; timing and notes stored (ticked) | Tick not supported by repository evidence | The [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) and the placement draft say no performed timing is recorded. A run sheet exists; a measured time does not. Only a presenter can supply it. Recommend the owner re-open or annotate the tick. |
| 4 | Owner decides on a finite measured batch; spend authority recorded; otherwise state the gap (unticked) | Proven for the demo | Authority: [authorization.json](./evaluation/heldout-batch-432-live-2026-11-18/authorization.json) (approved by the owner, 12 calls, 24,000 tokens, USD 0.50, expiry 2026-11-19T00:00:00Z, model gpt-4.1-nano, list-price source dated 2026-11-18), within the USD 5.00 authorisation of 2026-11-13. Result: [report-live.json](./evaluation/heldout-batch-432-live-2026-11-18/report-live.json), 12 calls, 2,522 tokens (882 input, 1,640 output), 180 to 225 per proposal, accrued USD 0.000744, label `measured held-out batch`. See the [#432 note](./ai-heldout-batch-432-live-2026-11-18.md). Limit: synthetic cases, no accepted-proposal count, list price not a billing record. |
| 5 | Deck challenged against the complete assessment guide (ticked) | Ticked; not re-proven | [capstone-assessment-challenge.md](../../capstone/pitch/capstone-assessment-challenge.md), an offline challenge, not an assessor score. |
| 6 | Every Tokenomics statement sourced and labelled; no price, saving or payback claim (ticked) | Ticked; consistent with the retained deck text | [current-deck-assessment-2026-11-12.md](../../capstone/pitch/current-deck-assessment-2026-11-12.md). The retained slide text labels USD 0.44 per home as a planning scenario on a dated secondary-source rate and says B25 establishes no saving, payback or full-project price. |

## Live check

[azure-readonly.txt](./evaluation/pitch-435-live-r3-2026-11-18/azure-readonly.txt), 2026-11-18T14:59:28Z, read-only `az` queries with field filters: `ca-cutover-test-demo-api` revision 0000031 Running, `ca-resident-demo` revision 0000012 Running, `evhns-cutover-test-demo` Active. This confirms the demo that produced the batch is up. No browser proof applies because no web file changed and the criteria concern a PowerPoint deck and owner and mentor actions.

## Findings

* The deck still shows only the planning scenario. The measured #432 figures are not on slide 22 or the B25 card, so the pitch does not yet use the one measurement that exists. Showing them needs a deck rebuild through the PowerPoint workflow, left to an owner-directed change.
* The issue checklist is inconsistent with the repository on criterion 3, and criterion 4 is already evidenced but unticked.
* Unproven for the demo: criterion 2 (mentor) and criterion 3 (timed rehearsal). Everything else is proven or was ticked on earlier evidence.
