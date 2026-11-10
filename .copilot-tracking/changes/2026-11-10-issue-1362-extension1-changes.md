---
title: "Changes: issue 1362 extension E1 visible associated version"
description: Prospective and then actual changes for the checker-only visibility fix
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Registered prospectively before implement-start (source clean at merged head `a6c8df61`, checker blob `dad25ca5...`). Evidence root (external): `ROOT/phase1362-extension1-evidence-1110/`.

## Authority

E1 of up to five additional corrections approved by the owner on 2026-11-10 23:13 for the existing checker scope. Four remain after this task. Earlier spent history and the conservative minimum of zero are unchanged.

## Planned source changes (two files)

* `src/api/checks/atlas_tensions_browser_check.py`: `DESIGN_VERSION_FIELDS` requires `checkVisibility({visibilityProperty: true, opacityProperty: true})` for both the label and the value.
* `src/api/tests/test_atlas_tensions_checker.py`: opt-in real-Chromium regression class.

Results are appended below once executed.

## Actual results (executed)

* Branch base: ordinary merge of `origin/main` `6d4cd624` into the branch (head `a6c8df61`, clean, no rebase); the checker and test blobs were unchanged by the merge.
* Source: `DESIGN_VERSION_FIELDS` now passes `{visibilityProperty: true, opacityProperty: true}` to `checkVisibility` for both `dt` and `dd` (checker blob `b1facccfa2c8396a3c798654a4e0544168659a40`). `DesignVersionBrowserTests` added to the unit module (test blob `63fd2327751bddce263b3973309975dc720ca882`), opt-in via `ZF_BROWSER_TESTS=1`. No other file; no manifest change (the scenario-manifest recipe binds `workbench_browser_check.py`, not this checker).
* RED (`ZF_BROWSER_TESTS=1`, old extraction, real Chromium): 20 tests, 6 failures `AssertionError not raised` for `dt`, `dd` and ancestor `section` with `visibility: hidden` and `opacity: 0`; positive and wrong-value cases passed. Log `candidate/red-unit.log`.
* GREEN: opt-in 20 tests OK, not skipped (`candidate/green-optin-unit.log`); default run 20 tests OK with 3 skipped (the real-browser class). Role conformance 11 OK, Atlas trace OK. Ruff check, format check and `mypy --strict` on both files clean.
* Full Atlas browser check (own venv, Playwright 1.64.0, Chromium 156.0.8078.4): exit 0, 370 PASS at 1280 and 320, one declared SKIP (screenshots env), same as the inherited correction.
* Actual served-fixture negative pair (D3 script, unmodified): at 1280 and 320 the positive control PASSED and `dd`/`dt` `visibility:hidden` and `opacity:0` FAILED at `'Current design version' value is visible`. D1 control (`diag_1362.py control`): case 1 PASSED; `2`, Unknown, `10`, empty, missing and duplicate label FAILED.
* Declared deviations: (a) the opt-in GREEN run first hit a busy heavy lock (another holder, empty log, no test executed; preserved `candidate/green-optin-attempt1-BUSY-no-run.log`) and was run again when free; (b) two static attempts failed on import order and formatting of my new test and were fixed with `ruff --fix` and `ruff format`; logs preserved; (c) one D1 control diagnostic run was added to the planned D3 pair to retain the prior actual-DOM negatives. No retry-until-green on any check result.
* Debit: E1 used, four of the five additional corrections remain. Earlier spent history and the minimum of zero are unchanged. Local assertions are not host or model attestation; no axe, assistive-technology, WCAG, usability, live or production acceptance.
