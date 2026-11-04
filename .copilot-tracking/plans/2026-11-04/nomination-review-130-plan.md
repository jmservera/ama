---
title: Issue 130 nomination human review plan
ms.date: 2026-11-04
---

## Plan

* [x] Add `nomination_review` action and `NOMINATION_OUTCOMES` in `resident_decisions.py`.
* [x] Stale earlier reviews on correction; expose `review_current` in the follow-up view.
* [x] Behavioural tests: independence, closed fields, closed outcomes, duplicate refusal, staleness, no ranking change.
* [x] Update core and API README action tables.
* [x] Focused tests, ruff, mypy as CI runs it (tests included).

Details: [details](../../details/2026-11-04/nomination-review-130-details.md).

Critique (single pass, self-applied): reviewer must be independent of the recorder (reused `_require_independent_reviewer`); no outcome may imply priority or eligibility; unknown recorder identity blocks review.

## Later slices (not started)

1. Dependent decision graph once a nomination-dependent decision type exists.
2. Automatic hazard onward routing (needs hazard owner decision).
3. Resident or representative participation evidence (human).
