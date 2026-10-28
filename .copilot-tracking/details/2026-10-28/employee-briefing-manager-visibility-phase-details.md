---
title: Employee briefing manager visibility phase details
description: Bounded implementation tasks and evidence expectations
ms.date: 2026-10-28
---

Task ID: employee-briefing-manager-visibility
Status: P01/P02/P03-T01 complete; original Review Complete / Conformant.
Readiness: research C1-C10 resolves role, permission, projection and fixture questions.
No new owner decision needed. Owner authorizes all four finite phases.

Original Review: .copilot-tracking/reviews/logs/2026-10-28/employee-briefing-manager-visibility-review.md.
No findings or acceptance blockers. P03-T02 remains pending actual publication;
there are no implementation changes after the assessed six-file source hash set.

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
