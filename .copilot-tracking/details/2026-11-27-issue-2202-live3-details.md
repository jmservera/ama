---
title: Issue 2202 live3 details
---

Phase 2: `_retry_lock_busy(save)` loops up to `SAVE_LOCK_RETRIES` extra attempts while `is_write_lock_busy(exc)`; other errors raise at once. The question save is `store.chat_add_message(user, tid, "user", masked)` inside `with store.lock` after the thread and prior-turn reads, so only that call is retried.
Phase 3: generalise `lock_busy_saves` with a `role` argument; assert 3 calls after two failures and re-raise after exhaustion.
