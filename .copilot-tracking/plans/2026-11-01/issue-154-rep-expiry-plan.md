---
title: Issue 154 representative expiry plan
ms.date: 2026-11-01
---

## Plan

* [x] Add tests to `src/core/tests/test_resident_preview.py` class `Representative`: review date equal to today denies, review date tomorrow allows, non-Confirmed status denies, denied outcome carries no case detail, representative view never includes the household address.
* [x] Focused validation: unittest for the file, ruff check, ruff format --check, mypy for `src/core`.
* [x] Commit, push, open PR with `Refs #154`.

## Critique (executed once, direct)

* Compatible: use a store-level mutation with restore, as neighbouring tests do; derive dates from `controls.today()` not hard-coded values.
* Rejected: adding resident-session enforcement; it needs OD-41/42 and is beyond the acceptance slice.
* No significant or divergent issue.
