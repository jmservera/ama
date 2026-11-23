---
title: Details for issue 2245 plan
ms.date: 2026-11-23
---

Phase 1: add `test_busy_sql_write_lock_on_thread_create_answers_503` and `test_busy_sql_write_lock_on_other_post_still_answers_500` using `ErrorLoggingTests`; patch `store.chat_create_thread` to raise the driver-shaped busy error.
Phase 2: `_unhandled` condition becomes `method in ("GET", "HEAD") or (method == "POST" and path == "/api/chat/threads")`.
Phase 3: update the 2237 comment, write the research note under docs/reference/research/, update the research index and the knowledge-base log.
