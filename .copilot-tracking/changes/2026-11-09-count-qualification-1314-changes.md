---
title: SQL wave checkpoint comparison count qualification 1314 changes
ms.date: 2026-11-09
task_id: 1314-count-qualification-1109
---

## Changes

* `docs/architecture/cutover-evidence-pack.md`: appended 16 lines, a dated subsection "Comparison count qualification, 2026-11-09 (Refs #1314 #440)" (Q1 C2 scope count, Q2 preparation range composition and zero-deletion scope, Q3 byte-prefix wording limit), placed after the #1292 note and before the controls checkpoint heading.
* `docs/reference/README.md`: 5 lines appended to the SQL-wave checkpoint index entry.
* `docs/reference/log.md`: one entry appended at the end (5 lines including blank separator).
* New records: research, plan, details, critique (independent, Revise, PC-001 to PC-005 applied) and state under `.copilot-tracking/`.
* No source, fixture, policy, workflow, SQL, runtime or original RPI record changed.

## Validation (pure documentation, no gate, owner demo tier)

Baseline `efb2f7e0cd84b1e5983481055047272c2cc3db88`.

* `git diff --raw -M efb2f7e0 HEAD`: seven `A` entries (the new records) and three `M` entries (pack, index, log), 10 paths (the first version of this line said five, measured before the changes and review records were added; corrected by C1); no `D`, `R` or mode change. Every other path of the baseline keeps its blob.
* `git diff --numstat efb2f7e0`: pack 16/0, index 5/0, log 5/0. The log is a byte-prefix extension of the baseline (`cmp`); the index is not a byte prefix because the sentence is inserted inside the SQL-wave entry, with 0 deletions.
* Added relative links and the log anchor `#comparison-count-qualification-2026-11-09-refs-1314-440` resolve (script over lines added versus the baseline; no added link fails). Zero non-ASCII characters in added lines.
* Re-run on the pinned ranges (paths, totals, pack/index/log numstat): `ef28d4da4..f2e07999` 17 paths, +700 -0, 116/13/10 additions and 0 deletions; `ef28d4da4..ec597d023` 15 paths, +604 -0; `ec597d023..f2e07999` 3 paths, +107 -11 (state record rewritten); `06f408dd7..f2e07999` 11 paths, +258 -5 (index 4/1, rubric score 4/4); `f2e07999..53cef9040` 230 paths, +7058 -34, pack 154/0; `53cef9040..45e8744f` 6 paths, +90 -7 (pack 17/0, index 4/0, log 5/0; deletions in the preparation state record); `f2e07999..45e8744f` 234 files, +7141 -34, pack/index/log 171/4/5 with 0 deletions; `3a9767d5c..53cef9040` 22 paths, +848 -0, 116/13/10; `3a9767d5c..45e8744f` 24 paths, +931 -0, 133/17/15.

## Not run

Unit, browser, SQL and `rpi-checks` gates (pure documentation, owner demo tier). Hosted CI for this branch, independent exact-head review and publication are outside this local pass.
