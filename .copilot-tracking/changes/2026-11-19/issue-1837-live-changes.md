# Issue 1837 live changes, 2026-11-19

Refs #1837. Tier: FULL classification applies (src changed); full gate not run by owner instruction; unproven.

## Files changed

* `src/api/src/zava_forward/api/nomination_routes.py`: standalone page head links `/style.css` and a viewport meta.
* `src/api/checks/nomination_route_forms_browser_check.py`: asserts zero axe target-size violations (open-finding exemption removed).
* `src/api/tests/test_nomination_api_routes.py`: asserts the stylesheet link.
* `docs/reference/research/issue-1837-live-demo-evidence-2026-11-19.md`, its `issue-1837-live-2026-11-19/axe-route-forms-result.json`, index and log entries.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| 1 Failing-first coverage, three submissions | Proven on source (2026-11-18 record; tests on main) |
| 2 Valid submissions retained, JSON compatible | Proven locally; unproven live (needs redeploy) |
| 3 Negative boundaries | Proven (tests, live probe 2026-11-18) |
| 4 Browser journeys with axe | Proven locally: zero violations, zero target-size; one color-contrast incomplete |
| 5 RPI evidence, independent exact-head review, hosted CI | Partly: dated artifacts only; review and CI unproven |
| 6 FULL-tier receipt | Unproven by instruction |

## Validation

* `tests.test_nomination_api_routes` 8 OK; `tests.test_accessibility_baseline` and `tests.test_content_standard` 48 OK.
* Browser check passed (axe 4.10.3, SHA verified).
* ruff format/check clean on changed files. mypy: 7 errors in `src/core/tests/telemetry_support.py` (missing opentelemetry stubs), identical with changes stashed; none in changed files.
* Manifest recipe SHA not applicable: the check script is not listed in `scenario-manifest.json`.
