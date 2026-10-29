---
title: Loading and briefing correction plan
description: Four bounded review corrections for PR 538
ms.date: 2026-10-29
---

## Task Metadata

* Task ID: 531-corrections-2026-10-29
* Task slug: loading-briefing-hax-531-corrections
* Planning status: Ready; original critique Revise, PC-001 resolved directly
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-corrections-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-corrections-plan-critique.md

## Executive Summary

Restore draft-review cancellation focus, keep queue search editable during
reads, restore pre-handler busy state and preserve sentence/citation boundaries.
Reuse current feedback, sequence guards and browser harness. Each correction
gets a regression. Local-only commits preserve historical parent RPI outcomes.
The requested journey venv is absent; use verified existing issue-531 Python
3.12 with this worktree first on PYTHONPATH and disclose the substitution.

## User Decisions and Requirements

* Run research, plan, implement and review with dated committed artifacts.
* Correct the four supplied findings, each with a regression test/assertion.
* Reuse feat/loading-briefing-hax-531, PR #538; Refs #531 only.
* No push, az, force-push or closing keyword. Conventional Commits and required trailer.
* Validate core/API units and relevant existing browser/axe checks locally.
* Full suites require flock -n /tmp/ama-rpi-heavy.lock; on contention run targeted tests only.
* Update scenario SHA-256 pins only if workbench manifest or browser recipe changes.

## Goals

Preserve usable keyboard interaction and accurately bounded source attribution
without changing draft authority, mutations or server access.

## Scope and Non-Goals

In scope: three named runtime files, direct regression owners and API README.
No redesign, dependency changes, cloud calls, publication, merges or global audit.
Original parent artifacts are immutable historical evidence for this round.

## Functional Requirements

* Cancel returns to the opener, including enabled rejection when edit is disabled.
* Search stays enabled/focused with progress and accepts overlapping queries.
* Busy cleanup restores the value from before task invocation.
* Trailing citations remain attached to separate sentence text.

## Non-Functional Requirements

Preserve native semantics, non-colour live feedback, stale-source refusals,
duplicate mutation suppression, handler-owned disable, sequence guarding,
newlines and citation resolution. Keep changes surgical and source-local.

## Acceptance Criteria

* Browser asserts edit and rejection cancellation focus for ordinary and unavailable drafts.
* Browser holds two debounced search reads, checks typing/focus/progress and
  releases responses in reverse order to assert latest results win.
* Helper test simulates synchronous busy set, finally cleanup after recoverable
  failure, retry and restoration of absent/false pre-action busy attributes.
* Core test asserts exact two statement objects for adjacent trailing
  citations, plus punctuation/newline/multiple-reference cases.
* Record actual unit/browser/static commands, exits, skips and lock admission.
* One independent critique and one independent post-implementation Review,
  retaining original verdicts and routing any findings rather than repeating Review.

## Sources

Research: .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-corrections-research.md
(C1-C6, W1). Commands: src/api/README.md and src/README.md.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement four bounded regressions and fixes

Dependencies: completed Research and dispositioned critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fix review focus and editable search

Track the review opener explicitly; null-control regional search feedback.
Extend loading/briefing Chromium assertions, including out-of-order results.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Fix pre-action busy snapshot and citation separation

Move busy capture before task; preserve separator in parser replacement.
Add helper lifecycle and direct core parser regression cases.
Run the new helper/parser regressions against unchanged runtime first to
preserve failing evidence, then apply the runtime corrections.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, review and commit locally

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted then admitted full suites and browser checks

Use source-first PYTHONPATH; never mutate the shared venv. Lock full unit,
loading/briefing, journey, assistants, employee briefing, design-system and
workbench checks together with nonblocking admission. If busy, only targeted
unit/check work, no waiting or polling. Targeted lint and JS syntax checks.
Execution: lock busy (flock exit 75, holder PID 640280); user-authorized
targeted fallback completed. Full units and browser/axe suites are unperformed,
not passed. No lock retry or browser launch.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Preserve independent Review and local commits

Commit implementation/original dated evidence, then final review/state evidence.
No full publication receipt is claimed; az prohibited and publication excluded.

## Test Ownership and Change Budget

Canonical runtime: app.js, async-action.js, core/ai_tasks.py.
Regression owners: existing API helper unit and loading browser check; at most
one new core test file with parameterized parser cases. No removals. Maximum
four coherent assertion groups (focus/search/busy/parser). No generated targets,
workbench recipe or manifest edits anticipated; if either pinned file changes,
synchronize and check scenario SHA-256 pins. Semantic coverage is exact focus,
input continuity, pre-action attribute and source association; full suites
provide regression breadth, not human accessibility acceptance.

## Dependencies

Existing Python 3.12, Node, Playwright Chromium and pinned axe 4.10.3;
verify dependency/import readiness before execution. Lock contention is a
permitted scoped validation limit, not a reason to block local implementation.

## Critique Disposition

One independent critique executed. Original verdict: Revise. PC-001
(Medium, planner-owned) accepted and resolved directly: the pre-fix failing
helper/parser run now belongs to P01-T02, before runtime corrections, rather
than P02 which depends on P01. No significant user decision or second critique.

## Follow-Up Items

* Coordinator retains publication gate and exact-head hosted/human acceptance;
  no cloud or publication authority in this correction round.
* Rerun full core/API and existing browser/axe suites on a later explicitly
  coordinated free-lock event; contention prevented execution in this round.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-29/loading-briefing-hax-531-corrections-changes.md.
P01/P02 complete under the explicit lock-contention fallback. Implementation
commit d6e0e864 preserves the source and original phase evidence.
One independent Review executed: Complete / Residual work, no implementation
defect found; RV-001 routes unperformed full/browser checks to FU-001.
Final evidence-only local persistence preserves that original outcome.
Session stops under explicit user direction; no push or child task.
