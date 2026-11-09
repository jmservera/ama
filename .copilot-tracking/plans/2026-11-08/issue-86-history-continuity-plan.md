---
title: Issue 86 history continuity plan
description: One normal two-parent merge keeping reviewed source, with proofs and stop conditions
ms.date: 2026-11-08
---

Scope: issue #86 only. Validation tier: history and record-only under the owner CI-first policy; no FULL, SQL, browser, image, scan or broad suite and no heavy lock.

1. Commit this research, plan and details first.
2. Re-fetch and stop on drift of Main, parent ref or PR head.
3. `git merge --no-ff -s ours 6ff492ad` with a message that states the rationale; no rebase, reset, cherry-pick or force.
4. Prove tree equality, the ancestry set, `git diff --check`, JSON parse of `.github/rubric/scores/latest.json`, and ignored-inclusive clean.
5. Write changes, a current-use amendment of the earlier records (appended, originals unchanged) and one author Review; commit.

Stop if drift occurs, the proof fails or the result tree differs from `ef583897`.

Not claimed: no product logic change, no hosted CI for the new head, no approval, tick, closure or push. Refs #86 and #1238 only.
