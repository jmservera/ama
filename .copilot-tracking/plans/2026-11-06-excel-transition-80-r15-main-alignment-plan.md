---
title: Issue 80 r15 plan, ancestor alignment to advanced main
description: Plan for a local no-ff merge of current origin/main into the issue 80 topic with light checks only
ms.date: 2026-11-06
---

* Research: [r15 research](../research/2026-11-06-excel-transition-80-r15-main-alignment-research.md). Details: [r15 details](../details/2026-11-06-excel-transition-80-r15-main-alignment-details.md).

## Phases

* [ ] Phase 1: commit research, plan, details and the one independent plan critique before any alignment.
* [ ] Phase 2: create a lightweight local tag preserving the pre-alignment head, re-fetch, confirm origin/main and the parent branch are still 56eec736 (stop on movement), then `git merge --no-ff` origin/main with a Conventional Commit message.
* [ ] Phase 3: prove ancestry and blob equality, then run light focused checks in an owned external environment.
* [ ] Phase 4: write Changes, a separate author Review and state, commit them, and freeze.

* Critique: one independent rubber-duck critique executed; verdict Proceed with changes. Both blocking items (anchor first-parent proof to the merge commit's actual pre-merge head; compare the incoming file blob to origin/main and stop on any failed proof) and the policy-neutrality qualification were applied directly to details and research. No decision conflicts with user direction.

## Limits and stop conditions

* Stop on any merge conflict, unexpected branch movement, or a non-tracking path changed beyond the merged main file.
* No rebase, push, PR, retarget, FULL, SQL, browser, image or scan. Prior receipts are unchanged and are not carried to the new head.
