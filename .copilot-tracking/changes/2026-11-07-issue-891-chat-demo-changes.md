---
title: Issue 891 chat demo changes
description: Change record
ms.date: 2026-11-07
---

* `src/api/src/zava_forward/api/web/chat.js`: disclaimer note placed above the scrollable intro; stray statement line fixed.
* `src/api/src/zava_forward/api/web/chat-widget.css`: `.chat-widget-demo-note`.
* `src/api/checks/employee_chat_browser_check.py`: demo scenario with status and model answer interception.
* `src/api/tests/test_chat_panel.py`: gates-in-force regression.
* `src/api/README.md`, `docs/reference/research/chat-demo-storage-approval-2026-11-01.md`, `docs/reference/log.md`.
* Validation so far: `test_chat_panel` (53 ok), isolation/continuity/widget/workspace scripts (71 ok), employee chat browser check PASS.
* Divergences: none. Live check not performed (blocker in details).
