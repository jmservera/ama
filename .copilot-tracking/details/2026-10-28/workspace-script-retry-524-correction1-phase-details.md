<!-- markdownlint-disable-file -->
---
title: Workspace script retry correction phase details
description: Task-level correction and validation boundaries
ms.date: 2026-10-28
---

# RPI Phase Details: workspace-script-retry-524-correction1

Task ID: 524-correction1.
Plan: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md.
Research: .copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md.

<!-- rpi:phase id=P01 -->
## P01: Correct session boundary and regression proof

<!-- rpi:task id=P01-T01 -->
### P01-T01: Guard session identity and extend unit contracts

Research C1-C3 identifies missing identity checks, not a loader-budget defect.
Target app.js route entry/post-await/catch and existing Node VM test owner.
Capture the actual me object, not user ID or boolean. Null session and a distinct
replacement object must leave cleared/replacement status and views untouched,
without test-side routeController.abort(). Cover recovery success and failure.
Browser P01-T02 additionally calls real api() with a constructed 401 response
while the retry is held, observing the real login UI and cleared status.
Completion evidence: source guard plus passing focused regression.
No auth/session storage redesign, no removals or new executable test files.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Make browser proof deterministic and update API guide

Depends on P01-T01. Target existing workspace_scripts_browser_check.py and README.
Separate initial navigation from sign-in as needed: assert aborted initial
request and missing global, then await the specific retry before releasing it.
Keep actual static source bytes and real map/specialist screen assertions.
For delayed lexical script attach load/error listeners directly to inserted
script nodes so removal cannot hide settlement. Chromium precise coverage
measures actual top-level evaluations; readiness and native load/error provide
a bounded deterministic wait. Assert exact hash, status and visible independent
view after settlement and before revisiting screens. No elapsed-time sleep.
If execution was cancelled, explicitly assert no evaluation/no global, unchanged
independent route and cached terminal failure without another insertion.
Also prove real 401 opens same-document login with no controller abort, no
stale role status and no recovered view dispatch; use measurement around the
real view rather than replacing companion bytes.
Semantic checks: status role/aria-live, native reload keyboard/focus. Regression
checks: request/document counts, evaluation count, actual globals/views/errors.
Maximum additions: zero executable files, no source/generated replacements.

<!-- rpi:phase id=P02 -->
## P02: Validate and prepare independent Review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run required checks with bounded shared-lock admission

Run our own commands, not delegated heavy execution. Existing venv is available;
avoid dependency mutation without a missing-dependency failure. Use external
cache/bytecode directories or disable bytecode to avoid generated candidate inputs.
Lightweight: node --check; focused workspace/role/workbench/design/content/a11y
units; package Ruff check/format and mypy; explicit changed Python line lengths.
Heavy: nonblocking flock on /tmp/ama-rpi-heavy.lock, retry at 60-second intervals
for up to 40 minutes, then full API unittest discovery with shared test fixtures
and python -m checks.workspace_scripts_browser_check. Capture actual exit/logs.
No foreign process/container interruption or output reuse. Owned synthetic
temporary server/data only. Bounded timeout or failed check remains a blocker.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile evidence and hand off once for independent Review

Depends on P02-T01. Reconcile plan markers, changes, details and state; preserve
all original Review outcomes. Dispatch one independent read-only Review with
write authority only for the correction1 Review artifact. Review may inspect
the whole correction and its evidence, not fix source or run heavy work.
Record execution separately from outcome. Routed findings become follow-up
work, never an in-cycle repeat Review.
After Review, use authenticated gh identity for repository-local noreply email
and both commit identities, Conventional Commit and required Copilot trailer.
Fetch main; full tools/rpi-checks.py --all --base SHA --out new-external-directory
--lock-timeout 0, using the runner's shared-lock admission (never hold the same
lock outside it). Retry only explicit lock contention every 60 seconds for up
to 40 minutes, with a unique external output directory per attempt. A check or
prerequisite failure is not lock contention and blocks publication.
Verify external receipt against fresh current-main immediately before push.
Obtain independent read-only exact-head assessment of receipt verification and
assessed source boundary before push, keeping its output external to avoid a new
commit invalidating the receipt. This is not a repeated RPI Review.
Any changed candidate/base/tool input invalidates receipt. Required human/hosted
approval and live checks remain distinct and incomplete, not fabricated.
Push only topic branch without force; gh pr create with evidence, actual
validation and Refs #524. No issue closure claim.

## Completion Evidence and Reconciliation

P01-T01 complete: actual session-identity guards and null/replacement Node
regressions; original regression reproduced stale status before the fix.
P01-T02 complete: observed initial abort/global absence, held retry, real script
HTTP 200/global/view, one document; native keyboard reload; late companion
load/ready with actual top-level evaluation count 1 in navigation, timeout and
same-document 401/login scenarios; unchanged settled route/status/no dispatch.
The cancellation branch is explicitly asserted if observed; this Chromium run
actually executed the late script, not cancelled it.
P02-T01 complete: 1149 API tests passed with 314 existing skips; 32 focused units,
Ruff check/format, mypy 92 files, syntax and Python lines <=100 passed.
Full logs and original failed test expectations are preserved externally.
P02-T02 complete for pre-Review reconciliation/handoff only. Original critique
Revise and original task Not accepted Review remain unchanged. The one correction
Review and committed-candidate publication sequence are next, not implied done.
