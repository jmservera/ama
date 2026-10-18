---
title: Issue 115 digest anchor delivery receipt
description: Actual publication, frozen original evidence and coordinator handoff
ms.date: 2026-10-18
---

## Actual Delivery

Historical initial receipt. Coordinator subsequently returned NOT ACCEPTED
for one Medium malformed-prefixed-anchor false green at bbb13521. Authorized
correction ONE is recorded separately in issue-115-digest-anchor-correction-one.md,
with failing-first and25/44 passing local checks; same-coordinator final-head
follow-up remains required, no new/amended original Review.

PR: https://github.com/jmservera/ama/pull/404, OPEN, non-draft, target main.
Branch: fix/digest-anchor-evidence-115.
Exact base: c803614e8ca7c604e509f1c088f8b8f90f3063ef.
Source candidate: d53a7c68245dc708c628bb37853c308d9811fcbe.
Initial published delivery:211458f94c25a705971b0f912b1990f0b8de7aec.
Final delivery is the evidence-only commit containing this receipt; its exact
hash is published in the PR body/live headRefOid and final handoff. A file cannot
embed its own containing-commit hash without self-reference. No source change
after the original candidate; verify with
`git diff d53a7c68245dc708c628bb37853c308d9811fcbe HEAD -- src`.

Initial `git push --set-upstream origin fix/digest-anchor-evidence-115` and
`gh pr create --repo jmservera/ama --base main --head fix/digest-anchor-evidence-115`
both succeeded. gh pr view and git ls-remote agreed on initial head/base.
Remote main remained exact pinned base immediately before/after publication.
No rebase, force-push, merge, main rewrite, policy/deployment action, or changes
to other PRs/issues/boards/settings. PR uses Refs #115, no issue-closing instruction.
Explicit dependencies None; parent #114 hierarchy only. PR #403 is merged base.

## Actual Ordered Phase Log

| Order | Execution | Actual result |
| --- | --- | --- |
| 1 | Research, rpi-research | Wider -> Deeper -> Contrarian, executed, Ready; false green reproduced offline |
| 2 | Plan, rpi-plan | Plan/details candidate written; one fresh independent rpi-plan-critique Complete / Revise, PC-001 Medium |
| 3 | Implement, rpi-implement | TMPDIR disposition adopted; failing-first17/four behavioral failures -> minimal guard/README ->21 focused/coupled and40 discovery passes; configured quality gates pass |
| 4 | Review, fresh independent rpi-review | Exactly one original: Complete / Residual work; bounded source Conformant, no implementation defects; independent21/40, quality and exact-base failure replay |
| 5 | Delivery continuation | Originals frozen, artifacts committed, branch pushed/PR404 opened, publication reconciled; session stopped for coordinator |

No source-correction cycle used (zero of maximum two). No second critique or
original Review; no adverse original edited. Reviewer residual findings are
not silently promoted to complete issue acceptance.

## Frozen Original Evidence

| Original | SHA-256 |
| --- | --- |
| .copilot-tracking/reviews/plans/2026-10-18/issue-115-digest-anchor-plan-critique.md | d1add2a5642689cb9a615f3aaa989871a3b405f7f5cab076689fdcc0110314e0 |
| .copilot-tracking/reviews/logs/2026-10-18/issue-115-digest-anchor-review.md | dc72719806ba648af00d34c9ef6b0c0d049ed87372d60ee49e959b328694186e |

Source hashes, full actual commands, before/after stdout, counts/errors/skips and
quality-exemption limits are in changes.md and adjacent before/focused/
orchestrator/quality.log files. Initial missing package/tool validation caused
task-local pip installation; no speculative dependency installation.
Before.log had only two unittest trailing spaces stripped for git diff --check;
raw and committed hashes disclosed, neither original assessment modified.
Reviewer shell rg exit127 was resolved with direct reads, not an application
failure. Existing tests/fake preserved, eight additions and zero removals.
Task fixture roots cleaned with empty-directory rmdir, no services started.

## Residual Findings and Limits

RV-001 publication portion completed; coordinator must independently assess
exact final PR head, including final receipt/state, not only source candidate.
RV-002 owner-approved retention duration and irreversible lock evidence,
RV-003 real scheduler/log/alert/missing-run/recovery acceptance and RV-004 second
human historical first-publication check remain unmet distinct follow-ups.
No retention duration, owner lock approval, cloud immutability, operational
monitoring, recovery or whole #115/#114 closure inferred.
SQL Server/Docker/Azure/browser checks N/A/not run for bounded offline delta;
coupled existing SQLite unit coverage is not external SQL/recovery acceptance.
Hosted initial-head checks had begun, not all completed; final live PR status
remains separate and is not independently accepted by this task.

## Artifact Inventory

All task artifacts use2026-10-18/issue-115-digest-anchor:

* research/: research.md
* plans/: plan.md
* details/: phase-details.md
* reviews/plans/: plan-critique.md (original frozen)
* reviews/logs/: review.md (original frozen)
* changes/: changes.md, before.log, focused.log, orchestrator.log, quality.log,
  pr-body.md, delivery.md (this receipt)
* rpi-sessions/: state.json (automatic task completed, session stopped)

Actual full paths are in state and PR body; all are committed with delivery.
Source changes are only orchestrator digest_blob.py, test_digest_blob.py and
the existing ledger README paragraph. No KB inventory/web/loadcheck/new-mvp edit.

## Next Owner

Coordinator: complete independent exact-final-head review of PR404. Stop here;
do not merge, rerun original Review, start a child loop or perform operational
follow-ups without new explicit authorization.
