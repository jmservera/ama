---
title: PR 508 IoT review correction phase details
description: Evidence-linked tasks, focused regression ownership and validation
ms.date: 2026-10-29
---

Task ID: pr-508-review-fixes-2026-10-29. Slug: iot-review-508.
Plan: `.copilot-tracking/plans/2026-10-29/iot-review-508-plan.md`.
Readiness: Research Ready; one critique complete and disposed in plan; no blocker.
Implementation reconciliation: P01/P02 complete; five new test methods, no removals.
All requested static checks pass; core 11 tests/API focused 69 tests pass.
No amendment or significant divergence. P03-T01 Review Complete / Conformant,
zero findings; P03-T02 completed in local implementation commit
19fb66a65629fb725625681bd51539e212cfcfe8. No push.

<!-- phase: P01 -->
## P01: Regression-first corrections

<!-- task: P01-T01 -->
### P01-T01: Focused regressions

C1/C4: use shutdown-entry asyncio events, not timing guesses, before cancelling
the runner. Exercise both receiver credential/client closes and publisher shutdown.
Use cancelled shutdowns that later raise a constructed error; spy on the existing
observation callback so late failures are demonstrably consumed. Release all owned
test tasks on assertion failure. Assert bounded runner return without waiting on
SDK cancellation acknowledgement.
C2: construct supplied Pacer from a different unvalidated RunBudget. Parameterize
bad limits, assert fixed error plus factory-not-called. Include a stricter valid
budget as a positive control.
C3/C5: injected fake clock and sleep record exact sub-50 ms targets at several
rates and short nominal wait; paused elapsed targets must still sleep >0 up to
50 ms, and deadline remainder can shorten that poll.
No tests in packages and no new test files; at most six added methods.

<!-- task: P01-T02 -->
### P01-T02: Source fixes

Use the shared `_cleanup` for both runners, retaining its normal 0.5s wait/error
semantics; finally loops all tasks and never awaits. Observation must include
completed failures, not just pending tasks. Check finite supplied deadline and
numeric finite positive rate within validated budget before factories. Keep
expired finite deadlines as runtime errors. `_wait_until` uses target remainder
only when active; existing stop/deadline ordering remains unchanged.

<!-- phase: P02 -->
## P02: Documentation and validation

<!-- task: P02-T01 -->
### P02-T01: Owning guides and rubric

Document interrupted cleanup ownership and supplied-control entry checks in
`src/api/README.md`; document precise active target sleeps and bounded pause
polling in `src/core/README.md`. Restore only `.github/rubric/scores/latest.json`
from origin/main, explicitly authorized by caller. Preserve historical evidence.

<!-- task: P02-T02 -->
### P02-T02: Focused validation

Run exact commands locked in plan from each owning project, using `/tmp/mv`
and requested PYTHONPATH. Capture exits/counts in changes evidence. Do not run
full API suite or broad gate that entails it. If static checks expose unrelated
failures, record rather than fix unrelated source. No installation unless a
chosen command has a missing-dependency failure. Regression tests must fail on
pre-fix source and pass with fix.

<!-- phase: P03 -->
## P03: Independent Review and local handoff

<!-- task: P03-T01 -->
### P03-T01: One Review

Reconcile plan markers, details, changes, amendments (or none), divergences (or
none), actual validation and remaining limitations before review. Independent
review writes one bounded report to
`.copilot-tracking/reviews/logs/2026-10-29/iot-review-508-review.md`.
Assess only this task diff and its explicit contracts, not all PR ancestry.
Preserve original findings and route any new ones to later work, not repeated Review.
Blocking in-scope findings make this handoff Not accepted, never silently completed
as successful. Preserve them for later user-selected correction rather than repeat
Implement or Review inside this task.

<!-- task: P03-T02 -->
### P03-T02: Local commit

Authenticated gh identity resolved before commit; repository-local noreply email
for author and committer, no global config. Stage only owned changes. Conventional
Commit and exact required Copilot trailer. Do not push. Coordinator retains final
exact-head publication receipt, independent head assessment and hosted/human gates.
Verify commit is persistent, branch remains correct and worktree is clean.
