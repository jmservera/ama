---
title: Issue 1231 r21 phase details
description: Prospective phase details for the r21 parent79 b8ad4a0e merge
ms.date: 2026-11-07
---

* Backup: `git branch backup/issue-1231-8d235-pre-r21-merge 8d2350a5eda4f1ff41e418cabb51c01f81c7d883`.
* Merge: `git merge --no-ff` of b8ad4a0e with Refs #1231 and the Copilot trailer.
* Proof: `git diff --raw 0a8ecd50 b8ad4a0e` vs `git diff --raw 8d2350a5 HEAD` excluding .copilot-tracking; `git diff --name-only 8d2350a5 HEAD` outside .copilot-tracking must be exactly the two incoming paths; `git diff --raw` of src, tools and .github/workflows empty; every start .copilot-tracking blob unchanged (`git diff --diff-filter=DM --name-only`); log.md zero deleted lines; `git merge-base --is-ancestor 23b26a7f HEAD`.
* Checks: JSON parse of latest.json and `git diff --check` with real exit files; no suites.
