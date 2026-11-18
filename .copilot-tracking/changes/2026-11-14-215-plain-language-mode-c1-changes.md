---
title: Issue 215 plain-language mode correction cycle 1 changes
---

* Modified `src/api/src/zava_forward/api/web/chat.js`, `tests/test_regulatory_a11y_cues.py`, `tests/test_alert_chat_role_wcag_plain_matrix.py` and `docs/reference/log.md`.
* Validation: `test_case_journey` (the status-lookup regression is gone), `test_accessibility_baseline`, `test_regulatory_a11y_cues`, the alert/chat matrix and keyboard provenance tests pass; mypy, `ruff check` and `ruff format --check` in `src/api` are clean with `/tmp` caches. `regulatory_ux_check.py` now sees one `[role=status]` in `#regulatory-alerts` but was not run (no browser run in this cycle).
* Full `src/api` discovery (2892 tests) still shows 268 failures and 147 errors that predate this change: the environment imports `zava_forward.core` from a different checkout (for example `CommittedReloadError` is missing), and one test errors identically on the parent commit. The one remaining `test_case_journey` error is among them.
* The requested `src/api/tests/test_chat_plain_language_modes.py` does not exist; the equivalent assertions live in `test_regulatory_a11y_cues.py` and were updated instead (the unique-module-name rule is kept).
* The requested header text "Live AI connected" does not exist in this slice; the visible text is the plain-language toggle state.
