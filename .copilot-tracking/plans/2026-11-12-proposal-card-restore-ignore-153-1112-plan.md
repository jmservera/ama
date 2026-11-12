---
title: Issue 153 restore type ignore plan
ms.date: 2026-11-12
task_id: 153-restore-ignore-1112
---

1. Restore the original ignore comment on line 560 only.
2. From src/api: canonical mypy with no file list (--no-incremental, fresh cache), unittest tests.test_case_journey, ruff check and format --check on the file, AST equality against a76417e8d, final hash.
3. Commit as a new commit; no amend, rebase or push.
Critique: independent subagent critique requested before editing; outcome recorded in the details file.
