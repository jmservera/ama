---
title: SQL wave checkpoint comparison count qualification 1314 plan
ms.date: 2026-11-09
task_id: 1314-count-qualification-1109
---

## Task metadata

* Task `1314-count-qualification-1109`, parent task `440-controls-checkpoint-1109` (declared target branch `docs/demo-controls-checkpoint-440-1109`, fork `efb2f7e0cd84b1e5983481055047272c2cc3db88`). Research: `.copilot-tracking/research/2026-11-09-count-qualification-1314-research.md` (executed, Ready). Details: `.copilot-tracking/details/2026-11-09-count-qualification-1314-details.md`.
* Branch `docs/demo-checkpoint-counts-1314-1109`, base `efb2f7e0`, not `main`. Owner demo tier: pure documentation needs no local gate; hosted checks and independent exact-head review stay mandatory.

## Executive summary

Add one dated qualification subsection to the SQL-wave part of the cut-over evidence pack, one sentence to its index entry and one log entry. They replace only the incorrect explanatory counts and ranges for two Low wording defects (C2 scope count; current-main preparation comparison scope). The original C2, preparation, review and adverse records stay unchanged. No source, fixture or policy edit; no SQL fix claim; no new live evidence; no #440 closure, C3 or budget renewal.

## User decisions and requirements

* First pass of an independently scoped #1314 follow-up; the spent #440 C1 and C2 counts and adverse findings are immutable.
* Both findings reproduced from pinned commits, never latest main.
* Preserve all original authored files byte for byte; qualify in new records and the pack only.
* No push, PR, issue or board write; no merge, rebase or touch of the parent worktree.
* One independent critique of the final candidate plan, one post-implementation Review; no repeats.

## Implementation phases

1. P1 Commit research, plan, details, critique and state before any documentation edit.
2. P2 Append to `docs/architecture/cutover-evidence-pack.md`, after the #1292 note and before the controls checkpoint heading, a subsection "Comparison count qualification, 2026-11-09 (Refs #1314 #440)" with a table of the reproduced ranges, the distinction of the three comparisons (final versus `ef28d4da4`; C2 versus `06f408dd7`; intermediate `ec597d023`) the preparation ranges with their composition, the scope limit of zero deletions and the limit of the byte-prefix wording (Q3: index and log only, not the pack).
3. P3 Add one sentence to the SQL-wave checkpoint index entry in `docs/reference/README.md` and append one entry to `docs/reference/log.md`.
4. P4 Validate: whole-tree and component ranges for every cited comparison; every baseline path and blob compared after the final commit; added-link check against a pinned baseline; clean tree.
5. P5 Record changes, one Review, state and handoff; commit.

## Acceptance criteria

* AC1 The qualification states 17 paths, 700 additions and 0 deletions for `f2e07999` versus `ef28d4da4`, labels 15 paths and 604 additions as the intermediate `ec597d023` observation, and states there is no index replacement in the final comparison.
* AC2 The index re-wrap (4 additions, 1 deletion) is attributed to C2 versus `06f408dd7`, distinct from the final comparison and from any later `origin/main` range.
* AC3 Preparation ranges: versus `f2e07999` pack +171, index +4, log +5 equals incoming main (+154, 0, 0) plus the new note (+17, +4, +5); versus `3a9767d5c` +133, +17, +15 equals inherited SQL-wave and C2 (+116, +13, +10) plus the same note. Zero deletions stated for those three files only.
* AC4 No original authored file changes: every path in `efb2f7e0` has the same blob except pack, index and log, which differ by additions only; the diff against `efb2f7e0` has no deletion, rename or mode change.
* AC7 The qualification states that index and log (not the pack) are byte-prefix extensions of `f2e07999` and that the pack proof is ordered zero-deletion line preservation.
* AC5 No source, fixture, policy, workflow, SQL, fix, live evidence, closure, C3 or budget claim.
* AC6 No closing keyword in any record; `Refs #1314` and `Refs #440` only.
