---
title: Changes issue 1837 live, run 2
ms.date: 2026-11-20
---

Tier FOCUSED: documentation and evidence only, no src, workflow, dependency or Dockerfile change. Added `docs/reference/research/issue-1837-live-demo-evidence-2026-11-20.md` and `docs/reference/research/issue-1837-live-2026-11-20/` (three axe results, live negative probe, live form probe and screenshot).

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 failing-first regression for all three forms, valid challenge target | Proven (earlier) | [failing-first at 9da3fcd](../../../docs/reference/research/issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); passes on main |
| 2 valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | route-forms check POST 200,200,200 and asserted records; live write skipped to avoid irreversible demo records |
| 3 negative tests | Proven | module tests (66 OK); [live probe](../../../docs/reference/research/issue-1837-live-2026-11-20/live-negative-probe.json): urlencoded 400, no header 403, malformed 400, unknown case 404, mismatch 400, case unchanged |
| 4 browser journeys with axe, zero unexpected skips | Proven locally | three axe results, zero violations, zero skips; live form transport confirmed (JSON plus CSRF header, validation 400, no write) |
| 5 independent exact-head review, hosted CI | Unproven | needs a human reviewer and hosted run; not available to this worker |
| 6 full tier receipt | Not applicable here | no src change; `rpi-checks.py --all` not run by instruction |

## Validation

* `python3 -m unittest tests.test_nomination_api_routes tests.test_accessibility_baseline tests.test_content_standard tests.test_nomination_screen tests.test_challenge_no_retaliation_api_220 -q` (src/api): 66 OK.
* Three `checks.*_browser_check` runs with axe 4.10.3: passed.
