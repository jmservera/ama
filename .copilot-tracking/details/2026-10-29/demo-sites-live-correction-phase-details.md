---
title: Demo sites live correction phase details
description: Operational execution and rollback contracts
ms.date: 2026-10-29
---

Task 5a7ca259-9fe8-407c-accf-fc965757c10e, demo-sites-live-correction.
Main 77c87e0d76b827544fde9b2f2ce7dfbd9d879232.

## P01-T01

Completed full raw management backups externally under current session files,
0700/0600. No listSecrets. Resident auth-current GET 404 AuthConfigNotFound
is explicit absence; employee auth captured. Eight complete job GETs Manual.

## P01-T02

Extract only the third GO batch from infra/sql/resident-showcase.sql, declaring
optional sensor history and CREATE OR ALTER VIEW, not schema/table/grant batches.
Use existing initializer image/identity/env with execution template override
python -c worker, args cleared, resources unchanged. No job configuration
update needed. Existing init managed identity connects using mssql_python and
existing mssqlstore connection-string helper. Include resident principal verifier
source in the worker, verify SID and rights before/after. Transactional DDL,
verify column shape before commit, counts-only result. Capture prior definition
hash/column names and allowlist counts; do not emit definition or rows.
Exception logs expose exception type only, not SQL bodies or data.
Check execution Succeeded and counts-only console evidence; unchanged complete
job GETs before/after, eight Manual. Do not retry an ambiguous SQL write.

## P02-T01

Export git archive origin/main src only; no .env/untracked upload. Unique tags,
source SHA OCI label. Nonblocking /tmp/ama-rpi-heavy.lock for local Docker build.
Approved previous route: current VM /32 only, public Disabled before adding rule,
enable export then public/default Deny. No Tasks bypass or broad rule. Token
in memory/stdin only, owned Docker config. New/old manifest presence and actual
config SHA vs local docker-save config bytes, not Docker29 index ID. Source label
must match exact main.

Each exception max600s, forward cutoff420s, private-first restoration reserve180s.
Bound every subprocess and HTTP to remaining deadline. Handle SIGINT/SIGTERM
through finally. Restore public Disabled first, original network rules/default/
export policy, then prove complete stable ACR response equality (only systemData,
provisioningState/status excluded). No policy timestamp exclusions.
Credential config cleanup names only; no image deletion. Failure blocks app writes.

## P02-T02

Raw API2025-07-01 PATCH only properties.template, copied from raw backup with
image/revisionSuffix edits. Remove service-only imageType/ephemeralStorage only
if present in writable request; preserve original absence/null/value in env.
Pre-write entire protected app baseline equality, no concurrent drift overwrite.
Resident first, retain ca-resident-demo--rollback-20261029-073718.
Anonymous /healthz cold-start probe allowed, /health separately recorded.
Require latest=ready target, Healthy/Provisioned, expected digest, active100%
and one added full-history revision. Preserve all prior revisions.
If actual resident startup fails, collect az console and system logs BEFORE
rollback; no second forward attempt. Failure-only raw-template recovery to
captured digest, with same preservation checks and explicit non-delivery status.
Then employee only after resident success.

## P03-T01

Main policy cap is December; #521 unmerged. Do not apply January expiry to this
image. Owner must reconcile source integration plus one-revision allowance,
owner-held password/private verifier/signing-key generation, reviewed existing-
secret exact-version Modify operation (Create-only helper is unsuitable), named
approved existing synthetic rows and expiry/alert/rollback window. No mass row
renewal, permission change or operator login. Park if unavailable.

## P03-T02

Reconcile all task statuses and preserve originals. One independent review of
the fresh operational boundary, not a repeat of parent's historical Review.
No implementation after Review. Commit current owner-identified evidence and
new evidence only using existing historical authenticated noreply identity
because gh is prohibited. Both author/committer privacy-safe, exact trailer.
No publication gate receipt or push. Coordinator owns publication/PR.

## Applied Critique Contracts

* PC-001: Existing Manual parallelism1/completion1, timeout600, retry1.
  Require no active initializer execution. Temporarily PATCH only captured
  configuration.replicaRetryLimit to0, Manual unchanged, and restore exact
  original configuration in finally before any app update. Worker explicitly
  BEGIN TRAN with XACT_ABORT ON; rollback on any precommit error. Capture
  permission/SID/allowlist state before/after, verify exact 17-column SELECT
  under EXECUTE AS USER with guaranteed REVERT, then COMMIT. No row output.
  Execution failure remains failure, no reapply or start retry after ambiguity.
  Record worker SHA, one execution ID, attempt/completion, commit status and
  ordered column/count proof. A failed/uncertain restoration blocks deployments.
* PC-002: Employee actual startup failure also requires console/system logs
  before one failure-only raw-template recovery to its captured digest, max600s
  convergence, same protection/history/readiness checks. Do not touch the healthy
  resident. Ambiguous writes are inspected, not retried; tooling-only uncertainty
  is verification-blocked, not automatic rollback. Recovered is not delivery.
* PC-003: Immutable SHA77c87e0d76b827544fde9b2f2ce7dfbd9d879232
  binds SQL batch and both git-archive builds, with source tree/archive hash.
  Assert fetched main equals this reused-validation SHA; stop on later drift.
* PC-004: Separate auth pre/post equality: employee full resource, resident
  exact AuthConfigNotFound. Unexpected errors/drift stop dependent work.
* PC-005: Fresh complete stable ACR equality before every exception; detect
  unexpected intermediate drift. Close public first on drift, do not overwrite
  unrelated changed fields. Block deployment until exact restoration is proven.

## Implementation Reconciliation

P01/P02 complete. SQL execution h6mm4i9 committed17-column view,522 rows
count-only; all eight jobs exactly restored including retry1 and Manual.
Both pinned-main images published with source/config/manifest proof and old
digests retained. ACR exact restoration verified after44.170433s; normalized
bare-IP cleanup correction retained, no app writes before proof.
Resident res-live-20261029-102142 and employee emp-live-20261029-102306 are
Healthy/Provisioned/latest=ready with one forward revision each, none removed.
Full protected app and separate auth equality passed, one ready replica each.
Resident verification resumed read-only after an ambiguous local asset selector;
no repeated deployment or rollback. /health is404 resident/401 employee;
actual /healthz200 both, source-byte-equal public shells, employee assets401.
Authority parked after both healthy with exact owner prerequisites in changes.
No January source/credential/row operation or authenticated smoke performed.
P03-T02 independent Review and local persistence remain. No publication gate
or approval is claimed. Parent local validation artifacts remain unchanged.
