---
title: Issue 160 chat thread storage plan
ms.date: 2026-10-15
---

* Add `mvp/zavaforward_mvp/chatthreads.py`: one `ChatMixin` service over a memory repository and a SQL repository.
* Mix into `Store`; add `chat_thread` and `chat_message` DDL to `SqlStore._create_schema` and `MssqlStore.TABLES` (idempotent, additive).
* Owner-filtered list, resume, archive, delete; thread rowversion with `ConflictError`; ledger events carry metadata only.
* Tests: `test_chatthreads.py` on memory and SQLite, `MssqlChatThreads` gated on ZF_TEST_MSSQL; portability scan; MSSQL wipe list.
* Docs: mvp/README section. No knowledge-base file changes, so no index or log entry.
* Critique (single pass): keep the slice storage-only; no model calls or memory; compatible findings applied directly.
