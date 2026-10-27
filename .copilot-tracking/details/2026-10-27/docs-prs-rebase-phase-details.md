<!-- markdownlint-disable-file -->
---
title: Documentation PR preparation phase details
description: Evidence and execution expectations for isolated documentation rebases
ms.date: 2026-10-27
---

## Metadata

Task ID: docs-prs-rebase-2026-10-27. Plan:
.copilot-tracking/plans/2026-10-27/docs-prs-rebase-plan.md.
Research: .copilot-tracking/research/2026-10-27/docs-prs-rebase-research.md.

## Phase Index

| Phase | Context and outcome | Status |
| --- | --- | --- |
| P01 | Fresh remote-based worktrees and content-preserving rebases | Complete |
| P02 | Scoped documentation validation and committed original evidence | Complete in this candidate commit; original adverse Review preserved |
| P03 | Full exact-head gates, assessment, publication and observation | Pending P02 |

<!-- rpi:phase id=P01 -->
## P01: Isolate and rebase

<!-- rpi:task id=P01-T01 -->
### P01-T01: Capture remote heads and create fresh worktrees

Use origin/main 885ee05fc45122cf7a1ea4f7f003dc88bfda08ee unless a fresh
fetch changes it. Original remote heads:

| PR | Remote branch | Head |
| --- | --- | --- |
| 454 | docs/resident-prd-backlog-readiness-441 | d4863a2a930771ce60dac9a8d069d1e6be92ed51 |
| 439 | docs/demo-cost-headroom-126 | 3648875eac31dd877ab274a2cc6af1eb87613f26 |
| 429 | docs/cutover-soak-review-201 | 002fc375d4644e761c6c8e7620693f8a899ebc73 |

Create docs-pr-454-rebase, docs-pr-439-rebase and docs-pr-429-rebase directories
under /home/azureuser/source/ama-wt, with local preparation branches from those
exact remote tips. Original existing local worktrees and branches stay untouched.
Capture refs and diff before editing. No uncommitted work may be moved.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Rebase each snapshot and resolve semantic/log conflicts

Rebase onto reviewed origin/main, preserving topic commits rather than merging
main. Inspect conflict stages before editing. For the knowledge-base log, retain
main as byte-identical prefix and append original branch-added entry blocks,
without duplicating already present entries. For index/addendum/PRD/evidence
conflicts, preserve non-overlapping changes and named human/acceptance boundaries.
Avoid replaying obsolete generated rubric scores over main's current snapshot.
Completion evidence: ancestor, remaining diff, original-to-new comparison and
zero unresolved conflict markers.

<!-- rpi:phase id=P02 -->
## P02: Validate and preserve evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Review Markdown, links, allowed paths and append-only preservation

Assemble available task evidence before validation and independent Review.
Check changed Markdown local destinations and fragment IDs, relative to each
owning file, with archive-backed historical exceptions reported separately.
Review newly added text for frontmatter, heading/table consistency, accidental
scope loss and invented acceptance claims. Run git diff --check and allowed-path
assertions. Compare original topic-added log blocks against final log and require
the entire reviewed-main log as a byte-preserved prefix.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit implementation and original RPI evidence after Review

Run one independent post-implementation RPI Review for the three semantic diffs,
record its original verdict and route findings without another Review loop.
After adding the original Review and its disposition, repeat scoped
Markdown/link/anchor, allowed-path and git diff --check validation over the
complete staged diff and record its inventory before committing.
Resolve gh api user immediately before committing and derive
{id}+{login}@users.noreply.github.com. Configure git config --local user.email;
ensure author and committer use that address and inspect every new commit's
headers. Include the required Copilot trailer. Do not claim later
gate or hosted-check outcomes in the earlier committed record.

<!-- rpi:phase id=P03 -->
## P03: Gate and publish

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run full gates and independently assess exact eligible heads

Run python3 tools/rpi-checks.py --all --base REVIEWED_MAIN --out NEW_EXTERNAL_DIR
from each clean committed candidate. Keep every failure external and immutable.
Do not fabricate status or fall back to cloud/partial evidence. Fetch main and
verify exact full receipt immediately before independent exact-head assessment
and publication. Assessment must affirm publication eligibility across every
final changed file, including evidence. Any failed, blocked or incomplete
assessment, or unresolved publication-blocking Review finding, blocks that PR.
Preserve original Review outcomes; record correction dispositions separately.
A correction or changed head/base/tool identity requires a new gate and
exact-head assessment, never a repeated original RPI Review.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Verify leases, push, mark ready and observe hosted checks

For eligible candidates push HEAD:refs/heads/REMOTE_BRANCH with explicit
--force-with-lease=refs/heads/REMOTE_BRANCH:ORIGINAL_REMOTE_HEAD. A moved remote
blocks the action. Run gh pr ready for the named PR, allow checks to start and
observe until a meaningful settled state or concrete blocker. Record current
head, draft flag, mergeable, mergeStateStatus and every check's status/conclusion.
Never merge, write main, change protection or touch excluded code PRs.
