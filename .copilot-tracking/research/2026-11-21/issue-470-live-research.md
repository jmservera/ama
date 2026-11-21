# Research: issue 470 gate journey scan count

Date: 2026-11-21. Planning Readiness: Ready. Research disposition: executed.

## Findings

* `tools/rpi-checks.py` `verify_results` requires `len(journey["scans"]) == 87`.
* Gate run10 (`~/.local/share/ama/gates/g2061/run10/case-journey-results.json`, read-only) holds 91 scans: browser 156.0.8078.4, axe 4.10.3, no page errors, zoom `chrome.tabs.setZoom=2; innerWidth<=640`, 91 distinct states, 0 serious or critical violations, 0 scans with any violation, no "skipped" text.
* The extra scans come from #2161 (staff case screen UX); 87 is stale.
* `src/api/checks/case_journey_browser_check.py` builds the scan list dynamically and declares no expected count. The gate tool cannot import it (needs playwright), so a shared constant would add coupling; the minimal fix is updating the literal.
* Other dependents: `tools/test_rpi_checks.py` lines 2282 (`range(87)`), 2385-2387 (`* 86`, `* 88`, `* 87` negative cases). No other hard-coded scan totals found in `tools/`, `src/api/checks/` or the scenario manifest (only an unrelated `87` in epic child ids).

## Acceptance criteria (issue 470)

See the changes record for the per-criterion table.
