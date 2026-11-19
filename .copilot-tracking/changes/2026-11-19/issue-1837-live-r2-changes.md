---
title: Issue 1837 second pass changes
ms.date: 2026-11-19
---

No source change. Validation tier: FOCUSED (documentation only); no src edit so no mypy/ruff/test run is applicable. Full receipt not run.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Failing-first coverage, three forms, valid challenge target | Proven | tests on main; 2026-11-18 failing-first record |
| 2 Valid submissions retain records; JSON compatible | Proven locally; live unproven | `tests.test_nomination_api_routes` 8 OK (2026-11-19 note); live write needs redeploy (production change, excluded) |
| 3 Negative tests: authz, isolation, malformed, same-origin/CSRF | Proven | tests plus 2026-11-18 live probe |
| 4 Browser journeys with axe, zero unexpected skips | Proven locally | 2026-11-19 axe result, zero violations |
| 5 Dated RPI evidence; independent exact-head review; hosted CI | Partly | dated artifacts here; independent review and hosted CI need a human/coordinator |
| 6 Full tier external receipt | Unproven | barred for this run (`--all` not run) |

Remaining criteria are production-only or human-gated; stopping.
