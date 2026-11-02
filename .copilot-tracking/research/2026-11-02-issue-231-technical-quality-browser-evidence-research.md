# Research: issue #231 slice 2, browser evidence for technical and quality queues

Disposition: reused (existing evidence adequate). Planning Readiness: Ready.

## Evidence

* Merged PR #656 delivered the read-only Technical queue and Quality queue in `src/api/src/zava_forward/api/web/role-screens.js` with unit tests (`src/api/tests/test_technical_quality_screens.py`). Its Review (`.copilot-tracking/reviews/2026-11-01-issue-231-retrofit-technical-quality-screens-review.md`) left the WCAG 2.2 keyboard and textual-state criterion unproven and routed "browser keyboard and axe check for both screens" as follow-up 1.
* The shared host check `src/api/checks/role_screens_browser_check.py` supports per-story scenarios (as `232`) but has none for 231.
* Pinned axe 4.10.3 (sha256 880970c0...) is already the repo convention (`checks/capacity_browser_check.py`).

## Scope of this slice

Add stories `231` and `231q` to the browser check with a synthetic home that has a returned sign-off, a stale (needs reassessment) sign-off, a missing sign-off, a missing EPC reference, a returned quality record with a defect owner, and a fixed record awaiting reinspection. Assert: blocked state in text, no ready claim, no write controls, keyboard reach of every table region, optional pinned axe scan.

## Limits

Desk-based hypothesis. Engineering checks do not establish assistive-technology testing or WCAG conformance; that stays with #151 and #155. Fluent component adoption (#150) is not changed here.
