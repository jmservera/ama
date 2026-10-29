<!-- markdownlint-disable-file -->
# RPI Plan: PR #504 main rebase

## Task Metadata

* Task ID: pr-504-rebase-2026-10-29
* Task slug: rai-release-218-rebase
* Plan date: 2026-10-29
* Planning status: Ready; original critique Revise retained, PC-001 to PC-003 resolved
* Phase details: .copilot-tracking/details/2026-10-29/rai-release-218-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/rai-release-218-rebase-plan-critique.md

## Executive Summary

Replay branch content, including unique integration-merge evidence, onto pinned origin/main
5653547507f3056f09a726a18516237728da5e5b. Resolve shared documentation without
losing either workstream; preserve main's briefing-cache tests and scenario pins
alongside the RAI additions. Run scoped local checks and record a new independent
Review, then commit the dated evidence without pushing.

### What You May Not Know

/tmp/mv editable imports point to another worktree. Explicit local src/test
precedence and import-origin assertions are required to validate this checkout.
Hosted CI cannot run on the new commit until the coordinator pushes. No local
full-gate receipt or actual RAI human acceptance is implied.

### Unresolved Decisions or Blockers

None for local integration. Publication remains the coordinator's responsibility.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review with dated .copilot-tracking artifacts.
* Fetch and rebase the named PR branch onto origin/main, preserving both intents.
* Keep both append-only log/index entries; select main for rubric and manifest.
* Keep implementation in src/ and tests outside packages; no legacy source.
* Use /tmp/mv, explicit project/sibling src/tests paths, Ruff/format/mypy and relevant unittest modules.
* No full API discovery unless the nonblocking heavy-lock probe succeeds.
* No Azure resource changes; no push or issue-closing keywords.
* Commit using Conventional Commit and the requested Copilot co-author trailer.

## Goals

* Establish ancestry to fetched main with no unresolved conflicts or lost RAI behavior.
* Deliver a persistent locally validated candidate and truthful coordinator handoff.

## Scope and Non-Goals

In scope: branch integration, necessary conflict resolutions, relevant regressions
and dated evidence. Out of scope: new features, human approvals, deployments,
hosted workflow dispatch, remote writes, full API suite and issue closure.

## Functional Requirements

* Existing dependent-policy release and review invariants remain unchanged.
* Preserve main's current dynamic briefing-cache key assertions and unrelated work.
* Main's rubric/scenario content remains byte-identical.

## Non-Functional Requirements

* All selected static checks and relevant tests must succeed, with skips disclosed.
* Validation resolves this worktree's packages, not another editable checkout.
* Keep original 2026-10-27 evidence intact; do not fabricate exact-head/hosted approval.

## Acceptance Criteria

* Pinned main is an ancestor; git ls-files -u is empty and diff checks pass.
* Three core production modules retain original branch content unless a proven
  tightly coupled incompatibility requires an explicitly documented correction.
* Main rubric/manifest copies match; test_scenario_manifest passes.
* Core/API Ruff check, format --check and mypy pass.
* Relevant release, oversight, ranking, quality and dependency tests pass.
* Original evidence survives; exactly one critique and one independent Review
  for this new integration task are recorded.
* A Conventional Commit with privacy-safe identity and requested trailer exists;
  worktree clean; no push performed.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-29/rai-release-218-rebase-research.md
(Complete / executed / Ready). Implementation creates
.copilot-tracking/changes/2026-10-29/rai-release-218-rebase-changes.md.
Automatic parent continues after critique dispositions resolve.

## Sources

* Research C1-C7/W1: branch identity, semantic delta, upstream tests/pins and import risk.
* .github/workflows/src-ci.yml and src/{core,api}/pyproject.toml: actual CI/tool contracts.
* .copilot-tracking/changes/2026-10-27/rai-release-218-changes.md: historical evidence only.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase and preserve both intents

Dependency: final critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Replay commits and resolve conflicts

Inspect original commit parents and merge-only annotations first. Ordinary rebase
omits e9b5604d's merge commit: record its original-evidence hashes and compare
against the result, explicitly reapplying unique publication annotations from
the original head if omitted. Verify both original index/log entries and retain
all main entries. Immediately require origin/main to equal the reviewed full SHA,
then run git rebase origin/main as requested; stop/reconcile the local boundary
if it moved. Record every stop. Resolve shared docs semantically;
main wins rubric and manifest. Continue non-interactively without dropping
nonempty source/evidence work. Empty merge-resolution replay may be skipped only
after proving it adds nothing. Verify source preservation, main copies and ancestry.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate the rebased integration

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted static and behavioral checks

Run core/API Ruff/format/mypy and combined relevant unittest modules, including
manifest, release, oversight, ranking/quality and dependency rule. Use /tmp/mv
with local src:tests and sibling src/tests paths. Runtime PYTHONPATH is distinct
from mypy resolution: set checkout-local MYPYPATH for all project/sibling roots
and use verbose mypy logs to verify followed module paths. Preserve existing
configured exclusions and report them as exclusions. Do not run full API discovery.
Record exact commands, counts, failures/skips and any correction.

<!-- rpi:phase id=P03 -->
### [x] P03: Independent Review and committed local handoff

Dependency: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Review once, reconcile evidence and commit without push

Preserve the review's original outcome and route findings, not a repeat Review.
Resolve authenticated identity through gh api user, configure repository-local
noreply email for author/committer, commit using Conventional Commit plus
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>.
Verify commit identity/trailer, clean status and main ancestry.

## Locked Test and Output Ownership

* Canonical targets: existing src/core and src/api modules/tests; shared docs.
* Generated targets: none. Rubric/manifest are retained from main, not regenerated.
* Test removals: none. Maximum new test methods: zero for pure integration;
  a discovered semantic defect requires an explicit plan amendment before additions.
* Semantic coverage: policy invalidation, review reliance and cache compatibility.
* Regression coverage: existing release/RAI/ranking/quality and manifest modules.
* Validation evidence: exact commands/results in changes; not historical counts.

## Dependencies

* /tmp/mv Python/tools already exist; do not mutate shared editable installation.
* Explicit src paths satisfy local namespace precedence; assert origins first.
* Main is pinned for the scoped task; later main advancement invalidates ancestry
  claims for that later base and is reported rather than silently rewritten.

## Critique Disposition

Execution Complete; original verdict Revise, preserved without repeat.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied directly | P01 explicitly inventories merge-only evidence and requires restoration/comparison against original head, plus both docs intents |
| PC-002 | Applied directly with caller-command preservation | P01 checks full origin/main SHA immediately before requested git rebase origin/main; no background fetch is performed; record actual target |
| PC-003 | Applied directly | P02 separates PYTHONPATH runtime assertions from MYPYPATH and verbose mypy followed-path evidence |

## Follow-Up Items

* Coordinator push and hosted CI; outside explicit no-push scope.
* Full publication receipt and original RAI human/owner acceptance remain separate.

## Handoff

P01/P02/P03 complete with the local commit containing this record. Independent
Review execution Complete, outcome Residual work; no introduced defect.
All three planner-owned critique findings disposed. Coordinator owns publication
and hosted checks; original RAI approvals remain distinct follow-ups. No push.
