---
title: Issue 164 plan
ms.date: 2026-11-17
---

## Plan

* [ ] Add `_valid_rate` and `_approved` helpers in `src/agents/src/zava_forward/agents/chat_eval.py`; use them in `threshold_checks` and `enablement_decision`.
* [ ] Add regression tests to `src/agents/tests/test_chat_eval.py`.
* [ ] Run chat_eval tests, ruff format check, mypy for `src/agents`.

Details: invalid floor/ceiling (non-number, bool, outside 0..1) gives outcome `insufficient`; blank approver is unapproved. Enablement stays disabled. Critique (single pass, recorded): compatible; no conflict with owner decisions; the change touches no grounding code, SQL, security or deployment, so FOCUSED holds.
