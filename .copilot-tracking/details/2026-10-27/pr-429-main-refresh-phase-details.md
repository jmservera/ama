---
title: PR 429 main refresh phase details
description: Exact inputs, preservation checks and publication boundary
ms.date: 2026-10-27
---

## Metadata

Task ID: pr-429-main-refresh-2026-10-27; slug: pr-429-main-refresh.
Plan: .copilot-tracking/plans/2026-10-27/pr-429-main-refresh-plan.md.
Research: .copilot-tracking/research/2026-10-27/pr-429-main-refresh-research.md.

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete in evidence candidate commit | P02-T01, P02-T02 |
| P03 | Pending Review and publication gates | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Preserve and rebase

<!-- rpi:task id=P01-T01 -->
### P01-T01: Replay substantive topic commits

Authoritative old topic: ad79455a3ec2c47d935fbc3cd055555ff188bc35.
Reviewed main: 49c942b33b89100c084d48a91215989e22de5887.
Worktree: ../ama-wt/pr-429; carrier: docs/pr-429-refresh-20261027.
Original local topic remains checked out elsewhere and must not move.
Before new commits, resolve gh api user and construct id+login@users.noreply.github.com
from its returned fields, setting repository-local identity for author and committer.
Rebase only five substantive commits, excluding final rubric-only ad79455a.
Preserve original objects as immutable evidence. Untracked new task evidence
must not be staged into an original replayed commit.
Inventory/hash and copy the task-owned evidence to persistent session storage,
verify no collisions with base/replay paths, and compare immediately after rebase.
Stage only named conflict files, never all untracked files during replay.

Completion: five substantive commits replayed, pre-maintenance head
f25344fc9f35bdf9468be6a2202ad4aebfa11196. Sole conflict was the reference log;
removed only conflict markers and inserted the entry-separating blank line.
Six task evidence files were collision-checked, backed up under persistent
session files/pr429-pre-rebase and verified hash-identical immediately afterward.
Only docs/reference/log.md was explicitly staged during replay.

Conflict targets: docs/reference/log.md and possibly README frontmatter/rows.
The complete current main log remains an exact byte prefix; append the old
topic-only entry unchanged. No historical text/date edit. Index retains both
#126 cost and #201 proposal navigation. Compare all original tracking blobs.

<!-- rpi:phase id=P02 -->
## P02: Validate and review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Documentation checks and preservation

Check all changed Markdown links, existing files and GitHub-style anchors.
Compare unresolved findings to main; new/modified broken destinations fail.
Original critique defects already corrected in the previous rebase remain fixed.
Do not treat archived missing assets as a new rebase defect.
Run git diff --check and staged equivalent. Check full diff path allowlist and
conflict markers. Confirm main ancestor, topic log exact bytes once, original
production topic hunks and tracking files, and main rubric unchanged.
No repo test/tool additions; external standard-library helper permitted.

Completion: external pr429-audit.py checked 709 local links in 15 changed
Markdown files, zero new defects, seven distinct unchanged main defect tuples.
Verified 17 original blobs byte-for-byte, exact main-log-plus-original-entry,
both index updates, main score unchanged and Git whitespace clean.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Independent Review and committed evidence

One fresh reviewer receives plan, details, research, changes and exact original
head/base, and writes .copilot-tracking/reviews/logs/2026-10-27/pr-429-main-refresh-review.md.
Review covers docs-only inventory, both-side preservation, all original evidence,
new link defects, whitespace, authority boundaries and publication sequencing.
Do not call local checks operational acceptance or hosted approval.
Commit dated task evidence after Review; set state to the actual publication
boundary. Later observations remain external, not a second Review or amended
original outcome.

Completion: one independent original Review executed Complete, outcome
Residual work. RV-001 routes already-planned publication PUB-429; RV-002 routes
unchanged baseline link debt separately. No new implementation defects.
This candidate commit records the Review and final reconciliation; P03 remains
pending its actual exact-head gates, not silently accepted.

<!-- rpi:phase id=P03 -->
## P03: Publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Gate, exact-head assessment and lease push

Caller bans Azure service use and uv. Enforce supplied complete --all gate
requirement despite newly merged main's documentation-tier alternative.
Local offline Bicep tooling is not Azure resource use. No cloud calls/fallback.
The critique's asserted /tmp prohibition does not exist in parent instructions;
reject PC-002's premise without changing its original artifact or runner.
If the complete gate cannot run, record the real blocker and do not bypass it.
If permitted: new external output, fresh main, exact-head receipt verification,
independent admission, explicit force-with-lease to only
refs/heads/docs/cutover-soak-review-201. No main push, merge, closing keywords
or PR-body rewrite needed. Observe exact remote head and mergeability with gh.
