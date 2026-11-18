---
title: Issue 215 plain-language mode correction cycle 2 research
---

* Source: independent review `independent-direct-215-c1-5ab2c3938.md` (NEEDS_CHANGES) with three blocking findings: (1) plain-language mode is not wired to the backend, (2) toggling the mode overwrote the operational `<p role="status">` banner, (3) the WCAG baseline row still called the mode text a `role="status"` region.
* Path reconciliation: the request names `api/chat.py`, `HomeChatRequest`, `answer_home_chat`, `answer_case_chat`, `static/chat.js` and `tests/test_home_chat_api.py`. None exist in this checkout. The real surfaces are `server.py` (`/api/chat/unstored-ask`, `/api/chat/threads/{id}/ask`, `/api/chat/regulatory/threads/{id}/ask`, each rejecting unknown body keys) and `web/chat.js`. The flag was wired there; `test_home_chat_api.py` was created.
* Evidence: `regulatory_ux_check.py:171` needs one `[role=status]` in `#regulatory-alerts`; the node harness in `test_case_journey.py` fakes `classList` with only `add` and `toggle`.
* Original and cycle 1 research, plan, changes and review files are preserved unaltered.
* Planning readiness: Ready. Disposition: executed.
