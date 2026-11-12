---
title: Issue 96 UI implementation changes
ms.date: 2026-11-12
---

## Changes

* `src/api/src/zava_forward/api/web/role-screens.js`: panel-local `fundingSavedCopyCheck` and helpers above `fundingDraftPanel`; rendered only when downloads are enabled and the draft has an id. Posts the original file text unchanged (raw JSON text transport, G4) so `12.0` and integers above 2^53 survive. Reuses the CSRF header, same-origin session, 401 login, route abort, pending-duplicate guard and readable errors. Never implies a write or approval. Programme, top and screenTable regions untouched.
* `src/api/checks/held_form_download_browser_check.py`: failing-first browser regression with a downloaded synthetic copy: current, stale, invalid, numeric fidelity (a re-serialising control answers Invalid), failure mapping, session end, keyboard, denied roles, axe 4.10.3 on the checker group.
* `src/api/tests/test_finance_grants_screens.py`: existing control assertion now allows exactly one file input and one button when enabled; all controls stay absent when OFF.
* `src/api/README.md`: one paragraph in the saved freshness section.

## Failing-first evidence

Session files `ui-2333-failfirst-1.log` (control absent), `ui-2333-failfirst-4-naive-stringify.log` (false Invalid for 12.0 under JSON.stringify), then `ui-2333-green-3.log` (88 PASS, 0 FAIL, axe no violations).

## Divergences

* Plan said no `style.css` change; a design-system contract test requires every class in the JS to exist in CSS, so custom classes were dropped (data attribute and existing classes only). `style.css` unchanged.
* Existing screen test edited (control allowance) because the enabled panel now legitimately has one input and one button.

## Validation (focused tier, no full gate)

16 canonical API tests, role endpoint inventory (24), finance grants screens (20), design system (8), content standard (19): OK. ruff check/format, mypy, `node --check`, `git diff --check`: clean. Browser check 88 PASS with pinned axe.

## Not run or disclosed

* No full gate, hosted CI, push or PR; local freeze only.
* No browser story for switch OFF (unit and API 404 tests cover it) or navigation during file read.
* Failures injected by route interception; no assistive-technology acceptance; axe scoped to the checker group.
* "Current" means the checked details match the supplied metadata, not authenticity.
