---
title: Plan, accuracy follow-up, demo wave checkpoint 440 (2026-11-12)
description: Plan for two bounded documentation accuracy edits
ms.date: 2026-11-12
---

Research: [research](../../research/2026-11-12/demo-wave-checkpoint-440-1112-accuracy-research.md). Details: [details](../../details/2026-11-12/demo-wave-checkpoint-440-1112-accuracy-details.md). Critique: [critique](./demo-wave-checkpoint-440-1112-accuracy-critique.md).

## Edits (documentation only)

* E1 in `docs/architecture/cutover-evidence-pack.md`, 1467 row of the wave table: replace the phrase "treats a non-finite or huge-integer-unsafe committed or tolerance observation as Unknown, not Within limits" with "treats a NaN or infinite committed or tolerance observation as Unknown (pause), not Within limits; finite values, including arbitrarily large integers, are assessed normally with no `isfinite` overflow".
* E2 in the same section, immediately after the preflight sentence in the environment paragraph: add one dated qualification that the namespace `zava_forward.agents` printed `None` in `02b`, that concrete modules and helpers were verified only later (post-freeze) by a same-environment import trace with hashes, the raw diagnostic path, and the limitation. The statement "Preflight imports resolved ... from this worktree" is qualified, not deleted.
* E3 add a dated "Accuracy follow-up" subsection at the end of the section naming that the 1467 row and the preflight claim were corrected, that originals are preserved in git history at `26cb3968`, that newer main `088e8c3` (PR 1470) is outside the tested wave, and that the tested pin is `bbb1d20cc984` with source-equal `5ee8ac14c70f`.
* E4 one log line appended to the existing 2026-11-12 entry is not allowed (append-only); append a new short entry in `docs/reference/log.md`. Index unchanged.
* Original research, plan, critique, changes and review files are not edited; a Review addendum file and changes file are new.

## Validation

`git diff` shows only the edited phrase plus additions; ASCII only; anchors unchanged; no test, install or service run.
