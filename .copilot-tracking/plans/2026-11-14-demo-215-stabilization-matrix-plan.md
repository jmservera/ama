# Plan: #215 stabilization matrix (2026-11-14)

* Add `src/api/tests/test_alert_chat_end_to_end_stabilization_215.py`: API matrix over generative, unavailable and withheld outcomes for the unblock and visit questions; context injection, provenance, citations, non-mutation; static `chat.js`/`chat-widget.js` checks for case context, badges, citation links and manual escape wording; an evidence-boundary test.
* Validate with the focused unittest, ruff check, ruff format --check, mypy only.
* Critique (once): scope is test-only and uses synthetic data; risk of duplicating siblings is mitigated by asserting cross-surface integration only.
* Refs #215.
