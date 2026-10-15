# Changes: per-user memory lifecycle (#161)

* `mvp/zavaforward_mvp/chatthreads.py`: columns, `chat_memory_control` DDL, repo methods, memory ids rejected as evidence.
* `mvp/zavaforward_mvp/chat_privacy.py`: lifecycle API, notice, classes, admin switches.
* `mvp/zavaforward_mvp/mssqlstore.py`, `mvp/tests/test_mssqlstore.py`: new table mapped.
* `mvp/tests/test_chat_memory.py` new; `mvp/tests/test_chat_privacy.py` opts in first.
* `docs/reference/research/chat-memory-dpia.md`, `docs/reference/log.md`.

Divergence: no registry-dict flag (would alter registry hash); per-task switch is a control row.
