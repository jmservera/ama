<!-- markdownlint-disable-file -->
# RPI Plan: hazard-referral-controls-85

## Task Metadata

Task ID: 85. Date: 2026-10-17. Planning complete; Ready after direct revisions.
Details: .copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md
Critique: .copilot-tracking/reviews/plans/2026-10-17/hazard-referral-controls-85-plan-critique.md

## Executive Summary

Retain the already delivered referral/receipt/acceptance/home-hold journey.
Correct reproduced gaps in who can record its evidence, independent restart
identity and failed-save audit integrity. Do not create a second hazard system.
The one independent Review found a post-commit audit-replay defect (RV-001).
Authorized correction ONE distinguishes committed outcomes from rollback;
the original Not accepted verdict remains, not replaced by parent self-closure.

### What You May Not Know

Case-only email self-release and a success audit for a failed save are possible
today. BRD FR-015 now describes tenure; FR-003/RULE-003 hold the hazard intent.
Operational role/timing ratification is still not evidence of this exercise.
No decision-critical blocker prevents local engineering; real approvals and
verified communications remain out of scope.

## User Decisions and Requirements

* Full ordered automatic RPI, one independent critique and Review; no skips.
* Preserve all four issue criteria and existing human/service boundaries.
* No invented legal clocks, duties, approvals or automatic hold release.
* Own hazard module and minimal linked surfaces; no quality/finance source or
  shared fixture churn. Preserve merged #84/#94/#90.
* Local venv/pip, actual task-owned loopback SQL Server parity, relevant tests
  and configured lint/format/types. Web skills/browser only if web changes.
* Commit owned source/docs/all dated artifacts, push normal branch and open
  main PR Refs #85; no merge/rebase/force-push/issue closure.

## Goals

Trustworthy current-actor evidence and independent retrofit-only decisions
without taking ownership of hazard categorisation, clocks or closure.

## Scope and Non-Goals

In scope: new canonical hazard helper, existing hazard methods in workflows,
one additive SQL validator hook, canonical core and HTTP/SQL regressions,
component docs and existing hazard synthesis/index/log.
Out of scope: UI edits, fixture redesign, new service workflow, delegation
policy, real communications, private data, Azure, legal activation or AI use.

## Functional Requirements

* Every existing hazard mutation validates registered current identity through
  existing `_actor`; SQL repeats validation under its writer lock.
* Destination is a separate validation subject, freshly resolved even when
  caller is valid, and rechecked under SQL writer lock. Receipt/acceptance must
  bind persisted destination identity, not code alone.
* Persist code/email/OID with historical event identity. Independent release
  rejects matching normalized email, staff code or nonempty OID for reporter
  or repair recorder, including historical legacy fallbacks.
* Failure discards staged SQL mutations/success audits before recovery reads,
  preserving prior audit and original exception with explicit recovery logging.
  Capture an independent pre-operation pending-audit baseline and restore it
  on both eager SQL authority/conflict discard and generic failures.
  After a successful COMMIT, do not replay already-committed pending audit;
  retain/log the original later synchronization error with persisted-outcome
  warning. Durable reread must show release and both audits exactly once.
* JSON saves precede successful hazard/emergency audit emission; known
  pre-replacement failure restores memory and leaves durable state/audit
  unchanged. Post-save audit failure is explicitly a potentially persisted
  outcome, retaining original error, not falsely claimed cross-file rollback.
* Keep source/awareness, separate evidence, owned follow-up, fixed affected home,
  release role/reason/reference and externally supplied times unchanged.

## Non-Functional Requirements

* No new persistence schema, transport, statutory timing calculation or module
  dependency violation. Additive SQL hook retains all existing validators.
* Atomicity measured by durable before/after state/audit and reload after
  injected failures; no inferred acceptance from a successful response alone.
* No edits to other dirty worktrees. Shared sqlstore overlap declared here;
  integration is one named additive hook, no shared abstraction rewrite.

## Acceptance Criteria

* Formal regressions fail before fix for unregistered/revoked caller, normalized
  self-release and failed-save audit; pass after on JSON/SQLite as applicable.
* Current actor/destination/receiver and transaction-time revocation tests
  refuse without persisted changes. Code/OID aliases cannot self-release.
* Independent eligible actor still completes record-only journey; all four
  criteria remain visible/durable with service ownership unmodified.
* Actual disposable loopback SQL Server reruns canonical hazard semantics plus
  commit-time staff revocation and persistence/audit failure probes.
* Relevant existing core/API suites and configured ruff/mypy pass. No web edits
  means no new browser/WCAG acceptance claim.

## Sources

.copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md:
C1-C12. Core/API existing hazard contracts and canonical tests, PRD FR-015/
AC-018/038, BRD FR-003/RULE-003 and ADR 0005 limits.

## Implementation Context Record

Automatic parent continues after one critique. Changes record owned by Implement:
.copilot-tracking/changes/2026-10-17/hazard-referral-controls-85-changes.md.
No required human operational review is claimed complete.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct hazard evidence boundary

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Prove defects and implement current/independent actor scope

Formalize fail-before cases; implement dedicated hazard scope and additive
SQL transaction validation; retain existing state/history/gate semantics.
Dependencies: completed Research and critique.

<!-- rpi:phase id=P02 -->
### [x] P02: Prove parity and document limits

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Validate persistence/API and update existing docs

Run canonical tests and actual isolated SQL Server with ephemeral unlogged
credentials and exact own-container cleanup. Update existing synthesis/index/
append-only log. Dependencies: P01-T01.

<!-- rpi:phase id=P03 -->
### [ ] P03: Independently assess and deliver

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: One independent Review

Executed Complete / Not accepted; RV-001 High retained. Dependencies: P02-T01.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Apply authorized RV-001 correction ONE

Mark actual SQL COMMIT in the active hazard scope, distinguish uncommitted
quarantine from post-commit recovery, log/annotate original synchronization
error, and avoid restoring committed baseline audit. Add one canonical
interleaved post-commit regression reused on actual SQL Server. Remain within
12 semantic methods and preserve all existing hooks. Dependencies: P03-T01.

<!-- rpi:task id=P03-T03 -->
#### [ ] P03-T03: Reconcile and publish owned work

Retain original independent finding and parent-only correction evidence.
Normal commit/push/main PR Refs #85 with exact head; independent final-head
closure not fabricated. Dependencies: P03-T02.

## Test Ownership and Budget

Owner: this task. Canonical targets: test_hazard_referral.py,
test_hazard_api.py and hazard-specific SQL harness; no generated suite copies.
Removals: none. Maximum new semantic test methods: 12; at most 3 harness adapter
methods. Reuse inherited semantic methods on actual SQL. Regression coverage
checks retained gates/ownership/fixture hash; do not duplicate whole suites.
No shared dataset edit expected; run existing manifest exact-hash audit and
preserve provisional eleven-profile/nine-workflow authority.

## Dependencies

No issue dependency. Parent #81 is hierarchy only. Installed source distributions
in worktree-local .venv, Docker daemon and existing SQL image are available.

## Critique Disposition

One critique executed; verdict Revise, all three compatible findings directly
applied without another critique.

| Finding | Owner/disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 High | Planner, resolved | Separate fresh destination subject and commit recheck; receiver binds persisted identity; details P01/P02 tests valid caller with invalid/revoked recipient |
| PC-002 High | Planner, resolved | JSON save-before-audit and partial post-save outcome contract; details failure matrix distinguishes backends |
| PC-003 Medium | Planner, resolved | Pre-operation pending baseline, eager-discard branch and original-error/recovery checks; details failure matrix |

## Follow-Up Items

* Repairs/Safety/Housing operational responsibility, release authority and
  timing/escalation ratification remain external owner work.
* Verified service transport and Azure/model/human acceptance remain separate,
  explicitly unauthorized in this local task.

## Handoff

Research, Plan/critique, Implement and the one independent Review executed in
order. Original Review Complete / Not accepted remains unchanged. Authorized
correction ONE now has canonical fail-before/fix-after SQLite and actual
loopback SQL Server evidence, not independent final-head closure.
Only P03-T03 authorized publication remains; no second Review.
