---
title: Issue 153 restore type ignore details
ms.date: 2026-11-12
task_id: 153-restore-ignore-1112
---

Plan critique: independent rubber-duck subagent, run before any edit. Verdict pass, no blocking findings; non-blocking note: local mypy is 2.4.1 vs CI pin 2.4.0, and narrow file-list runs are not equivalent. No critique repeat. Edit: line 560 of src/api/tests/test_case_journey.py only.
