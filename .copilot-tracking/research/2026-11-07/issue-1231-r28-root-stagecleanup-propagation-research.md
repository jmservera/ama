---
title: Issue 1231 r28 research, root stage-cleanup masking correction propagation
description: Evidence for adopting root bb7e044c into the child without duplicating the child's stage cleanup
ms.date: 2026-11-07
---

Task `issue-1231-r28-root-stagecleanup-propagation`, parent task `issue-1231-r26-parent-dirsync-alignment`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: child HEAD `4ec4c28030528e2550d98864defa44d1eae5b7d6`, tree `3c63e15cb8e17a50ca3e4edc1992a69b4286ad3e`, ignored-inclusive clean. Declared PR #1242 target remains `feat/ranking-publication-runner-79`. `origin/main` `23b26a7f3a4693cd20dcf0447303d97491096cb3` (fetched; it may move before FULL).
* Root worktree `issue-79-publisher`: `bb7e044c33d7f3670ad293ae9e3ff0cae2a801fc`, tree `430c07c72607f6d8cb91bb5c245067724c45feaa`, ignored-clean, read only. It descends from `fd57f086` (the merge-base with the child). Root delta over fd57f086 (11 paths): five r25 RPI records plus state, a 4-line `docs/reference/log.md` append, `ranking_publication.py` (adds `_remove`, `stage_retained` on result and error), core README (+2 lines), core test (+2 tests, one changed source-text assertion), API test (+1 test).
* Root High finding: a failing stage unlink in the `finally` masked `DurabilityUnconfirmedError`, so Store skipped the unconfirmed audit and the API returned 403.
* The child already contains the same mechanism: non-throwing `_remove(stage)`, `stage_retained` on result and error (via `_confirmed`), Store retained-stage warning and the specific unconfirmed handler. The child's retained-stage test on the typed error and the r26 API test cover retained stage, audit and 409.
* Dry-run `git merge-tree` over bb7e044c: four content conflicts, in both test files, the core README and `ranking_publication.py`.
* Root tests select the stage by the name prefix `.publishing-`. The child's stage is `.<record>.<random>.tmp`, so those tests, merged unchanged, would not trigger their fault.
* Out of scope: #1258 (archive ancestor fsync) and #1259 (unusable archive window); not edited.

## Conclusions

* Keep the child's `publish`, `_remove` and `_confirmed`; do not copy the root body or fold anything else into the root.
* Adapt the adopted root tests to the child's stage names so each exercises its real fault; drop only what is demonstrably duplicate after running them against the child, and record which.
* Use one ordinary `--no-ff` merge, not a rebase: the child's history includes merges r16 to r26 and PR #1242 commits, and a rebase would rewrite them and need a force push. This departs from the coordinator's "authorized local rebase" wording only in choosing the merge form; recorded in the changes file.
