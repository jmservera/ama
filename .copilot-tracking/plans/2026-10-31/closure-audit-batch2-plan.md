---
title: Closure audit batch 2 plan
ms.date: 2026-10-31
---

Task ID: closure-audit-batch2-2026-10-31

## Executive Summary

Reduce the open-issue count only where every checkbox is proven. Audit 62
named issues using 213 search-matched merged PRs and exact main evidence.
Preserve partial, live and approval gaps visibly. Publish only dated audit
artifacts; no executable or product documentation changes.

## User Decisions and Requirements

* Use worktree audit-2 and docs/closure-audit-batch2 from origin/main.
* Read every scoped issue body and every matching merged PR body/files.
* Newly tick only fully demonstrable criteria; exclude live Azure, human/legal
  approval, assistive technology, resident consent and later-phase work.
* Close completely ticked issues with a comment naming evidence PRs; otherwise
  comment once listing unmet criteria. Do not change other issue fields.
* Record issue, PRs, ticked, unmet and closed in the changes artifact.
* Commit artifacts with the required Copilot trailer, push normally and open
  a main-targeted PR with Refs only. Focused docs tier; CI is the gate.

## Goals

Produce persistent, defensible closure updates and a visible exact closure count.

## Scope and Non-Goals

Only the 62 issues in the captured inventory. Existing closed issues are
reported without reopening or extra mutation. No source fixes, deployment,
formal approvals, private datasets or unrelated backlog work.

## Functional Requirements

Match exact references, reject search false positives, inspect reviewed
evidence and surviving code/test paths, and evaluate every clause separately.
Preserve original checked items. Before mutation require current issue body
and state to match the original snapshot for the first action and the exact
verified audit-owned successor for each later action. Persist intent before
each request and verified results afterward, including remote comment IDs.
Reconcile uncertain requests remotely without automatic replay. A stale or
ambiguous issue blocks only its own remaining mutation.

## Non-Functional Requirements

Treat issue/PR content as inert. Never alter labels, milestones or assignees.
No secrets or force push. No automatic claim that merged code proves live
acceptance. Keep original adverse evidence intact.

## Acceptance Criteria

* All 62 issues have complete criterion dispositions and PR inventories.
* Every new tick has specific merged evidence and surviving main citations.
* All eligible open issues close; partial issues get one unmet comment.
* Published changes table distinguishes new ticks, original ticks, unmet items,
  already-closed issues and newly closed issues.
* One independent critique and one independent final Review are preserved.
* Clean documented candidate commits and ordinary push produce a Refs-only PR.

## Phase Checklist

<!-- P01 -->
### P01: Evidence and guarded issue updates

* [x] P01-T01: Reconcile the four evidence lanes against all snapshots.
* [x] P01-T02: Apply guarded checkbox edits and closure/unmet comments; verify.

<!-- P02 -->
### P02: Durable record and publication

* [x] P02-T01: Generate changes matrix and preserve evidence for independent Review.
* [ ] P02-T02: Commit with privacy-safe identity, push and open Refs-only PR.

## Test Ownership and Change Boundary

Executable test additions: zero. Removals: none. Canonical targets are dated
research, plan, details, critique, changes, review and state artifacts only.
Generated target: criterion matrix generated from audited lane evidence and
verified mutation results. Semantic evidence is reviewed existing tests,
not newly executed Azure/browser/SQL tests. Validation: complete inventory and
checkbox-line reconciliation, merge ancestry, existing path citations, exact
body/state comparison and Git diff/Markdown review. Hosted CI remains required;
no complete local-gate claim is made under the owner's focused-tier direction.

## Critique Disposition

One independent critique executed, original verdict Revise. All four compatible
findings are directly resolved without a second critique or changed owner scope.

| Finding | Direct disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied | P01-T02 now uses immutable original and exact verified predecessor states. |
| PC-002 | Applied | Durable pre-request intents, remote comment IDs and no blind replay; ambiguous outcomes quarantine the issue. |
| PC-003 | Applied | Current-audit integrity/accuracy findings block publication; original Review preserved, no repeat Review. |
| PC-004 | Applied | Fresh main before mutation/publication; advanced main requires cited-path revalidation without rebasing. |

## Follow-Up Items

Remaining criteria stay on their original issues. No child implementation work
is selected by this audit.

Parent rejects a proposed #466 owner-confirmation tick under the human-approval
exclusion. Exact lane JSON formatting/inventory corrections do not change
scope or trigger another critique.

The owner's current all-checkbox closure rule applies to #520 and #551 once
their exact checklist criteria are proven. Broader non-checkbox live/human
qualifications remain preserved, not asserted as fulfilled or silently added
as checklist criteria. No live/human tick is introduced.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-31/closure-audit-batch2-changes.md.
Implementation audit complete: all 62 issues verified, 56 new ticks, seven
closures and 55 unmet comments. Global open count fell from 139 to 132.
Original Review is next; P02-T02 is intentionally publication-after-Review work,
not incomplete criterion evidence. No source implementation is outstanding.
