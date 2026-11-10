---
title: Issue 80 capacity browser check aftercare route, changes
description: Prospective and final change record for C2
ms.date: 2026-11-10
---

## Prospective (before implement-start)

* Planned source change: `src/api/checks/capacity_browser_check.py` only, per [details](../../details/2026-11-10/issue-80-capacity-c2-1110-details.md).
* Planned records: this file, review, state. No app, UI, API, core, auth, role, `ops.js` or dataset change.
* Not yet done: edit, validation, browser run, review.

## Final (2026-11-10)

* Changed `src/api/checks/capacity_browser_check.py` only (+38): `MANAGER_ROUTES["#/aftercare"]` (heading "Aftercare concerns", reads `/api/aftercare/concerns` and `/api/aftercare/evaluator`, content `section[aria-labelledby=ac-list-title]`); a request listener that adds a request to `expected_failures` only for scenario `#/aftercare`, GET, exact URL `<base>/api/aftercare/form`; a response recorder for that URL; route assertions (statuses exactly `[403]`, JSON error exactly "Your role cannot record a concern. Ask a colleague who can.", status line "Your role can read these concerns but cannot record one. Ask a colleague who can.", zero `#ac-form`, zero submit buttons); and an unchanged-POST-count assertion for the route. No other source changed. C1 batched-preflight disclosure stays: C1 seven-record verify is local phase verification, not strict separate-call conformance. This chain issued each validation in its own call before each marker.

| Check | Exit | Result |
| --- | --- | --- |
| Ruff check, format check (checker) | 0, 0 | Pass |
| `node --check ops.js` (unchanged) | 0 | Pass |
| `test_list_export_api` | 0 | 11 OK |
| Related static (5 modules) | 0 | 60 OK |
| `capacity_browser_check --axe`, ONE run (self-taken heavy lock, free), `browser-run3.log/.exit/.head/.diff` | 1 | FAILED later, see below |

## Browser run 3 outcome

* Passed: seeded render, axe 0 violations, `packages.csv` (1 row) and `workorders.csv` (601 rows) keyboard downloads, all manager routes including `#/time` (corrected, C1) and `#/aftercare` (new: exactly one 403 on the form read with the exact error, read-only status line, no form or submit, no POST, no unexpected failure or console error), `#/screens`; packages and workorders unavailable scans; draft-safe packages and workorders refresh/retry.
* Failed: scenario `delayed sibling 401 after packages refresh failure`, `capacity_browser_check.py:754`, `AssertionError: Locator expected to contain text 'We could not load packages'`; `#app > [role=status]` stayed empty for the 60 s timeout. Not touched by this change; cause not determined (no baseline run; no app-defect claim). Not repaired, not retried.
* Not reached: `empty capacity` zero-anchor assertion (line 885) and later scenarios, so withholding on empty remains source-read only.
* Cleanup: no `/tmp/ama-capacity*` scratch or helper left.

## Process disclosure

I drafted a review file in the same step as these final notes, before the `implement-done` marker. I removed that draft (kept outside the repository at `/tmp`, not used as evidence) so the review artifact was absent at `implement-done`, and wrote the review afterwards from the diff and run 3. The draft's conclusions were not altered by this.
