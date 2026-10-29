---
title: Map disposal and enlarged-font correction changes
description: Original implementation and validation evidence for PR 539
ms.date: 2026-10-29
---

## Metadata

* Task ID: issue-532-pr-539-map-disposal-reflow
* Plan: .copilot-tracking/plans/2026-10-29/map-disposal-reflow-532-plan.md
* Details: .copilot-tracking/details/2026-10-29/map-disposal-reflow-532-phase-details.md
* Date: 2026-10-29

## Execution Status

Full plan active. P01-T01 is first; remaining P02-T01/P02-T02.
Write boundary is the five planned files and dated RPI artifacts.
P01 source batch and source contracts implemented. Strict/static/unit and
browser validation pending.

## Completed Work

### Disposal and sizing corrections (P01-T01)

Added seq++ immediately after collapse(false) and capped the desktop grid at
min(19rem,45%). Updated existing unit methods to assert the disposal-local order
and capped track. No auth, route-abort or mobile breakpoint behavior changed.

### Browser coverage (P02-T01, validation pending)

Added two helpers in the existing browser check. Disposal instrumentation
observes real draw Promises, API signals, fit/layer mutations and a controlled
collapse moveend; real successful response bounds are verified. Font helper
uses the Chromium Blink setting with unstyled and app-root probes, actual
geometry, summary close/exit and pinned axe. Updated API README coverage.
Actual local probe confirmed the unstyled browser font resolves to 32px.

## Implementation-Time Plan and Detail Updates

Single critique executed with original Revise verdict preserved. PC-001/002
were incorporated directly in plan/details. PC-003 rejected because the
restriction reported by the critique worker does not apply to the parent.
Parent /tmp/mv exists, but import probe failed with ModuleNotFoundError for
zava_forward.api. Install the required editable src packages under the shared
nonblocking lock before validation. No dependency manifest changes are needed.

## Validation Record

External evidence root: `/tmp/ama-532-disposal-reflow-20261029-0330`.
Editable installation succeeded under `flock -n -E 75 /tmp/ama-rpi-heavy.lock`:
`/tmp/mv/bin/python -m pip install -q -e src/core -e src/agents -e "src/api[dev]"`.
The isolated Chromium default-font probe passed (32px, unstyled about:blank).

The next nonblocking admission for full map browser/API checks returned exit 75.
Actual holder inspection: PID 661156, command flock. No waiting, retry, foreign
output inspection or interference. The browser command and chained checks in
that admission did not execute; targeted.log is empty, not passing evidence.
Full unit discovery and browser/negative-control execution remain unperformed
under this contention. Do not retry without a later explicit coordination event.

Lightweight fallback commands all passed:

| Check | Result |
| --- | --- |
| API targeted unittest: test_map_fullscreen test_design_system test_accessibility_baseline test_ui_support test_workbench | 33 passed, no skips |
| API ruff check . | Passed |
| API ruff format --check . | Passed, 53 files |
| API mypy | Passed, 101 source files |
| Core targeted unittest: test_dependency_rule test_scenario_manifest | 10 passed, no skips |
| Core ruff check . | Passed |
| Core ruff format --check . | Passed, 103 files |
| Core mypy | Passed, 156 source files |
| node --check src/api/src/zava_forward/api/web/app.js | Passed |
| git diff --check | Passed |

Each package used /tmp/mv executables. PYTHONPATH explicitly included this
worktree's src/api/src, src/core/src, src/agents/src, src/api/tests,
src/core/tests and src/agents/tests (plus src/api for the browser import).
The API source-contract/HTTP fixtures emitted their existing explicit
"law store is not loaded" synthetic warnings while all 33 tests passed.
Core scenario-manifest tests passed: none of the five changed files are pinned
inputs, so no pin change is required.

## Plan Reconciliation and Validation Limitation

P01-T01 is complete. P02-T01 code and documentation are implemented but browser
verification and both pre-fix negative controls are blocked by contention.
P02-T02 lightweight checks are complete; full units/browser and independent
Review are not yet complete. Preserve these distinctions in Review and final
handoff rather than declaring a full verified acceptance.

Final lightweight rerun after the request-capture handshake correction passed:
API strict tools plus the same 33 tests; core strict tools plus the same 10 tests.
Logs: api-targeted.log and core-targeted.log under the external evidence root.
Package-origin probe confirmed all three imports resolve inside this worktree.
Guidelines were refreshed successfully immediately before scoped Review.

## Pre-Review Reconciliation

Plan markers, details, changes and state distinguish completed P01 from
implemented-but-unexecuted P02 browser coverage. No source defect is knowingly
left open. Browser/negative-control and full-suite verification is still blocked,
so overall implementation is Partial, not a fully verified acceptance.
The user explicitly authorizes targeted fallback on contention and all four RPI
phases; proceed with one independent Review of this disclosed boundary.

## Blockers and Remaining Work

Heavy-lock contention blocks full units, map browser and negative controls.
The user explicitly permits targeted checks when busy. Continue the requested
single independent Review with this limitation, then commit locally and stop.
Publication and human/hosted approval remain out of scope.

## Follow-Up Items

Run full API/core units and the map browser check plus negative controls after
an explicit coordination event establishes heavy-lock availability. This is
validation follow-up, not a second Review or authority to push.
