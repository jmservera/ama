# Research: issue #229 slice 2, browser evidence for the data steward and operator screen

Disposition: reused (existing evidence adequate). Planning Readiness: Ready.

## Evidence

* Merged PR #654 delivered the read-only Data steward and operator view (`src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_data_operator_screen.py`). Its Review (`.copilot-tracking/reviews/2026-11-01-issue-229-data-steward-screens-review.md`) left the WCAG 2.2 keyboard criterion unproven and routed a browser accessibility and keyboard check.
* Open slice PRs touch `role-screens.js` (#771), the role-screen browser check files (#769) and `safety_screens_browser_check.py` (#776), so this slice adds a standalone check file mirroring #776.
* Pinned axe 4.10.3 is the repo convention.

## Limits

Desk-based hypothesis. Engineering checks do not establish assistive-technology testing or WCAG conformance (#151, #155). Fluent adoption (#150) unchanged. The exception queue and integration run state have no data source (the screen says Unknown). Open exceptions are server-derived work blockers, so the check asserts them from the real projection.
