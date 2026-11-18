---
title: Issue 215 plain-language mode correction cycle 2 changes
---

* Added `src/api/src/zava_forward/api/plain_language.py`; modified `server.py`, `web/chat.js`, `docs/reference/research/ux/wcag-conformance-baseline.md` and `docs/reference/log.md`.
* Tests: added `tests/test_home_chat_api.py`; extended `test_regulatory_chat_api.py` and `test_accessibility_baseline.py`; updated pinned markup in `test_regulatory_a11y_cues.py` and `test_alert_chat_role_wcag_plain_matrix.py`.
* Validation (in `src/api`, `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src`): `test_home_chat_api test_accessibility_baseline test_connected_home_check test_role_screens_conformance` 59 tests OK; `test_regulatory_a11y_cues`, the alert/chat matrix, `test_regulatory_chat_api`, `test_chat_panel` and `test_case_journey` pass; `mypy`, `ruff check .` and `ruff format --check .` are clean.
* Not verified: `test_chat_isolation` and `test_chat_fixture_roles` fail to import `chat_fixture` (environment, unrelated); `regulatory_ux_check.py` was not run (no browser run); full `src/api` discovery was not repeated.
* Divergence: the requested `chat.py`, request classes and `static/` path do not exist; the server endpoints and `web/chat.js` were used. Employee chat sends the flag for stored and unstored asks (case context travels as `case_id`).
