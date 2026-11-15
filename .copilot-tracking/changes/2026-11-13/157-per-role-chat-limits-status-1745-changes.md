---
title: Issue 157 per-role chat limits changes
ms.date: 2026-11-13
---

## Changes

* `chat_panel.py`: `role_limits()`, `all_role_limits()`, `MAX_THREAD_TURNS` (30), `THREAD_LIMIT_REACHED`; `_ask` falls back to workflow-only with zero model calls when the role bound is 0 or the thread turn cap is reached; receipt reports `calls_per_request`, `role_limits`, `thread_turns_used`, `thread_turn_limit`, `context_chars`, `history_chars`, `memory_used`.
* `server.py`: `/api/chat/status` adds `role_limits` (including Contractor and Application Administrator at 0), `your_role_limits`, `calls_per_request`, `turns_per_thread`.
* `chat.js`: limits note and usage note show the question cap and usage.
* `test_chat_panel.py`: three new tests.

## Validation

* api `test_chat_*` 106 OK, core `test_chat_*` 119 OK, `test_chat_widget_focus`, `test_content_standard`, `test_role_endpoint_inventory` OK; ruff and mypy clean (core and api) in /tmp/venv-157l-1745.
* Hosted CI and browser harness not run locally.
