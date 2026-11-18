# Changes: #215 doubt route and no-source held-state parity (2026-11-14)

* Added `src/api/tests/test_epic215_doubt_route_held_state_wcag_parity.py` (10 tests): 7 static UI contract tests and 3 runtime tests over all 7 `STAFF_ROLES` roles (no-source turn, cited answer, invalid doubt input) with zero controlled-record mutation checks.
* No product code changed.
* Validation run: focused unittest OK (10 tests); ruff check; ruff format --check; mypy shows no error in the new file. Three pre-existing `unused-ignore` mypy errors remain in sibling `test_alert_chat_*_215.py` files (same at HEAD, untouched).
* Not run by design: complete gate, browser, screen reader. Refs #215.
