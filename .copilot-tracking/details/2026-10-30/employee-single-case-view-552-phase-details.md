---
title: Employee single case view phase details
ms.date: 2026-10-30
---

## Metadata

Task ID 552; slug employee-single-case-view-552.
Plan: .copilot-tracking/plans/2026-10-30/employee-single-case-view-552-plan.md.
Research: .copilot-tracking/research/2026-10-30/employee-single-case-view-552-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Implemented | P01-T01 |
| P02 | Scoped validation and Review complete; full gate blocked | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Strengthen focused verification

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add scoped axe and responsive attached-tab checks

Existing runtime already meets the requested structure (research C1-C4).
Reuse the general journey's scan routine, but assert no violations rather than
only serious/critical, and preserve complete reports/incomplete entries in
results.json even on failure. Verify pinned axe hash before launching the app.
Baseline-only capture remains available without axe.

Scan each responsive overview and an open blocker disclosure at 1280/390/320.
Assert one-line summary and existing density ceilings unchanged. For each
viewport, select Resident, retain its note, scroll tabs into view, measure
tablist/panel/surface ancestry and bounding boxes, use keyboard to scroll panel
to end and compare tablist before/after. Record viewport dimensions, panel
scroll dimensions and tablist positions, plus an attached-tab screenshot.
Focus panels rather than imperatively assigning scrollTop. Keep keyboard,
touch, fallbacks and 200% root text existing checks.

Targets: existing dedicated check and README. No new dependencies, runtime
changes, test methods or test removals. Completion: current check passes and
records explicit responsive scroll and axe states. Unexpected behavior is
investigated before Review, not waived or silently defaulted.

<!-- rpi:phase id=P02 -->
## P02: Validate, independently review and persist

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute API and browser checks

From src/api use PATH=/tmp/mv/bin:$PATH and the exact requested
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Run full unittest discovery, ruff check ., ruff format --check ., mypy.
Use flock -w 600 /tmp/ama-rpi-heavy.lock around heavy commands.
Run the dedicated check with pinned axe and fresh external output directory
/home/azureuser/.copilot/session-state/efa3c0ae-28bb-4df9-acfd-bd663c72eec3/files/case-552-browser.
Read JSON and inspect generated journey/disclosure/attached-tab images.
Record exact command, tool versions, outcomes, test skips and uncertainties.
Completed: full API discovery 1379 tests / 320 skips; Ruff check/format and
mypy pass. Real-server browser/axe passes all three widths and nine scans,
with scrolled/offscreen Resident heading/Notes contrast incomplete retained.
Panel checks assert positive keyboard scroll and stationary tabs, not end
arrival; only popover checks assert final-item reachability. This clarifies
the measurement contract without changing issue acceptance.

<!-- rpi:task id=P02-T02 -->
### P02-T02: One Review, local commit and complete local gate attempt

Only after P01 and P02-T01 reconcile, invoke rpi-review and one independent
reviewer. Scope includes focused script, README and unchanged runtime source
needed for issue acceptance. Reviewer must inspect raw external evidence when
available; absence remains explicit. Refresh Web Interface Guidelines and
assess scoped runtime against them, retaining repository overrides.
No changes or second Review after it returns; findings become later work.

Resolve gh api user, configure local noreply identity for author/committer,
commit all implementation and original dated RPI evidence with Refs #552 and
Copilot trailer. Do not push. Attempt complete local gate only if compatible
with no-Azure boundary; otherwise persist a concrete blocker before commit,
and report it. Complete gate self-locks and needs --lock-timeout 600.
Human/hosted/publication approval remains unperformed.
One independent Review is Complete / Residual work with RV-001 publication
blocker, RV-002 manual contrast evidence and RV-003 inherited guideline debt.
No introduced defect. Local persistence uses the enclosing commit; the phase's
complete-gate requirement stays unmet, never checked as passing.

## Critique Reconciliation

PC-001 original Revise preserved. Parent is allowed to execute existing /tmp/mv
tools and acquire the user-required /tmp lock; no parent file restriction
prohibits either. Reviewer receives fresh external session-path evidence rather
than /tmp assets. Full gate's mandatory az commands conflict with no-Azure
direction; do not run it or invent a receipt.
