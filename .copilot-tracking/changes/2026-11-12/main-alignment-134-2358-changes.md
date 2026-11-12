---
title: Main alignment of the #134 candidate, changes
description: Record of the local merge of origin/main into the #134 documentation candidate
ms.date: 2026-11-12
---

## Result

Merge commit `f8aad2889` (parents `84ba86c8b`, a descendant of frozen `cc7e3c3a9` by two RPI evidence commits, and `origin/main` `774a91e5f`). Local only; nothing pushed, no PR, no merge into main, no tick.

| Check | Result |
| --- | --- |
| Conflicts | Exactly the two predicted, `docs/architecture/cutover-evidence-pack.md` and `docs/reference/README.md`; `log.md` auto-merged. Resolved by keeping both sides |
| Order deviation | The plan said main-first. The resolution keeps the #134 section or paragraph first and main's post-fix-wave section or paragraph second, because only the edit tool may change files and reordering the 43-line block by hand risked an unreviewed text change. Both are kept and one blank line separates them. No content is affected |
| Markers | None in the three docs files |
| #134 section | Identical to `cc7e3c3a9` except one added separator blank line before the next heading (extracted by heading and diffed) |
| Main's section | Identical to `origin/main` (diff rc 0) |
| Pack end | Final byte `0a`, preceded by `.`; no trailing blank line; the pack diff against `cc7e3c3a9` has zero deleted lines and adds only after the old last line (lines before it unshifted) |
| README | Diff against `cc7e3c3a9` is main's paragraph only, with a blank separator |
| Log | Zero deleted lines against both parents (append-only) |
| Merge shape | Two parents, PR 1495 head `bbdacadcb` not an ancestor, clean tree, trailer present, `git diff --check` clean |
| Non-tracking files changed against `cc7e3c3a9` | Only main's own files (rubric score, capstone pitch, `src/core` form export and its test and README, pack, README, log) |

## Not done

No source edit by this task (the `src/core` changes are main's PR 1482 content arriving through the merge), no executable gate, no new log entry, no correction (the one permitted alignment correction is unused), no change to the #134 claims: six partial, four deferred, #83 and #134 OPEN, criterion 2 not met. No anchor or link was changed; independent review follows.
