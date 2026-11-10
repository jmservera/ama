---
title: Issue 1384 workspace exhaustion oracles research
description: Instrumented current-main red and the existing bounded script-retry contract for the two generic workspace browser checks
ms.date: 2026-11-10
ms.topic: reference
---

## Task and Boundary

* Task: `workspace-oracles-1384-1110` (issue #1384), branch `fix/demo-workspace-retry-oracles-1384-1110`, own worktree, pinned main `caaf989148aff21ed8ecb5b71eb0be75b29c16de` (tree `ca940dd47be4510b1ad5efd2762e75f92b8e5e25`). Target is main; independent checker bug, not a child of #133, not #133C6, not a production repair.
* Admission: one initial native RPI attempt, no automatic correction pool, no other issue's budget reset.
* Research disposition: executed (new instrumentation on current main). Parent-run evidence (`demo-next-admission-after216-1228.txt`, `handoff-133-workspace-baseline-1220.md` and its raw comparison) is used as an input only. Those runs were on `50e1d214` and `cc7dbb4b`, not on this main.
* Planning Readiness: Ready.

## Current-Main Red (observed, not inferred)

Environment: own venv `/home/azureuser/.cache/ama-venv-1384-workspace-oracles-1110` (plain venv, third-party pins from the #133 baseline freeze, editable installs of this worktree's `src/core`, `src/agents`, `src/api`; created because the global editable installs point at the primary checkout). Chromium 156.0.8078.4, Python 3.12.3, Node v24.21.0. Server child process uses this worktree's `src/*/src` through `PYTHONPATH`. Synthetic loopback only. Browser runs used `flock -n /tmp/ama-rpi-heavy.lock` (non-queued). An unrelated holder existed at the first probe (pids 4077638/4077639/4080157, command lines not recoverable) and had exited before the first run; no run waited, retried or killed anything.

Raw evidence, unique names, never overwritten: `.copilot-tracking/evidence/2026-11-10-issue-1384-workspace-oracles/`.

| Artifact | Meaning |
| --- | --- |
| `00-baseline-test_workspace_scripts.*` | Existing loader tests on main: 5 OK |
| `01-original-red-employee_workspace_browser_check.*` | Unmodified check, exit 1 |
| `01-original-red-workspace_scripts_browser_check.*` | Unmodified check, exit 1 |
| `02-diag-employee.json`, `02-diag-scripts.json` | Observation-only diagnostic (`diag_script_requests.py`) |
| `03-diag-scripts-pre-unroute.json` | Second diagnostic run that also captures the terminal state before the native reload |

Original failures on current main, byte-for-byte the same assertions as the parent/child comparison:

* `employee_workspace_browser_check.py`: exit 1 after 11 PASS lines, `missing_ops_recovery`, `check("missing ops exhausts the bounded initial/retry attempts", original_ops == 3)` raising `AssertionError: missing ops exhausts the bounded initial/retry attempts`.
* `workspace_scripts_browser_check.py`: exit 1 after 3 recovery PASS lines plus the server line, `exhaustion()`, `assert len(requests) == count` (`count = 3`) raising a bare `AssertionError`.

Diagnostic observations (the diagnostic runs the unmodified scenario functions, keeps their assertions and records network events, script element add/load/error/remove events and the terminal page state):

| Scenario | Target requests at terminal state | Identity and timing | Terminal state |
| --- | --- | --- | --- |
| Employee `/ops.js` answered 404 | 4 | all `resource_type=script`, all `?v=<release>` URL; the initial load is followed by three retries spaced ~505 ms and ~1505 ms after the first retry (the declared 500 and 1500 ms delays; the first retry starts 250 ms after the sign-in-triggered load) | script `error` events each time; heading Workspace unavailable, alert and status name `/ops.js` |
| Scripts `/vendor/leaflet.js` aborted | 4 | initial plus three retries, all `?v=<release>`, each `net::ERR_FAILED`; retries spaced ~505 ms and ~1504 ms after the first retry | `leaflet` global absent, Workspace unavailable names `/vendor/leaflet.js` |
| Scripts missing-global (initial aborted, retry answered 200 without the global) | 2 | initial `ERR_FAILED`, one retry HTTP 200 | retry script element fires `load` with `leaflet:false`, then removed; no further retry; terminal Workspace unavailable; passes `count == 2` |
| Delayed companion timeout | 2 | initial `ERR_FAILED`, one retry left unanswered | element removed at the 5 s timeout with no `load` or `error`; recovery stops; a late 200 later evaluates once (existing test asserts a single evaluation) |

Conclusions from observation:

* Both original assertions fail because the observed total is 4, not 3: one initial HTML-driven load plus three retries. Three delays are not three total requests.
* An aborted load or an HTTP 404 both fire `error` and continue the budget. A successful evaluation without the global (`load`) and a timeout both stop recovery. These are separate branches; the checked-in `count = 2` for missing-global is proved correct and must stay separate.
* The numerical cause is therefore a stale check expectation, not a runtime defect: the observed four equals `1 + len(SCRIPT_RETRY_DELAYS)`.

## Existing Contract (loader and documents)

* `src/api/src/zava_forward/api/web/app.js` lines 275 and 304 to 330: `const SCRIPT_RETRY_DELAYS = [250, 500, 1500];`; `retryWorkspaceScript(path)` loops `attempt = 1..SCRIPT_RETRY_DELAYS.length`, waits the declared delay, reuses the original release-versioned `src`, stops when the outcome is not `error` (a timed-out or evaluated script may install lexical declarations), memoizes one promise per path in `workspaceScriptLoads` so a route revisit adds no attempt, and `requireWorkspaceScripts` throws the `reloadWorkspace` error.
* `src/api/README.md` section Workspace script recovery (#524): three-retry budget shared across navigation, timeouts and finished-without-global scripts stop recovery, persistent failure keeps the plain-language error, status/alert and native Reload workspace button.
* `docs/reference/research/ux/briefing-hax-design-note.md` Loading feedback: the script-retry path (#524) states retries and persistent failure. No PRD or ADR provision for script loading was found under `docs/` (searched `docs/` for the loader names and error text; only `docs/reference/log.md` matched); no requirement ID is invented.
* This is the script-tag loading budget. It is distinct from the API GET retry policy (`fetchReadRetrying`, `STARTUP_RETRY_DELAYS`, cold-start gateway failures only, never network errors), which stays out of scope.

## Prior Art

* `src/api/checks/loading_briefing_browser_check.py` lines 20 to 28 already define `script_attempts()` (1 plus the number of `SCRIPT_RETRY_DELAYS` entries) and `SCRIPT_ATTEMPTS`; its missing-global and helper branches keep a literal 2. Delivered by the #531 retry-count drift fix (`.copilot-tracking/research/2026-11-03-issue-531-derive-retry-counts-research.md`, `...-retry-check-drift-research.md`).
* Its parser is lenient: it counts non-blank comma parts, so an empty list gives 1 and non-numeric parts are counted. #1384 requires a loud failure on absent or malformed declarations, so the convention is reused (declaration parsing) with a strict validation rather than copying the lenient count. That file is not modified.
* `src/api/tests/test_workspace_scripts.py` already drives the real `app.js` loader in a Node VM (`retry_uses_the_initial_release_url...`, `retry_contracts_and_route_isolation`); the extension point for coupled regressions.

## Findings and Decisions for Planning

* No product change is required. Delays, loader, auth, API, aftercare and policy stay untouched.
* Expected exhaustion total is derived from the declaration (`1 + len(delays)`), validated strictly; the missing-global total stays the separately proved 2; no number is taken from observed requests.
* Controlled negative controls are needed because a derived oracle only has value if it fails on a changed loader: extra attempt, early termination and route-revisit budget reset, run against the actual served page with a controlled transformation of the served `app.js` (check-side only, no source edit).
* Out of scope and routed elsewhere: the lenient parser in the loading check, whole-workspace and accessibility acceptance, any production retry policy.

## Follow-ups (current)

* Optionally align `loading_briefing_browser_check.script_attempts` with the strict shared helper (separate, outside the two-checker grant).
* Live employee verification of #531 remains owner-run and is unchanged.
