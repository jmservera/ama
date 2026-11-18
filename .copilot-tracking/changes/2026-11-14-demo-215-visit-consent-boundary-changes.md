# Changes: #215 visit consent boundary (2026-11-14)

* `src/core/src/zava_forward/core/chat_case_answers.py`: `_unblock` names resident consent/access confirmation and independent safety sign-off.
* Added `src/api/tests/test_alert_chat_visit_consent_boundary_215.py` (16 tests including inherited role-matrix tests).
* Narrowed `CLAIMS` in the unblock-grounding and stabilization sibling tests.
* Validation run: focused unittest OK; sibling and `test_chat_case_answers.py` 72 tests OK; ruff check; ruff format --check; mypy on the new file.
* Not run by design: complete gate, live model, browser, screen reader. Refs #215.
