<!-- markdownlint-disable-file -->
# Details: issue 134 connected same-home check, C5 (2026-11-11)

Plan: [plan](../plans/2026-11-11-connected-c5-134-1111-plan.md). Amendment: [amendment](../plans/2026-11-11-connected-c5-134-1111-amendment.md). Earlier details: [details](./2026-11-11-connected-plan-134-1111-details.md), which stay as written; this file supersedes them only where stated.

## Factory

* A function `journey_snapshot()` instantiates `StoreJourney` with the method name `test_store_journey_reaches_financial_closure_in_order`, calls `setUp()` and `journey()`, takes `copy.deepcopy(store.data)` before `doCleanups()`, and returns it. The copy happens first because cleanup removes the temporary Store directory.
* The check inserts `src/core/tests` on `sys.path` as `home_case_browser_check.py` does. No journey step is copied. If the TestCase cannot be instantiated or the snapshot lacks the journey records, stop and report the blocker.
* A pure `snapshot_failures(data)` rejects an empty, seed-only or partial snapshot: it requires the ZF-1 records the journey writes (a resolved SQ-1 stock query, four technical sign-off states with a design version, a resident decision for Loft insulation, a quality acceptance and handover, invoice INV-100 with status) and distinguishable, different retained ZF-2 data. If the journey leaves ZF-2 without any distinguishing record, the negative control is blocked rather than weakened (blocker returned to Root).

## Walk and markers

* Declared `CHAIN` of (login email, role label, screen id, required markers). It never enumerates the menu.
* Each required marker names its region selector, the home, and the field or reference it proves (for example, the finance invoice reference in the invoice table of the selected-home evidence). Generic words (Accepted, design version number alone, repeated person names) are not markers by themselves; a marker pairs a value with its field label in the same row or definition.
* Markers are read from the render functions at I1 and recorded with `file:line` in the Changes record. They are not guessed.
* A missing marker fails the run. `gap` or `not-run` appears only for the deferral list.
* The walk uses the existing helpers by import: `login`, `tab_to`, `wait_status`, `expected_status`, `status_contract_failures`, `focus_failures`, and the selectors `ENTRY`, `MENU`, `HOME`, `RESET`. Signatures and scoped focus behaviour are confirmed at I1 before use; the probe stays unmodified.
* The same-home carry between the first two screens uses the prefix selector `a[href^="#/screens?screen=<id>&case=ZF-1"]` with no reset between them. Reset is exercised once per login at the end.
* Sibling control: the PM session opens ZF-2 and the check asserts that its evidence region contains ZF-2's own distinguishable retained data and none of ZF-1's reference markers.
* Run-only mutations (heading removal, mid-walk switch to ZF-2, link target dropped, marker removed) feed the same production predicate functions used by the walk and must each be rejected.
* No browser writes, no approval clicks.

## Environment (private)

Private HOME, TMP, cache and profile under a short scratch outside the checkout; `ZF_BROWSER_SCRATCH` absolute and short. Missing imports are recorded first; only then restore core, agents and api (and the Playwright package if that is the failure) into a throw-away venv outside the checkout. Cached Chromium and the pinned axe file are used if present; otherwise that validation is recorded as not run. Nothing is fetched.

## Evidence wording

Constructed-fixture DOM evidence; roles are fixture identities; the status text is not assistive-technology output; Asset is a proxy; the states are those the Store journey wrote; the check passes no AC and nothing is user validation.
