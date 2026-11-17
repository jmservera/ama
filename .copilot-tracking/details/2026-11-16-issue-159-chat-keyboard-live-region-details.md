---
title: Issue 159 phase details
ms.date: 2026-11-16
---

## Phase 1

* `chat-widget.js`: add `<small id="{id}-keys" class="chat-widget-meta">` with "Press Enter to send. Press Shift and Enter for a new line. Press Escape to close the chat." between input and tools; default `aria-describedby` on the input.
* `chat.js`: append `employee-chat-keys` to both employee `aria-describedby` assignments.

## Phase 2

* `test_assistant_panel_a11y_159.py`: expected describedby and hint text.
* `employee_chat_browser_check.py`: expected describedby, hint visible, Tab order.

## Phase 3

* `src/api/README.md` chat paragraph.
