---
title: Issue 157 per-role chat limits plan
ms.date: 2026-11-13
---

## Plan

* [ ] 1 chat_panel.py: add `ROLE_LIMITS` (7 staff roles: 1 call per request, 30 turns per thread, 600 output tokens; Contractor and Application Administrator: 0 calls, access refused), `role_limits()`, `MAX_THREAD_TURNS`, and `THREAD_LIMIT_REACHED` text.
* [ ] 2 chat_panel.py `_ask`: fallback to workflow-only without a model call when role cap is 0 or the thread already holds `MAX_THREAD_TURNS` user turns; receipt reports `calls_per_request`, `role_limits`, `thread_turns_used`, `context_chars`, `history_chars`, `memory_used`.
* [ ] 3 server.py `/api/chat/status`: add `calls_per_request`, `turns_per_thread` to `limits`, and `role_limits` for every role.
* [ ] 4 chat.js: limits note mentions the per-conversation turn cap and role cap.
* [ ] 5 Tests in test_chat_panel.py; run suites, ruff, mypy, content standard.

Details: see details file.
