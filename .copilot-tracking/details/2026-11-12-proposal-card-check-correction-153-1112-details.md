---
title: Issue 153 formatting and type-check correction details
ms.date: 2026-11-12
task_id: 153-check-correction-1112
---

* `tests/test_case_journey.py:560`: delete the trailing `# type: ignore[no-untyped-call]`.
* `ruff format` on `checks/assistants_browser_check.py` and `tests/test_content_standard.py` (the two files that failed; formatting only, mostly wrapping pre-existing lines).
* Semantic check: `ast.dump` of all three files is identical before and after.
