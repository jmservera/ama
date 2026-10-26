<!-- markdownlint-disable-file -->
---
title: Issue 350 main c8d16059 integration plan critique
description: One independent pre-merge critique
ms.date: 2026-10-26
---

Execution: complete, once, read-only `rubber-duck`, after the research, plan and details and before the merge. Verdict: **Revise**. Blocking 0, non-blocking 2, suggestions 1. `git merge-tree` confirmed a clean predicted merge.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-401 | Non-blocking | Focused-test commands were not executable as specified: no repo-root `tests`, `python` not on PATH, resident tests live in `src/core/tests` and `src/api/tests`. | Applied at execution, not by amending the plan or details (which stay as written): use the explicitly discovered existing interpreter, run from `src/core` or `src/api` or `tools` as applicable, and record interpreter path, `zava_forward.__file__` and `sys.path`. An installed path outside the merged worktree is a recorded stale-environment limit, not evidence for the merged tree. |
| PC-402 | Non-blocking | Residual evidence risks need to be explicit closeout requirements. | Applied: the review brief and final report must state RV-001 fixture provenance unresolved, historic process gaps not retroactively closed, checker output offline and non-acceptance, merge readiness is not issue acceptance. |
| PC-403 | Suggestion | Require `origin/main == c8d16059` after fetch before merging; conflict handling is contingency only. | Accepted. If main moved, stop and re-plan. |

Preserved by the reviewer's assessment: RecursionError and Application Administrator handling stay unchanged; `980` open-case baseline is distinct from 443 open and 980 total; disk 6.8 GB limit and no-install, no-gate scope are honest.
