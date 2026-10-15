# Issue 163 review fixes plan

Critique (inline, once): compatible; no conflict with confirmed decisions.

* [x] Add `chat_memory` DDL (SQLite and MSSQL) and repo memory methods in `chatthreads.py`; register in `mssqlstore.TABLES`.
* [x] Rework `ChatPrivacy` to use `store.chat_repo`, `chat_create_thread`, `chat_add_message`; remove own connection and DDL.
* [x] Tests on in-memory and SQL stores; portability tests (no INSERT OR/AUTOINCREMENT/PRAGMA, no own DDL).
* [x] Docs, index, log: state provider terms unrecorded and warning not wired; DPO items open.
* [x] Validate, commit, push, update PR title and body.
