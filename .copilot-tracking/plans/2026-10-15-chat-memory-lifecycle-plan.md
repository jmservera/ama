# Plan: per-user memory lifecycle (#161)

* [x] 1. Schema: `item_class`, `source`, `updated_at` on `chat_memory`; `chat_memory_control` in both dialect hooks and the mssql table map.
* [x] 2. Repo: update/delete one item, get/set control (portable upsert); reject `CM-` ids as chat evidence.
* [x] 3. `ChatPrivacy`: opt_in, opt_out, memory_status, add/list/edit/delete/clear, set_global, set_task, prompt_memory, per-class retention statement, metadata-only audit.
* [x] 4. Tests `test_chat_memory.py` (in-memory and SQLite); adjust `test_chat_privacy.py` for opt-in.
* [x] 5. Docs: DPIA record section, log entry.

Critique (single, final candidate): global switch must hide but not delete items; edit must not extend expiry; withdraw must delete. All applied directly.
