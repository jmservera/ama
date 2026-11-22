---
title: Changes issue 1837 live, 2026-11-22
ms.date: 2026-11-22
---

Tier FOCUSED: documentation and evidence only; basis: no src, workflow, dependency or Dockerfile change. Added the [evidence note](../../../docs/reference/research/issue-1837-live-demo-evidence-2026-11-22.md) and `docs/reference/research/issue-1837-live-2026-11-22/` (three axe results, live negative probe, live form probe, screenshot).

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 failing-first regression, three forms, valid challenge target | Proven (earlier) | 2026-11-18 failing-first run; tests pass on base 8bc751023 |
| 2 valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | route-forms check POST 200,200,200; live write skipped to avoid irreversible demo records |
| 3 negative tests | Proven | 66 unit tests OK; live probe: urlencoded 400, no header 403, malformed 400, unknown case 404, mismatch 400, case unchanged |
| 4 browser journeys with axe, zero unexpected skips | Proven locally | three axe results, zero violations; live form posts JSON with CSRF header, validation 400, no write |
| 5 independent exact-head review, hosted CI | Unproven | needs a human reviewer and a hosted run; not available to this worker |
| 6 full tier receipt | Not applicable here | no src change; `rpi-checks.py --all` not run by instruction |

## Validation

* `python3 -m unittest` (five modules, src/api): 66 OK.
* Three `checks.*_browser_check` runs with axe 4.10.3: passed.
* Live probes on revision 0000045: as above.
