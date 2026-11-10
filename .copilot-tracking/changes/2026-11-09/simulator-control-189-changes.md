# Changes: admin simulator run control (#189)

Base `df8e858b2150198e5e22c73d224a0d3592c73daa` (tree `af1e9ea329f7ff5116c1279ab780ef649b1593cd`), equal to fetched `origin/main`. Plan: `.copilot-tracking/plans/2026-11-09/simulator-control-189-plan.md`. Critique: one run, verdict Revise, all three findings applied.

## Added

* `src/api/src/zava_forward/api/simulator_admin.py`: admin-only status/start/stop over the existing `live-sim-control-v1` file; reuses `live_control.parse/check_window/write`, `live_simulator.check_capacity`, `accountable_text`, `identity.display`.
* `src/api/src/zava_forward/api/web/simulator-control.js`: screen using existing `h/api/show` helpers and native controls.
* `src/api/tests/test_simulator_admin.py` (25 tests): authorization matrix (module and HTTP), guards, stale/rejected/unavailable, cap, expiry, stop idempotence, second start, failed and unverified writes, audit failure, lock busy, racing starts.
* `src/api/checks/simulator_control_browser_check.py`: Playwright and pinned axe 4.10.3 on a synthetic store.

## Modified

* `live_control.py`: `locked()` advisory flock on `<file>.lock`; CLI start/stop use it (busy refuses, exit 2).
* `server.py`: narrow GET hook and POST hook (CSRF kept; path-specific exception to the view-only gate for verified app admins).
* `workbench.py`: admin `#/simulator` destination. `app.js`, `index.html`: loader entry, route, script tag.
* Tests adapted deliberately: `test_entra_authoritative` (simulator entry is "available", the rest unchanged), `test_live_control` (lock sidecar file expected), `test_content_standard` (new file audited).
* `src/api/README.md`: replaced "not delivered" with the delivered surface and limits.

## Divergences and findings

* Browser check found a real defect (nested arrays in `h`, `dl` rendered as objects); fixed with `flatMap`.
* Budget alert is always "not recorded, not verified live": the schema has no alert field. AC3 stays unproven.

## Validation (local, synthetic, no Azure)

* `test_simulator_admin` 25 OK; `test_live_control` 34 OK; `test_entra_authoritative` 36 OK; `test_auth` 41 OK; `test_workspace_scripts` 5 OK; `test_content_standard` 18 OK; `test_design_system` 8 OK; `test_live_simulator` 30 OK.
* Whole `src/api` discover: 2103 ran, 365 skipped, 1 error in `test_ai_consumption_api` (capacity quarantine, unrelated); that file passes alone (17 OK).
* ruff check and mypy clean on touched files; ruff format applied to new files.
* Browser/axe: passed for unavailable, rejected start, permitted and stopped states; axe sha256 `880970c0...8a68bb` verified.
* Merge trial of this tree against `fix/demo-recovery-1292-1109`: clean (no textual overlap). Final integration still waits for #1292 on main.
* Not run: `rpi-checks --all`, SMB flock proof, live Azure, any deployed job.
