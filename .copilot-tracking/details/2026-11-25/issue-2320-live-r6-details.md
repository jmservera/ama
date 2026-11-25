---
title: Issue 2320 live r6 details
ms.date: 2026-11-25
---

* `mssqlstore.py`: `BEGIN` text takes `{timeout}`; `_Conn._begin` formats with the thread-local override or 15000.
* `store.py`: `Store.BRIEFING_WRITE_WAIT_MS = 2000`; `write_wait` default `nullcontext`; briefing recording wrapped.
* Tests: `src/api/tests/test_mssqlstore.py` (or core) for BEGIN timeout; `test_assistant_release.py` for briefing.
