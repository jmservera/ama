---
title: Loading and briefing correction phase details
description: Execution boundaries and evidence contracts for PR 538 corrections
ms.date: 2026-10-29
---

## Metadata

Task ID: 531-corrections-2026-10-29.
Task slug: loading-briefing-hax-531-corrections.
Plan: .copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-corrections-plan.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Targeted fallback complete; Review/commit pending | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Surgical behavior corrections

Research C1-C5 confirms supplied failures. No changes to review authorization,
server APIs, public appearance or handler disable ownership.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Focus and search

Use explicit review choice identity, not document.activeElement after rendering.
Return to rejection on rejection cancel and edit on edit cancel, retaining text.
Use `AsyncAction.run(null, ..., "Finding cases", region)` so search cannot be
disabled or deduplicated; keep existing load sequence guard.
Hold real search routes with synthetic distinct totals; type after first
250ms pause, deliver newest response first, assert old result cannot overwrite.
Existing loading check owns these assertions; workbench recipe stays unchanged.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Busy restoration and parser

Snapshot busy beside originalDisabled before invoking task. Leave disabled
ownership, observer and pending cleanup intact. Simulate handler-set busy and
finally-cleared busy after recoverable failure; verify subsequent retry and
pre-existing false restoration. Add direct core parser coverage for the exact
two trailing citation example, all sentence terminators, newlines and adjacent
references, checking exact objects rather than aggregate source counts.
Preserve parser structure; add a separator after relocated punctuation.
Before runtime corrections, the newly added helper/parser regressions must
fail against unchanged runtime (PC-001); retain that output externally.

<!-- rpi:phase id=P02 -->
## P02: Local evidence and review

Use only constructed data and loopback. Requested journey interpreter is absent;
verify existing /tmp/ama-531-venv, with absolute source-first paths. Do not install
or rewrite foreign worktrees. Source baseline: e2ce9ebb554c9bad0952faa541da883e4a0896ad.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validation

P01-T02 first reproduces helper/parser failures before its runtime edits.
This resolves PC-001 without contradicting the P02 dependency on P01.
Run focused units, lint and JS syntax. Attempt one nonblocking flock admission
for core/API full units and relevant browser/axe suites. Preserve exit codes
and output externally; report exact skips and any missing dependency failure.
No retry/poll on busy. Keep axe reports/incomplete results external.
No pin changes required if neither pinned workbench file changes.
Execution: nonblocking admission returned 75; actual holder PID 640280.
Full units and Chromium/axe suites were not launched. Targeted 69 tests plus
8 manifest tests passed; Ruff, browser-check mypy, JS syntax and diff checks
passed. Browser regressions are authored/type-checked but unexecuted.
No workbench manifest/recipe changes, so no scenario pin changes.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Independent Review and persistence

One independent critique before implementation; one independent Review after.
Reviewer assesses only this correction round and records execution separately
from verdict. Route findings to later work, never repeat Review in this task.
Configure authenticated privacy-safe email repository-locally; use Conventional
Commits with Refs #531 and required coauthor. Leave commits local, no push.
Keep final state, changes and plan markers reconciled with actual evidence.
Publication and human acceptance remain outside this round, not implied passes.
