---
title: Issue 127 regulatory change review changes
ms.date: 2026-10-15
---

## Changes

* `mvp/zavaforward_mvp/rulecards.py`: review items carry affected rules, requirements, tests, versions and effective date; `assess_review` and `rule_card_review_event`; both SQLite and MSSQL DDL.
* `mvp/tests/test_rulecards.py`: three new tests (affected fields, owner-only assessment and hold, no activation by agents).
* `mvp/README.md`: rule card section updated.

## Divergences

None. Knowledge-base files unchanged, so no index or log entry.

## Open items

* Named owners and interpretation authority (OD-24); real source effective dates; mapping of communications, templates, reports and journeys.
* Automated detection feeding `source_changed` is #213.
