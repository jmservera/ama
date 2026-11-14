# Plan: issue 531 briefing loading and provenance

* [x] Set `aria-busy` on the briefing section and content during load; clear in `finally`.
* [x] Plain-language visible status for first load and refresh; reserve status height (`.briefing-status`).
* [x] Provenance list: priority by fixed rules, wording by AI or rules, manual control; per-statement "Why listed".
* [x] Unit tests in `src/api/tests/test_briefing_loading_provenance.py`.
* [x] Run mypy, ruff check, ruff format --check, targeted unittests.
* Critique: executed once (self-critique): no conflicts with confirmed decisions; no AI behaviour or ranking changed.
