# Details: issue 2245 live

Phase 1: edit src/core/src/zava_forward/core/chat_panel.py `finish` to loop the `chat_add_message` call on lock-busy.
Phase 2: test in test_chat_panel.py.
Phase 3: validation (unittest chat tests, mypy, ruff check and format --isolated --line-length 100 --check).
Phase 4: docs and records.
