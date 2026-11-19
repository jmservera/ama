# Research: issue 1830 live r2 (2026-11-18)

Task: re-create the non-receipt preflight and gate timing tools from the retained unmerged branch `ci/gate-preflight-benchmark-1830` (frozen `a2c27fda6`) with unit tests.

Disposition: executed. Planning Readiness: Ready.

## Inputs

* Issue 1830 body and five owner comments (2026-11-16). Correction cycles are exhausted; the candidate refuses all selected unit, browser and SQL execution (exit 5). The owner offered "scoped partial delivery (timing analysis only)" as one option.
* Owner decisions 2026-11-18 (task brief): synthetic demo, desktop only, live Azure authorised but irrelevant to the local gate; no private data.
* Prior audit already on main: `docs/reference/research/issue-1830-live-20261118T1648Z-2026-11-18.md` (criteria 1 and 3 partly evidenced, 2 and 4 unproven).
* Branch diff against main is only two tools, two test files, `docs/reference/method/rpi-gate-preflight.md`, index and log; no gate file (`tools/rpi-checks.py`, `src/README.md`) is touched.

## Impact classification

Tools and docs only, no `src/` change, gate semantics untouched (preflight is non-receipt and refuses execution; the analyzer is read-only). Tier FOCUSED. `rpi-checks.py --all` is not run.

## Open questions carried forward

* Trust or isolation boundary for selected test code: owner decision still absent, so the preflight stays fail-closed.
