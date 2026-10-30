---
title: Employee loading and briefing phase details
ms.date: 2026-10-30
---

## Metadata

Task ID: 531. Task slug: employee-loading-feedback-531.
Plan: .copilot-tracking/plans/2026-10-30/employee-loading-feedback-531-plan.md.
Research: .copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md.

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Strengthen and execute local evidence | Complete; review ready |

<!-- rpi:phase id=P01 -->
## P01: Strengthen and execute local evidence

Existing runtime already meets local behavior; the meaningful new coverage is
the shell with page scripts disabled, distinct from delayed app.js.
Boundaries: two scoped files plus RPI evidence, no production behavior change.
No live data or identity. Tool execution must use the heavy lock.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Static pre-script coverage and guide

Add static_shell_check to the existing actual-app Playwright script. Create a
javascript_enabled=False context, block off-origin traffic, load /app, assert
the starting message, role/live semantics and no app rendering.
Verify DOM ordering puts shell before all scripts. At 320/1280 px assert
visible text/no page overflow and take a screenshot. Close context in finally.
The early retry is correctly hidden before the watchdog runs; the existing
script-enabled test owns the 4s/15s states and retry action.
Keep screenshots external. Preserve the existing axe scan scenarios.
Update README with flock -w 600 instead of the obsolete nonblocking policy.
The noscript element returned empty locator text in the first run; the later
screenshot shows help text. Do not infer parser behavior from that locator.
Completion: scoped diff and fresh no-JS browser pass.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validation and reconciliation

From src/api use PATH=/tmp/mv/bin:$PATH and
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Run python3 -m unittest discover -s tests -q, ruff check ., ruff format --check .,
and mypy; capture independent exit statuses rather than hide later results
behind an earlier failure. Use the existing pinned /tmp axe asset only after
the runner verifies its SHA256. Run checks.loading_briefing_browser_check.
Record baseline unrelated failures rather than silently fix them.
Exact 199/200 ms evidence belongs to the actual-helper Node unit test, not the
browser runner. Browser evidence covers real controls, reduced motion and axe.
Parent is permitted to use the caller-required /tmp shared lock and existing
tools/assets. Worker-local path restrictions in PC-001 do not override the
parent's explicit caller direction. Use fresh external output directories
prefixed /tmp/ama-issue-531-20261030-, never the candidate checkout for receipts.
Completion: command output, axe JSON, screenshot paths and acceptance matrix.
After implementation reconcile markers/details/changes; Review runs once,
then commit and attempt full exact-head gate. No later changes to candidate
without invalidating gate. Missing prerequisites are publication blockers.

## Completion Evidence

P01-T01 complete: added scenario passed at both widths with no script requests;
README reflects the actual lock and test boundary.
P01-T02 complete: 1370 API tests / 318 opt-in skips, Ruff lint/format and mypy
116 source files all pass. Browser scenario and four axe scopes pass.
External logs and screenshot/JSON evidence are recorded in the changes record.
Exact 199/200 ms is covered by the executed actual-helper unit test.
No remaining active implementation task or new runtime defect.
Full exact-head gate and live/hosted/human approval are not these local passes.
