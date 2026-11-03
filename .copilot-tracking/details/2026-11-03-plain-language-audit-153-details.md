---
title: Details, issue 153 plain-language copy audit increment
ms.date: 2026-11-03
---

## Phase 1

* `src/api/src/zava_forward/api/web/panels.js`: `actForm` renders object options as value and label; `financeDecisionLabel` maps "Keep on hold" for display; submit value stays "Keep on hold".
* `src/api/src/zava_forward/api/web/role-screens.js`: Finance decision line shows "Keep payment paused".

## Phase 2

* `src/api/tests/test_content_standard.py`: `test_finance_decision_shows_pause_wording_but_stores_value`.
* `docs/reference/research/ux/content-standard.md`, `docs/reference/log.md`.

## Phase 3

Validation (focused tier): unittest for test_content_standard, test_programme_screen, test_finance_grants_screens; ruff check on the test file.
