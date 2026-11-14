---
title: Issue 229 steward and operator screens WCAG slice changes
ms.date: 2026-11-14
---

* `role-screens.js`: added `indicatorRows` and a "State at a glance" panel with written states for lineage freshness, ingestion quarantine, sensor feed health and AI tasks.
* Added `src/api/tests/test_data_steward_screen_wcag.py` (6 tests).
* Validation: new tests, `test_accessibility_baseline` and `test_data_operator_ai_state`, `test_data_operator_screen` pass; mypy, ruff check and ruff format --check clean in `src/api`. Tests ran with a transient PYTHONPATH because editable installs point at another checkout. Browser checks and hosted CI not run; nothing pushed.
* Open: server `/api/exceptions` does not supply `indicators`; keyboard behaviour is static and Node-rendered only. #229 criterion remains unproven (`Refs #229`).

## Cycle 1 independent-review fixes (0ff56f162)

* Names in the review brief differ from the code: the screen is `data-operator` (`exceptionRegisterPanel`) and the helper is `indicatorState`; fixes were applied there.
* Added `nav.screen-section-jump` (aria-label "Data stewardship sections") with four `button type=button data-jump-target` controls that call `.focus()` and `.scrollIntoView()` on `tabindex=-1` headings; `screenPanel("Exception register", ...)` call sites unchanged; no new table, so `EXPECTED_REGIONS`/`NO_REGION_GAPS` are unchanged.
* `indicatorState` now uses `Object.hasOwn`, so `constructor`/`toString` read as Unknown.
* `/api/exceptions` still has no `indicators` and no lineage, splits or quality-gate data, so absent indicators fall back to written Unknown states; no derivation is invented.
* Tests: added inherited-key and jump-nav tests; two existing tests now exclude jump buttons from their no-control counts.
* Validation: mypy, ruff check, ruff format --check clean; targeted unittest suites pass (39 and 46). Browser check and hosted CI not run; independent re-review and owner approval still open; nothing pushed.
