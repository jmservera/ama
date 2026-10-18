---
title: Issue 110 offline sensor consumer research
description: Focused constructed-only persistence and finite API boundary investigation
ms.date: 2026-10-18
---

## Brief and controls

Purpose: implement a meaningful finite offline subset of issue 110, not live
IoT Hub delivery or whole AC-066 acceptance. Audience: engineering reviewers.
Stable task: issue-110 / issue-110-offline-sensor-consumer.
Output mode: convergence. Posture: focused, explicitly bounded by the owner.
No live systems, private data, new daemon, public route, SDK, AI, provisioning,
credentials or operational policy authority. Only bounded constructed observations
and separately supplied exercise controls. Preserve exact-replay generator loader.

## Extensions and participation

Repository instructions, original case, index and owner memory inspected.
RPI research selected; backend-only work exempts frontend skills.
Specialist delegation skipped: this is one continuous persistence trace.
No interaction needed: owner explicitly supplied authority, boundaries and gates.
Only original critique and original Review will be delegated, not implementation.

## Cycle 1: Wider

Live issues retrieved 2026-10-18 with `gh issue view`.

* W1: https://github.com/jmservera/ama/issues/110 requires distinct simulated
  identities, stable IDs, SQL append idempotence and visible owned DQ outcomes.
  Still open; live product and infrastructure decisions remain unresolved.
* W2: https://github.com/jmservera/ama/issues/140 depends on 110, 137 and ADR
  approval. Its module-not-present description is stale, not implementation
  authority. It does not block this offline slice and no reverse dependency is added.
* W3: https://github.com/jmservera/ama/issues/109 is the parent; 111 depends on
  ingestion, not a prerequisite. Analysis and review tasks are out of scope.

Initial evidence: backfill loader and fault observation generator exist; no
consumer surfaced by the initial sensor-file inventory. Deeper trace pending.

## Cycle 1: Deeper

* C1: `src/core/src/zava_forward/core/synthetic/sensor_backfill.py:325`
  validates a limited row shape; `:358` admits only exact current-generator
  snapshots and explicitly refuses fault observations. Its `sensor_reading`
  schema and composite primary key are existing persistence prior art.
* C2: `src/core/src/zava_forward/core/synthetic/sensor_faults.py:22` exposes
  a closed observation schema with units/calibration claims; `:113` separates
  evaluator truth from delivered rows. Only Packet.rows may enter processing.
* C3: `src/core/src/zava_forward/core/sqlstore.py:226` already supplies owned
  independent connections; `:191` uses WAL and busy timeout. `mssqlstore.py:58`
  serializes writers with a transaction-owned application lock, and `:204`
  provides independent SQL Server connections. No shared-store edit is needed.
* C4: `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:62`
  requires the existing API consumer, sensor_reading authority and owned DQ;
  `docs/prds/zava-forward-retrofit-programme-demonstrator.md` FR-050/AC-066
  explicitly retains live IoT Hub, Azure SQL restart and real AI acceptance gates.
* C5: No existing sensor DQ persistence/route appears in core source search.
  General property exceptions belong to case workflows and are not a sensor
  delivery ledger. Create a narrow restricted SQL DQ table, not a case task.
* C6: `src/api/Dockerfile:1` requires src build context, nonroot UID 10001.
  Existing `src/api/tests/test_mssqlstore.py:1` requires a disposable SQL server;
  its fake recorder is portability evidence, not concurrency acceptance.

Reflection: a distinct core sensor_consumer module and API sensor_ingestion
callable fit better than expanding a synthetic file whose intentional replay-only
contract must remain intact. Explicit trusted constructed control installation
is separate from observations; no payload field can install authority.

## Cycle 1: Contrarian

Rejected alternatives: reusing load_into would weaken its provenance boundary;
putting DQ into cases would mutate unrelated workflows; process-local duplicate
sets would fail independent writers/restart; JSON persistence would falsely
claim SQL durability. Existing loader rows may lack consumer receipts, so
same-key legacy rows must fail visibly rather than invent receipt/provenance.
No transport adapter may imply authenticated hub identity.

DDL must reuse sensor_reading, preserving its loader columns and support both
existing generator-created SQL and fresh stores. A separate admission ledger
retains canonical observation fingerprint, bounded status/reason/receipt metadata.
Accepted duplicate retries create neither a second reading nor DQ. Out-of-order
observations are rejected visibly, not promoted to latest or analyzed.
Independent SQL connections re-read current controls and home existence inside
the existing database writer lock. No new framework or shared sqlstore hook.

Reflection: no material gap requires new operational policy. Explicit exercise
windows/ranges/calibration/consent/reviewer fixtures supply the finite test
contract. Unknown owner is Unassigned with manual route, not a staff assignment.
Local MSSQL container evidence is distinct from Azure acceptance.

## Decisions, readiness and disposition

Research disposition: executed. Planning Readiness: Ready.
Select the narrow SQL consumer plus existing-API callable composition.
One focused cycle completed wider -> deeper -> contrarian. No re-entry needed:
in-scope source and contracts cover the design; live decisions remain deferred.
Questions answered: placement C1/C3/C4; observation authority C2/C4; SQL/DQ reuse
C1/C3/C5; actual validation C6. No worker participated in research.
Self-check: sources, alternatives, boundaries, readiness and disposition recorded.
Original case and memory remain unchanged. ADR remains Proposed.
