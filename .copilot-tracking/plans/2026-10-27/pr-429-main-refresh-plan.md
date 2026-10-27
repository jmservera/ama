---
title: PR 429 main refresh plan
description: Isolated rebase, documentation preservation and branch-only publication
ms.date: 2026-10-27
---

## Task Metadata

* Task ID: pr-429-main-refresh-2026-10-27
* Task slug: pr-429-main-refresh
* Planning status: Ready after one independent critique and direct dispositions
* Phase details: .copilot-tracking/details/2026-10-27/pr-429-main-refresh-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/pr-429-main-refresh-plan-critique.md

## Executive Summary

Replay the authoritative remote documentation topic onto main at 49c942b3 in
the requested isolated worktree. Preserve both log additions and index rows,
all substantive topic content and original RPI evidence. Omit only the obsolete
rubric-only commit, retaining main's score snapshot. Review links, anchors,
whitespace and exact preservation before branch-only lease-bound publication.
No operational acceptance or merge is implied. Require the complete local
publication gate. Offline local Bicep tooling is not Azure resource use; forbid
cloud calls and cloud fallback. The scoped documentation tier is supplementary,
not a replacement for the stricter supplied complete-gate instruction.

## User Decisions and Requirements

* Run research, plan, implement and review with dated tracking artifacts.
* Rebase PR #429 onto latest origin/main in ../ama-wt/pr-429.
* Keep both sides of conflicts; reference log is append-only, index stays useful.
* Re-run prior link review and git diff --check.
* Use repository-local noreply identity and the specified Copilot trailer.
* Push only docs/cutover-soak-review-201 with force-with-lease.
* No closing keywords, merge, main write, secrets, Azure or uv.
* Report final exact head and observed GitHub mergeability.

## Goals

Remove the integration conflict without changing proposal scope, accepting
criteria, losing historical evidence or disturbing another checkout.

## Scope and Non-Goals

Scope: four existing production Markdown paths, original tracking records,
new dated RPI records, local Git history and explicit topic remote update.
Non-goals: application/infrastructure changes, issue closure, paid execution,
historical defect cleanup, hosted approval or merge.

## Functional Requirements

* Current main is an ancestor of the candidate.
* Main log is a byte-exact prefix and the original #201 entry appears exactly once.
* Main's #126 cost row and topic's #201 preparation row both survive.
* All substantive original topic blobs survive; original Review outcomes remain.
* Explicit lease expects ad79455a3ec2c47d935fbc3cd055555ff188bc35.

## Non-Functional Requirements

No ignored/untracked source input, secrets, executable modification or new
dependency is introduced. Existing worktrees and unrelated files stay unchanged.
Historical broken links are reported separately from newly introduced defects.
Any remote/base movement requires reevaluation, not blind retry.

## Acceptance Criteria

* Rebase completes, conflict markers absent, no executable diff.
* Exact main-log prefix, original topic log entry and substantive topic contents
  pass preservation comparisons; README contains both sides.
* Changed Markdown local destinations and GitHub-style fragments introduce no
  unresolved link relative to current main.
* git diff --check passes for whole candidate and staged changes.
* One independent critique and one post-implementation Review are recorded.
* Candidate uses local noreply identity and trailer.
* Authorized publication uses explicit topic-only lease and reports remote SHA,
  mergeability and hosted status separately. Publication is blocked if a required
  gate cannot run within caller limits.

## Sources

Research: .copilot-tracking/research/2026-10-27/pr-429-main-refresh-research.md.
Prior validation: .copilot-tracking/changes/2026-10-27/docs-prs-rebase-changes.md.
Gate scope: src/README.md, tools/rpi-checks.py at reviewed main.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve and rebase

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Replay substantive topic commits

Dependency: independent critique disposition. Resolve log by retaining complete
main and appending original topic entry. Resolve README by retaining both rows.
Retain substantive tracking records; omit verified rubric-only commit.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and review

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Documentation checks and preservation

Dependency: P01. Parent owns existing link/anchor review and Git checks.
Removals: none. Additions: zero production tests/tools/dependencies; at most
one external standard-library audit helper. Canonical targets: changed Markdown
and original Git blobs. Generated targets: external logs only. Semantic checks:
both sides survive and proposal gates unchanged. Regression checks: compare
all link defects with main and original topic blobs.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Independent original Review and committed evidence

Dependency: P02-T01. One fresh reviewer inspects final assembled boundary and
writes only its review artifact. Preserve outcome and route remaining work
without another implementation/review loop. Commit exact candidate with identity.

<!-- rpi:phase id=P03 -->
### [ ] P03: Publication

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Gate, exact-head assessment and lease push

Dependency: P02-T02 and complete publication gate. Run --all locally with no
cloud calls or fallback; record any real execution blocker. Fetch main,
verify receipt at exact committed head/base, obtain
independent exact-head assessment, then push HEAD explicitly to the requested
topic with its original SHA lease. Observe PR head and mergeability; do not merge.

## Dependencies

Git/GitHub available; remote head and base unchanged at publication. Local
complete-gate dependencies must be available without Azure service use.

## Critique Disposition

Critique execution Complete, original verdict Revise; no repeat.

| Finding | Disposition | Evidence and response |
| --- | --- | --- |
| PC-001 | Applied | Require --all and exact full receipt; distinguish offline Bicep from prohibited Azure service calls. Research qualification and details synchronized. |
| PC-002 | Rejected: unsupported premise | The active parent instructions do not prohibit /tmp file operations. A hardcoded lock there is not a blocker. Do not invent a policy restriction or alter the runner. Original critique preserved unchanged. |
| PC-003 | Applied | Inventory/hash and recoverably copy task-owned evidence externally; collision-check before rebase, compare immediately after, and stage only named conflict paths. |
| PC-004 | Applied | Derive local email from live gh api user output, preserve replayed authors, use derived author/committer for new evidence commits and verify trailer. |

## Follow-Up Items

* Prior ten historical production-link defects: unchanged baseline debt, outside
  this rebase. No log rewrite or presentation restoration is authorized.

## Handoff

Implementation changes: .copilot-tracking/changes/2026-10-27/pr-429-main-refresh-changes.md.
P01/P02 are complete in the candidate commit containing this record.
Original Review execution Complete, outcome Residual work. Continue only the
already-authorized PUB-429 publication boundary P03; retain gate, admission
and remote observations externally so committed evidence remains immutable.
