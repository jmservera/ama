---
title: Sensor ingestion consistency research
ms.date: 2026-10-30
---

## Research Brief

Investigate #188 for the coordinator: implement a local proof that streamed and
backfill readings share home identifiers, units, timestamps and distribution,
and replay windows are idempotent. Output mode: convergence. Status: Complete.
Resolved evidence root: `.copilot-tracking/`. Research disposition: executed.

## Research Parameters

Focused posture, selected for the explicitly bounded issue. Initial internal
areas: core sensor generators/storage, API ingestion and tests, project guides
and IoT synthesis. External scope: GitHub issue/dependency metadata only.
No Azure, deployment, sign-in, secrets, private data, push or UI changes.
Research writes only research evidence and required lifecycle state.

## Extension Registry and Provenance

Repository instructions and user local-validation/commit constraints selected.
RPI phase skills selected in order. Web skills skipped for backend-only scope.
Research lanes remain inline because the generator/ingestion trace is coupled.

## User Participation and Research Decisions

Caller explicitly requests all four phases in order and local commit without
push; sufficient intake, no interactive clarification required.

## Direction Controls

Use supplied topic branch and main base a31048f15fa3120c58bacd22a375d86ae5ab7431.
Use Refs #188 only. Live Azure acceptance cannot be claimed from local proof.

## Research Questions

* Q1: Which generator, ingestion and SQL contracts already implement the seam?
* Q2: What executable proof covers joint queries, declared tolerances and replay?
* Q3: Which live/dependency criteria remain unprovable under no-Azure authority?

## Prior Knowledge Gate

Read original/addendum, reference index/memory, source gate policy and issue
metadata. #183 and #186 are delivered; #110 remains open with actual transport
and Azure SQL acceptance incomplete. Verify implementation before selecting work.

## Research Cycle Log

### Cycle 1

#### Wider

Inline inventory found shared replay, backfill, SQL consumer and fake-SDK
receiver tests (C1-C4). Reflection: existing legacy two-point equality is not a
statistical handover check and does not cover the composed climate writer.

#### Deeper

Backfill already composes pinned climate, household conditions and dated
retrofit effects from a full origin; replay regenerates only the legacy
seasonal path. SQL admission persists common home/sensor IDs and rejects
conflicting replay. Reflection: extend existing replay rather than invent a
second generator; exercise both producer paths through the existing consumer.

#### Contrarian

Raw adjacent-window means can differ legitimately with weather, daily cycles
or dated works. Compare the observed handover against a continuous
same-input reference, and declare numeric mean/stddev and point tolerances.
Require exact keys, cadence, units and schema, and fail missing/duplicate rows.
Retain explicit no-Azure limit. Reflection: a positive-only two-point equality
test could pass with missing data or a biased suffix; negative controls must
prove detection. No independent lane justified for this coupled trace.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/188, retrieved 2026-10-30:
  three acceptance criteria and Azure SQL/live-stream requirement.
* W2: https://github.com/jmservera/ama/issues/110, retrieved 2026-10-30:
  idempotent append delivered, live criteria incomplete.
* W3: https://github.com/jmservera/ama/issues/183 and
  https://github.com/jmservera/ama/issues/186, retrieved 2026-10-30:
  backfill and versioned schema delivered.
* C1: `src/core/src/zava_forward/core/synthetic/sensor_stream.py:150`:
  replay advances the original seasonal sequence before selecting slots.
* C2: `src/core/src/zava_forward/core/synthetic/sensor_backfill.py:109`:
  composed projection already shares household and dated retrofit effects.
* C3: `src/core/src/zava_forward/core/sensor_consumer.py:101`:
  independent policy and controls bind units, mapping, consent and time.
* C4: `src/api/tests/test_iot_stream.py:319`:
  existing SQLite fake-receiver seam covers two legacy points, not distribution.
* C5: `src/api/tests/test_sensor_ingestion.py:18`:
  inherited SQL consumer suite can run with task-owned SQL Server.

## Alternatives and Decision State

Select additive optional composed replay and a strict per-home/sensor statistical
report against a continuous reference. Keep legacy default bytes unchanged.
Use constructed climate only in tests and SQL Server via the existing isolated
gate. Reject independent restarted suffix generation (different RNG/conditions),
raw mean equality (confounds modelled changes), new public endpoints and Azure
execution (out of scope). Report tolerances as exercise controls, not physical
calibration or approval.

## Findings Mapped to Questions and Evidence

Q1 answered by C1-C3. Q2 answered by C4-C5 and the negative-control design.
Q3 answered by W1-W3: actual Hub routing and Azure SQL acceptance remain unmet.
All findings accepted within the local engineering boundary; live evidence
deferred. No further cycle is needed because remaining gaps require forbidden
external execution, not additional local discovery.

## Planning Readiness

Ready for bounded local implementation. Research Complete; disposition executed.
Self-check: all questions answered, three ordered inline waves complete,
alternatives and evidence boundaries preserved. Actual live Azure proof remains
excluded, not inferred from local substitutes. Parent continuation: Plan.
