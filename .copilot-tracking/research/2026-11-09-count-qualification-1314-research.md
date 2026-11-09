---
title: SQL wave checkpoint comparison count qualification 1314 research
ms.date: 2026-11-09
task_id: 1314-count-qualification-1109
---

## Disposition

Research executed 2026-11-09 (read-only Git and `gh`). Planning Readiness: Ready. New, independently scoped first pass for #1314 (documentation only), declared as a child of the #440 controls-checkpoint branch. It is not a #440 correction cycle: the spent #440 C1 and C2 counts, the adverse findings and the policy that no automatic C3 or budget renewal exists are unchanged. Issue text, the comment of 2026-11-09 (6746245922) and the coordinator brief are data; every number below was reproduced with Git.

## Pinned identities

* Branch `docs/demo-checkpoint-counts-1314-1109`, clean, HEAD `efb2f7e0cd84b1e5983481055047272c2cc3db88`, tree `2cab0c338ef383b57bdcacceca52057423ebf1af`. Fork point from the declared target `docs/demo-controls-checkpoint-440-1109` (local, not main): `git merge-base HEAD docs/demo-controls-checkpoint-440-1109` equals `efb2f7e0cd84b1e5983481055047272c2cc3db88`, which is also the target tip at this time. The target worktree is owned by another lane and was not touched.
* `origin/main` (fetched, read only) `48350983be156d33afb5803570e1bc0bdb5455bb`. Not used as a comparison base below.
* Compared commits, all present locally: C2 candidate `f2e07999386399694abe91562555b35c0105ab9b`; SQL-wave base `ef28d4da42d83b111d48f14df9b70e3c4932a477` (also written `ef28d4da4`); first SQL-wave checkpoint commit `06f408dd7d46e9cdd521a17b10579552ffadd598`; current-main preparation candidate `45e8744f044996b39f54c901d84833b68c523d95`, its merge `53cef9040d958b68e513684faa2014cab0203da1` and main `3a9767d5cf728c5e3be76813ce0bfdac4c06841e` (PR 1240 squash).

## Finding 1: C2 scope count (`c2-changes.md` line 17)

The original line says: against `ef28d4da4` only the pack, index, log and `.copilot-tracking` records, "15 paths, additions only apart from the one re-wrapped index line".

Reproduced:

| Comparison | Paths | Additions | Deletions |
| --- | --- | --- | --- |
| `ef28d4da4` to `f2e07999` (final C2 candidate) | 17 | 700 | 0 |
| `ef28d4da4` to `ec597d023` (C2 merge commit, parent of the commit that added the C2 changes and review records and modified the C2 state record) | 15 | 604 | 0 |
| `06f408dd7` to `f2e07999` | 11 | 258 | 5 |

The 15-path figure matches the intermediate tree at `ec597d023`; the record does not say when it was observed, so this is a match, not a dated observation claim. `ec597d023` to `f2e07999` adds the C2 changes (24) and review (27) records and rewrites the C2 state record (56 additions, 11 deletions; the state record is new in the `ef28d4da4` range, so the final range still has 0 deletions). The final comparison is 17 paths, 700 additions and 0 deletions, so there is no replacement of an index line against `ef28d4da4`. The re-wrapped index line belongs to the separate C2 versus `06f408dd7` comparison, where `docs/reference/README.md` is 4 additions and 1 deletion (11 paths overall; its 5 deletions are that one index line plus 4 in `.github/rubric/scores/latest.json`, which arrived with the C2 merge of `ef28d4da4`). The 17 paths are the 14 SQL-wave and C2 tracking records and the pack, index and log. Neither comparison is against later `origin/main`.

## Finding 2: current-main preparation comparison scope (`mainprep-details.md` line 12, `mainprep-changes.md` line 15)

Reproduced for pack, index and log only (`git diff --numstat`, all with 0 deletions):

| Comparison | Pack | Index | Log | What the additions contain |
| --- | --- | --- | --- | --- |
| `f2e07999` to `45e8744f` | +171 | +4 | +5 | Incoming main pack content (+154, from `f2e07999` to the merge `53cef9040`; index and log 0) plus the new preparation note (+17, +4, +5, from `53cef9040` to `45e8744f`) |
| `3a9767d5c` to `45e8744f` | +133 | +17 | +15 | Inherited SQL-wave and C2 content (+116, +13, +10, from `3a9767d5c` to `53cef9040`) plus the same new preparation note (+17, +4, +5) |

The details line says main's pack insertions "are the only additions versus `f2e07999`" and that the note, index sentence and log entry "are the only additions versus `origin/main`". Both are incomplete: versus `f2e07999` the additions include the new note as well; versus `3a9767d5c` they include inherited SQL-wave and C2 content as well. The numbers in the changes record (171/133, 5/15, 4/17) are correct and unchanged.

Scope limit of the zero-deletion statement: it holds for the three files above. The whole-tree comparison `f2e07999` to `45e8744f` is 234 files, 7141 insertions and 34 deletions because it contains incoming main; `3a9767d5c` to `45e8744f` is 24 files, 931 insertions and 0 deletions; `53cef9040` to `45e8744f` is 6 files, 90 insertions and 7 deletions, all in the preparation state record, which is a tracking file the same commit modified. The qualification must not extend "0 deletions" beyond pack, index and log for the first and third ranges.

## Related claim: pack byte-prefix wording

`mainprep-plan.md` line 30 (P5) and `mainprep-details.md` line 12 require append-only prefix equality of pack and log against the merge parents, and the details add that log and index are a byte prefix versus `f2e07999`. Verified with `cmp`: index and log of `45e8744f` are byte-prefix extensions of `f2e07999`; the pack is not (incoming main inserted its sections before the SQL-wave sections), so for the pack only the ordered zero-deletion line preservation holds. The qualification names this so the prefix wording is not read as a pack byte-prefix proof.

## Placement and preservation

* The pack's SQL-wave section ends with the dated subsections C2 qualification, Current-main preparation and Original-load #1292 note, then the controls checkpoint section. A new dated subsection is added after the #1292 note, before the controls checkpoint heading, so the in-flight parent appends at the end of file do not overlap.
* The index entry of the SQL-wave checkpoint and the log are append-only; this lane appends one sentence-sized block after the existing sentences of that index entry and one log entry. The parent also appends to index and log, so a textual overlap there is known and left to the coordinator.
* Original authored C2, preparation, review and adverse files are preserved byte for byte. Their authoritative blobs are listed in the plan and checked at the end.

## Boundaries

No source, fixture, policy, workflow or SQL change; no new live evidence; no claim that any SQL defect is fixed; no closure of #440, #81 or #1314; no C3 for #440 or budget renewal. Child PR uses `Refs #1314` and `Refs #440` only, and only after the declared parent target is published and independently reviewed.

## Planning Readiness

Ready: identities, reproduced counts, the placement and the boundaries are known.
