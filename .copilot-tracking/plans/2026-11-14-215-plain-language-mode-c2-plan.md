---
title: Issue 215 plain-language mode correction cycle 2 plan
---

* [x] New `api/plain_language.py`: strict boolean `plain_language` (default false), `plain_summary` added beside an unchanged reply, citations and provenance.
* [x] `server.py`: accept the flag on the three ask endpoints; a non-boolean value is a validation refusal; other unknown keys stay rejected.
* [x] `chat.js`: `regulatoryPlainMode(root, id)` updates only `.regulatory-mode-state` (`aria-live="polite"`, `aria-atomic="true"`, no `role`); employee chat gets an off-by-default "Plain-language answers" checkbox; both panels send the flag and show `plain_summary`.
* [x] Tests: new `test_home_chat_api.py`; additions to `test_regulatory_chat_api.py` and `test_accessibility_baseline.py`; pinned markup updated in `test_regulatory_a11y_cues.py` and the alert/chat matrix.
* [x] Docs: correct the WCAG baseline sentence; append a `docs/reference/log.md` entry.
* Critique: one pass on the final candidate. Applied: read the toggle through `querySelector("input")` instead of `classList.contains` (the node harness fake lacks it). No conflicts with confirmed decisions. Validation tier: focused API and static tests, mypy, ruff.
