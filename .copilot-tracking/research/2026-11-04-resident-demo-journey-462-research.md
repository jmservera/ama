---
title: Research for #462 resident demo journey weaknesses
ms.date: 2026-11-04
---

* Disposition: executed. Planning readiness: Ready.
* Scope: owner decision 2026-11-04 extends the resident demo (ca-resident-demo) to the end of January 2027; improve the journey in source. No SQL sizing, employee app, role, network or cost change. No credential read or printed.
* Already delivered (merged): #455 preview, #463 showcase source, #465 allowlist cap, #478 and #479 deployment evidence. Criteria 3, 4 and 8 are ticked on the issue. Criteria 1, 2, 5, 6 and 7 are retrospective process conditions; they stay unticked.
* Reviewed in source: `resident_demo/web/index.html`, `demo.js`, `demo.css`, `core/resident_showcase.py` (sensor status text), existing browser checks.
* Journey findings:
  * Strong already: skip link, synthetic banners, focus management on sign in and sign out, table alternative to charts, `<meter>` gauges with text values, no fake zero for missing readings, session expiry handling, manual help routes.
  * Weak 1 (plain language): sensor channel status text shown to residents used jargon: "Demo fault: outlier", "Demo fault: stuck reading", "Outside demo range", "Not recorded".
  * Weak 2 (plain language): the gauge note said "demo faults".
  * Weak 3 (first load): idle scale-to-zero means a cold start of about 27 seconds (recorded in the issue); the page only said "Loading..." with no explanation, which looks like a hang.
  * Considered and rejected: falling back to the last usable reading when the latest is faulty. An existing core test deliberately forbids an older-value fallback; keep it.
  * Considered and deferred: showing local time instead of UTC (an existing browser check and the exact-UTC table alternative depend on it); authenticated live checks remain owner-run because the password is owner-held.
* Boundaries: no authentication, session, SQL or deployment change, so the focused tier applies. No live deploy was done in this slice.
