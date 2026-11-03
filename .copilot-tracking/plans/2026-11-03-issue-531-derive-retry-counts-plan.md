---
title: Issue 531 derive retry counts plan
ms.date: 2026-11-03
---

* Slice: `src/api/checks/loading_briefing_browser_check.py` reads `SCRIPT_RETRY_DELAYS` from `app.js` and uses one load plus its length as the expected attempt count. No product code change; no security, infrastructure, SQL or deployment surface, so the focused tier applies.
* Critique: executed once inline. Verdict: compatible. Paths that never retry (optional `/case-workspace.js`, missing global, unready helper or method) keep their counts. No conflict with confirmed decisions.
* Phases: 1 edit the check (details file); 2 run focused tests, the browser check with pinned axe, ruff and mypy; 3 write changes, review, state and log.
* Out of scope: live Azure verification, assistive-technology acceptance, the gate, benchmarks, full suites.
