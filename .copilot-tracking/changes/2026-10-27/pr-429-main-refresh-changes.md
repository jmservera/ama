---
title: PR 429 main refresh changes
description: Rebase preservation, documentation checks and publication evidence
ms.date: 2026-10-27
---

## Context and Scope

Task pr-429-main-refresh-2026-10-27, slug pr-429-main-refresh.
Declared implementation scope: P01 and P02-T01; independent Review owns
P02-T02, and publication P03 follows committed evidence and exact-head gates.
Plan and phase details are ready after one critique with direct dispositions.

## P01: Preserve and Rebase

Completed. Worktree ../ama-wt/pr-429 started at authoritative old head
ad79455a3ec2c47d935fbc3cd055555ff188bc35 on fresh local carrier
docs/pr-429-refresh-20261027. Reviewed base:
49c942b33b89100c084d48a91215989e22de5887. Other worktrees remain untouched.

Replayed five substantive commits; omitted only the verified rubric-only
ad79455a commit. New pre-maintenance head:
f25344fc9f35bdf9468be6a2202ad4aebfa11196.
Only conflict: docs/reference/log.md. Kept all of main's log unchanged, then
appended the complete original #201 entry once. README merged automatically:
both main's #126 cost row and topic's #201 preparation row survive.

Before replay, six new task evidence files were inventory/hash backed up at
/home/azureuser/.copilot/session-state/f81f525a-5b02-44f2-9bd3-9f1cf41c0fa4/files/pr429-pre-rebase.
No paths collided with either Git tree. Immediate post-rebase comparison
confirmed all six hashes unchanged. Only the named conflict file was staged
during rebase; new evidence was not folded into original commits.

The external audit confirms 17 old topic blobs exactly preserved, including
all original tracking records and both non-index production documents.
Shared prior rebase evidence already present on main remains byte-identical.
Main's rubric score is unchanged; old score Git objects remain historical.
Authenticated GitHub id/login dynamically derived the repository-local
noreply email; all five replayed committers and historical authors use it.

## P02: Documentation Validation

External standard-library audit:
/home/azureuser/.copilot/session-state/f81f525a-5b02-44f2-9bd3-9f1cf41c0fa4/files/pr429-audit.py.
Initial review identified four malformed relative navigation links in this
task's new critique. Corrected only their destinations, not findings/verdicts.
Repeated audit: 15 changed Markdown files, 709 local links, zero new defects.
Seven distinct unchanged main defects cover missing mentor/old presentation
assets and old MVP anchors; repeated occurrences are deduplicated. They remain
baseline debt, not rebase regressions, and no old log entry is rewritten.

Checks pass: exact main-log prefix plus original topic entry, both index updates,
17 original blob comparisons, main rubric unchanged, no conflict markers,
main ancestor, docs/tracking-only path inventory, git diff --check origin/main.
Range-diff preserves original substantive patches apart from changed log context
and already-main shared tracking evidence.

## Amendments and Divergences

PC-001/003/004 directly applied. PC-002 rejected because its asserted /tmp
restriction is absent from parent instructions. No new user-owned decision,
source change or second critique. Full offline local gate remains required;
Azure service calls, uv, merge and main writes remain forbidden.

## Review Handoff and Publication

One original independent Review executed Complete with outcome Residual work:
.copilot-tracking/reviews/logs/2026-10-27/pr-429-main-refresh-review.md.
No new implementation defect; RV-001 retains PUB-429 publication and RV-002
routes unchanged baseline links separately. Earlier task reviews are historical
and unchanged. P01/P02 are complete in the evidence candidate commit; P03
publication and hosted results are not yet run.
External exact-head gate and later observation must not be reported as a second
implementation Review or operational acceptance.

Final evidence assembly is part of the commit containing this record. The
committed state is the immutable pre-publication boundary; later exact-head gate,
admission and remote observations are retained in persistent session files
under pr429-publication without modifying or invalidating the candidate.
