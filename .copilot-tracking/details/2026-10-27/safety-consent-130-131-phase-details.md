<!-- markdownlint-disable-file -->
# RPI Phase Details: Safety-consent intake

Task ID: 130-131. Slug: safety-consent-130-131. Date: 2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md.
Research: .copilot-tracking/research/2026-10-27/safety-consent-130-131-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete bounded implementation | P01-T01, P01-T02 |
| P02 | Complete; draft PR #509 | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Independent intake and holds

Context: research C4-C10 establishes the reusable resident operation, SQL
replay validation, projection and hazard boundaries. New actions use _operation,
never a parallel persistence or authority mechanism.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Nomination and correction ledger

Targets: src/core/src/zava_forward/core/resident_decisions.py,
projection.py and existing resident tests.
Add closed nomination_record and nomination_correct actions.
Record exact original account (reject >4000 characters), source and supplied
channel, explicit case binding, named current owner, acknowledgement evidence,
next update and a non-digital route. Identity/support/risk remain Unknown.
Acknowledgement is staff evidence only, not a send operation.
Correction requires current revision, retains original, new account and
evidence/actor/time, flags the nomination for human re-review, and may reference
an existing challenge in this case without changing that challenge's state.
Refuse emergency/hazard input with the independent hazard intake route;
do not classify or change statutory clocks. Do not implement eligibility,
representative task grants or nomination acceptance.
Require both existing evidence entitlements for write and raw read.
Prove rollback, wrong case/identity, explicit unknowns, manual routes,
version history and unrelated-state isolation in both current test backends.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Unverified tenure ledger and affected holds

Targets: same resident module/projection and tests.
tenure_intake is a closed append-only household report with expected_version,
case/household reference, reported tenure, reported lease interest, source,
identity state Unknown/Ambiguous, named data-follow-up owner and next update.
No reported value grants verified route or lease authority.
Expose static questions about home/lease identity, who decides, permission,
Legal-reviewed responsibility, Finance-approved cost and consultation.
All answers remain Unknown until separately authorized implementation.
resident_gate and new scope recording must refuse affected unresolved intake.
No release action is added, so changed scope/disputes cannot silently release
it. Missing all-home/all-household enumeration remains an acceptance gap.
Data-owner appointment is not inferred from the staff-selected follow-up.

Critique corrections PC-001/002/004: preserve reported_subject_ref in every
nomination revision; a correction may replace this unverified reference, never
the containing case or resident identity/authority records. Any tenure report
sets case-wide tenure_review_required, including Unknown/Ambiguous household
identity. No measure/household acceptance narrows or releases that hold.
nomination_records and tenure_reports join RESIDENT_FIELDS for existing
synthetic deletion handling. The non-sensitive boolean hold is separate and
survives authorized evidence deletion. This does not approve any new actual
retention applicability, duration, lawful basis or real-data activation.

<!-- rpi:phase id=P02 -->
## P02: Evidence and handoff

<!-- rpi:task id=P02-T01 -->
### P02-T01: Local regression, documentation and publication

Document callable/API payloads, unverified status and permanent human hold
in component READMEs. No new KB synthesis, legal claim or web interface.
Use temporary constructed fixtures exclusively, include core and API tests
and full API discovery as requested. No tests removed; <=12 methods added.
Record missing dependencies honestly, use a task-owned pip environment if
needed. No full gate or Azure. One independent review after implementation,
findings routed later without changing its original outcome.
Commit implementation and dated RPI artifacts together using account-derived
privacy-safe identity and required trailer; push topic, open one draft PR to
main with Refs #130/#131, a criterion-by-criterion partial/blocked matrix.
Required human approvals remain unchecked. Final report includes PR URL.

PC-003 test allocation: six shared JSON/SQLite methods for original/corrected
subject history, schema/identity rejection, tenure/CAS/hold/reopen, deletion
hold survival, permission/projection and precommit rollback; up to three
SQL-specific methods for writer-time actor/owner/revision change and committed
outcome; up to three API methods for both intake routes, permission/schema/
current-registry denial and non-sensitive projections. Reuse existing generic
postcommit tests; assert no handler side effects outside supplied case/audit.

## Final Completion Evidence

P01/P02 and all three bounded tasks complete. Final core boundary suites:
373 tests OK, 87 skipped. Required API discovery: 1124 tests OK, 314 skipped.
Focused Ruff/format/mypy and diff checks pass. Review executed exactly once,
Complete / Residual work, no material bounded-source defect.
Draft https://github.com/jmservera/ama/pull/509 targets main, source ebb80098,
no closing issue references. Whole-issue and operational acceptance remains
blocked by named human decisions; no second Review or further source edit.
