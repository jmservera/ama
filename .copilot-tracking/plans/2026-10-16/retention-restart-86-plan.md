---
title: Resident retention restart plan
ms.date: 2026-10-16
---

## Task Metadata

* Task ID: issue-86-retention-restart
* Task slug: retention-restart-86
* Planning status: Ready after one critique and direct dispositions
* Phase details: .copilot-tracking/details/2026-10-16/retention-restart-86-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-16/retention-restart-86-plan-critique.md

## Executive Summary

Restart the five-calendar-year resident retention period only when actual contact
is recorded after manager-approved deletion. Preserve unrelated contact records
without letting their old timestamps pin the new period.
Implementation and local validation are complete. One implementation Review was
Conformant and PR 338 is published to main. No product decision remains unresolved.

### What You May Not Know

The existing deletion date alone cannot order contacts on the same day. A
personal-data-free count tombstone preserves the boundary without copying any
resident content. Existing date-only tombstones need conservative handling.
This is current-payload retention, not historical erasure or operational approval.

## User Decisions and Requirements

* Implement the latest owner decision in issue #86, read before any other command.
* Replace the pinning test with returning-resident, repeat-expiry/renewal and
  personal-data-free tombstone tests; prove failure without the implementation.
* Build only in src, tests outside packages; no private data or excluded files.
* Use local pip-venv unit suites, Ruff and mypy; no uv, Docker or Azure operations.
* Update core README, reference index and append-only reference log.
* Produce RPI artifacts, commit with owner noreply identity and Copilot trailer,
  push without force and open a PR whose only issue linkage is Refs #86.

## Goals

* Allow a returning resident's new scoped decisions without reviving deleted consent.

## Scope and Non-Goals

* Scope: core retention helper/deletion, inherited JSON/SQLite tests, README,
  knowledge-base routing/log and RPI evidence.
* Non-goals: SQL/schema changes, deployment, real resident acceptance, historical
  erasure, complaint integration or unrelated issue #86 acceptance criteria.

## Functional Requirements

* Deletion leaves retention Unknown until later actual contact establishes a new
  five-year period; decisions/scopes alone cannot establish the start.
* Both general contact and safe-contact routes establish the first new origin,
  including same-day contact. Subsequent contact does not extend that period.
* Old dates cannot re-enter the new period; each later approved deletion repeats
  the boundary. Existing date-only deletion records exclude old contacts.
* Tombstones contain only deletion-boundary metadata, never personal content.
* Preserve legal hold, anniversary/leap-day handling and permission/readiness gates.

## Non-Functional Requirements

* No new SQL or dependencies. Use installed packages in an isolated pip venv.
* Persist/reopen behavior in JSON and SQLite; do not claim live SQL Server evidence.

## Acceptance Criteria

* New tests pass for both stores and fail against the original implementation.
* Core unit suite plus resident API tests pass; core Ruff and mypy pass.
* No old personal data appears in tombstone metadata; audit chain stays valid.
* README limit removed and replaced by the owner-approved reset contract.
* PR published with references-only issue linkage; merge left to owner.

## Sources

* .copilot-tracking/research/2026-10-16/retention-restart-86-research.md:
  reused evidence, Ready; no further research needed.
* src/core/src/zava_forward/core/resident_decisions.py and store.py:
  shared contact helper and append-only contact paths.
* src/core/tests/test_resident_decisions.py: canonical inherited test ownership.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and validate the restart

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Reset the contact evidence boundary

* Update only the shared core helper and deletion method.
* Details: P01-T01 in the phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Replace pinning coverage and validate

* Remove exactly test_expired_retention_stays_blocked_after_deletion_pending_owner_rule.
* Add at most five methods in JsonResidentDecisions, inherited by SQLite.
* Adjust existing deletion assertions and opt-in Azure assertions to match cleared
  origin; no new Azure test or generated test targets.
* Semantic coverage: unknown until contact, both contact routes, same-day boundary,
  fixed origin until deletion, repeated expiry/deletion, legacy tombstone.
* Regression coverage: retained contacts, deleted payload, audit, gates and
  personal-data-free tombstone. Mutation against the original implementation.
* Run full core suite and targeted resident API suite, Ruff/mypy in core.
* Independently test general-only and safe-contact-only recovery, including
  an old general contact with the same timestamp as the new same-day contact.
  Assert Unknown/no automatic consent, then fresh scoped acceptance and reopen.
* Test legacy negative filtering followed by positive later-day recovery.
* Mutation runs the complete original module from HEAD in a fresh Python
  process before importing Store/tests, including the store-bound helper alias.
  Require assertion failures in new semantic tests, not import/setup failures;
  follow with green unmodified installed-code execution.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Document and prepare publication

* Update core README, reference routing and append log; record changes/review.
* Documentation and implementation evidence complete. Commit/push and
  references-only PR to main are a post-Review publication handoff.

## Dependencies

* P01-T02 depends on P01-T01 for green validation; tests can be authored first.
* Publication handoff depends on completed validation and one Review.

## Critique Disposition

* Execution: complete, verdict Revise; no repeat critique.
* PC-001 resolved directly: independent route/reopen/acceptance and legacy
  positive recovery assertions added to P01-T02 and corresponding details.
* PC-002 resolved directly: full original module baseline loaded before Store
  imports in a fresh process; assert semantic failures, then rerun green.
* PC-003 rejected as unsupported: no prohibition on /tmp or /var/tmp exists in
  caller constraints. The established tests use self-cleaning synthetic
  TemporaryDirectory stores; venv is isolated in the session workspace.
  No canonical test or environment policy change is needed.

## Follow-Up Items

* Existing issue #86 operational/human acceptance and historical erasure remain
  outside this narrow owner-directed rule correction.

## Handoff

Implementation context: this plan, matching phase details, one critique and the
research artifact above. Changes record:
.copilot-tracking/changes/2026-10-16/retention-restart-86-changes.md.
Continue under explicit rpi-quick orchestration when critique is disposed.
Local implementation is review-ready: 482 core tests (one opt-in Azure skip),
3 resident API tests, core Ruff check/format and mypy passed. Complete original
module mutation caused assertion failures in all 10 new JSON/SQLite cases;
restored installed code passed all 40 resident tests (one opt-in skip).
One Review completed with no findings; implementation commit 2cc3e3d normally
pushed and PR 338 opened to main with Refs #86 only. Hosted checks and merge
remain the owner's next action, not local acceptance evidence.
