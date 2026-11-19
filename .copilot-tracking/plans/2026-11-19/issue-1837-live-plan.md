# Issue 1837 live plan, 2026-11-19

1. Add `<link rel="stylesheet" href="/style.css">` to the standalone routes page head in `src/api/src/zava_forward/api/nomination_routes.py`.
2. Make `src/api/checks/nomination_route_forms_browser_check.py` assert zero target-size violations (drop the open-finding exemption).
3. Add a unit assertion that the page links the stylesheet.
4. Run affected tests, accessibility and content-standard tests, the browser check, mypy, ruff. Update the scenario-manifest recipe SHA-256 for the changed check script and run its two tests.
5. Record the per-criterion table in changes; review; commit locally.

Tier: FULL classification applies by src change; the full gate is not run by owner instruction; recorded as unproven.
