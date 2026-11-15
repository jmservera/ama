---
title: Issue 228 criterion 5 changes (2026-11-13)
ms.date: 2026-11-13
---

## Changes

* `src/api/checks/procurement_screens_browser_check.py`: rewritten (see plan).
* `src/api/README.md`: paragraph for the check updated.
* Run log: [228-procurement-a11y-2122-browser-run.log](228-procurement-a11y-2122-browser-run.log).

## Validation

* Browser check with pinned axe 4.10.3 and `ZF_AXE_REQUIRED=1`: exit 0, 308 PASS, 16 axe scans (2 roles x 4 states x 1280 and 320 px) with 0 violations and 0 incomplete.
* `unittest` `test_procurement_screens`, `test_accessibility_baseline`, `test_content_standard`, `test_role_screens_conformance`: 68 tests OK. `ruff check`, `ruff format --check` (src/api) and `mypy` on the check: clean.
* Not run: `test_scenario_manifest`, `test_needs_inventory` (manifest untouched); complete local gate and hosted CI (focused tier; the check is not in the CI matrix, so CI gives no coverage of it).

## Limits

Engineering evidence only. Not human assistive-technology or usability sign-off (#155); non-Issued states are rewritten real responses, not store-built states; axe covers `main` only. Criterion 5 should stay unchecked until the owner accepts this evidence.
