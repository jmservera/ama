# Changes: #215 badge contrast tokens (2026-11-14)

* Added `src/api/tests/test_alert_chat_provenance_badge_contrast_tokens.py` (10 tests).

Validation (from `src/api`, `PYTHONPATH=../core/tests:../agents/tests`): new test OK; `test_*accessibility*` 34 OK; `test_*regulatory*` 68 OK; `test_*alert_chat*` 97 OK; `ruff check`, `ruff format --check`, `mypy` clean.
Not run: hosted CI, complete local gate (focused tier, test-only). No push.
