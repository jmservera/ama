---
title: Issue 228 criterion 5 research (2026-11-13)
ms.date: 2026-11-13
---

## Scope

Focused validation tier. Prove criterion 5 of #228 (WCAG 2.2 baseline #151, textual state meaning, keyboard navigation) for the Package queue and Contractor job pack screens. Criteria 1 to 4 and 6 are already checked on `main` (`ee068a4b5`).

## Evidence

* Planning Readiness: Ready. Research disposition: executed.
* `src/api/src/zava_forward/api/web/role-screens.js` registers `procurement-packages` and `contractor-job-pack`; both are read-only, use `screenTable` (labelled focusable region, caption, `th scope=col`), `role=status` for the draft-readiness statement and `p.empty` text for empty tables.
* The named files `test_supplier_procurement_screens.py` and `workbench-browser-check.mjs` do not exist. The real files are `src/api/tests/test_procurement_screens.py` (node vm unit tests) and `src/api/checks/procurement_screens_browser_check.py` (Playwright and optional axe, from #782). `rpi-checks.py` does not run it; the README says it is not in the CI matrix.
* Baseline run on `ee068a4b5` with pinned axe 4.10.3 (sha256 `880970c8...68bb`, verified) FAILED: `.screen-record` uses `content-visibility: auto` (`style.css:346`), so Playwright `inner_text` omits off-screen panels and the check could not read "A contractor acknowledgement is not acceptance". The screen is not defective (the DOM and accessibility tree hold the text); the harness was stale.
* The existing check covered one state (Issued), one 1280 px axe scan per role, and an optional skip.
* Invariants verified unchanged: `test_content_standard.py` banned words, `test_accessibility_baseline.py` pins (`aria-invalid` 8, `h("table"` 13, `position:fixed` 2). No product JS or `workbench-browser-check` touched, so the scenario manifest is not affected.

## Boundary

Engineering evidence only. Human assistive-technology and usability sign-off (#155) is not claimed.
