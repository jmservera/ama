---
title: Resident SQL fixture authorization window phase details
description: Execution boundaries and evidence for the fixture-only correction
ms.date: 2026-10-27
---

## Metadata

Task ID: pr-479-resident-sql-fixture-window.
Plan: `.copilot-tracking/plans/2026-10-27/resident-sql-fixture-window-plan.md`.
Research: `.copilot-tracking/research/2026-10-27/resident-sql-fixture-window-research.md`.

<!-- rpi:phase id=P01 -->
## P01: Correct and regress the fixture

<!-- rpi:task id=P01-T01 -->
### P01-T01: Restore SQL fixture endpoint and add behavioral tests

C1-C6 establish a single SQL-bound application-cap reuse. Keep the SQL cap at
2026-11-01T00:00:00 UTC and convert only at DATETIME2 insertion. Preserve server
and image application expiry. Add up to three tests in one API test file,
with fake SQL calls/connector so database() executes its real setup/yield/
cleanup path without SQL. Block Playwright imports while loading the test
module to verify runtime-only discovery remains possible. Prefer lazy browser
imports under TYPE_CHECKING when needed rather than mocking the package
globally. Exercise both inserts with a substituted later cap. Restore patched
objects after each test. No test deletions or generated targets.

Completion: red/green behavioral test and diff with unchanged schema/runtime.

Execution complete: SQL_AUTHORIZATION_END is November 1 UTC; both fixture
inserts are checked with substituted January application cap. The second test
blocks Playwright import. Lazy browser import makes the shared SQL fixture
usable for unit discovery and image checks without the browser dependency.
Both tests failed against the original implementation, then passed.

<!-- rpi:phase id=P02 -->
## P02: Validate and independently review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute focused checks and retain original Review

Depends on P01. Explicit absolute worktree PYTHONPATH begins with API/core/
agents src roots, followed by core/tests and agents/tests. Focus resident API,
fixture and core showcase suites; Ruff/mypy cover changed Python. SQL/browser/
image validation runs foreground under flock -w 0 on the shared heavy lock.
Create only a labeled task-owned SQL Server container on a random loopback
port; readiness must be an actual SELECT. Execute the existing two check
modules unchanged apart from the shared fixture fix. Remove only exact owned
containers/images. Retain logs externally, no passwords in evidence.

Current assumptions: Docker responds and SQL image is cached; Playwright and
lint/type tools are missing from system Python. Missing dependencies may be
restored with pip in session scratch. Failed prerequisites remain blockers.
One independent Review assesses the final scoped diff and evidence.

Checks complete before original Review: API resident discovery 108 tests,
7 expected opt-in skips; core showcase discovery 77 tests, 19 real-SQL opt-in
skips. Real browser 55 assertions and image 22 assertions passed against an
exact-owned local SQL Server under timeout-zero heavy lock. Scoped Ruff,
format and mypy passed. Missing pinned tools restored in external session venv
with pip; no manifest changes. Logs remain in session files. Original
independent Review Complete / Conformant, no findings; P02 complete.

<!-- rpi:phase id=P03 -->
## P03: Publish correction and resolve review thread

<!-- rpi:task id=P03-T01 -->
### P03-T01: Commit, synchronize and publish without merge

Depends on P02. Existing branch is clean at intake and PR 479 remains open.
Initial pull --rebase advanced only the bot's rubric latest.json. Configure
the email as {id}+{login}@users.noreply.github.com using the current gh api user
response, repository-locally, for both author and committer. Include the
required Copilot coauthor trailer.
Commit normally and pull --rebase before normal push. Preserve all original
parent evidence; never amend, force-push, merge or update live resources.
Reply to the sole unresolved thread with commit and measured check results;
resolve only after remote publication confirms the correction.

After synchronization, record final HEAD and freshly fetched origin/main SHA,
run fresh scoped validation against those exact inputs, and obtain an
independent exact-head publication assessment before normal push. Preserve the
original Review and any adverse findings. Any subsequent HEAD/base/input change
invalidates the binding; refresh checks/assessment before publication. This
small correction does not authorize a broader matrix or imply a full receipt.

Pre-publication snapshot: P03 remains unchecked until remote publication and
thread disposition occur. Keep final commit/base-bound evidence external and
post actual completion to PR 479, rather than committing a self-referencing
receipt or predicting a successful push.
