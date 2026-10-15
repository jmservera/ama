---
title: Issue 160 chat thread storage changes
ms.date: 2026-10-15
---

* Added `chatthreads.py`; edited `store.py`, `sqlstore.py`, `mssqlstore.py`, `tests/test_mssqlstore.py`, `mvp/README.md`; added `tests/test_chatthreads.py`.
* Validation: full `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` gave 622 tests OK (92 skipped, MSSQL-gated); `test_chatthreads` 20 tests OK.
* Divergences: none. Message sequence is computed under the write transaction (no AUTOINCREMENT).
