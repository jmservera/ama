---
title: Details for issue 2245 round 2
ms.date: 2026-11-23
---

Phase 1: in `ErrorLoggingTests` after `test_busy_sql_write_lock_on_chat_thread_create_answers_503_with_retry_after`, patch `chat_create_thread` to raise a `ProgrammingError` ("Invalid object name") and assert `(500, no Retry-After)` and a `status=500` log line. Validation: `python3 -m unittest` for the module, `ruff check`, `ruff format --check`, `mypy`.
