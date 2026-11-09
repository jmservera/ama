---
title: Issue 86 history continuity changes
description: Normal merge of published 6ff492ad keeping the reviewed source, with proofs and a current-use amendment
ms.date: 2026-11-08
---

Scope: issue #86 only. Prospective research and plan committed first as `6a7a4542`. Merge commit `aa79eec0` (parents `6a7a4542` and `6ff492ad`, tree `735ec563`, identical to its first parent) used `-s ours`: a conflict-resolving merge conflicted in README, `complaints_route.py` and `resident_decisions.py`, and the incoming source equals the earlier local ancestor `91c8c5f6` (later corrected by `2eda7691`), so no incoming content is dropped.

## Observations (historical source equivalence, not test execution)

* `src`, `tools`, `infra`, `.github` trees equal `a8efb903`; the only paths changed from `a8efb903` are under `.copilot-tracking`.
* Ancestry exit 0 for `6ff492ad`, `c5edb320`, `e888a499`, `0f05e9aa`, `a8efb903`. Main and the parent ref and PR 1243 head were unchanged.
* `git diff --check` exit 0; rubric JSON parses; ignored-inclusive clean. The trial `merge-tree` may have written loose objects. No test was run on the final head.

## Current-use amendment (originals unchanged)

* The 108-class `MssqlResidentControls` run failed once; B1 and B2 were single-method baselines; the fix was checked by 3, 45 and 21 test runs. The whole class was not rerun after the fix. "Already run" in the fixture plan means that earlier historical run.
* A stable `route_key` is not receiver-side duplicate suppression or cross-process proof.
* #1238, remaining approvals and the resident no-detriment criterion stay open.
