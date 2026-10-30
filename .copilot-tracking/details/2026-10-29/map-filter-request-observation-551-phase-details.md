---
title: Map filter request observation phase details
description: Implementation and validation boundaries for issue 551 correction
ms.date: 2026-10-29
---

## Task Context

Task 551 / map-filter-request-observation-551. Ready research establishes the
held-route oracle defect and existing listener/two-frame pattern. No planning
blockers. One critique is required before source edits.

<!-- rpi:phase id=P01 -->
## P01: Correct observation and documentation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Observe all map requests and document coverage

In check_expanded_filters, install a typed request callback immediately around
the two safety Space presses, record the initial map request, snapshot its
count and verify no additional request after browser processing. Use nested
finally cleanup; retain outer route cleanup and later stale-response scenario.
Update the focused browser coverage paragraph in src/api/README.md only.
Completion evidence: reviewable small diff with no app changes.
Status: Complete. Ruff also normalized existing formatting in the touched
Python file to satisfy the caller's whole-file format check.

<!-- rpi:phase id=P02 -->
## P02: Validate the oracle and deliver locally

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused checks and positive/negative browser checks

Run from src/api with
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests:
/tmp/mv/bin/python -m unittest test_map_fullscreen test_accessibility_baseline
test_design_system test_content_standard test_loading_feedback
test_workspace_scripts -q.
Run /tmp/mv/bin/python -m ruff check and ruff format --check on the changed
Python file, node --check src/zava_forward/api/web/app.js and git diff --check.
Use pinned axe 4.10.3 and the existing actual loopback browser harness.
Mutation validation may wrap run_browser externally and intercept app.js to
remove exactly the already-selected guard in memory. Assert that the failure
is specifically "selected flag suppresses duplicate reads"; another failure
does not prove sensitivity. Do not persist the app mutation.
Reports, logs and runner stay under this session's external files directory.
For both browser runs, acquire /tmp/ama-rpi-heavy.lock using flock -n and
release when the command exits. If busy, retry nonblocking for at most 40
minutes, then record a blocker. Set TMPDIR to a specifically created
repository-root .venv/map-request-observation-551 scratch directory before
launch; remove only that owned empty scratch directory after process cleanup.
The existing harness health-checks and cleans its owned loopback server.
Status: Complete. 35 focused tests and all requested static checks pass.
Positive browser: 248 assertions; targeted duplicate-read mutation rejected.
Both browser runs acquired the shared lock and used the isolated TMPDIR;
the owned scratch directory was removed after cleanup.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile evidence, run one independent Review and commit

Record command outcomes, original failures, deviations and remaining work in
the changes artifact. Dispatch one independent rpi-review for this correction,
not the entire parent PR; retain its original outcome and route new findings.
Resolve gh api user, configure repository-local privacy-safe identity, stage
only task-owned files and commit with Conventional Commit plus requested trailer.
No push, Azure operations, score edits, publication receipt or human approval.
Status: Review Complete / Conformant with justified divergence, no findings.
All task-owned source and original evidence are prepared for the same local
commit; its success, identity/trailer and clean worktree are checked afterward.
