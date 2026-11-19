# Issue 1837 live changes, pass 4, 2026-11-19

Refs #1837. No source change. Tier: focused (documentation only); the FULL classification of the underlying fix stays open and unproven. Nothing in Azure was created or changed; only an unauthenticated read-only probe ran.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Failing-first coverage, three submissions | Proven on source | 2026-11-18 failing-first record; tests on main |
| 2 Valid submissions retained, JSON compatible | Proven locally; unproven live | Tests pass locally; live needs redeploy from main (production change, excluded). Unauthenticated live POST returns 401 for form and JSON, inconclusive |
| 3 Negative boundaries | Proven | Unit tests and 2026-11-18 live probe |
| 4 Browser journeys with axe | Proven locally | 2026-11-19 axe result, zero violations; one color-contrast incomplete |
| 5 RPI evidence, independent exact-head review, hosted CI | Partly | Dated artifacts only; review and CI need a human and a push |
| 6 FULL-tier receipt | Unproven by instruction | `rpi-checks.py --all` forbidden |

Every remaining criterion is production-only or needs a human; stopping.
