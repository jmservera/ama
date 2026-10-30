---
title: Employee briefing manager visibility phase details
description: Bounded implementation tasks and evidence expectations
ms.date: 2026-10-28
---

Task ID: employee-briefing-manager-visibility
Current continuation: P04-T01/T02/T03 complete; T04 validation complete,
independent Review Complete / Conformant, correction published and three
Copilot threads resolved. P04 complete. No blockers; hosted/owner review pending.
Original P01-P03 evidence below is historical.
Status: P01-P03 complete; original Review Complete / Conformant; PR #516 open.
Readiness: research C1-C10 resolves role, permission, projection and fixture questions.
No new owner decision needed. Owner authorizes all four finite phases.

Original Review: .copilot-tracking/reviews/logs/2026-10-28/employee-briefing-manager-visibility-review.md.
No findings or acceptance blockers. P03-T02 publication observed: implementation
commit 041a13c5d49b2eb92ba0a09c7015a03d6ffbd5f7 pushed on the topic branch and
https://github.com/jmservera/ama/pull/516 opened against main with Refs wording.
All six committed source blobs matched the independently reviewed hashes.
Only administrative tracking closeout follows; hosted/human approval is pending.

<!-- phase:P01 -->
## P01: Scoped briefing

<!-- task:P01-T01 -->
### P01-T01

Store.briefing first applies projection.allowed(user, "briefing"), then selects
existing list_cases(all if role in MANAGER_ROLES else mine). list_cases returns
ranked permitted open rows on both stores. Rehydrate only selected top eight
for source/citation checks; use each row's projected status for model facts.
Keep existing release and continuity cache checks, adding actor/role/reason
visibility/full ordered eligible IDs/mode to cache identity. Return programme/assigned scope,
All programme cases/My assigned cases labels, eligible case_count and selected
summary_count. Distinct scope-sensitive empty wording. No assignment mutation.

<!-- task:P01-T02 -->
### P01-T02

aiBox adds a scope subheading and count explanation from server response, keeps
Today's briefing heading and native workflow toggle, and uses neutral reading
and refresh text. Keep listView My cases labels unchanged. Apply current web
guidelines to changed web lines; repository ASCII punctuation takes precedence.

<!-- task:P01-T03 -->
### P01-T03

Update Employee briefing section and ms.date in src/api/README.md. Explain the
two existing managers, all permitted open candidates, existing top-eight cap,
personal queue distinction, unbound identity continuity and local test commands.
Do not rewrite historical PR #514 evidence or add knowledge-base claims.

<!-- phase:P02 -->
## P02: Validation

<!-- task:P02-T01 -->
### P02-T01

Extend TasksMixin (maximum nine new methods; no removals) for manager role set,
all other staff roles, closed exclusion, zero assignment unbound manager,
cache actor/role/scope/reason separation, permitted-set filtering (patch existing
list_cases, not the authorization rule), denied roles, projected prompt status,
top-eight deterministic order/count and no controlled-record mutation.
Within the same cache test, remove a non-top-eight permitted case at unchanged
store.version and prove the full eligible count refreshes (PC-001).
Record IDs from ai_task comparison records; spy on host AI interface for model
facts without any remote call. Keep release_support synthetic fixture.
Maintain two existing cache references so release-invalid/stale results are still
injected/asserted on the actual new cache entry.

<!-- task:P02-T02 -->
### P02-T02

Use checks.design_system_browser_check.main and public synthetic workbench data.
Test both existing managers, including no-owned-case manager, plus ordinary staff.
Block non-loopback requests. Verify actual API response labels/counts against
rendered section and personal queue, workflow-only toggle by keyboard and narrow
reflow. No new production role or private data. Capture bounded browser evidence
outside git if needed and retain the repeatable check in src/api/checks.

<!-- task:P02-T03 -->
### P02-T03

From src/api use installed distributions and python3 -m unittest:
PYTHONPATH=tests:../core/tests:../agents/tests for focused selectors;
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q.
Run focused core sensor-privacy/cache checks where needed. Changed-file Ruff,
mypy, Node syntax and git diff --check. Install pinned missing dependencies
only after observed failure (initial system import already failed).
Owner prohibits --all and permits --changed only for large work: no gate
invocation for this bounded change. Do not equate local passes to live SQL,
Azure, human review or all-issue acceptance.

<!-- phase:P03 -->
## P03: Review and publication

<!-- task:P03-T01 -->
### P03-T01

Reconcile implementation markers and validation evidence before activating
rpi-review once. Fresh independent reviewer assesses changed source/tests/docs
and exact diff against AC1-AC8; retain original findings and outcome. Any open
findings receive a per-finding block/defer disposition and route to later work,
never a repeated Review within this task. Unresolved acceptance-blocking
findings (including authorization, disclosure or required failed checks) stop
publication. Only explicitly justified nonblocking residuals may be deferred.

<!-- task:P03-T02 -->
### P03-T02

Proceed only when the original Review has no unresolved publication blocker
(PC-002). Record reviewed candidate, original outcome and each finding's
disposition, required checks and any exact-head changes.
Use current owner-created topic branch (clean at intake, parent origin/main).
Commit original critique/Review and state with implementation, Conventional
Commits and required Copilot trailer; resolve privacy-safe identity with gh.
Fetch main before publication; do not rebase/rewrite or push main. Inspect exact
head/diff and report hosted/human checks as pending. Open one Refs PR with
test/browser evidence and explicit no-deployment/no-full-gate boundary.

<!-- phase:P04 -->
## P04: Copilot review corrections

<!-- task:P04-T01 -->
### P04-T01

Import existing `wait_cases` and call with the expected personal queue length
before exact IDs/empty text checks. Delay only the initial `/api/cases` response
in the synthetic browser harness so the test actually covers separate loads.

<!-- task:P04-T02 -->
### P04-T02

Use `_filtered(user, all/mine, "", {})`, sorted by `_ranking` rank. Unlimited
SQL lists already use this path; preserve full ordered candidate IDs in the
key and every release/epoch/continuity check. After a miss, rehydrate at most
eight and call `summary` only for those cases; briefing does not need
work-context/queue projection. Redact waiting status with the existing role
policy before producing facts. Cache-hit regression must observe zero new
summary calls, and no work_context call; removing a non-top-eight permitted
candidate without a version bump must still refresh case_count.

<!-- task:P04-T03 -->
### P04-T03

Keep all eight source inputs and comparison-record provenance. Only display
summary_count changes: final source template means at most three; AI means at
most eight. Cover workflow, absent endpoint, failed model, AI success and empty/
one-case inputs. Browser compares min(expected, 3) in workflow-only fixtures.
Clarify the cap in API README, not in unrelated knowledge-base documents.

<!-- task:P04-T04 -->
### P04-T04

No test removals; at most one new TasksMixin method, executed on both stores.
Run focused task/release regressions before full core and API discovery using
their documented commands and existing installed distributions. Run the synthetic
browser, changed-file Ruff/mypy and diff checks. Independent Review assesses
this correction boundary once and appends its original result to the existing
Review file. Preserve the earlier Review and failure evidence. Resolve GitHub
identity, commit source and evidence with trailer, fetch main, push only this
topic with --force-with-lease after the existing rebase, then reply/resolve each
named thread. No merge, Closes, `.env`, private data or cloud activity.
