<!-- markdownlint-disable-file -->
# Issue 189 plan: admin simulator control surface (2026-11-09)

Research: [research](../../research/2026-11-09/simulator-control-189-research.md). Details: [details](../../details/2026-11-09/simulator-control-189-details.md). Critique: [critique](simulator-control-189-critique.md). Initial RPI; correction budget unspent (five TOTAL default, no reset).

## Objective

Deliver the documented missing admin-only start/status/stop surface over the EXISTING `live-sim-control-v1` file and guards. No new simulator, model, provisioning, backend rewrite or quota/cost duplication. Refs #189 only; live AC3 stays unproven.

## Phases

* [x] P1 `simulator_admin.py`: authorization, status, start, stop reusing `live_control` and `live_simulator.check_capacity`.
* [x] P2 Host hooks: `server.py` GET and POST (before the `view_only` gate, path-specific), `workbench.py` administrator destination, `app.js` route and loader entries, `index.html` script tag.
* [x] P3 `simulator-control.js` screen using existing `h`, `api`, `show`, `AsyncAction`; non-colour status text, manual route, confirmation, failure and unavailable states.
* [x] P4 Tests: `test_simulator_admin.py` (module and HTTP, negative auth first), browser and axe check script, existing-test update for the intended administrator navigation entry, content-standard audit file list.
* [x] P5 Docs: `src/api/README.md` replaces the "not delivered" sentence with the delivered surface and its limits.
* [x] P6 Targeted demo-tier validation, one Review, local commit, handoff.

## Success criteria

* Only an Entra principal with `app_admin` and a verified tenant/oid is served; every other principal, header or provider gets 401/403 with no state change or disclosure.
* Start cannot bypass `parse`, `check_window`, `check_capacity`, cap 100, 14-day maximum, non-placeholder owner and approval reference; a second start while sending is refused; a stale revision is refused; a failed or unverifiable write is surfaced and claims nothing.
* Stop is always available when a readable control exists, idempotent, and never needs the simulator process.
* Status never calls a declared or fixture reference a configured or verified alert.
* Manual CLI and Azure RBAC routes stay documented; nothing deploys, calls Azure or starts a job.

## Validation (owner-selected demo-targeted tier, no `rpi-checks --all`)

`test_simulator_admin`, `test_live_control`, `test_entra_authoritative`, `test_auth`, `test_workspace_scripts`, `test_content_standard`, `test_design_system` and other nav-affected modules found by grep, live_simulator/receiver tests, ruff and mypy on touched files, Playwright browser check with pinned axe-core 4.10.3 when obtainable (otherwise recorded as NOT RUN), post-change `git merge-tree` trial against the #1292 branch.

## Risks and dependencies

* #1292 touches the same two host files in line-disjoint hunks; trial merge decides; freeze partial LOCAL if a conflict appears.
* API container may lack a writable control file: screen reports unavailable; no infra change.
