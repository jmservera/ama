---
title: Issue 229 steward and operator screens WCAG slice plan
ms.date: 2026-11-14
---

* Add a read-only "State at a glance" definition list to the exception register view: lineage freshness, ingestion quarantine, sensor feed health, AI task enabled or disabled.
* Every state is written text prefixed `State:`; absent or unrecognised values read `Unknown`, never healthy. Optional `indicators` contract field; no mutating controls.
* No new `role=status`, no `aria-invalid`; use `dl` so existing table-row tests are unaffected.
* Add `src/api/tests/test_data_steward_screen_wcag.py`; run it with `test_accessibility_baseline` and `test_data_operator_ai_state`; mypy and ruff with /tmp caches in `src/api`.
* Critique (single pass, self): compatible; server does not yet emit `indicators`, so states show Unknown until it does (follow-up).

## Cycle 1 independent-review fixes (0ff56f162)

* Names in the review brief differ from the code: the screen is `data-operator` (`exceptionRegisterPanel`) and the helper is `indicatorState`; fixes were applied there.
* Added `nav.screen-section-jump` (aria-label "Data stewardship sections") with four `button type=button data-jump-target` controls that call `.focus()` and `.scrollIntoView()` on `tabindex=-1` headings; `screenPanel("Exception register", ...)` call sites unchanged; no new table, so `EXPECTED_REGIONS`/`NO_REGION_GAPS` are unchanged.
* `indicatorState` now uses `Object.hasOwn`, so `constructor`/`toString` read as Unknown.
* `/api/exceptions` still has no `indicators` and no lineage, splits or quality-gate data, so absent indicators fall back to written Unknown states; no derivation is invented.
* Tests: added inherited-key and jump-nav tests; two existing tests now exclude jump buttons from their no-control counts.
* Validation: mypy, ruff check, ruff format --check clean; targeted unittest suites pass (39 and 46). Browser check and hosted CI not run; independent re-review and owner approval still open; nothing pushed.
