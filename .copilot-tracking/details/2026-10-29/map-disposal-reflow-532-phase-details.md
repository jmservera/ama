---
title: Map correction phase details
description: Bounded targets and evidence expectations for PR 539
ms.date: 2026-10-29
---

## Metadata

Task ID: issue-532-pr-539-map-disposal-reflow.
Plan: .copilot-tracking/plans/2026-10-29/map-disposal-reflow-532-plan.md.
Research: .copilot-tracking/research/2026-10-29/map-disposal-reflow-532-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete; source contracts passed | P01-T01 |
| P02 | Implemented, validation partial under lock contention | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct disposal and sizing

<!-- rpi:task id=P01-T01 -->
### P01-T01: Surgical source corrections

app.js dispose currently calls collapse(false), removes map then nulls it.
api() 401 invokes login without route abort. Increment seq after collapse to
invalidate every earlier draw, including one started by collapse resize.
style.css desktop expanded workspace uses 19rem; cap at min(19rem,45%).
Update the existing unit methods to protect ordering and new track value.
No new disposal flags, auth changes, layout redesign or dependency changes.
Completion: source diff matches this scope and focused unit checks pass.
No unresolved implementation choice.

<!-- rpi:phase id=P02 -->
## P02: Regression and final evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Deterministic browser checks

Use the real Overview tile/area handlers to start two pending fits. Intercept
map requests, obtain a genuine successful response and assert bounds exist.
Deliver earlier 401, wait for the real sign-in alert, then release the successful
response. Observe actual async completion (not merely network delivery) and
assert no fit call, JS error, subsequent request or modal/body residue.
Exercise embedded and expanded disposal and retain live-signal verification.
Instrumentation is check-only; no production hooks. Before navigating to the
Overview install a wrapper around mapPanel's returned draw function and observe
each returned Promise with fulfillment/rejection handlers. Capture fetch's actual
AbortSignal and request URLs. Settle initial rendering before interception.
Invoke the existing area's change handler via DOM dispatch for expanded mode
(do not pointer-click inert background). Identify fit requests by absence of
bbox and request order before disposal, never require unchanged seq afterward.
Wait for the captured Promise's settled flag and a two-animation-frame drain
with bounded Playwright timeouts. Record and assert any rejection.

For expanded mode instrument invalidateSize to fire an actual moveend during
collapse after the dialog closes. Retain the resulting real draw(false) request,
then release its successful response after disposal as well. Observe fitBounds
and layer clear calls; neither late response may mutate the disposed map.
The cleanup source contract extracts only the dispose closure and checks
collapse(false) < seq increment < dialog/map removal < map = null.

Launch a separate Chromium instance with
`args=["--blink-settings=defaultFontSize=32"]` before creating the 640px context.
Verify an unstyled about:blank document's computed body font is 32px before
navigation and the real app root font is 32px afterward; no author-CSS override
is allowed. Close this owned browser in finally to isolate the setting.
At 640px verify computed root font, select a point, expand, measure document/
dialog/workspace overflow plus sidebar/map widths, and exercise close/exit.
Reuse pinned axe and screenshots with existing evidence output.
Run pre-fix asset-override negative controls without editing source back and
forth. Record exact expected failure, then corrected pass.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Validation and local-only closeout

Hold flock -n /tmp/ama-rpi-heavy.lock for any full suites and shared venv mutation.
Record admission and all actual commands/exits under a new external evidence
directory. Verify /tmp/mv imports use this worktree, installing editable required
packages as necessary. Explicit PYTHONPATH includes this worktree API/core/agents
source and tests. Run API/core mypy, ruff check ., ruff format --check .,
unit discovery and focused map browser check. If lock busy, run targeted light
checks only and record unperformed full work.

Refresh guidelines before scoped web Review. Independent reviewer owns one
original Review artifact, records execution separately from outcome, routes open
findings to later work, and leaves human/hosted approvals unclaimed. Final
evidence includes changes, reconciled markers/state and privacy-safe local commits.
No az, push, force-push, complete publication-gate or live acceptance claim.
Critique PC-003 described the worker's filesystem restriction, not a parent
restriction: /tmp tool reads already succeeded here. Preserve original critique,
but execute the user-authorized parent validation contract without replacement.

## Current Completion and Review Boundary

P01-T01 source and unit-contract work is complete. P02-T01 browser helper code
and README are implemented and strictly type/lint checked; actual execution and
pre-fix controls remain unperformed because nonblocking lock admission returned
75 (actual holder PID 661156). P02-T02 API/core strict checks and 43 targeted
unit tests passed; full discovery/browser remain blocked and are not marked done.

The independent Review receives this exact partial-verification boundary.
Its outcome must not claim conformant acceptance or completed browser coverage.
Original source/critique/review evidence and the local-only commit are in scope;
no repeated lock admission without an explicit coordination event is authorized.
