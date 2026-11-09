---
title: SQL wave checkpoint comparison count qualification 1314 details
ms.date: 2026-11-09
task_id: 1314-count-qualification-1109
---

## Phase details

* P1 `git status --short` shows only the five prospective records (research, plan, details, critique, state) before the commit; commit with the repository-local privacy email and the Copilot trailer.
* P2 Source of every number is `git diff --name-only <a> <b>` and `git diff --numstat <a> <b> -- <paths>` between the pinned commits named in the research. The pack subsection follows the style of the existing dated qualification subsections (intro paragraph, table with Id, Qualification, Evidence, closing paragraph with the not-claimed list). Ids Q1 (C2 scope count), Q2 (preparation range composition and zero-deletion scope) and Q3 (byte-prefix wording limit). Link the records in this lane by relative path.
* P3 Index: one sentence appended to the SQL-wave entry after the existing sentences, ASCII only. Log: one `update` entry at the end, in the existing format, with a `Not claimed` line.
* P4 Commands: `git diff --name-only` and `--numstat` (whole tree and pack, index, log) for `ef28d4da4..f2e07999`, `ef28d4da4..ec597d023`, `06f408dd7..f2e07999`, `ec597d023..f2e07999`, `f2e07999..53cef9040`, `53cef9040..45e8744f`, `f2e07999..45e8744f`, `3a9767d5c..53cef9040` and `3a9767d5c..45e8744f`; `cmp` byte-prefix tests of index and log against `f2e07999`; `git diff --raw -M efb2f7e0 HEAD` must list only `A` entries plus `M` for pack, index and log, whose numstat has 0 deletions; for every path in `git ls-tree -r efb2f7e0` the blob id at HEAD equals the baseline except those three; a Python script checks relative links and anchors added by this lane, and failures present at `efb2f7e0` (the original preparation record notes pre-existing broken links in the log) are compared against that baseline, not treated as regressions.
* P5 Changes record lists the commands, outputs and file inventory. Review is one authored pass after implementation (independent exact-head review is the coordinator's later step).

## Constraints

* Plain ASCII, `*` lists, no em dashes, no bold-prefix list items.
* Do not edit any earlier record; do not copy the parent worktree's uncommitted files.
