<!-- markdownlint-disable-file -->
---
title: Workspace script retry phase details
description: Task context and validation ownership for issue 524
ms.date: 2026-10-28
---

# RPI Phase Details: workspace-script-retry-524

## Metadata

* Task ID: 524
* Task slug: workspace-script-retry-524
* Plan: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md
* Research: .copilot-tracking/research/2026-10-28/workspace-script-retry-524-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Bounded recovery | Source/tests/documentation complete | P01-T01, P01-T02 |
| P02 | Validation and handoff | Heavy validation blocked; reconciled | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Bounded recovery

Context: synchronous HTML loading may leave a required global absent. Existing
route detection is authoritative for which scripts are needed; companion scripts
have lexical declarations that prohibit indiscriminate reload.

Intent: repair only missing dependencies without changing ordinary startup.
Excluded: app.js initial load recovery (the guard itself must execute), CSS,
infrastructure, auth and private data.
Targets: app.js, test_workspace_scripts.py, workspace_scripts_browser_check.py,
API README. Dependencies: research and critique. Completion: new tests and actual
browser recovery. Unresolved: historical live delivery cause, owner verification.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Await missing dependencies safely

Retain route predicates, extract current missing-path calculation if useful,
share page-lifetime path promises and perform two attempts using dynamic classic
script tags. Delay 250ms then 500ms; each attempt has a 5000ms timeout. Only
definitive script error permits a second insertion. Timeout ends the path's
recovery because removal does not guarantee execution cancellation. A load event
also ends attempts; if the sentinel is absent, fail explicitly instead of risking
lexical redeclaration of partially initialized code. Remove elements and clear
timers/handlers on success, error or timeout. Return control
through existing route failure handling after readiness recheck. The awaited
route signal must be checked before invoking any view or publishing a late error.
Reusing a completed failed promise must not create another request cycle.
Progress uses existing polite status; native markup and final copy remain.
Completion evidence: unit assertions for bounded requests, timer cleanup, global
recheck, healthy dependencies, and route cancellation.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add regression coverage and operator documentation

Reuse Node VM via unittest for deterministic fast timeout/budget tests and existing
synthetic server callback for Chromium. Use only constructed fixtures. Browser
intercepts first Leaflet delivery, then allows real bytes; assert map appears and
document navigation count stays one. Permanent failure must yield exactly three
total requests (initial plus two), identical message, semantic alert/status and
native keyboard reload action. Include companion-script recovery and delayed
navigation/sign-out isolation. Browser request API checks status, byte count,
Content-Length, no-store and JavaScript type without reading a private dataset.
Hold a lexical companion response beyond 5000ms, assert terminal error with no
overlapping attempt, navigate to an independent view, then release the response
and assert one evaluation and no stale view/error/progress. A subsequent visit
may use a now-present global, but must never trigger a new path budget.
README records retry bounds, focused command and live limitations.

<!-- rpi:phase id=P02 -->
## P02: Validate and hand off

Scope: tests, original implementation evidence and independent Review handoff.
Dependency: P01 complete. No deployment. Completion: required checks executed
and failures/blockers surfaced explicitly.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused and API validation

From src/api with task venv on PATH:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest test_workspace_scripts -q
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q
python3 -m checks.workspace_scripts_browser_check
ruff check tests/test_workspace_scripts.py checks/workspace_scripts_browser_check.py
mypy checks/workspace_scripts_browser_check.py tests/test_workspace_scripts.py
```

Use flock -n /tmp/ama-rpi-heavy.lock around heavy unit/browser execution. Full
runner owns its lock, using --lock-timeout 0. No second outer lock around it.
Node --check validates changed production JavaScript. No changed Ruff config or
line-length exemptions. Browser outputs remain external; evidence summaries
are committed. Post-review, commit candidate and original RPI evidence, then
attempt complete exact-head gate in a new external directory.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile evidence and hand off to Review

Reconcile plan checkboxes, details, changes, blockers and validation. Run exactly
one independent Review after implementation; do not loop back to implementation
inside this task. Commit original outcomes with source. Resolve GitHub identity
and privacy-safe email before commit. Fetch main and require exact-head receipt
verification before push. If publication gates block, keep local committed work
and report blocker rather than force-pushing or creating an unsupported PR.
If published, use Refs #524 while post-deployment checks remain pending.

Current handoff: source stable, 32 lightweight unit tests and package-wide
Ruff/mypy pass. Required API discovery and Chromium never started because the
mandated shared lock was occupied; repeated nonblocking attempts after independent
work exited with contention status, without waiting or bypass. Review may assess
this explicitly incomplete boundary once, but cannot claim full conformance.
