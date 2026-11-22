# Details: issue 2245 chat ask timeout

* Phase 1: in `ensure`, after computing `configuration`, build `seeded = (label, configuration, CALLS, TOKENS, AMOUNT)`; return True when `ledger.demo_chat_seeded == seeded`; set the attribute only after both ledger writes succeed. Test in `src/core/tests` using a fake store whose ledger counts `price` and `authorize` calls.
* Phase 2: `python3 -m unittest` for the new test and `src/api/tests/test_chat_panel.py`; `python3 -m mypy` in `src/core`; `python3 -m ruff check`.
* Phase 3: note `docs/reference/research/issue-2245-chattimeout-2026-11-22.md`; index row in `docs/reference/README.md`; append `docs/reference/log.md`.
