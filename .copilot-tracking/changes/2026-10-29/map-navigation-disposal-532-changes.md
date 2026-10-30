<!-- markdownlint-disable-file -->
# RPI Changes: Map navigation disposal correction

## Metadata

* Task ID: issue-532-pr-539-map-navigation-disposal
* Related plan: .copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md
* Implementation date: 2026-10-29

## Execution Status

* Status: Complete, full plan.
* Completed scope markers: P01/P01-T01/P01-T02/P02/P02-T01.
* Remaining active-plan markers: none.
* Current boundary: single independent Review Complete / Conformant; local-only
  commit and stop.

## Execution Summary

Single independent critique passed without findings. The four approved
source/documentation files implement inert/disconnected cleanup, a guarded
expand callback, pending-navigation regression and per-iteration document reset.
Full requested local validation is now complete under nonblocking lock.

## Completed Work

### End obsolete map UI lifetime at disposal

P01-T01: app.js marks the slot inert and toggle disabled before collapse,
retains collapse/sequence ordering, removes the slot before destroying Leaflet,
and prevents stale expand callbacks using the inert state. Extended the
existing test_map_fullscreen cleanup-order contract and API README.
Completion evidence: source now disconnects the slot synchronously in dispose;
validation of runtime behavior belongs to P02.

### Pending navigation regression and independent expiry iterations

P01-T02: added one browser helper holding real /api/facets, asserting the
aborted old route and still-rendered Overview, clicking former Expand pointer
coordinates and dispatching retained toggle events. It checks slot inertness,
disabled toggle and zero modal/body-lock residue before/after destination.
Scenario evidence writes pending-navigation.json externally. Added page.reload()
before each expiry iteration's Coordinator navigation and fresh instrumentation.
No existing scenario was removed or weakened; full runtime evidence is P02.

### Complete local correction verification

P02-T01: final full map browser passed both expiry modes and enlarged-font
coverage. Old app.js served without worktree mutation failed at the exact
pending-Expand check and left its modal/body lock over All open cases, proving
the new check detects the reported defect. Fixed source has no such residue.
Ten axe scans, zero violations, Chromium 156.0.8078.4, no uncaught JS errors.
At 640px/32px default font: document width 640, dialog 590/590 client/scroll,
workspace 540/540, sidebar 243/243, map width 271. Embedded/expanded expiry
requests 2/4, no late fits/clears or rejected draws. No fixture/pin edits.

## Implementation-Time Plan and Detail Updates

### Correct the regression's readiness predicate and unit import precedence

P02-T01 local verification exposed two harness issues: Leaflet's absolute map
pane is attached but has no visible own box, so a visible-pane wait timed out;
core discovery inherited API/tests first and collided on test_buildings.
Use attached-pane readiness and prioritize each component's own test directory
in PYTHONPATH. These are ordinary implementation-time test/command refinements,
not new requirements or a significant divergence; no repeat critique.
Original failed logs remain unchanged. No source production correction needed.

### Preserve strict CSP while executing browser waits

The corrected wait allowed the browser to reach a further real harness failure:
expression-only wait_for_function invokes eval under the application's strict
CSP. Updated the new navigation wait and four existing expiry waits to function
predicates, matching the other waits in this check. Assertions and CSP remain
unchanged; no unsafe-eval, bypass_csp or skip is introduced. This is tightly
coupled to making the requested expiry/enlarged-font scenarios actually execute.

### Settle held facets on assertion failure

The full positive browser passed, including both expiry modes and 32px font.
The old-JS negative control reproduced the exact modal/body-lock race, but
closing while its deliberately held request remained unresolved emitted an
asyncio cancellation callback. Release that request in the helper's finally
when not already released; the negative control now also verifies the leaked
modal/lock over the rendered destination before browser shutdown.
The first cleanup refinement released after unroute, but unroute can already
resume the request through the context handler. Final cleanup releases before
unroute, matching the successful ordinary path and avoiding double handling.

## Validation Record

| Check | Status | Evidence |
| --- | --- | --- |
| API mypy | Passed | 101 source files, no issues |
| API ruff check / format --check | Passed | All checks passed; 53 files formatted |
| Core mypy | Passed | 156 source files, no issues |
| Core ruff check / format --check | Passed | All checks passed; 103 files formatted |
| Manifest pins | Passed | All four existing source hashes match; no pinned files edited |
| Diff whitespace | Passed | git diff --check |
| Heavy admission | Acquired nonblocking | /tmp/ama-532-navigation-20261029-U2JSTW/lock.txt |
| Full API units | Passed | 1214 tests, 479.352s, 316 existing skips; /tmp/ama-532-navigation-20261029-U2JSTW/api-units.log |
| First core discovery | Failed command setup | API/tests shadowed core/test_buildings; no core tests executed |
| First browser / negative control | Failed new harness wait | Attached zero-size Leaflet pane cannot meet visible predicate; /tmp/ama-532-navigation-20261029-U2JSTW |
| Corrected core units | Passed | 1454 tests, 299.607s, 190 existing skips; /tmp/ama-532-navigation-recheck-20261029-lTmkGK/core-units.log |
| Second browser / negative control | Failed CSP-unsafe wait | Expression-only predicate blocked by strict CSP; /tmp/ama-532-navigation-recheck-20261029-lTmkGK |
| Third full map browser | Passed | Both expiry modes, 640px/32px font, zero axe violations and no JS errors; /tmp/ama-532-navigation-browser-20261029-kvftqo/browser.log |
| Third original-JS negative control | Expected regression detected; cleanup warning | Reopened modal/body lock observed; pending route shutdown emitted cancellation callback, fixed before final run |
| Fourth full map browser | Passed | /tmp/ama-532-navigation-verified-20261029-O2Wypw/browser.log |
| Fourth negative control | Failed cleanup ordering | Explicit continue after unroute double-handled the held route; reordered before final rerun |
| Final full map browser | Passed | /tmp/ama-532-navigation-final-20261029-l51h74/browser.log and browser/*.json |
| Final original-JS negative control | Passed, expected assertion failure observed | /tmp/ama-532-navigation-final-20261029-l51h74/negative-control.log; no cleanup warning |
| Final API/core strict tooling | Passed | mypy 101/156 files; ruff check . and ruff format --check .; 53/103 formatted files |
| Final app.js syntax / diff whitespace / scenario pins | Passed | node --check; git diff --check; all four manifest pins match |

### Commands and environment binding

From each component: /tmp/mv/bin/mypy, /tmp/mv/bin/ruff check .,
/tmp/mv/bin/ruff format --check . and
/tmp/mv/bin/python -m unittest discover -s tests -q.
PYTHONPATH uses only this worktree's src/api, api/src, api/tests, core/src,
core/tests, agents/src and agents/tests absolute paths. Each component's own
tests directory takes precedence for duplicate test module names.
Editable api/core/agents distributions already resolve to this worktree;
no dependency installation was needed.

Final browser invocation from src/api:
`/tmp/mv/bin/python -m checks.map_fullscreen_browser_check --axe /tmp/ama-532-navigation-20261029-U2JSTW/axe-4.10.3.min.js --out /tmp/ama-532-navigation-final-20261029-l51h74/browser`.
The check verifies axe SHA-256
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb
before execution. Each heavy batch acquired
`flock -n -E 75 /tmp/ama-rpi-heavy.lock`; no contention, waiting, skip-token or
cloud fallback. Lock released after each batch, including failures.

Negative runner:
/home/azureuser/.copilot/session-state/7ea8a749-09ea-4588-9bb5-768af3a41c5a/files/map_navigation_negative_control.py.
It serves app.js exported from starting HEAD 310889fa, catches only the exact
expected regression assertion, verifies the reopened modal and lock before
and after destination rendering, and fails on unexpected success/error.

## Pre-Review Reconciliation

Ready: all plan markers/details, completed source work, test refinements,
validation state, handoff and empty remaining-work/follow-up lists reconciled.
No significant divergence, repeated critique or unresolved decision.

## Blockers

None for the user-requested local correction. Full suites retain their existing
optional/environment skips (316 API, 190 core). No real SQL, hosted check, human
assistive-technology acceptance or complete publication-gate receipt is claimed.
No push is authorized; the publication gate is not run and az is not invoked.

## Remaining Work

None in Implement or Review. Single independent Review executed Complete /
Conformant with no RV findings or follow-ups. Only the authorized local commit
remains in parent closeout; no source changes planned.

## Follow-Up Items

None. Canonical list is in the related plan.

## Return-to-Caller State

Full-plan implementation Complete, P01/P02 and all task markers complete.
Requested strict/unit/browser checks and exact negative control pass, original
failures preserved. Single independent Review Complete / Conformant; no
blockers/findings/follow-ups. Manual mode, stopped session; local commit and
stop under the user's bounded full-loop request.

## Local Commit Preparation

The authenticated account was resolved through gh api user. Repository-local
user.email is constructed from its returned id/login as the GitHub noreply
address, and the same address is used for author and committer. The existing
.gitignore is nonempty and the final pre-stage inventory contains only the
four reviewed source/documentation files and this round's seven dated artifacts.
No secrets, generated browser assets or private datasets are staged.

The git-commit skill's get_changed_files helper is unavailable in this CLI.
The actual final diff and complete inventory were reviewed with available Git
tools before staging; no unavailable helper execution is claimed. Its relocated
commit-message rules were read from rules/hve-core after the supplied
instructions/hve-core path proved unavailable. Conventional format is retained,
with the explicitly required Copilot coauthor as the final trailer. No push,
force-push, merge, az or closing keyword is used.
