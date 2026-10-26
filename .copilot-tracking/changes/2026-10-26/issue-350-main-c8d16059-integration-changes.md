<!-- markdownlint-disable-file -->
---
title: Issue 350 main c8d16059 integration changes
description: Changes made by this continuation
ms.date: 2026-10-26
---

* Merged `origin/main` `c8d16059` (#455 resident preview) into the branch as merge commit `938283a3` (parents `8dbac283`, `c8d16059`); no conflicts, no source edit, no checker, app, auth, default or fixture change, no rebase, amend or force.
* Prospective research, plan, details and critique (Revise) committed in `8dbac283` before the merge; this changes record, the review and the state were added after.
* Order: lifecycle inspection, research, plan and details, critique, commit, merge, focused tests, review.
* Candidate gate readiness: the merged head needs a fresh `tools/rpi-checks.py --all --base c8d16059c0c0a22c4ffba88c6b65ac068f64accc --lock-timeout 14400 --out <new external dir>` and `--verify-receipt`; #360 holds the heavy gate and disk is 6.8 GB free, so it is not started. Push, PR body and issue actions are not done.
