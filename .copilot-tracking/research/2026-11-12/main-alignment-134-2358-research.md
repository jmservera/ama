---
title: Main alignment of the #134 disposition candidate, research
description: Evidence for a local docs-only merge of current main into the frozen #134 candidate before UX parent integration
ms.date: 2026-11-12
---

## Disposition

Research executed (new increment) after the parent integration merge-tree proved a conflict. Planning Readiness: Ready.

## Evidence (read 2026-11-12)

* Frozen candidate: `cc7e3c3a9` on `research/demo-134-main-alignment-2358` in the exclusive worktree `issue-134-main-alignment-2358`, clean. Three commits above its merge base `43b2187b9` with `origin/main`. The existing #134 source worktree is not touched.
* Fresh `origin/main`: `774a91e5f` (rubric score record), six commits above the merge base, including PR 1492 (`e4854bd7e`, post-fix-wave checkpoint, Refs #440) and PR 1491 (capstone deck assessment).
* `git merge-tree --write-tree --name-only HEAD origin/main` reports content conflicts in exactly two files: `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md`. `docs/reference/log.md` auto-merges. No source, test, tool or workflow file conflicts.
* Nature of the conflicts: both sides append a new dated section after the same last line of the pack (the file has no trailing newline) and a new paragraph after the same last paragraph of the README index. Both are independent additions, so the genuine resolution keeps both, historical (main's post-fix-wave checkpoint) and current (the #134 AC-034 to AC-043 section), in main-first order.
* Issue states, live `gh` on 2026-11-12: #83 OPEN, #134 OPEN. PR 1495 is OPEN and unmerged (head `bbdacadcb`), so it is not merged here.
* Mandatory context read: case study original and addendum, the knowledge-base index and memory, `src/README.md` validation tiers. No private data, `support/`, `.env`, cloud, model or deploy input is used.

## Process defect and spent corrections (preserved, not edited)

* Original #134 process defect: the original RPI artifacts record that edits to the pack were applied before the plan and critique files were written (ordering disclosure). It stays recorded in [the original plan](../../plans/2026-11-12/ac-dispositions-134-1112-plan.md) and its critique.
* Two spent corrections exist: [correction 1](../../plans/2026-11-12/ac-dispositions-134-1112-correction1-amendment.md) (R-1 to R-5) and [correction 2](../../plans/2026-11-12/ac-dispositions-134-1112-correction2-amendment.md), which fixed the false wording that #83 is closed. Neither is renewed. The correction 1 entry's false wording stays in the append-only log and is superseded by the correction 2 entry.

## Risks

* R1: a naive "ours" or "theirs" resolution would drop either main's checkpoint or the #134 section. Mitigation: keep both and verify by section count.
* R2: the merge could silently alter the historical claims in the #134 section (six partial, four deferred, #83 open, no ticks). Mitigation: compare the section byte for byte before and after.
* R3: alignment could be mistaken for acceptance. Mitigation: no wording change beyond conflict resolution; the pin text in the #134 section states a read-time `origin/main` and remains historical.
* R4: the single permitted alignment correction must stay within existing history, with no new correction pool.
