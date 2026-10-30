<!-- markdownlint-disable-file -->
# RPI Phase Details: PR #504 main rebase

## Metadata

* Task ID: pr-504-rebase-2026-10-29
* Task slug: rai-release-218-rebase
* Related plan: .copilot-tracking/plans/2026-10-29/rai-release-218-rebase-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/rai-release-218-rebase-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Rebase | complete; aae74f28 | P01-T01 |
| P02 | Validate | complete | P02-T01 |
| P03 | Review and commit | complete in local evidence commit | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Rebase

<!-- rpi:task id=P01-T01 -->
### P01-T01: Replay commits and resolve conflicts

Context: clean original worktree, now containing only this task's untracked
dated evidence. Main is 5653547507f3056f09a726a18516237728da5e5b;
original head e9b5604d, source/evidence commit 63e9074a. New evidence paths
must not collide with main; check before replay.

Topology verified: e9b5604d has parents 63e9074a and 09099ecd; it is a merge.
Inventory its unique changes with git diff 63e9074a e9b5604d over original
dated artifacts and shared index/log. Record original-head blob IDs for all
seven original artifacts, and require equality after integration. If default
replay omits merge-only annotations, reapply those exact original blobs before
validation and final evidence commit. This is preservation, not rewriting the
original outcomes. Keep main rubric/scenario content. Require the current
origin/main ref to equal 5653547507f3056f09a726a18516237728da5e5b immediately
before the caller's git rebase origin/main; record actual target and stop if
the ref moved. Do not assume both commits replay as ordinary commits.

Intent: preserve RAI changes plus all later main work. Likely conflicts are
docs/reference/README.md and docs/reference/log.md. Tests have newer dynamic
briefing-cache assertions on main. Do not select entire test files blindly.

Validation: git merge-base --is-ancestor; no unmerged entries; git diff --check;
compare three original production files and main rubric/scenario content.
Preserve all original task evidence, including e9b5604d's publication annotations
where they are unique. No reset, stash, push or Azure operations.

Completion evidence: replay output, per-conflict resolutions and explicit
preservation checks in changes. No unresolved decision.

<!-- rpi:phase id=P02 -->
## P02: Validate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Static and behavioral checks

Depends on P01. Work from each project directory with /tmp/mv/bin executables.
Core PYTHONPATH: src:tests:../api/src:../api/tests:../agents/src:../agents/tests.
API PYTHONPATH: src:tests:../core/src:../core/tests:../agents/src:../agents/tests.
Set MYPYPATH separately to the same checkout-local roots for mypy; inspect its
verbose followed-path output and preserve intentional configured skip/exemptions.
Do not treat runtime path probes as proof of static sibling coverage.
Assert core/API/agents
module __file__ paths belong to this checkout before invoking suites.

Actual origin guard uses concrete agents.dispatch.__file__, not namespace
__path__: PEP 420 correctly includes both local and installed namespace roots.
An initial overly strict namespace assertion failed before core statics; the
corrected concrete-module guard passed. Mypy logs show local source paths and no
foreign iot110 checkout references; configured migration exemptions remain.

Run Ruff check ., Ruff format --check ., mypy in core and API. Run combined
core test_rai_release, test_quality_procurement, test_scenario_manifest and
test_dependency_rule; API test_assistant_release, test_assistants,
test_ranking_policy and test_dependency_rule. Add a tightly related existing
selector only if the resulting changes or failures justify it. No full API
discovery or heavy concurrent job.

Completion evidence: exact commands, test counts and failures/skips recorded.
Opt-in SQL skips remain skips, not passes. Browser, native SQL, images, full
gate, hosted CI and human acceptance are not implied by this selection.

<!-- rpi:phase id=P03 -->
## P03: Independent Review and committed handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Review once and commit

Depends on P02. Reconcile plan/details/changes and pending items first.
Fresh independent reviewer owns only
.copilot-tracking/reviews/logs/2026-10-29/rai-release-218-rebase-review.md.
Review the scoped integration, evidence and preservation checks. Record
execution separately from outcome; route residual findings without repeating
Review. Human/hosted approval checkboxes stay unapproved.

Commit after review using gh-resolved authenticated noreply email for both
author and committer, Conventional Commit plus exact requested trailer. Commit
all this task's dated evidence and deliberate resolutions only. No push.

Completion: verify clean worktree, latest commit message/identity, pinned main
ancestry and no unmerged entries. Coordinator receives exact commit and any
remaining publication/acceptance limits.

Independent Review execution Complete, outcome Residual work; 20 independently
passing focused tests, no introduced defect. RV-001 publication and RV-002
original RAI human acceptance remain routed. No repeat Review or source changes
followed. Final local evidence commit uses the verified authenticated noreply
identity and exact trailer; post-commit verification is the final shell check.
