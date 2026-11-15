---
title: Issue 104 criterion 5 non-exercise bounds plan
ms.date: 2026-11-14
---

* [x] Phase 1: failing-first tests in `src/api/tests/test_nonexercise_capability_bounds.py`.
* [x] Phase 2: guard in `Consumption.authorize` (billable price requires non-blank owner, positive finite call/token/money limits, `alert` and `alert_owner`; recorded as optional authority fields) and in `reserve_in` (billable authority without binding or with zero limit is held `alert-unowned`, zero reservations; alert owner is the bound alert owner).
* [x] Phase 3: add alert binding to billable fixtures in agents and api tests.
* [x] Phase 4: focused validation (ruff, mypy, targeted tests).

Details: [details](../../details/2026-11-14/104-nonexercise-bounds-0122-details.md). Critique: [critique](../../critiques/2026-11-14/104-nonexercise-bounds-0122-critique.md).
