---
title: Issue 215 plain-language mode announcement changes
---

* Modified `src/api/src/zava_forward/api/web/chat.js`, `style.css`, `tests/test_regulatory_a11y_cues.py`, `tests/test_alert_chat_role_wcag_plain_matrix.py`, the WCAG baseline, content standard and `docs/reference/log.md`.
* Validation: focused unittest modules (a11y cues, alert/chat matrix, keyboard provenance, regulatory UX, accessibility baseline exit 0, widget focus/layout, origin badge) pass; `ruff check .` pass; `ruff format --check .` flags only pre-existing `src/check-container.py`; `mypy` in `src/api` clean.
* `test_chat_panel.py` (backend model-gating tests, 24 failures/errors) fails in this environment; the change touches no Python source, so it is unrelated and not investigated.
