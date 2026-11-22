# Details: issue 2245 thread creation 500

Phase 1: test uses `store.db.set_trace_callback` on the SQLite-backed `SqlStore` and counts `BEGIN` statements during `chat_create_thread`; bound 2 (insert and audit). Verification: 28 tests in `test_chatthreads` pass.
Phase 2: note carries probe results (`issue-2245-thread500-2026-11-22/`), the console log evidence, and a per-criterion table. Phase 3: git status clean after commit.
