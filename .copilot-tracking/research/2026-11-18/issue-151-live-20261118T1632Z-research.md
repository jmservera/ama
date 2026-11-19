# Research: issue 151 closure, live demo re-verification (2026-11-18)

Research disposition: executed (opening note; findings appended below).

* Issue 151 has one unticked criterion: "Manual screen-reader and keyboard checks are recorded for each role workflow".
* Prior live notes (axe, r2, r3) cover the Programme Manager role and the resident app.
* Open question: which other employee role workflows can be reached with the one available test account.
* Owner decision 2026-11-18: demo, desktop only; person-run assistive-technology testing not needed.

## Findings (2026-11-18 16:33 to 16:36 UTC)

* The live employee account holds one role, Retrofit Programme Manager (`/api/me` `user.role`); navigation lists 13 screens, all scanned in earlier rounds.
* The Specialist screens route exposes nine `#/role/*` aliases. The role-screens code lists only screens installed for the signed-in role, and others render "Screen unavailable" (`src/api/src/zava_forward/api/web/role-screens.js` lines 118 to 128).
* Live scan of all nine aliases (Playwright Chromium 1366x900, axe-core 4.10.3 wcag2a/2aa/21a/21aa/22aa, Tab walk, 320 px reflow): seven rendered role screens had 0 axe violations, 0 incomplete, no keyboard trap, an indicator on every stop, no unnamed stop and no horizontal scroll at 320 px. `role/repairs` and `role/contractor` rendered the denial screen (1 stop, 0 violations).
* Evidence: `.copilot-tracking/evidence/2026-11-18/issue-151-live-r4/`. Credentials were not printed; a literal scan of that folder for each credential value found no match. No Azure resource was created or changed.
* `src/api` `test_accessibility_baseline` passes (18 tests).
* Planning readiness: Ready. Remaining unticked criterion cannot be fully proven: no screen-reader run (owner excluded person-run AT for the demo), and only one real role identity exists, so repairs, contractor and other roles are untested as users.
