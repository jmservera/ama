---
title: Issue 110 offline sensor consumer plan
description: Finite constructed SQL processing in existing core and API packages
ms.date: 2026-10-18
---

Task ID: issue-110. Slug: issue-110-offline-sensor-consumer.
Base: 578631ac75cc8c6a7af53922c6aaae4435e7761c.

## Executive Summary

Build a narrow restricted SQL sensor processor and a finite callable in the
existing API package, without a public route or transport loop. Reuse
sensor_reading and the existing independent SQL connections/writer lock.
Constructed controls explicitly supply mapping, consent, calibration, window,
ranges and manual DQ route independently of observations. Local actual SQLite,
disposable SQL Server and hardened image evidence are required, not Azure
acceptance. Whole issue 110 and ADR acceptance remain open.

## Sources

Research: .copilot-tracking/research/2026-10-18/issue-110-offline-sensor-consumer-research.md
(C1-C6/W1-W3). Details:
.copilot-tracking/details/2026-10-18/issue-110-offline-sensor-consumer-phase-details.md.

## User Decisions and Requirements

* Full ordered automatic RPI, one original critique and one original Review;
  preserve their bytes, adverse outcomes and all initial validation failures.
* No nested implementation workers; parent implements.
* Stay on supplied pinned branch/base; no rebase, merge, issue closure, AC ticks
  or live external authority. PR uses Refs #110 only.
* Inputs are observations, never evaluator truth; controls are trusted explicit
  constructed fixtures. Synthetic labels and calibrated claims are not authority.
* Real SQL independent-connection concurrency, rollback, restart and postcommit
  reconciliation; no fake connection proxy as acceptance.
* No private data/env, IoT Hub provisioning, live SDK, new service, UI, AI or
  device credentials. Do not modify issue 122 shared-store files.

## Goals

G1: exercise a real finite API -> core -> authoritative SQL processing path.
G2: deterministic visible rejection and idempotence across independent writers.
G3: bounded nonsensitive receipts and durable honest engineering evidence.

## Scope and Non-Goals

Owned core module sensor_consumer.py; API sensor_ingestion.py; focused core/API
tests and task-owned SQL execution helper; narrow guide/ADR/addendum/index/log
updates and all dated RPI artifacts. No shared store edits or new dependencies.
No analysis, SENSOR_REVIEW_DUE, resident communications or property mutations.

## Functional Requirements

* R1: closed sensor-fault-input-v1 primitive schema with exact UTC seconds,
  stable bounded IDs, finite numeric strings, bounded seed/source/scenario,
  units, calibrated claim, and explicit range checks without clamping.
* R2: trusted SQL control per sensor with mapped existing home, half-open
  mapping/calibration intervals, current granted consent and calibration units.
  Read and validate current control inside each writer transaction.
* R3: append sensor_reading once per sensor_id/reading_id. Canonical fingerprint
  detects exact replay vs conflicting identity; legacy existing rows without
  a consumer witness produce explicit identity conflict, not guessed success.
* R4: out-of-order/equal timestamps cannot advance latest; visible DQ with
  separate observed/received times retained in restricted SQL.
* R5: atomic outcome ledger and DQ metadata. Identical accepted replay produces
  no second reading, success witness or exception; rejected identical replay
  reconciles existing DQ. Unknown reviewer is Unassigned, manual route required.
* R6: callable finite batch (1..100) preflighted before writes; only SQL stores.
  JSON explicitly Unsupported. SQL unavailable/malformed/uninitialized is an
  explicit unavailable result/error, not an empty successful batch.
* R7: commit acknowledgement uncertainty exposes reconciliation metadata only;
  next exact replay recovers recorded outcome without duplicate admission.

## Non-Functional Requirements

* N1: raw observations and keys restricted to SQL; no payload/device IDs in
  receipts, diagnostics, exceptions, ordinary UI, AI or map.
* N2: SQLite and SQL Server parity with database locks/primary keys, not process
  sets. Each operation owns/closes an independent connection.
* N3: no silent database recovery, broad success fallbacks or guessed policies.
* N4: preserve existing replay loader and privacy/regression boundaries.

## Acceptance Criteria

A1: fail-before/pass-after check proves missing API adapter, then actual runtime
batch integrates with SQL and persists across reopen.
A2: schema, boolean/missing/extra/nonfinite/range/time/id faults; unknown sensor,
home mismatch, mapping boundaries, units, independently controlled calibration,
consent unknown/declined, clock/window boundaries all visible, owned DQ.
A3: exact replay, conflicting reuse, out-of-order, independent concurrent writers
(same key and different time order), rollback on database failure, postcommit
ack reconciliation on actual SQLite and task-owned SQL Server.
A4: no raw/device identifiers in receipts/error messages; no case/audit/task/
ranking/consent changes; JSON unsupported; SQL empty vs failed distinguished.
A5: existing sensor/privacy and core/API regressions, configured Ruff/mypy/
formatter; actual nonroot read-only image focused suite and finite adapter run.

## Phase Checklist

<!-- P01 -->
### P01: Consumer and API boundary

* [x] P01-T01: failing-first API test and core SQL implementation/control schema.
* [x] P01-T02: finite API callable and full semantic/privacy tests.

<!-- P02 -->
### P02: Actual runtime and documentation

* [x] P02-T01: SQLite/MSSQL independent writer, reopen/rollback/ack checks.
* [x] P02-T02: regressions/static checks/hardened image and narrow docs.

Available scoped validation passed; full API mypy remains limited by nine
baseline missing Playwright imports. This is not a green whole-project type
claim; no UI/browser execution is authorized. See changes for exact commands,
initial failures, final counts and the baseline comparison.

<!-- P03 -->
### P03: Original Review and publication

* [x] P03-T01: reconcile artifacts, run one independent original Review, retain
  its outcome unchanged; route findings, correction count 0.

Original Review execution Complete, outcome Defects found. RV-001 Medium and
RV-002 Low remain open for later authorized work; RV-003 Low is baseline tooling
residual. This checkbox records execution, not conformance or repaired findings.
Original Review and critique remain unchanged; no source correction or repeat.
* [x] P03-T02: commit owned evidence/source, push, open main PR at pinned base
  lineage; clean only task-owned resources; stop for exact-head review.

Publication: PR 411, pinned source ancestry preserved; actual main PR base
9d625a09e34491ecf9fd27ffc7d59e67c2373b29. Automatic session stopped on explicit
owner direction for complete independent exact-published-head source/artifact/log
review. No merge or issue-state/AC changes. RV-001/RV-002 remain unresolved;
RV-003 remains separate tooling residual. Correction count 0.

## Locked Test Ownership and Evidence

Parent owns src/core/tests/test_sensor_consumer.py and
src/api/tests/test_sensor_ingestion.py. Maximum additions: these two test files,
one shared constructed fixture module and one task-owned SQL runner.
Removals: none. No generated production targets. Semantic tests directly assert
reason/status/SQL counts; existing tests are regression evidence. SQL fake/proxy
tests cannot satisfy A3. A real engine failure (trigger/connection state) supplies
rollback evidence. Postcommit acknowledgement seam may raise after actual COMMIT,
but never substitutes a fake connection. Logs contain commands/counts not secrets.

## Critique Disposition

Original critique executed once: Revise (3 High, 4 Medium). Original bytes retained
at .copilot-tracking/reviews/plans/2026-10-18/issue-110-offline-sensor-consumer-plan-critique.md.
All seven are compatible direct corrections, applied in one planning refinement;
no significant/divergent owner decision and no repeat critique.

| Finding | Owner | Direct disposition and resolving contract |
| --- | --- | --- |
| PC-001 | Parent | Widen only legacy MSSQL schema_version to VARCHAR(32); preserve table/rows/PK. Support fresh/legacy/stock shapes; refuse incompatible state. Canonical uppercase ASCII IDs <=20/40, no spaces; decimal numeric strings <=2 places in DECIMAL(5,2) capacity. Actual legacy/stock tests retain rows and loader compatibility. |
| PC-002 | Parent | Concrete independent fixture matrix and inclusive/half-open boundaries added to details. |
| PC-003 | Parent | Actual two-connection authority mutation/lock ordering cases added for consent, mapping, calibration and home existence. |
| PC-004 | Parent | Exact delivery fingerprint lookup first reconciles historical outcome irrespective of later control/window; new fingerprint then checks accepted stable identity conflict, then current authority. A rejected exact retry remains historical after repair. |
| PC-005 | Parent | Envelope shape/size/primitive checks happen before writes. Primitive closed-schema errors, including missing IDs, receive digest-keyed DQ, never invented device identity. Per-row transactions commit a prefix; store/ack failure stops batch and raises bounded error with committed-prefix receipts and uncertain outcome reference. |
| PC-006 | Parent | SQL DQ includes reference/reason/status/observed/received/accountable exercise role/manual route/reviewer or Unassigned. Restricted in-process inspection only, no public route. |
| PC-007 | Parent | Real engine trigger rejection rollback and rejected postcommit acknowledgement/reopen tests added alongside accepted equivalents. |

## Follow-Up Items

Live IoT Hub identities/transport and infrastructure owner decisions; Azure SQL
and registered real AI acceptance; analysis issue 111. Not prerequisites for this
offline slice. Independent exact published-head review remains a separate gate.

## Handoff

Planning Ready after direct dispositions. Changes record:
.copilot-tracking/changes/2026-10-18/issue-110-offline-sensor-consumer-changes.md.
