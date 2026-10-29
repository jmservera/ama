<!-- markdownlint-disable-file -->
# RPI Phase Details: Map navigation disposal correction

## Metadata

* Task ID: issue-532-pr-539-map-navigation-disposal
* Task slug: map-navigation-disposal-532
* Related plan: .copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Disposal and scenario isolation | Complete, browser verified | P01-T01, P01-T02 |
| P02 | Local verification | Complete | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct disposal and browser isolation

Context: route abort happens before facets settles. The old screen remains
connected; the map toggle can resurrect a modal without an owning disposer.
Intent: end the obsolete UI's lifetime at disposal rather than destination render.
Boundaries: no backend route, consent, data or layout changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden obsolete map cleanup

Targets: mapPanel expand/dispose, existing cleanup source contract and README.
Set slot.inert and toggle.disabled before collapse; collapse first, invalidate
draw sequence afterward, remove dialog and slot, then remove/null Leaflet and
clear listeners/disposer as before. expand checks the inert state so a retained
event cannot reopen after live-signal session disposal. This reuses the DOM
lifetime state rather than a second independent boolean.
Completion: no accessible obsolete map controls while listView awaits facets;
existing collapse-triggered resize negative checks remain effective.
Dependency: C1/C3 and critique disposition. Unresolved: none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Cover pending facets and reset session iterations

Target: existing map fullscreen browser check; no new fixture or server.
Retain original slot/toggle handles and pointer coordinates before navigation.
Hold /api/facets; follow actual Show these as a list; prove old route aborted,
facets held and destination not yet rendered. Click the old Expand location
while pending, assert no modal/lock, assert disconnected/inert/disabled nodes,
and dispatch a retained click to exercise the guard. Release the real response
and assert All open cases with zero map/dialog/body-lock residue. Always unroute
and release any still-held facets request in finally; retain scenario JSON with
meaningful pending/destination evidence.

Reload at the top of each expiry iteration, then goto Coordinator, await its
heading/clusters, and install the existing wrappers only in the fresh document.
Keep real authentication initialization and valid server cookie. Continue all
existing embedded/expanded/32px font scenarios without bypass or skip.
All browser wait predicates must be functions rather than expression strings,
so Playwright does not require eval under the unchanged strict application CSP.
Completion: pending-state and destination checks plus full browser reaches its
existing enlarged-font result. Dependency: P01-T01 for passing interaction.
Unresolved: none; lock admission controls execution, not source coverage.

<!-- rpi:phase id=P02 -->
## P02: Verify the correction

Context: supplied venv already binds editable core/agents/api to this worktree.
Intent: exact requirement checks with honest lock admission and no cloud use.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute local validation with lock discipline

From API and core run /tmp/mv/bin/mypy, ruff check ., ruff format --check .
using existing project configs. Unit/browser PYTHONPATH explicitly includes
absolute current-worktree core/agents/api src and tests paths, with the current
component's tests first to avoid duplicate-module shadowing. Leaflet pane
readiness means attached, not visible: its absolute pane has no own box. Nonblocking
flock -n /tmp/ama-rpi-heavy.lock owns full API/core unit discovery and map
browser check. If busy, no waiting/polling; run targeted API test_map_fullscreen,
test_design_system, test_accessibility_baseline and test_coordinator_api plus
core test_coordinator, then record full/browser evidence as blocked.

With admission, run full browser and a bounded old-app.js served-response
negative control proving the pending-navigation assertion fails without the
fix. Keep old source outside the worktree and do not modify pinned fixtures.
Check scenario-manifest pins by reading/hash only. Retain external logs/assets;
do not commit generated screenshots or fabricate a full-gate receipt.
Completion: record exact commands/results/admission, reconcile P01/P02 markers,
changes evidence, remaining work and Review boundary. Required human/hosted
approval remains unchecked. No publication or Azure tool invocation.

## Completion Evidence and Review Boundary

P01-T01/P01-T02/P02-T01 complete. API/core strict tooling passes; full units:
API 1214 tests (316 existing skips), core 1454 (190 existing skips). Final
complete browser and exact original-JS negative control pass cleanly under
nonblocking lock at /tmp/ama-532-navigation-final-20261029-l51h74.
Both expiry modes complete with no late map mutations, navigation leaves no
dialog/slot/body lock, and 640px/32px-font coverage completes. Ten axe scans have
zero violations; browser errors is empty. Failed prior attempts are retained
in the changes record, not upgraded. No implementation work remains.
