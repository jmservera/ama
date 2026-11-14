# Changes: #164 officer chat consent boundary (2026-11-14)

* `src/core/src/zava_forward/core/chat_case_answers.py`: added `AI_CONSENT` workflow rule naming the manual case-card path.
* `src/core/src/zava_forward/core/chat_isolation.py`: `ai_consent_state` reads `resident.ai_data_use_consent`.
* `src/core/src/zava_forward/core/chat_panel.py`: `consent_guidance` plus a guard in `_ask` and `ask_unstored`, after the out-of-scope refusal and before any prompt or model call.
* `src/api/src/zava_forward/api/web/chat.js`: unchanged; existing labels already render the reply.
* Added `src/api/tests/test_chat_consent_boundary.py` (17 tests incl. inherited role-matrix tests).
* Divergence: `src/api/.../api/chat.py` and `tests.test_chat` do not exist; logic lives in core and `tests.test_chat_panel` was run instead.
* Validation: `unittest tests.test_chat_consent_boundary` OK (17); with `test_chat_panel`, `test_chat_isolation` 122 OK; core `test_chat_case_answers`, `test_chat_panel` 64 OK; ruff check, ruff format --check, mypy clean. Tests ran with PYTHONPATH pointing at this worktree's `src/*/src` because the installed distributions point at another checkout. Refs #164, Refs #215.

## Cycle 1 correction (independent review f54cd0c5e)

* Fixed the Major E501 finding in `consent_guidance` (`chat_panel.py`) by splitting the `shown` expression; behaviour unchanged. The earlier 'ruff clean' statement above was inaccurate for the first commit.
* Re-validated: `ruff check .`, `ruff format --check .`, `mypy` exit 0 in `src/core` and `src/api`; `tests.test_chat_consent_boundary`, `tests.test_chat_panel`, `tests.test_accessibility_baseline` 103 OK (1 skipped); core `test_chat_panel`, `test_chat_case_answers` 64 OK. The Minor finding (only `Given` is consent) is an owner decision, no change. Refs #164, Refs #215.
