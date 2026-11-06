---
title: Issue 79 details, continuation r13
ms.date: 2026-11-06
---

* Allowed diff: the merge commit (main content only) and new r13 changes, review and state files. No source, test, policy or old-record edit.
* Ref: `git branch preserve/issue-79-pre-r13-align 43080ab42a96fada36b9d0bc523dfa16fe0c3cd5` (local only).
* Merge: `git merge --no-ff origin/main`; on any conflict stop and report.
* Proof: `git diff HEAD~1.. --stat` against the first parent shows only main's paths; blobs of the 51 branch-changed paths compared between pre-ref and result.
* Checks (logs under a fresh `/tmp/79-align-r13-1106/`): unittest for `test_ranking_publication*.py`; pinned `ruff==0.17.1` check and format check and `mypy==2.4.0` from an external venv with `--cache-dir` under `/tmp`; `PYTHONDONTWRITEBYTECODE=1`.
