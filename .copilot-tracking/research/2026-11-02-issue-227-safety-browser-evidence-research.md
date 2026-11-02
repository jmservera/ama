# Research: issue #227 slice 2, browser evidence for safety screens

Disposition: reused (existing evidence adequate). Planning Readiness: Ready.

## Evidence

* Merged PR #653 delivered the read-only Building safety referral queue and Repairs and hazard triage screens (`src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_safety_screens.py`). Its Review (`.copilot-tracking/reviews/2026-11-01-issue-227-safety-screens-review.md`) left the WCAG 2.2 keyboard and textual-state criterion unproven and routed "browser keyboard and axe check".
* Sibling open PRs edit `role_screens_browser_check.py` and `role_screens_fixtures.py` (#769) and `role-screens.js` (#771), so this slice uses a new standalone check file.
* Pinned axe 4.10.3 is the repo convention.

## Limits

Desk-based hypothesis. Engineering checks do not establish assistive-technology testing or WCAG conformance (#151, #155). Fluent adoption (#150) unchanged. The cross-home referral queue needs a portfolio endpoint and is out of scope.
