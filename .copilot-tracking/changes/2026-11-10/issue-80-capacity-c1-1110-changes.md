---
title: Issue 80 capacity browser check time-status expectation, changes
description: Prospective and final change record for the C1 correction
ms.date: 2026-11-10
---

## Prospective (before implement-start)

* Planned source change: `src/api/checks/capacity_browser_check.py`, `#/time` branch only (see [details](../../details/2026-11-10/issue-80-capacity-c1-1110-details.md)).
* Planned records: this file, review, state. No `ops.js` or other source change.
* Not yet done: edit, validation, browser run, review.

## Final (implementation complete, 2026-11-10)

* Changed `src/api/checks/capacity_browser_check.py` only (+14 -3): the `#/time` branch now uses a `banner` locator with three branches (enabled exact text; `flag_on` false exact switched-off sentence with owner and next action; other blocked states `\S\. Owner: .+\. Next action: .+`). No `ops.js`, application, core, API, route, export, permission or fixture change. The original stale assertion remains visible in the committed original records and `ROOT/phase80-capacity-exports-evidence-1110/browser-run1.log`.
* Process note: the standalone state validation and the `implement-start` marker were issued in the same tool batch (validation printed success first), not as strictly separate calls; later markers were issued as separate calls. Disclosed, not healed.

| Check | Command | Exit | Result |
| --- | --- | --- | --- |
| Ruff | `ruff check` and `ruff format --check` on the checker | 0, 0 | Pass |
| Node syntax | `node --check src/api/src/zava_forward/api/web/ops.js` (unchanged) | 0 | Pass |
| API unit tests | `python -m unittest tests.test_list_export_api -q` | 0 | 11 tests OK |
| Related static tests | `test_workspace_paging`, `test_workspace_scripts`, `test_content_standard`, `test_design_system`, `test_ui_support` | 0 | 60 OK |
| Browser, one run | `python -m checks.capacity_browser_check --axe /tmp/axepk/package/axe.min.js` (self-taken `/tmp/ama-rpi-heavy.lock`, free) | 1 | FAILED, see below |

## Browser run 2 outcome

Evidence `ROOT/phase80-capacity-c1-evidence-1110/browser-run2.log`, `.exit` (1), `.head`, `.diffstat`. Run once; no retry.

* Passed: seeded capacity render; axe `seeded capacity` 0 violations and 0 incomplete; `packages.csv` keyboard Enter download (1 row); `workorders.csv` keyboard Enter download (601 rows); manager routes `#/`, `#/all`, `#/overview`, `#/progress`, `#/visits`, `#/funding`, `#/finance`, `#/capacity`, `#/closed`, `#/assistants`, and `#/time` (the corrected assertion, PASS with heading and `/api/time/status` read).
* Failed: `capacity_browser_check.py:517`, `AssertionError: ('Unchecked manager route', '#/aftercare')`. The manager navigation now contains `#/aftercare`, which is not in the check's `MANAGER_ROUTES`. By source reading (`git log -S"#/aftercare"` finds `64c3f9191`, #1400 "integrate delivery-quality aftercare persistence"; this is a source-read attribution, not a baseline re-run) this is another drift in the whole-page check, unrelated to the time expectation and to the export links. It was not repaired: Root admitted only the time expectation, and further repair or a second run is not admitted.
* Not reached: the `empty capacity` scenario and its zero-anchor assertion, and later scenarios. Withholding on empty therefore remains verified by source reading only.
* Helpers: the check owns its server and temporary store; no helper process or `/tmp/ama-capacity*` scratch remained afterwards.

## Dated clarification of "no rendered evidence" (2026-11-10)

The original handoff phrase is loose. Actually observed in the owned synthetic browser runs (run 1 and run 2, both with exit 1): rendered DOM for seeded `#/capacity`, one download-link accessibility check by axe (0 violations, 0 incomplete) in the `seeded capacity` state, real keyboard Enter downloads with CSV row counts (1 and 601), and rendered manager routes through `#/time`. Not available: screenshot or layout review, manual screen-reader testing, deployed or user acceptance, and any conformance claim. The empty-state rendered observation is not available.
