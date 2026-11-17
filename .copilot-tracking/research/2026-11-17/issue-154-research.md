# Issue 154 research: resident and representative UX criteria assessment (2026-11-17)

Base origin/main eb51af5c9. Tier FOCUSED. Scope: assess criteria, record evidence only; demo-first, desktop-only.

## Measurements (baseline, before any edit)

* `cd src/core && python3 -m unittest tests.test_resident_journey_design tests.test_resident_access tests.test_resident_preview -q`: 48 tests OK.
* `cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_resident_preview_api -q`: 15 tests OK.

## Criteria status on main

* C1, C4: ticked; asserted by `src/core/tests/test_resident_journey_design.py`.
* C2: specified assisted/non-digital paths exist; service availability and AT acceptance are not evidenced. Unmet.
* C3: `src/api/tests/test_resident_preview_api.py` covers resident-grant expiry/revocation on the next request (`SYN-RES-A`) and a representative view limited by task (`SYN-REP-B`, `SYN-REP-WRONG`). Gap found: no HTTP test that a representative grant's expiry/revocation takes effect on the next request. Core `representative_view` expiry is tested, but not through the server boundary for the representative viewer kind.
* C5: usability scripts (#155) not run; no resident/representative/AT acceptance. Unmet.

## Out of scope

#1818/#1641 (core mssqlstore, chat grounding). Comment on #154 mentions #1772 merged into a parent branch, not main; not relied on.

Planning Readiness: Ready. Disposition: executed.
