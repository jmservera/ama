---
title: Issue 531 PR 604 correction phase details
description: Exact repair boundaries and validation/publication expectations
ms.date: 2026-10-31
---

Task ID: 531. Slug: employee-briefing-loading-531-pr604-corrections.
Research C1-C6/W1-W2 is complete, readiness Ready; no pending ordinary decision.
Caller direction replaces complete-local-gate waiting with hosted CI.

<!-- P01 -->
## P01: Repair and Validate

<!-- P01-T01 -->
### P01-T01: Repair

Six inventories, all dated 2026-10-31:

* reviews/logs/employee-briefing-loading-531-capacity-correction-review.md: 18.
* reviews/logs/employee-briefing-loading-531-publication-harness-review.md: 10.
* reviews/logs/employee-briefing-loading-531-review.md: 9.
* reviews/plans/employee-briefing-loading-531-capacity-correction-plan-critique.md: 7.
* reviews/plans/employee-briefing-loading-531-plan-critique.md: 4.
* reviews/plans/employee-briefing-loading-531-publication-harness-plan-critique.md: 5.

Actual directories are .copilot-tracking/reviews/{logs,plans}/2026-10-31.
Compute each destination from the artifact's parent to the existing repository
file. Tracking targets use ../../../{plans,details,research,...}/...,
source/doc/tool targets use ../../../../src/... or docs/... or tools/...; same-file links can use
the basename. Do not change labels/descriptions or other historical text.

Fix the prospective command in publication-harness-phase-details.md to
--jobs 3 --lock-timeout 1800. Correct the related changes record's
--lock-timeout 1800 typography, retaining its actual failed gate results.

<!-- P01-T02 -->
### P01-T02: Validation

Compare every corrected URL's resolved path with its retained label and require
all 53 files exist. Compare original bodies after reversing destination-only
changes; require byte-identical historical prose. Require CLI strings match the
existing argparse names and whitespace. git diff --check and ancestry/log/
rubric inspection cover the merge.

From src/api run PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest
test_loading_feedback test_workspace_scripts test_case_journey test_ai_tasks
test_assistant_release -q; run ruff check ., ruff format --check . and mypy.
Use installed src distributions. Restore dependencies with pip only after
missing-dependency failure, in a task-owned venv rather than shared mutation.
No browser/full SQL/scanner gate waits; no private environment or datasets.
Record actual commands, tool versions, counts and any setup failure.

Executed: all 53 targets and byte-identical historical prose passed, CLI-only
edits passed, main ancestry/rubric/both log entries passed, whitespace passed.
Five named API test modules ran 145 tests in 40.754s, OK. Ruff 0.17.1 lint
passed; format reported 65 files already formatted. mypy 2.4.0 passed 123
source files. Installed src distributions via task-owned pip venv after the
initial missing-package failure. Full local gate not run as directed.

<!-- P01-T03 -->
### P01-T03: Review

Reconcile plan/details/changes/state. One fresh independent reviewer activates
rpi-review and assesses this bounded correction, preservation, exact semantic
link checks and actual validation, writing only the original dated Review.
Do not claim live/manual/hosted acceptance.

<!-- P02 -->
## P02: Publication

<!-- P02-T01 -->
### P02-T01: Commit and Push

Resolve gh api user identity again; local privacy-safe author/committer email.
Commit includes Co-authored-by: Copilot
<223556219+Copilot@users.noreply.github.com> and Refs #531.
Push exactly git push -u origin HEAD. On rejection first git pull --no-rebase,
preserve remote changes, resolve any rubric conflict with current main's side,
retain log entries and use a trailer on the resulting merge commit. Never force.

PC-001 recovery checkpoint: inspect pre/post-pull candidate diff and conflicts;
rerun exact links, CLI syntax, historical-prose preservation and whitespace.
Rerun API tests/tooling if their inputs changed. Record candidate SHAs and whether
the one Review's assessed correction remains content-equivalent. If substantive
unreviewed correction changes invalidate it, record the blocker, never fabricate
coverage or launch a second Review. A remote rubric-only merge does not change
the assessed correction/API inputs. Accounting-only commits may update outcome
metadata, but verify repair and validation inputs unchanged before repushing.

<!-- P02-T02 -->
### P02-T02: Thread Disposition

For every captured unresolved thread, call addPullRequestReviewThreadReply with
the fixing commit and exact disposition, then resolveReviewThread. Verify all
seven resolved and remote HEAD equals local HEAD. Existing PR remains open;
preserve Refs #531 and unmet live AC7. Record publication outcome in durable
state/evidence, with a further non-force push if accounting is committed.

PC-002: retain a seven-node ledger in the new changes artifact, sourced from
the initial gh reviewThreads capture stored in the session files/pr604-threads.json.
Refresh current metadata before mutations and match IDs, original comment IDs,
paths and repairs. Require a successful reply response ID before resolve;
reject GraphQL errors even with HTTP success. Verify per-node resolved state.
On uncertain response, re-read the node before retrying to avoid duplicates.
Do not expand scope to new threads; record already-external resolutions honestly.
