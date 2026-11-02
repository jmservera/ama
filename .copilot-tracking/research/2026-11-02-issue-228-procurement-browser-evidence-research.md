# Research: issue #228 slice 2, browser evidence for procurement and contractor screens

Disposition: reused (existing evidence adequate). Planning Readiness: Ready.

## Evidence

* Merged PR #655 delivered the read-only Package queue and Job pack screens (`src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_procurement_screens.py`). Its Review (`.copilot-tracking/reviews/2026-11-01-issue-228-supplier-procurement-screens-review.md`) left the WCAG 2.2 keyboard and textual-state criterion unproven and routed "browser and axe check".
* Open sibling PRs edit `role_screens_browser_check.py` and `role_screens_fixtures.py` (#769 merged), `role-screens.js` (#771 merged) and a standalone check (#776), so this slice adds a new standalone check file and changes no production code.
* The package, capacity and work-order shapes come from the real store (`create_package`, `set_capacity`, `issue_work_order`) so the check exercises the real `/api/packages` and `/api/workorders` projections.
* Pinned axe 4.10.3 is the repo convention.

## Limits

Desk-based hypothesis. Engineering checks do not establish assistive-technology testing or WCAG conformance (#151, #155). Fluent adoption (#150) unchanged. Submission, correction and checklist capture remain unbuilt (OD-47). Commitment source bytes are not seeded into the check server, so capacity evidence shows Unknown, which the check asserts is not presented as met.
