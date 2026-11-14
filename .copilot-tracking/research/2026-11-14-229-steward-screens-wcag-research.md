---
title: Issue 229 steward and operator screens WCAG slice research
ms.date: 2026-11-14
---

* Criterion: `Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`. Stacked on PR #1639 (base `c9d4204029692886e26fdf56011c25d2fd180e1a`). `Refs #229`.
* Screen: `data-operator` in `src/api/src/zava_forward/api/web/role-screens.js`, with the exception register contract from `/api/exceptions`.
* Existing: tables sit in focusable named regions with captions; quarantined and fallback AI rows are written distinctly. No panel showed lineage freshness, sensor feed health or AI task enabled state, and no contract field supplies them.
* Constraints: `test_accessibility_baseline` audits `aria-invalid` sites (add none); `#regulatory-alerts` allows one `[role=status]` (add none).
* Planning Readiness: Ready. Research disposition: executed (code inspection only; desk hypothesis, not observed behaviour).

## Cycle 1 independent-review fixes (0ff56f162)

* Names in the review brief differ from the code: the screen is `data-operator` (`exceptionRegisterPanel`) and the helper is `indicatorState`; fixes were applied there.
* Added `nav.screen-section-jump` (aria-label "Data stewardship sections") with four `button type=button data-jump-target` controls that call `.focus()` and `.scrollIntoView()` on `tabindex=-1` headings; `screenPanel("Exception register", ...)` call sites unchanged; no new table, so `EXPECTED_REGIONS`/`NO_REGION_GAPS` are unchanged.
* `indicatorState` now uses `Object.hasOwn`, so `constructor`/`toString` read as Unknown.
* `/api/exceptions` still has no `indicators` and no lineage, splits or quality-gate data, so absent indicators fall back to written Unknown states; no derivation is invented.
* Tests: added inherited-key and jump-nav tests; two existing tests now exclude jump buttons from their no-control counts.
* Validation: mypy, ruff check, ruff format --check clean; targeted unittest suites pass (39 and 46). Browser check and hosted CI not run; independent re-review and owner approval still open; nothing pushed.
