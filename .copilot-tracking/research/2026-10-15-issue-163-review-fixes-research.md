# Issue 163 review fixes research (PR 281)

Planning Readiness: Ready. Disposition: executed (local code reading).

* Finding 1: `chat_privacy.py` made its own `chat_thread`/`chat_message` (user_key, role, task, at). The merged #160 repository (`chatthreads.py`) owns those tables: `owner`, `owner_role`, `rowversion`, composite `(thread_id, seq)`. Only `chat_memory` is new.
* Finding 2: separate `chat.sqlite`, bare `sqlite3` and string-built DDL. Stores already expose dialect hooks: `SQLITE_DDL`/`MSSQL_DDL` in `chatthreads.py`, wired by `sqlstore._create_schema` and `mssqlstore.TABLES`.
* Finding 3: provider terms not retrieved; warning not wired into any UI; lawful basis, notice and DPIA decision stay with the DPO (Juan Manuel Servera).
