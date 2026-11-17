---
title: Issue 159 changes
ms.date: 2026-11-16
---

## Changed files

* src/api/src/zava_forward/api/web/chat-widget.js
* src/api/src/zava_forward/api/web/chat.js
* src/api/tests/test_assistant_panel_a11y_159.py
* src/api/checks/employee_chat_browser_check.py
* src/api/README.md

## Validation (focused tier; local only)

* Unit: `test_assistant_panel_a11y_159 test_chat_widget_focus test_chat_panel test_accessibility_baseline test_ui_support` 95 OK (PYTHONPATH to worktree sources, because the installed editable distributions point at another checkout).
* `checks.employee_chat_browser_check` with pinned axe 4.10.3: pass (rc 0).
* `checks.chat_widget_browser_check`: employee stages pass; resident stage fails identically at base 5e0c7f744 (pre-existing).
* ruff check/format and mypy on touched Python: clean.

## Not done

Manual screen-reader testing (human gate), hosted CI, full local gate (not required in focused tier).
