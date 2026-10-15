# Issue 163 review fixes changes

* `chatthreads.py`: `chat_memory` DDL, `MEMORY_COLS`, memory methods on both repos. `mssqlstore.py`: `chat_memory` table.
* `chat_privacy.py`: runs through #160 chat repository (owner column); no `chat.sqlite`, `sqlite3` or own DDL. API now takes the user dict.
* `test_chat_privacy.py` rewritten for both stores plus portability tests; `test_mssqlstore.py` table list.
* Docs, index and log: limits stated (provider terms unrecorded, warning not wired into any UI).
* Divergence: MSSQL path not run locally (needs ZF_TEST_MSSQL).
