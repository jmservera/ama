---
title: Sensor ingestion consistency plan
ms.date: 2026-10-30
---

## Task Metadata

Task ID: 188. Slug: sensor-ingestion-consistency-188. Implementation ready.
Details: .copilot-tracking/details/2026-10-30/sensor-ingestion-consistency-188-phase-details.md.

## Executive Summary

Extend the existing bounded replay to the composed backfill model and add a
strict statistical handover report. Prove common per-home queries and durable
window replay through existing SQL admission with constructed local inputs.
No new transport, endpoint, deployment or UI is required. Actual live Hub to
Azure SQL proof remains blocked by the explicit no-Azure boundary and #110.

## User Decisions and Requirements

* Execute Research, Plan, Implement, Review; preserve dated original evidence.
* Implement #188 exactly on supplied branch/base; source in src, tests outside packages.
* Validate API unittest discovery, Ruff check/format and mypy; heavy gates locked.
* No Azure, deploy, live sign-in, secrets or credential files. No push.
* Local commit with privacy-safe identity and required Copilot trailer; Refs #188 only.

## Goals

* Eliminate the composed-model replay gap and make seam evidence reproducible.

## Scope and Non-Goals

In scope: optional composed replay, strict continuity metrics, local SQL/receiver
regressions, owning guides and knowledge-base evidence boundaries.
Excluded: UI, new public APIs, real devices, production calibration, cloud execution.

## Functional Requirements

* Replay the same full-origin climate/household/dated-works model before slicing;
  preserve default legacy replay behavior.
* Report per-home/sensor count, handover mean and population-standard-deviation
  comparisons against a continuous reference. Require exact identity, UTC cadence,
  units and schema. Reject malformed, duplicate or incomplete coverage explicitly.
* Declared finite nonnegative tolerances apply to numeric point error and
  distribution change; reference-adjustment avoids treating weather/works as a seam.
* Prefix backfill plus receiver suffix queries return the continuous series and
  repeated windows retain exact counts and values after reopening SQL.

## Non-Functional Requirements

* Existing replay scale/rate limits and synthetic-only consent fences unchanged.
* No silent fallback, schema migration or new dependencies.
* Deterministic exercise tolerances: default zero C and zero percentage points;
  these are model-parity controls, not physical sensor accuracy.

## Acceptance Criteria

* AC1: local SQL joint queries per canonical home prove prefix/suffix coverage;
  actual live Azure SQL criterion remains not proven.
* AC2: local statistical report passes declared zero tolerance for clean
  handover and fails drift/missing/duplicate/unit/time/identifier negative controls;
  actual live handover remains not proven.
* AC3: replaying a complete admitted window after reopening leaves rows,
  deliveries and DQ unchanged; actual live restart remains not proven.

## Sources

Research: .copilot-tracking/research/2026-10-30/sensor-ingestion-consistency-188-research.md,
C1-C5 and W1-W3.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Shared model and continuity contract

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Extend replay and implement statistical report

Optional climate and dated measures reuse existing backfill functions. Add
strict typed report in core synthetic package; provenance identifies composed
versions, climate and dated history.

<!-- rpi:phase id=P02 -->
### [x] P02: Evidence and validation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Prove SQL handover, negative controls and replay

Test ownership: core tests own report/model semantics; API tests own admission,
fake receiver and actual task-owned SQL Server. Remove none. Add at most two
test files and ten test methods; extend existing stream tests as needed.
Canonical targets are source modules and tests, no generated fixture payloads.
Regression coverage preserves legacy replay, semantic coverage exercises drift,
coverage/metadata failures and post-restart idempotency.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Document, validate and prepare original Review

Focused tests and requested API/static/owned-SQL commands passed under
`flock -w 600 /tmp/ama-rpi-heavy.lock`; implementation evidence is ready for one
independent post-implementation Review. Lifecycle continuation after implementation:
commit candidate/original Review, then run complete local RPI gate externally.
Do not overwrite adverse evidence or claim hosted/human approval.

## Dependencies

#183/#186 delivered; #110 live integration incomplete. Local Docker available.
Missing runtime/static packages observed; isolated pip venv installed.

## Critique Disposition

One critique executed, original verdict Revise preserved.

| Finding | Disposition | Resolution |
| --- | --- | --- |
| PC-001 | Applied | Extend existing task-owned sensor_sql_check.py invocation to the new API selector. Ordinary full gate does not imply sensor-specific SQL coverage. |
| PC-002 | Rejected conflicting recommendation | Worker cites an unavailable temporary-path prohibition not applicable to this parent. Caller explicitly requires the shared /tmp lock with -w 600 and external evidence; obey caller. Inspect actual holder first; do not interrupt foreign work or nest the runner lock. |
| PC-003 | Applied | Independent point/mean-step/stddev limits, inclusive boundaries and invalid/nonfinite tolerance subtests added to details. |

## Follow-Up Items

* Coordinator/owner: actual live Hub/Azure SQL exercise after #110 prerequisites,
  authority and budget evidence. This task does not authorize it.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-30/sensor-ingestion-consistency-188-changes.md.
Implementation markers complete. Proceed to one independent original Review,
then local commit and external exact-candidate gate. No push or live authority.
