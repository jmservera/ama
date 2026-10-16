---
title: Source monitor retry phase details
description: Task-level evidence and completion boundaries for issue 332
ms.date: 2026-10-16
---

Task: #332 / source-monitor-retry-332. No blockers.

<!-- rpi:phase id=P01 -->
## P01: Implement and validate

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fix cadence, regressions and documentation

Read at/body observations ordered by descending id. Check the newest attempt
against today before scanning for the first body without an error. Measure
cadence from that successful attempt, or return due if no success exists.
Use existing JSON decoding, lock and adapter. Cover both long intervals,
failure-only history, prior success, recovery and clock rejection. Update
core/orchestrator README behavior and append the reference log.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate

Set TMPDIR to src/.tmp-332 before pip, monitor tests and mutation interpreters
(PC-001 applied). Full core suites use system temporary storage because
generator tests explicitly forbid outputs inside any repository. No generator
guard is bypassed. Use a task-local pip venv under src/.venv-332, install editable core/orchestrator
and their declared dev extras only after verifying the missing tools.
Run both component unit suites and Ruff/mypy as in src CI, without Docker.
Mutation: load original due() from git, replace the class method only in a
separate interpreter, and require selected core/job next-day tests to fail.
Never rewrite the source file for the mutation.

<!-- rpi:phase id=P02 -->
## P02: Review and publish

<!-- rpi:task id=P02-T01 -->
### P02-T01: Review

One post-implementation review against the plan, diff and measured evidence.
Keep any external acceptance separate from local acceptance. Reconcile markers,
changes and state; do not repeat Review.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Publish

Reuse clean topic fix/source-monitor-retry-332 (no prior PR).
Authenticated id/login matches requested privacy email. Configure local author
and committer, include Copilot trailer, push normally and open main-based PR.
PR body references issues only with Refs #332; do not merge.
