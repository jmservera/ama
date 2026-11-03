---
title: Details, issue 153 plain-language copy audit increment
ms.date: 2026-11-03
---

## Phase 1

* `src/api/src/zava_forward/api/web/panels.js`: `actForm` renders object options as value and label; `financeDecisionLabel` maps "Keep on hold" for display; submit value stays "Keep on hold".
* `src/api/src/zava_forward/api/web/role-screens.js`: Finance decision line shows "Keep payment paused" through a local `screenFinanceDecision` helper (no shared scope with panels.js).

## Phase 2

* `src/api/tests/test_content_standard.py`: `test_finance_decision_sources_contain_display_mapping` (source-contains check); `src/api/tests/test_finance_grants_screens.py`: `test_finance_decision_shows_plain_label_without_panels_loaded` (behavioural, no panels.js).
* `docs/reference/research/ux/content-standard.md`, `docs/reference/log.md`.

## Phase 3

Validation (focused tier): unittest for test_content_standard, test_finance_grants_screens, test_workspace_scripts; ruff check and ruff format --check on touched files; mypy on the touched tests (4 errors remain in an untouched file).
