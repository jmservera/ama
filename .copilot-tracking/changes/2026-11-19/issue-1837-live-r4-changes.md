---
title: Issue 1837 live demo, fourth pass changes (2026-11-19)
ms.date: 2026-11-19
---

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Failing-first coverage, three forms, valid challenge target | Proven | merged tests; 2026-11-18 failing-first record |
| 2 Valid submissions retain records; JSON compatible | Proven locally; live unproven | `tests.test_nomination_api_routes` 8 OK (this run); live write needs redeploy (production change, excluded) |
| 3 Negative tests: authz, isolation, malformed, CSRF | Proven | existing tests and 2026-11-18 live probe |
| 4 Browser journeys with axe | Proven locally | 2026-11-19 axe result file |
| 5 Dated RPI evidence; independent exact-head review; hosted CI | Partly | dated artifacts only; reviewer and CI are human or coordinator gates |
| 6 Full tier receipt | Unproven by instruction | no src change; `rpi-checks.py --all` barred |

Tier: focused (docs and tracking only). No src change, so no mypy or ruff scope. Result: every remaining criterion is production-only or needs a human; stopped.
