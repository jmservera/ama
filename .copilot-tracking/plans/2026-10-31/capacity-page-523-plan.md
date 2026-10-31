---
title: Capacity page 523 regression-only implementation plan
ms.date: 2026-10-31
---

## Task Metadata

* Task ID: 523
* Task slug: capacity-page-523
* Planning status: Implementation and one independent Review complete; publication pending
* Plan date: 2026-10-31
* Phase details: .copilot-tracking/details/2026-10-31/capacity-page-523-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/capacity-page-523-plan-critique.md

## Executive Summary

The runtime defect is already repaired in merged work. Current local SQL Server
and Chromium confirm capacity, all twelve manager destinations and recovery.
Add one persisted-reopen HTTP regression instead of changing runtime behavior.
The owning class is also inherited by JsonProcurementApi: reopen each backend
through its existing fixture factory and execute both, without added skips.

### What You May Not Know

Live owner verification remains pending despite merged repairs. The full local
publication gate is additional to the requested API checks; a failing gate blocks
push and PR creation. Human and hosted approvals are not local test outcomes.

## User Decisions and Requirements

* Execute research, plan, implement, review in order, committing dated evidence.
* Verify merged fixes first; if fixed, make no change beyond regression coverage.
* Use src/ with tests outside packages, pip only, no secrets or credential files.
* Run exact API discovery with PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests, Ruff check and format check.
* Commit and push fix/capacity-page-523; PR to main uses Refs #523 only and records evidence/validation.
* Never touch main or other worktrees.

## Goals

Protect legacy work-order reads after persisted SQL reload without duplicating
the merged source repair.

## Scope and Non-Goals

One regression method in src/api/tests/test_procurement_api.py and dated RPI
evidence only. No runtime, browser harness, dependency-manifest, design or
knowledge-base changes; no removals. No deployment, live authentication, real
model calls, private/default dataset, branch rewrite or merge.

## Functional Requirements

* Persist a legacy package without contract_version, retaining valid order resident bindings.
* Reopen the actual SQLite-backed SqlStore and inherited JSON Store through
  self.make_store(self.path), preserving each fixture's backend and cleanup.
* Both HTTP reads return 200 with the same package/order identities and Unknown appointment control.
* Repeated reads do not repair/invent metadata, alter procurement state or append audit.
* Appointment offer remains 403 with current-authority explanation and no mutation.

## Non-Functional Requirements

Regression remains typed, fast, offline, fixture-owned and outside installed packages.
Runtime source is byte-unchanged. Requested lint/format and complete gate must pass;
opt-in skips remain disclosed rather than counted as browser/SQL execution.

## Acceptance Criteria

* AC1: Current owned real SQL Server / Chromium evidence covers seeded and empty
  capacity, both failing reads/retry, twelve manager routes and session/draft recovery.
  Already evidenced in Research C4.
* AC2: One new test persists/reopens legacy SQL state, reads both endpoints twice,
  verifies null/Unknown projection, preserved resident bindings and unchanged
  procurement/audit, then verifies unchanged denied offer. SQL and inherited
  JSON instances both run without skips, with original backend preserved.
* AC3: New regression fails when the original strict contract-version lookup is
  substituted by a scoped test-only patch; no runtime edits or separate checkout.
* AC4: Caller full API discovery and both Ruff commands pass.
* AC5: One independent critique and one independent implementation Review are retained.
* AC6: Local commit, complete external gate and verified receipt precede push/PR;
  live verification explicitly pending owner, with Refs #523 and no closing keyword.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-31/capacity-page-523-research.md,
executed / Ready, C1-C7 and W1-W3. Automatic bounded caller-authorized task.
Changes will be created by implementation at
.copilot-tracking/changes/2026-10-31/capacity-page-523-changes.md.
Critique executed Complete / Revise; PC-001 applied, PC-002 rejected with evidence.

## Sources

* Research C1-C4: merged root-cause repair and fresh actual SQL/browser evidence.
* Research C5: reopened SqlStore assignment to app.store in test_resident_api.py.
* src/README.md: complete local publication and receipt protocol.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Regression-only implementation

Dependencies: one critique with dispositions and ready research.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add persisted legacy SQL read regression

Maximum additions: one unittest method in test_procurement_api.py, no new fixture
or helper files, no removals. Canonical target is the existing ProcurementApi
class. Generated targets: none. Semantic coverage reuses actual HTTP/store
contracts; regression coverage adds persisted reopen, isolated missing contract
metadata and read invariance. Existing tests and browser checks remain untouched.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and freeze

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused and requested checks

Focused test, test-only original-defect mutation, owning procurement tests and
requested API discovery/Ruff under shared heavy lock. Dedicated external pip
venv restores missing distribution metadata. Preserve all failed attempts.

<!-- rpi:phase id=P03 -->
### [ ] P03: Independent Review and gated publication

Dependency: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute one independent Review

Review frozen test/evidence diff against synchronized current origin/main.
Initial research/critique base 5666bd33e1827670e5c07e3e3063bbbe989b59d3 stays historical.
Findings route to later work, not another Review or source correction in this task.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Commit and complete publication gate

Resolve gh api user identity, configure repository-local noreply email and commit
test plus dated original evidence with required coauthor trailer. Fetch main, run
tools/rpi-checks.py --all with new external output, verify immediately before push
and independent exact-head assessment. No branch/base rewrites.

<!-- rpi:task id=P03-T03 -->
#### [ ] P03-T03: Push and open PR

Only if complete gate and required independent assessment pass. PR main target,
Refs #523 only, current evidence and validation, live verification pending owner.
Hosted/human approval remains external; never merge.

## Dependencies

Current branch was clean at intake and equaled fetched main; no matching open PR.
Main subsequently advanced to 1330869ea675ff019958846330108b4f45e163ce.
The full gate requires candidate ancestry from the current main base. Merge
origin/main into only this topic branch after committing implementation;
no rewrite, rebase, force-push, main or other-worktree change. The new main changes
infra/workflow/gate/docs, not API/core runtime or this regression. Preserve initial
Research/critique base and review the current synchronized publication boundary.
Missing distribution metadata has been restored with pip in
/tmp/ama-523-20261031-c70d35f2-venv. SQL/browser prerequisites worked in Research.
Shared heavy lock required. Complete gate may expose unrelated baseline failures;
preserve and report blockers without scope expansion or fabricated success.

## Critique Disposition

The one critique is preserved unchanged at
.copilot-tracking/reviews/plans/2026-10-31/capacity-page-523-plan-critique.md.

| Finding | Disposition | Resolving evidence / owner |
| --- | --- | --- |
| PC-001 Medium | Applied directly | Parent updates P01 to use existing backend factory; SQL-only connection cleanup and DB path assertion; focused SQL+JSON instances and full owning suite will run |
| PC-002 High | Rejected: premise absent in parent execution context | No active parent instruction forbids /tmp or temporary directories. Repository explicitly requires /tmp/ama-rpi-heavy.lock and new external outputs; Research actually acquired lock and ran owned SQL/Chromium, and pip venv restoration exited 0. Keep original critique outcome, preserve serialization and complete gate; no protection/source/tooling substitution |

No significant/divergent user decision remains. Critique is not repeated.

## Follow-Up Items

* Live employee-site verification after separately authorized deployment, owner.
* Hosted checks and human approval after gated publication, owner/reviewer.

## Handoff

P01/P02/P03-T01 complete, source frozen. Original independent Review executed
Complete / Residual work, scoped regression Conformant, no source defect.
RV-001 publication qualification is remaining P03-T02/P03-T03 work; RV-002 live
owner verification and RV-003 hosted/human approval remain distinct follow-ups.
Parent commits original Review and current evidence, then runs the complete gate.
No runtime changes authorized because current local evidence confirms the repair.
