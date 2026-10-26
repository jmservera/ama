<!-- markdownlint-disable-file -->
---
title: Issue 350 current-main readiness changes
description: Changes made by the current-main readiness continuation
ms.date: 2026-10-25
---

* Merged `origin/main` `ea5577b2` into the branch with merge commit `01bee57e` (parents `ec9d4d92` and `ea5577b2`). No conflicts, no source edit, no rebase, amend or force.
* Added the readiness research, plan, details, critique (before the merge, in commit `ec9d4d92`), and this changes record, the review and the state file (after).
* Actual order: lifecycle inspection, research, plan and details, critique (Revise), plan commit `ec9d4d92`, merge, focused checks, one scoped assessment (non-conformant, corrections recorded), records.
* Candidate gate readiness: the merged tree has the focused checks passing, but the old receipt for a9bdae31 no longer covers the head and every later commit changes it. A fresh complete `tools/rpi-checks.py --all --base ea5577b2... --lock-timeout 14400 --out <new dir>` and `--verify-receipt` are still required. The last full gate used several GB for Docker images and venvs; disk now is 22 GB free (92 percent), which is likely enough for one gate but should be rechecked and the retention policy applied before starting it. Not run here.
* No push, PR or issue edit, acceptance tick or closure.
