---
title: Issue 127 regulatory change review plan
ms.date: 2026-10-15
---

## Plan

* [x] Phase 1: extend `rule_card_review` with affected (rules, active version, requirements, tests), prior source version and source effective date; add append-only `rule_card_review_event`.
* [x] Phase 2: add `assess_review`, owner-only, requiring interpretation, tests, effective date, notification and rollback, with optional hold; never activates.
* [x] Phase 3: tests in `mvp/tests/test_rulecards.py`; README update.
* [x] Phase 4: validate with the full mvp test suite.

Critique (single, self-run): conflicts none; risk that the static trace is invented is mitigated by labelling it an exercise map and flagging unmapped cards.
