<!-- markdownlint-disable-file -->
# RPI Plan: Resident authority extension

## Task Metadata

* Task ID: 521
* Task slug: resident-authority-extension-521
* Date: 2026-10-30
* Planning status: Ready after direct critique dispositions
* Details: .copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/resident-authority-extension-521-plan-critique.md

## Executive Summary

Retain the rebased January renewal, execute its previously blocked local
validation, and correct only defects demonstrated within #521. The shared
exclusive cap is February 1 UTC; existing guards and approvals stay unchanged.
P01 execution is complete: API, domain/helper and real-SQL tests passed; API/core
static checks passed. Targeted infra static debt reproduces on the base.
Origin/main advanced during validation; final gate is blocked pending a separately
reconciled current-base candidate. No second rebase is silently performed.

### What You May Not Know

The source change does not renew SQL rows or existing secret versions. Paid-model
authority still expires independently on November 1. Live application is not
authorized by this local task, so whole-issue acceptance cannot be claimed.

## Sources

* .copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md:
  completed focused research, C1-C7/W1, Planning Readiness Ready.
* .copilot-tracking/reviews/logs/2026-10-28/resident-authority-extension-521-review.md:
  original residual work, preserved.
* src/README.md: full local gate and external exact-head receipt.
* Issue #521 and current user request: scope, acceptance and local-only boundaries.

## User Decisions and Requirements

* Rebase the existing local commit onto origin/main before this ordered full loop.
* Extend resident authority through January 31 UTC, consistently across consumers.
* Preserve min0, synthetic resident-only scope, narrow rights and all owner gates.
* Record rotation/renewal and added cost inside unchanged USD700 cap.
* Run requested API unittest, Ruff check/format and mypy; heavy work holds the lock.
* No Azure/cloud actions, deploys, live sign-in, secrets or credential files.
* Commit locally with Refs #521 and required trailer; never push.

## Goals

Produce executable local boundary evidence and an honest acceptance matrix.

## Scope and Non-Goals

In scope: the existing 12-file source implementation and fresh RPI evidence,
validation setup outside the worktree and tightly coupled fixes if demonstrated.
Excluded: UI changes, private data, inference renewal, Azure application,
resources/roles/network changes, remote publication and unrelated baseline fixes.

## Functional Requirements

* One packaged authority feeds all consumers; valid at the former cutoff and
  January's final instant, denied at February 1 UTC.
* SQL checked migration is atomic and repeatable, preserving rows/revocation/
  provenance and principal rights.
* Secret/deploy helper maximum remains aligned without weakening Modify refusal.

## Non-Functional Requirements

* No resource, RBAC, network, replica, synthetic-data or approval guard change.
* Costs remain assumption-labelled, overlapping estimates not summed, subject
  to actual headroom and exact approval before any paid action.
* No secrets/private inputs; isolated synthetic local SQL only.

## Acceptance Criteria

* AC1: Code/SQL/helpers/docs/tests consistently implement the exclusive new cap;
  domain/HTTP/helper tests prove the former cutoff allowed and new cutoff denied;
  real SQL proves migrated constraint, rollback and preserved rights.
* AC2: Record USD46 incremental proxy (USD56 with reserve) from original cutoff,
  or USD15.50 (USD25.50 with reserve) for January only, unchanged USD700 all-in
  ceiling, with no added resources or roles.
* AC3: Credential/SQL rotation steps documented and independently technically
  reviewed; separate owner operational review remains explicitly pending.
* AC4: Live apply only after explicit exact owner confirmation, verified and
  recorded. Not executable in this run; do not mark whole criterion proven.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Validate and reconcile implementation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Restore local tools and run bounded checks

Install existing project dev distributions with pip into an external venv after
the observed missing-import/tool failures. Under flock -w 600 run core resident,
infra helper and API requested suites plus Ruff/mypy. No cloud integration.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Correct demonstrated in-scope gaps and reconcile docs

Keep the existing source unless checks expose a coupled defect. Record actual
commands, failures, skips and accepted boundaries; update current docs only where
necessary. Reconcile plan/details/changes before Review.

<!-- rpi:phase id=P02 -->
### [ ] P02: Independent Review and final candidate gate

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute one original independent post-implementation Review

Fresh reviewer activates rpi-review, assesses source-only acceptance and rotation
plan, writes only the current Review. Findings become follow-ups, no Review loop.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Commit and run complete external exact-head local gate

Commit source/evidence using authenticated noreply identity, Refs #521 and
Co-authored-by trailer. Run tools/rpi-checks.py --all --base a02984e8d71d312f089ad75713d7a98e59aee420
--out a fresh external directory. The runner owns the same heavy lock, so do not
wrap it in a second flock (deadlock). Offline Azure CLI Bicep compilation/version
only, isolated AZURE_CONFIG_DIR; never cloud APIs/sign-in or existing credentials.
Fetch main and verify any passing receipt. No push. A failed gate stays unmet.
After a passing gate, refetch and verify against current main, then obtain a
distinct external read-only exact-head/receipt assessment without modifying the
candidate or repeating the original Review. Base/HEAD/tool/image/input drift
invalidates the gate; stop and report rather than silently reconcile or rebase.

## Dependencies

Research complete; namespace/tool setup missing. Real-SQL/container/browser/scanner
prerequisites may block required integration. No fallback or skipped-test waiver.
Current execution supersedes setup uncertainty: tools restored and owned SQL
passed. Base drift to 4b37c2c9ae5553e55604a10e97e7ab21a2a265fb blocks the
exact-head full gate against the reviewed a02984e8 base.

## Test Ownership and Locked Budget

* Canonical owners: core/tests for domain/SQL, api/tests for HTTP, infra/tests
  for helper contracts; no tests inside packages.
* Removals: none. Maximum new methods this continuation: 2, only for a proven
  in-scope gap; existing October 28 additions retained.
* Canonical generated input: core resident-demo.json; SQL template rendered,
  never direct execution. No new generated output committed.
* Semantic evidence: runtime cutoff, helper refusals, SQL integrity/rights.
  Regression evidence: full API suite and package lint/types.
* No UI edits planned, so UI-specific Playwright/axe is not triggered; the full
  runner still owns its existing browser contracts.

## Critique Disposition

One critique executed: Revise. Original findings preserved in the critique.

| Finding | Disposition | Resolution |
| --- | --- | --- |
| PC-001 | Rejected: unsupported parent constraint | Critic reported a worker-local temporary-directory restriction not present in this executor. Caller explicitly requires /tmp shared flock; external venv/receipt remain permitted. No policy/tool change. |
| PC-002 | Applied | Separate owned local SQL fixture runs exact core SqlBoundaryTests; full runner alone is not claimed to cover this class. Lifecycle in details. |
| PC-003 | Applied | All setup/checks use env -i allowlist, isolated HOME/data/Azure config and external caches; no inherited opt-ins/credentials. |
| PC-004 | Partially applied; conflicting advice rejected | Inspect lock holder; no foreign process/output access or nested flock. Explicit current caller requires flock -w 600, taking precedence over generic nonqueued guidance. Runner native lock uses the same timeout. |
| PC-005 | Applied | Explicit changed-infra Ruff/format/mypy selectors recorded in details; baseline debt distinguished. |
| PC-006 | Applied | External exact-head assessment only after passing receipt verification, with base drift stop rule. |

No unresolved significant/divergent decision. No second critique.

## Follow-Up Items

* Owner: exact live renewal/funding/operational review and result verification.
* Coordinator: publication only after required gate/human/hosted approvals.
* Coordinator: reconcile newer main, rerun required current-base gate and
  independent exact-head assessment. This continuation does not silently rebase.
* Infra maintainer: pre-existing targeted lint/format and SQL driver attribute
  type findings, reproduced against a02984e8, outside this boundary-only change.
* Original Review Complete / Residual work: RV-001 High publication/base drift,
  RV-002 Medium owner/live/funding, RV-003 Low pre-existing static debt. No new
  source defect. Preserve outcome; no repeated original Review or source fixes.

## Handoff

P02-T01 executed. P02-T02 remains incomplete: commit evidence locally and record
the unchanged gate's admission result externally; no passing receipt/exact-head
assessment is possible until current-base reconciliation. Changes record:
.copilot-tracking/changes/2026-10-30/resident-authority-extension-521-changes.md.
