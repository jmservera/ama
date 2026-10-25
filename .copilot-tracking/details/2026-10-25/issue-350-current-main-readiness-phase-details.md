<!-- markdownlint-disable-file -->
---
title: Issue 350 current-main readiness phase details
description: Prospective phase details for the merge and focused checks
ms.date: 2026-10-25
---

* Phase 1: dispatch one read-only `rubber-duck` with the research and plan paths; record its verdict in `reviews/plans/2026-10-25/issue-350-current-main-readiness-plan-critique.md` before the merge.
* Phase 2: `git merge --no-ff origin/main` on the branch with the repository-local noreply identity and the Copilot trailer; then verify `git merge-base --is-ancestor` for both `origin/main` and `origin/test/deployed-feedback-harness-350`.
* Phase 3: `PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -m unittest tools.test_check_demo_feedback` from the repo root; confirm the deep-nesting and Application Administrator regressions run by name. Confirm the venv holds the merged `src/core` (editable or fresh copy), otherwise rebuild from `git archive` under `/tmp` and delete it afterwards. Remove any `__pycache__` or egg-info before the final status check.
* Phase 5: scoped read-only `rubber-duck` over the merge commit diff against main and the branch, the two named tests, and the RV-201 wording in the critique file.
* Phase 6: commit the changes, review and state records; report candidate gate readiness and expected disk needs.
