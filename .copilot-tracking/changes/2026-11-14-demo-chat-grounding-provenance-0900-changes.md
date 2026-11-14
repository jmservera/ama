---
title: Chat grounding and provenance changes
ms.date: 2026-11-14
---

## Changed

* src/core chat_case_answers.py: `RULES` workflow sources; `_unblock` cites them.
* src/core chat_panel.py: `answer_origin`, new labels, rules-first unblock, shared
  `_rules_answer`, workflow sources in rule-based citations.
* src/api web/chat.js: "Answer origin:" labels for rule, model and withheld replies.
* Tests: core and api chat tests, provenance cue test; browser check text; README.

## Validation (focused tier)

* core chat_panel and chat_case_answers: 64 passed.
* api `test_*chat*.py`: 280 passed (1 skipped); accessibility baseline 13; content standard 29.
* agents chat_eval: 60 passed.
* ruff check and format check clean; mypy (core project config) clean.
* Not run: browser check, hosted CI, full gate.
