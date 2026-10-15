---
title: Chat memory review fixes changes (PR 285)
ms.date: 2026-10-15
---

* Modified `mvp/zavaforward_mvp/chat_privacy.py`, `chatthreads.py`, `sqlstore.py`, `mssqlstore.py`.
* Modified tests `test_chat_memory.py` (task required, register role, expiry, migration) and `test_chat_privacy.py`.
* Modified `docs/reference/research/chat-memory-dpia.md` and `docs/reference/log.md`.
* Azure SQL ALTER is not executed in CI here (SQL Server tests skipped without a server).
