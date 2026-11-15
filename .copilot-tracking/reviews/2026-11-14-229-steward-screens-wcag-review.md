---
title: Issue 229 steward and operator screens WCAG slice review
ms.date: 2026-11-14
---

* Execution: one post-implementation review by the implementer; independent exact-head review still required.
* Outcome: conformant for the slice as scoped (focused tier); not a WCAG conformance claim.
* Findings routed to later work: (1) emit `indicators` from the server contract; (2) browser keyboard check of the new panel; (3) validation in #155.
* Human review boxes: [ ] independent assessment, [ ] owner approval.

## Cycle 1 independent-review fixes (0ff56f162)

* Names in the review brief differ from the code: the screen is `data-operator` (`exceptionRegisterPanel`) and the helper is `indicatorState`; fixes were applied there.
* Added `nav.screen-section-jump` (aria-label "Data stewardship sections") with four `button type=button data-jump-target` controls that call `.focus()` and `.scrollIntoView()` on `tabindex=-1` headings; `screenPanel("Exception register", ...)` call sites unchanged; no new table, so `EXPECTED_REGIONS`/`NO_REGION_GAPS` are unchanged.
* `indicatorState` now uses `Object.hasOwn`, so `constructor`/`toString` read as Unknown.
* `/api/exceptions` still has no `indicators` and no lineage, splits or quality-gate data, so absent indicators fall back to written Unknown states; no derivation is invented.
* Tests: added inherited-key and jump-nav tests; two existing tests now exclude jump buttons from their no-control counts.
* Validation: mypy, ruff check, ruff format --check clean; targeted unittest suites pass (39 and 46). Browser check and hosted CI not run; independent re-review and owner approval still open; nothing pushed.
