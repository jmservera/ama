---
title: Capstone pitch Tokenomics preparation, seventh pass with regression tests (Refs #435)
description: Per-criterion status of the unticked acceptance criteria of issue 435 on the synthetic demo, with two new regression tests that bind the recorded placement and spend decisions to the deck and the batch record
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. No Azure resource was created or changed, no credential was read, and no deck, SQL or `src` change was made. Earlier passes: [sixth pass](./capstone-pitch-435-live-2026-11-23.md).

## Evidence

* python-pptx read of the [v2 deck](../../capstone/deck/zava-forward-cowork-v2-draft.pptx) (55 slides): slide 22 "Model inference. Measure accepted value." carries the labelled planning scenario (E21, E19, E05, "#435 not accepted"); slides 53 and 55 are the B25 and B27 question cards.
* [#432 batch](./evaluation/heldout-batch-432-live-2026-11-18/): 12 calls, USD 0.000744 at list price, 2,522 tokens, inside the authorised 12 calls, 24,000 tokens and USD 0.50, with approver and spend authority recorded.
* New tests in `tools/test_capstone_pitch_docs.py`: `test_deck_placement_matches_owner_decision` and `test_measured_batch_stays_within_recorded_authority`. Both pass with the existing two (4 tests, `python3 -m unittest tools.test_capstone_pitch_docs`).

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Placement decided; deck rebuilt if changed | Proven for the demo | Decision 2026-11-13 in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md); the deck already carries slide 22, B25 and B27, guarded by the new deck test. No rebuild needed |
| 2 | Mentor confirms meaning and figure or method | Unproven; cannot be proven for the demo | Needs a mentor statement; the repository holds only the owner's report |
| 4 | Finite measured batch authorised, spend authority recorded | Proven for the demo | Authorisation and report under #432, guarded by the new batch test. Usage only: no accepted-proposal count, so no cost per accepted outcome |

Criterion 3 stays ticked in the issue, but the [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) hold no performed timing; that tick is not supported by repository evidence. Issue 435 is referenced, not closed.
