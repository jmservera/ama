---
title: Tenant Staff Initialization Details
description: App-scoped role and roster write boundaries
ms.date: 2026-10-12
---

## P01-T01

Initializer accepts a private operator JSON roster keyed by stable staff code
and directory user id. Resolve current users, enabled app roles and app
assignments from the isolated administrative profile; validate tenant against
deployed API. Read group membership to detect inherited conflicting roles.
Use live role map, not hardcoded legacy role ids. Validate all before mutation.
Read-only check reports missing roles/bindings; apply adds missing roles only.
No deletions, new Graph consent, directory roles or group writes.

SQL uses the existing MssqlStore connection adapter/shared exclusive write lock.
Preserve ten existing codes, main-admin oid and supplier scope; one explicit
Contractor addition. Validate distinct identities/emails and all current codes.
Replace current staff name/email/oid only; preserve other profile fields.
Rename current case owner labels by owner_code, increment rowversion/seq,
preserve all other body fields and indices. Append one hash-chained generic
initialization entry, never edit old audit/approvals/recommendations.
Rollback SQL on failure. Retry reads Graph and SQL again; no duplicate grants
or further SQL mutations on a fully matching roster.
Private roster mode 0600; parent directory 0700. No actual identities in source.

## P01-T02

Minimum distinct accounts: ten existing positions plus one Contractor.
Preserve existing manager and Coordinator. Select other enabled people using
live department/job/group hints; exclude rooms, desks and workspaces.
Use one current synthetic supplier as the explicit contractor scope.
Keep complete directory listing and selected roster privately for owner review.
Apply app roles then SQL; failed SQL leaves access fail-closed and is retryable.
Restart all ready API replicas only after successful SQL commit; keep image,
secret, role-map, SQL/AI, evidence and token-store settings unchanged.
Read-only check verifies live identity and effective role coverage, row/owner
counts and unchanged prior ledger. Signed-in browser acceptance is not fabricated.

## P01-T03

Document separate enterprise-app role and SQL staff binding, private roster,
least-privilege management prerequisites, read-only check/apply/restart steps,
retry and historical-data boundaries. Update existing routing/log.
Publish on continuing branch/#65 with privacy-safe author/committer.

## Critique Reconciliation and Validation Protocol

PC-001: merge DEFAULT_ROLE_MAP with deployed ZF_ROLE_MAP exactly as runtime.
Read every app-assignment page and each user's direct-group page; stop on
unreadable or non-Graph continuations. Evaluate this resource's direct/group
assignments as a set of mapped internal roles. Ignore but preserve Default
Access. Reject conflicts; no grant when group already supplies matching role.
After additions, bounded re-read must confirm exactly the intended internal
role before SQL. No role-removal or group mutation. Entra enterprise-app
assignments do not cascade to nested groups; a transitive-only grant must not
be treated as satisfying the person's intended app role.

PC-002: MssqlStore._Conn rewrites BEGIN IMMEDIATE to BEGIN TRAN plus exclusive
sp_getapplock on zavaforward_write, transaction-owned. Use it through commit or
rollback, not Python-only locking. Fresh staff/case/seq/audit reads under lock.
Validate old bound identities remain; delete/reinsert only the validated roster
keys within the transaction to permit email-key swaps safely. Case UPDATE uses
expected rowversion and checks one affected row. Exactly one sequence advance
and audit append on changes; no-op changes neither.

PC-003: apply restarts even after SQL no-op, covering all active revisions with
nonzero traffic, and waits for new ready replicas rather than merely old
revision readiness. Restart failure returns incomplete; next apply safely
retries convergence without another grant/audit mutation. Check never restarts.

PC-004: retain private before/after snapshots of case ids/body/owner_code,
versions, staff, recommendations, full audit prefix/head and sequence.
Only staff identity fields/new scoped Contractor, current owner label,
changed-case version/sequence and one new generic audit entry may differ.
Workload membership, supplier scope, all other case fields and historical
actors/approvals/recommendations remain byte-equivalent. No-op repeat stable.
Twelve test methods cover input validation/private-file permissions,
runtime map overlay, same-role group/direct duplicates and Default Access,
conflicts, missing roles/add-only idempotency, incomplete reads, SQL label-only
change/preservation, collision handling, protected identities, rollback,
no-op stability and restart-failure/no-op retry.
