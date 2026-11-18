# Changes: unblock/visit chat grounding

* `src/core/src/zava_forward/core/chat_case_answers.py`: widened `unblock` intent.
* `src/api/src/zava_forward/api/web/chat.js`: origin token in footer detail.
* `src/api/tests/test_chat_panel.py`: two regression tests.
* Validation (PYTHONPATH pointed at worktree): api test_chat_panel, test_chat_consent_boundary, test_accessibility_baseline (rc=0); core `test_chat_*` 128 OK; mypy core and api clean; ruff check clean. `ruff format --check` flags only pre-existing `src/check-container.py`.
* Not run: full local RPI gate, hosted CI, browser harness. Tier: focused. No push.
