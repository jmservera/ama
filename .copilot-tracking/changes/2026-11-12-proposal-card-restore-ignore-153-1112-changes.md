---
title: Issue 153 restore type ignore changes
ms.date: 2026-11-12
task_id: 153-restore-ignore-1112
---

* Restored `# type: ignore[no-untyped-call]` on the App construction (src/api/tests/test_case_journey.py:560). AST identical to a76417e8d; no other edit; no wrap needed.
* From src/api: canonical `mypy --no-incremental` exit 0 (236 files); unittest tests.test_case_journey 31 OK exit 0; ruff check and format --check exit 0. Local Python 3.12.3, mypy 2.4.1 (CI pins 2.4.0). Module origins are the worktree. File sha256 59ff02f8...0ef1b.
* Raw: /home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/153-restore-ignore-correction-1112. Not run: browser, full gates, hosted CI.
* Prior adverse records (timeout, format/type, hosted failure) and the earlier unauthorized unpublished metadata amend qualification stand.
