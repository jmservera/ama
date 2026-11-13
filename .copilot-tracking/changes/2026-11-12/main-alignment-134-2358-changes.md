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

## Alignment correction (2026-11-13)

Authorized by [amendment](../../plans/2026-11-12/main-alignment-134-2358-correction-amendment.md) after [critique](../../plans/2026-11-12/main-alignment-134-2358-correction-critique.md) (both in `.copilot-tracking/plans/2026-11-12/`), following independent assessment `rpi-134-alignment-independent-0004` of head `81c8bfae1c064f247fbb1472e9cda44bed53c8d4`. This is the one reserved alignment correction. The original text above is retained and qualified here, not rewritten.

| Original wording or defect | Corrected statement |
| --- | --- |
| "Main's section" row, cell "Identical to `origin/main` (diff rc 0)" | The main section has the same content as `774a91e5f` except one added EOF newline on its last pack line. It is not byte identical |
| Result-summary claim "non-tracking diff vs origin/main is none" (external result JSON, preserved byte for byte, unedited) | False as written, as assessment 0004 reports. Against `774a91e5f`, outside `.copilot-tracking/`, exactly three docs files differ (`docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`): 66 insertions and 1 deletion measured at `81c8bfae1`, 67 and 1 after this correction adds the one log blank line. The deletion is that EOF newline marker. The union claim (both sides kept, no content lost) stands |
| `docs/reference/log.md` lines 11599 and 11600 had no blank separator (auto-merge consumed main's leading blank line) | One blank line inserted between them. One separator byte changes at the seam; earlier entries and main's block are otherwise unchanged, so the prior HEAD log is not a byte prefix of the corrected log |

The committed review already records the main-side EOF-newline exception and is unchanged. Preserved, not edited: the external result JSON, the original adverse process and review defects, the original critique and review artifacts, and corrections 1 and 2 of the AC-034 to AC-043 work. No pack or README change, no acceptance upgrade, tick, approval, issue change or log entry; #83 stays OPEN, six partial and four deferred stay. `origin/main` was not merged and PR 1495 was not merged. A new independent Review of the correction commit is recorded in the external result `rpi-134-evidence-correction-0012-result.json`; it found the 66 versus 67 count and an unescaped pipe, both fixed above by amending the unpushed correction commit afterwards, so the final head is not re-reviewed.
