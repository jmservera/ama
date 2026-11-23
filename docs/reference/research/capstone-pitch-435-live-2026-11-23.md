---
title: Capstone pitch Tokenomics preparation, sixth per-criterion pass (Refs #435)
description: Comparison of the three unticked acceptance criteria of issue 435 with main and live revisions 0000054 and 0000026 on the synthetic demo, with what cannot be proven stated precisely
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only, documentation only. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, cap USD 700; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed). No source, deck, SQL or Azure change was made, no Azure resource was created (none to delete) and no credential was read. Earlier passes: [first](./tokenomics-pitch-criteria-435-live-2026-11-18.md), [second](./capstone-pitch-435-live-2026-11-18.md), [third](./capstone-pitch-435-live-r3-2026-11-18.md), [fourth](./capstone-pitch-435-live-2026-11-20.md), [fifth](./capstone-pitch-435-live-2026-11-22.md).

## Observations (2026-11-23)

* `main` and the worktree head are both `342fad401d`.
* Read-only `az containerapp revision list` with the existing login: `ca-cutover-test-demo-api` has one active revision, `0000054` (Healthy, 100% traffic, created 2026-11-22T23:14:23Z); `ca-resident-demo` has `0000026` (Healthy, 100%, created 2026-11-22T23:14:37Z). Both apps are up; neither serves Tokenomics content, so the revisions add no acceptance evidence for #435.
* `python-pptx` read of [the v2 deck](../../capstone/deck/zava-forward-cowork-v2-draft.pptx): 55 slides; slide 22 "Model inference. Measure accepted value.", slide 53 is the B25 CFO card, slide 55 the B27 card; last changed by `05e94d3036`.
* The held-out batch code path from #1559 still passes offline: `unittest tests.test_heldout_batch tests.test_heldout_aoai` in `src/agents` ran 56 tests, OK.
* #432 batch records remain in [evaluation/heldout-batch-432-live-2026-11-18](./evaluation/heldout-batch-432-live-2026-11-18/) (12 calls, USD 0.000744 at list price, 2,522 tokens).

## Code gaps

None found. All three criteria are decisions or confirmations, not application behaviour, and the batch adapter tests pass, so no source change or test was added.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt and revalidated if changed | Proven for the decision; no rebuild needed | Owner decision 2026-11-13 in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md); the deck read above carries it on slides 22, 53 and 55. The issue's "slide 16" is stale (slide 16 is S14). Presentation format (15 or 30 minutes) stays with the owner |
| 2 | Mentor confirms meaning and whether a figure or method is expected | Unproven; owner-gated | Needs a mentor statement; the repository holds only the owner's report of the 2026-10-22 review. Not provable for the demo and nothing was assumed |
| 4 | Owner decides on a finite measured batch; spend authority recorded | Proven for the synthetic demo | Decision 2026-11-13 (up to USD 5) and executed authorisation under #432 (12 calls), see the [#432 note](./ai-heldout-batch-432-live-2026-11-18.md). Usage only, no accepted-proposal count, list-price estimate rather than a billing record |

## Flags for the owner

* Criterion 3 is ticked but the [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) record no performed timing; the tick is not supported by repository evidence.
* The #432 figures are not on slide 22 or B25; adding them is a deck rebuild through the PowerPoint workflow.
* Issue 435 is referenced, not closed.
