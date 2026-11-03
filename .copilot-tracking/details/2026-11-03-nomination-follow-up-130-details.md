---
title: Issue 130 nomination follow-up view details
ms.date: 2026-11-03
---

## Phase 1: view

* `resident_decisions.nomination_follow_up(record, today=None)` returns `route_ready`, `missing`, `next_update_overdue` (True, False or `Unknown`), `re_review_pending`, `review_owner` text and a `not_inferred` list.
* `followup_view` sets it on a copy of the case in `Store.detail`; unrelated roles still have intake removed afterwards.

## Phase 2: tests and docs

* `test_nomination_follow_up_is_read_only_and_shows_gaps_as_unknown` in `src/core/tests/test_resident_decisions.py`.
* README paragraph under the nomination intake section.

## Plan critique

One critique pass, performed by the author within this task (not an independent agent): see [critique](../reviews/plans/2026-11-03-nomination-follow-up-130-plan-critique.md).
