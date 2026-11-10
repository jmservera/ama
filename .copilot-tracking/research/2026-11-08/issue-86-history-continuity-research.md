---
title: Issue 86 history continuity research
description: Why published 6ff492ad is not an ancestor of the reviewed head and what a normal merge must prove
ms.date: 2026-11-08
---

Scope: issue #86 only, history and records only. Head `a8efb903`, tree `ef583897`; Main `0f05e9aa`; published parent `c5edb320`; PR 1243 head `6ff492ad` (base `feat/controlled-lifecycle-integration-81`). Ancestry exit 1 for `6ff492ad` to HEAD; merge-base is `c5edb320`; six commits are in `HEAD..6ff492ad` (all authored by the noreply identity). `git cherry` reports all six as not patch-equal, because local history rewrote them (`3dd0ae3f`, `91c8c5f6`) before later corrections.

## Findings

* The `c5edb320` to `6ff492ad` source delta is five files: `core/README.md`, `complaints_route.py`, `resident_decisions.py`, `store.py` and `tests/test_resident_decisions.py`. Each is byte-identical to the same path at local commit `91c8c5f6`, an ancestor of HEAD that was then corrected by `2eda7691` and merged with the parents and Main.
* All 14 `.copilot-tracking` files in that delta have identical blobs at HEAD.
* A trial `git merge-tree --write-tree HEAD 6ff492ad` (disclosure: may write loose objects) conflicts in README, `complaints_route.py` and `resident_decisions.py`, since both sides edited the same lines. A conflict-resolving merge would require choosing code by hand, which is not authorised. A normal merge recording both parents with the tree of HEAD (`-s ours`) keeps the reviewed source and drops no content, because the incoming source is a strict earlier version and the incoming records already exist.

## Proof required before and after merging

Unchanged `src`, `tools`, `infra`, `.github` trees equal `a8efb903`; the whole tree equals `ef583897`; `6ff492ad`, `c5edb320`, `e888a499`, `0f05e9aa` and `a8efb903` are all ancestors of the result (explicit exit codes); `git diff --check`; metadata JSON parses; ignored-inclusive clean.

## Qualifications for current use

* The earlier whole 108-class run failed (one test); B1 and B2 were single-method baselines; the fix was checked by 3, 45 and 21 test runs, and the 108 class was not rerun after the fix.
* Plan wording "already run" in `issue-86-sql-fixture-plan.md` refers to the earlier historical run, not a rerun after the fix.
* A stable `route_key` is not receiver-side duplicate suppression or cross-process proof.
* #1238 and the remaining approvals stay open. The resident no-detriment criterion stays unmet.
