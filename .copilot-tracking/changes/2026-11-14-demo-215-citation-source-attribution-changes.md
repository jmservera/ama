# Changes: #215 citation and source-origin attribution (2026-11-14)

* Added `src/api/tests/test_alert_chat_citation_source_attribution_215.py` (18 tests).

Validation (from `src/api`, `PYTHONPATH=../core/tests:../agents/tests`): new test OK; `test_alert_chat_*.py` 115 OK; `test_*regulatory*.py` 68 OK; `test_*grounded*` matches no files (none exist); `ruff check`, `ruff format --check`, `mypy` clean.
Not run: hosted CI, complete local gate (focused tier, test-only). No push.
