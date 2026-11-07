---
title: Issue 79 research, r21 merge of main a1d26534
ms.date: 2026-11-07
---

Task `issue-79-r21-merge-main-1252`, parent `issue-79-r20-merge-main-1253`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: `feat/ranking-publication-runner-79`, head `9b21a6a0d2bc0646076cd2da03f7fc4d088af06e`, tree `5d571a4a0215aac35638509a5672638bee0fa98c`, ignored-clean; PR 1239 open, base `main`, remote head `181a1c1bb`. Child 1231 is not touched.
* `origin/main` is `a1d265340ba7d6f14b24e028362b2d5f4bb80126`, PR 1252 squash merge (issue 1251). It descends from the previously merged `395060275`. Scorer run 42381926533 on `a1d265340` is `completed`/`success`; no score-only descendant exists at fetch time.
* Delta against previous main `395060275` (15 paths): modified `tools/backlog-sync.py` (blob `8c82130c5` to `43338cb8f`) and `tools/test_backlog_sync.py` (`c0b5e3b6b` to `fca73c2cd`); 13 added issue 1251 RPI records plus `.copilot-tracking/github-issues/issue-1251.md`. No `src` production, schema, workflow, log or score path.
* Overlap with topic-changed paths: none, so the merge is expected to be conflict-free. `git merge-tree` reports a clean tree.
* Preserve ref `preserve/issue-79-pre-main1252-merge` at the start head.
* The three 357e842d Medium findings stay author-corrected only, not independently confirmed.

## Conclusions

* One normal merge of exactly `a1d265340` is safe and keeps all history. Whole 107 and the other open gaps are unchanged.

## Limits

* No FULL, SQL, browser or heavy lock. The incoming tools test is run only if it is light and needs no service; otherwise recorded as not run.
