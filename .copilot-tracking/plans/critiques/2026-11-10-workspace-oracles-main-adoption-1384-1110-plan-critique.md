---
title: Issue 1384 main adoption plan critique
description: Single critique of the main adoption plan with dispositions
ms.date: 2026-11-10
ms.topic: reference
---

## Execution

* One critique, executed once on the final candidate plan, details and research by an independent read-only rubber-duck agent. Verdict: Revise (four blocking findings, all compatible with confirmed decisions). No user decision needed. Not repeated.

## Findings and dispositions

* Witness order: `review-done` must be recorded while the merge is staged, before the merge commit, otherwise the reviewed snapshot is empty and the binding vacuous. Applied: plan Phase 4 and details now record implement-done, Review and review-done before `git commit`.
* Merge parents: committing tracking artifacts first makes the tracking commit the first parent. Accepted and stated: `3f1fa48` remains an ancestor, as required; the merge's parents are the tracking commit and `111847191`. Applied in details.
* Commands: `$V` was a directory; the employee-chat check requires `--axe` and `--out`. Applied: `$P=$V/python`, explicit pinned axe copy and output path. The axe file is a byte copy of an existing local copy matching the check's pinned SHA-256.
* Evidence path: `ROOT` was undefined and must be absolute and outside the worktree. Applied: defined in details.
* Critic note: loader-derived expectations are not alone behavioural proof; the real-loader unit test and browser mutation controls supply independent checks. No change.
