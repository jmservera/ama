<!-- markdownlint-disable-file -->
# RPI Plan: Safety-consent intake

## Task Metadata

* Task ID: 130-131
* Task slug: safety-consent-130-131
* Date: 2026-10-27
* Status: Ready for bounded implementation; original critique Revise preserved
* Details: .copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/safety-consent-130-131-plan-critique.md

## Executive Summary

Implement independent staff-recorded nomination/correction and unverified
household tenure intake in the existing transactional resident ledger.
Keep original accounts, named acknowledgement owners, manual channels and
revision history. Registered unresolved tenure blocks affected work; no
screen or agent gains lease, consent, safety or cost authority.
Publish one draft PR with Refs #130 and Refs #131, not whole-issue closure.

### What You May Not Know

The existing generic RAI challenge is already implemented, but does not close
nomination-specific FR-037. Current staff roles contain no Legal reviewer.
No independent implementation can appoint that owner or validate real
representatives. The user expressly directs independent work and a stop on
these human decisions, so full issue acceptance remains blocked.

## Sources

Research: .copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md,
C1-C11. Named issues and linked BRD/PRD/journey/ADR sections were read.

## User Decisions and Requirements

* Deliver #130/#131 together on the supplied topic branch, full ordered RPI.
* Preserve human resident, Legal, professional, safety and financial authority.
* Implement independent work; record missing owner decisions and stop.
* Use src packages, existing API/SQL/ledger and local tests only.
* No --all; at most one locked --changed gate for large changes.
* Commit dated evidence, push non-main without force and open one draft PR.
* Use Refs unless every issue criterion is proven; never tick unproven criteria.

## Goals

* Persist exact original accounts and explicit unknowns without automatic ranking.
* Give staff safe manual intake with named owner and correction history.
* Capture unverified tenure without fabricating a Legal-reviewed position.

## Scope and Non-Goals

Included: resident_action intake actions, existing case persistence, projection,
focused core/API tests and component documentation.
Excluded pending human decisions: verified eligibility/identity policy,
operational representative authority, Legal position recording, interpreted
responsibility, approved cost, live communication and operational offer release.
No web edits or new AI feature; existing generic challenge remains separate.

## Functional Requirements

* Closed input schemas, bounded text rejecting truncation, explicit case binding.
* Nomination source/kind/channel/original account, named owner,
  staff-recorded acknowledgement evidence, next-update and manual route retained.
* Corrections append competing accounts and stale only that nomination's review;
  optionally link an existing same-case generic challenge without resolving it.
* Hazard-marked input fails explicitly to the independent hazard intake before
  any nomination write; no hazard clock/classification is guessed.
* Tenure intake records each supplied household's reported tenure/lease interest
  and evidence, but verification and decision route remain Unknown.
  Ambiguous identity holds reuse and names data-owner follow-up.
* Revisions preserve prior records; no package completion closes these holds.
* A static responsibility-question checklist identifies missing reviewed
  evidence; no unsupported reviewed-record question pack or approval claimed.

## Non-Functional Requirements

* Existing transaction, registered-identity revalidation, CAS and audit apply.
* Private intake evidence requires both resident-workflow and recorded-reason
  rights; contractors and unrelated staff receive no raw intake details.
* Synthetic tests use temporary data, no existing datasets or cloud.
* Existing workflow names and legacy behavior without new intake remain intact;
  whole-programme tenure gate coverage is explicitly not established.

## Acceptance Criteria

These are bounded implementation criteria, not substitutes for issue criteria.

* [x] Original account/source/channel survive correction and SQL reopen.
* [x] Wrong case, forged staff, restricted role, unknown fields, overlong text
  and stale revision fail without state or audit mutation.
* [x] Manual channels, named acknowledgement and correction provenance persist.
* [x] Tenure remains Unknown and affected gates hold; no API payload can approve
  tenure, legal responsibility, consent or cost.
* [x] Unrelated decisions, ranking, support status and hazard history unchanged.
* [ ] Exact human blockers and issue-criterion evidence appear in the draft PR.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Independent intake and holds

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Nomination and correction ledger

Reuse resident_decisions transaction and API dispatch, no new auth/service.
Details: P01-T01 in phase details.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Unverified tenure ledger and affected holds

Persist reported status, all revisions and unresolved data/Legal handoff.
Details: P01-T02 in phase details.

<!-- rpi:phase id=P02 -->
### [ ] P02: Evidence and handoff

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Local regression, documentation and publication

Run focused core/API tests then the required API discovery. Run existing core
lint/type commands for touched targets where available. Record exact outcomes,
one independent Review, blocker matrix and draft PR.

## Test Ownership and Validation Contract

Canonical behavior: core tests/test_resident_decisions.py, existing JSON and
SQLite subclasses. API boundary: api tests/test_resident_api.py.
Removals: none. Maximum additions: 12 focused test methods, no generated tests
or new runner. Semantic checks assert histories/holds, not status codes only;
regressions retain current challenge/consent/hazard checks. No browser check
is represented as run: no web changes and participation gate remains unmet.
This bounded slice is not large; no heavy --changed invocation planned.
Missing packages may be installed with pip in a task-owned local venv.

## Dependencies

P01-T02 shares the transactional/projection foundation with P01-T01.
P02-T01 depends on both. Actual Legal and OD-41/42 approvals block only
operational extensions and whole-issue acceptance, not independent intake.

## Critique Disposition

Exactly one independent critique executed, original verdict Revise. All four
planner-owned corrections applied; no repeat critique or human policy invented.

| Finding | Disposition | Resolving contract |
| --- | --- | --- |
| PC-001 | Applied | Any registered unresolved tenure holds the entire containing case, including unknown/ambiguous households; no narrower inference or release. |
| PC-002 | Applied | Reported subject reference is append-only correctable; identity remains Unknown, cross-case transfer refused, no representative authority granted. |
| PC-003 | Applied | <=12 methods allocate JSON/SQLite histories, rollback/CAS, SQL commit-time actor/owner changes and API current-role/projection denial; no side effects in replay handlers. |
| PC-004 | Applied | Sensitive intake is in existing resident deletion set; a separate non-sensitive tenure_review_required marker survives deletion. Real-data retention applicability remains a human gate. |

Audit messages contain only action/record identifiers, never accounts or lease
sources. Explicitly remove intake fields after resident-data restoration for
roles lacking either evidence entitlement. Fixed-field export/prompt paths
must be checked by canary tests or exact allow-list evidence.

## Follow-Up Items

* Owner/Resident Engagement/DPO/Legal: resolve OD-41/42, appointment and
  operational authority evidence before enabling nomination decisions.
* Legal/Home Ownership/Finance: appoint responsible reviewer, validate tenure
  identity and approve responsibility/cost evidence and release policy.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-27/safety-consent-130-131-changes.md.
Ready only for independent intake after critique disposition. Do not silently
convert these bounded criteria into issue closure.
