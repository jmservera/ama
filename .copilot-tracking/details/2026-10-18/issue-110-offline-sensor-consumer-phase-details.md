---
title: Issue 110 offline sensor consumer phase details
description: Task-owned implementation boundaries and completion evidence
ms.date: 2026-10-18
---

Task: issue-110 / issue-110-offline-sensor-consumer. No implementation delegated.

## Later authorized correction ONE

Same-task RV-001/RV-002 implementation only, no new Research/Plan/critique/Review.
Historical accepted witness shape/digest and retained reading semantic consistency
are checked before replay acknowledgement, independently of current authority.
Latest consumer reading must also match its historical witness before new
timestamp ordering. Legacy generator rows retain their witness-free contract.
Timestamp/numeric parse failure or mismatch raises bounded
SENSOR_OUTCOME_MALFORMED so the existing API BatchStopped preserves the earlier
committed prefix. Red/green actual-engine evidence and exact pinned integration
are recorded in the correction ONE receipt, not a replacement Review.

## Single planning refinement after original critique

PC-001: inspect existing SQLite columns/PK and MSSQL column capacities/types/PK.
For supported legacy/stock MSSQL, widen schema_version from 12 to 32 only;
no replacement/truncation/data deletion. Fresh table uses loader-compatible
columns, binary collation and full schema capacity. Uppercase ASCII sensor IDs
<=20, reading IDs <=40 with no whitespace avoid legacy CI/trailing-space key
collisions. Decimal inputs are strings with at most two fractional places,
within DECIMAL(5,2) capacity, not rounded. Unknown schema is unavailable, not
success. Tests install both original SQL_DDL and STOCK_SQL_DDL and retain rows.

PC-002 independent fictional fixture matrix:

| Control | Exercise value and exact interpretation |
| --- | --- |
| Receipt | 2024-10-01T02:00:00Z, trusted adapter argument |
| Observation window | [2024-10-01T00:00:00Z, 2024-10-02T00:00:00Z) |
| Clock | maximum past 7200s and future 0s, inclusive |
| Mapping | SENS-SYN-1 -> ZF-1, same half-open interval as window |
| Calibration | same sensor/context interval; degC/percent; confirmed true |
| Consent | granted for baseline; unknown/declined always reject new admission |
| Ranges | temperature [-10,45], humidity [0,100], inclusive exercise values |
| Ownership | exercise-data-quality-review role, manual-sensor-review route; reviewer Fixture Reviewer or Unassigned |

Observed time governs mapping/calibration/window; supplied receipt governs skew
and must be UTC seconds. Current SQL consent governs new admission at processing.
At start valid, one second before invalid; end invalid, one second before valid
if clock permits. Exact range/skew edges accepted; outside rejected. Controls
never derive from Packet.clean/label or observed calibrated=true.

PC-003/004: construct consumer first, then a second actual writer changes controls
or home under the existing writer lock. Held lock + synchronization events prove
waiting new admission reads the newly committed authority. Inverse order proves
prior committed admission remains historical and exact replay after withdrawal/
window change reconciles its original reference. Changed payload is conflict;
rejected exact retry remains rejected even after repair.

PC-005: preflight only outer list/tuple 1..100 and each bounded dict of <=20
string keys/primitive values, maximum serialized row 4096 bytes. Nonprimitive
or oversized envelope raises before writes. Closed-schema/type errors within
that envelope, even missing identity, write digest-keyed outcome plus DQ (no
invented sensor ID). The digest is dedup identity, never authorization.
Valid-then-invalid and invalid-then-valid produce two receipts. Each row commits
independently. Database/uncertain acknowledgement failure stops immediately,
returns bounded committed-prefix receipts in the raised error, and identifies
the uncertain fingerprint without exposing input. Retrying the whole finite
batch reconciles committed prefix and resumes remaining rows.

PC-006/007: DQ is restricted SQL metadata with outcome reference, status Open,
reason, parseable observed UTC or null, trusted receipt UTC, declared accountable
exercise role/route, and reviewer or Unassigned. Trusted missing route refuses
initialization. Restricted callable inspection returns metadata only. Real engine
triggers fail accepted witness and rejected DQ writes separately; neither
transaction's partial writes survive. After actual COMMIT, injected ack loss on
accepted and rejected paths must reconcile same reference on fresh consumer.

## P01

### P01-T01

Run the new API import/integration check before module creation and preserve its
failure. Implement core SensorConsumer against SqlStore/MssqlStore independent
connection, with explicit initialize/configure constructed controls, not HTTP.
Use existing sensor_reading columns (including nullable injected_fault); preserve
legacy backfill. Add sensor_consumer_control and sensor_delivery restricted SQL
records plus a sensor_data_quality_exception table. No existing DQ SQL route was
found (research C5). No general framework or changes to shared stores.

Install controls transactionally; validate typed dataclasses and persisted JSON
strictly. Existence of mapped case is rechecked per observation inside writer
lock without mutating that case. Half-open effective windows; explicit UTC receipt,
window and allowed skew/ranges in supplied policy. Payload home/calibrated/source
never grants control. No hash is an authorization proof.

### P01-T02

API sensor_ingestion consumes an already materialized finite list/tuple <=100,
not iterator/daemon. Own adapter class composes core with existing store; unsupported
JSON raises an explicit bounded error. No route registration.
Only Packet.rows from bounded sensor_faults.packets participate; tests independently
supply controls, never pass labels/clean/truth as admission authority.
Receipts expose statuses/reason and opaque outcome reference only.

## P02

### P02-T01

Share the exact API test class across SQLite and task-owned disposable SQL Server.
Two separate Store instances/connections race via barriers. SQL writer lock
serializes control recheck, read, append and outcome/DQ. Reopen checks use fresh
consumer instances. Engine triggers force failure after reading insert but before
outcome insert; verify all transaction writes rolled back. A subclass acknowledgement
method raises after actual COMMIT; retry exact input reconciles one retained result.
No proxy connection or process-local duplicate state is acceptance.
Create unique local container/database name, loopback port, random process-only
password; never log environment or connection strings; cleanup in finally.

### P02-T02

Use installed project distributions; install only after import/tool missing.
Run focused tests first, regressions and configured checks next; preserve every
failure and distinguish baseline from introduced failure. Build existing API
Dockerfile using src context. Run nonroot, --read-only, --cap-drop=ALL,
no-new-privileges and tmpfs runtime with public tiny fixture plus task tests.
No network transport exercised; no UI/Playwright. Update core/API guides and
accurate ADR/addendum status, index and append-only log. Preserve Proposed.

## P03

### P03-T01

Before Review reconcile plan checkboxes, details, changes, validation and blockers.
Dispatch exactly one original Review through rpi-review. Assess source and full
phase evidence, include known initial failures and acceptance limits. Preserve
original artifact bytes/hash and adverse findings; no second original Review or
silent correction. Route later work separately.

### P03-T02

Resolve gh authenticated identity and repo-local noreply author/committer.
Conventional commit plus required Copilot trailer. No secret files included.
Normal push, gh pr create main, Refs #110 only. Record exact head and actual
current PR base without claiming origin/main still equals pinned ancestry.
Publish immutable artifact hashes, inventory, phase log, correction count 0.
Stop for complete independent exact-head source/artifact/log review; no merge.
