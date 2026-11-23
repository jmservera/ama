---
title: Capstone pitch Tokenomics preparation, eighth pass with stale-wording fix (Refs #435)
description: Per-criterion status of the unticked acceptance criteria of issue 435 on the synthetic demo, a corrected spoken script that no longer says the held-out batch has not run, and a computed read-aloud timing check
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. No Azure resource was created or changed, no credential was read, and no deck or `src` change was made. Earlier pass: [seventh pass](./capstone-pitch-435-live-2026-11-23b.md).

## Finding and fix

The spoken B25 answer and the rehearsal pass check in the [rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md), and the [Q&A brief](../../capstone/tokenomics-qa-brief.md), still said the held-out batch was "authorised but not run". The batch ran on 2026-11-18 under #432: 12 synthetic proposals, 2,522 tokens, USD 0.000744 at list price, usage only ([record](./evaluation/heldout-batch-432-live-2026-11-18/)). A presenter reading the script would have understated the evidence, and the notes contradicted their own slide 22 cue. Both documents now say the batch ran on synthetic cases with no accepted outcomes, and still claim no price, saving or payback. `test_spoken_scripts_do_not_say_the_batch_has_not_run` guards the wording (5 tests pass; ruff clean).

The deck was not changed: slides 22, 53 and 55 carry no "not run" statement. The older [assessment challenge](../../capstone/pitch/capstone-assessment-challenge.md) is a dated record and keeps its original wording (lines 16 and 80), which is now historical.

## Computed timing check

Word counts of the scripts at 130, 150 and 160 words per minute give the slide 22 cue 20.2 to 24.9 s (limit 25 s), the B25 answer 25.5 to 31.4 s and B27 12.0 to 14.8 s. This is arithmetic, not a rehearsal; the rehearsal record stays blank.

## Per-criterion status

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Placement decided; deck rebuilt if changed | Proven for the demo | Decision 2026-11-13 in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md); deck already carries slide 22, B25 and B27; no rebuild needed |
| 2 | Mentor confirms meaning and figure or method | Unproven | Needs a mentor statement; only the owner's report exists |
| 4 | Measured batch authorised, spend authority recorded | Proven for the demo | #432 authorisation and report; usage only, no cost per accepted outcome |

Criterion 3 is ticked in the issue but no timed run is recorded; the tick is unsupported and needs a presenter's timed run, which only a person can perform. Issue 435 is referenced, not closed.
