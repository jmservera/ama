---
title: ADR 0003 Journey-Derived Capabilities and IoT Hub Sensor Ingestion
description: Owner-accepted decisions with an exercise Basic IoT Hub amendment, retaining proposal history and separate live implementation gates
author: AMA programme
ms.date: 2026-10-27
ms.topic: reference
---

## Status

Accepted with amendment by the AMA project owner on 2026-10-15, reconciled on
2026-10-18 against the
[owner decision on issue 129](https://github.com/jmservera/ama/issues/129#issuecomment-6194409951)
(comment created 2026-10-15T14:24:33Z). Basic IoT Hub is sufficient for the exercise;
cloud-to-device messages, device twins and device management are excluded for
now. This records the existing owner decision, not a new approval or evidence
of deployment, cost/network/provisioning/credential authority, DPO/legal review,
real AI, Azure application acceptance or completion of issue 110.

### Proposal history (2026-10-14, superseded status)

The following paragraph preserves the original proposal status and narrower
product-choice evidence. It is historical, not the current owner disposition.

Proposed. This ADR records a proposal by the AMA programme. It does not record
approval by the owner, the DPO, Legal, the Board, control owners or any
customer role. It applies the runtime of [ADR 0001](./0001-azure-architecture.md) and
[ADR 0002](./0002-pilot-readiness-architecture.md) to the requirements added by
[BRD v0.17.0](../brds/agentic-retrofit-programme-brd.md) and
[PRD v0.16.0](../prds/zava-forward-retrofit-programme-demonstrator.md).
Decision 6 amends the ingestion choice in ADR 0002's sensor section on the
AMA project owner's direction (2026-10-14) that Azure IoT Hub is the product
for IoT; the owner has not approved any other part of this ADR.

### Source-only infrastructure authorization (2026-10-27, Refs #140)

The owner supplied approval of ADR 0003 for this task on 2026-10-27, within
Free/B1, existing resource group `ama` only and the overall USD700 cost cap.
The authorized action is Bicep authoring and local compilation/tests only:
do not deploy, run Azure what-if, read secrets or delete `ama`. This adds no
operational, DPO/legal or real-device approval and does not erase the narrower
2026-10-15/18 history above.

The [infrastructure decision and budget entry](../../infra/README.md#iot-hub-issue-140-adr-0003-decision-6)
selects B1/one unit, `uksouth`, two partitions, one-day transport retention,
individual device identities and Juan Manuel Servera as exercise credential
issue/rotation/revocation owner. SQL record retention and BRD OD-43 remain
separate. Free is not the selected profile, and S1/scale-out need a new decision.

The old built-in-endpoint receiver assignment is corrected: Microsoft's
[Entra guidance](https://learn.microsoft.com/en-us/azure/iot-hub/authenticate-authorize-azure-ad)
(retrieved 2026-10-27) requires a custom Event Hub for keyless consumption.
Decision 6 therefore permits an authored dedicated Standard/one-TU Event Hub
adapter, with API Data Receiver on the entity and IoT system-identity Data
Sender on its dedicated namespace. IoT Hub remains the device boundary.
Public namespace access is disabled, with private endpoint and the documented
trusted-services exception for IoT routing. Metrics-only diagnostics exclude
device-bearing resource logs. Bootstrap registers no custom endpoint or route;
future activation requires separately approved actual sender-role propagation.
No Azure provisioning, role activation or consumer SDK implementation follows.

## Context

The [customer journey atlas](../reference/research/ux/customer-journeys/customer-journey-atlas.md)
(2026-10-14) is role-instrument desk research. It is a sector-informed
hypothesis set, not user validation. It led to three product requirements:

* PRD FR-045 (extended) and AC-064: task-limited representative authority.
* PRD FR-048, AC-062 and AC-065: offers distinct from confirmed commitments.
* PRD FR-049 and AC-063: complaint, remedy and defect status that package or
  financial closure cannot erase.

The question is whether these need new architecture. The retained constraints
are the single API with Azure SQL state, the five bounded assistants with
normal authority and proactive scans off, deterministic supervision as primary,
and BRD CON-007 / PRD CON-009 (real AI, SQL and Azure for each delivered
build).

## Decision

1. Implement the new capabilities as deterministic records and state
   transitions in the existing Azure SQL schema, using additive idempotent
   migrations (ADR 0002 decision 1 and the migration contract in AC-061). No
   new service, queue, store or network path is added.
2. Enforce authority, confirmation and closure rules in the API, not in a view
   label or an assistant (ADR 0002 decision 3). An offer never becomes a
   commitment, and a closure never closes a remedy, without the recorded
   confirmations. Representative fields follow the permitted-field matrix
   (NFR-003); retention stays Unknown until the DPO approves it.
3. Reach AI only through the existing five registered assistants (PRD FR-047
   and FR-036). A journey opportunity that needs a new assistant or wider
   authority is a registry change with its own review, not part of this ADR.
   Assistants stay proposal-only, with independent human review.
4. Run the five candidate learning-test bundles as experiments with a
   non-AI comparator, as set out in the PRD. A comparator never waives CON-009.
   Opportunities O10 and O18 to O20 stay out of scope.
5. Treat saved minutes as capacity until Finance validates them.
6. Use Azure IoT Hub as the device-to-cloud ingestion product for in-use
   monitoring (BRD FR-048, PRD FR-050), replacing the ADR 0002 position of "no
   IoT Hub for the demo". The shape is:
   * Each simulated or real sensor, or its gateway, is a distinct IoT Hub
     device identity sending device-to-cloud telemetry with a schema version
     and stable reading ID. The simulator is one labelled source (source
     type, scenario, seed) and is never exposed as a resident or device
     system.
   * A server-side consumer in the existing API reads IoT telemetry through
     managed-identity message routing to the dedicated Event Hub (2026-10-27
     source-only correction above), validates schema, device-to-property
     mapping and effective dates, units, UTC time, duplicates, order and
     calibration status, and appends accepted readings to Azure SQL
     (`sensor_reading`) idempotently on sensor ID plus reading ID. Rejected or
     unmapped input raises an owned data-quality exception. IoT Hub is the
     transport and device-identity boundary; Azure SQL stays the system of
     record and there is no public unauthenticated ingestion endpoint.
   * Derived analysis (`sensor_analysis`) is deterministic, versioned and
     reproducible from retained readings. Method selection, including dew
     point and other trend measures, follows the
     [research plan](../reference/research/iot-sensor-analytics-research-plan.md);
     no threshold is fixed until it is sourced or labelled an exercise value.
   * Only an approved derived signal may create a `SENSOR_REVIEW_DUE` human
     review task. It never diagnoses a hazard, starts a clock, overrides a
     resident report, releases a hold or changes ranking directly. Missing or
     stale data is `INSUFFICIENT` and never lowers priority.
   * Devices authenticate to IoT Hub with per-device X.509 certificates or
     symmetric keys, because Microsoft Entra ID is not supported for the IoT
     Hub device APIs (Microsoft Learn, retrieved 2026-10-14). The API consumer
     and other services use a managed identity with least-privilege roles.
     No device key or connection string appears in source or telemetry, and
     device credential issue and rotation need a named owner. Raw readings and device identifiers stay
     out of AI prompts, map tiles, cluster payloads and diagnostic logs.
   * The 2026-10-15 owner amendment selects Basic for the exercise, with no
     cloud-to-device messages, device twins or device management. Region
     (`uksouth`), unit count, device provisioning (for example the Device
     Provisioning Service) and retention remain separate implementation items.
     The basic tier
     supports device-to-cloud only, and the standard tier adds cloud-to-device
     messaging, twins and IoT Edge; message routing is on both (Microsoft
     Learn, retrieved 2026-10-14). Verify sizing and pricing before
     provisioning. Event Hubs alone is
     not chosen.

## Consequences

* The journey capabilities add no infrastructure: they are schema, API and
  screen work inside the current runtime. Decision 6 adds Azure IoT Hub, the
  2026-10-27 keyless Event Hub adapter and a consumer in the existing API.
  The linked budget scenario estimates transport only; actual aggregate
  headroom, paid provisioning and consumer acceptance are not established.
* Representative-authority data adds personal data about third parties. It
  needs DPO review before any real data (ADR 0002 open items DH-002, DH-006).
* The atlas stays hypothesis evidence until real resident, staff and
  contractor validation (BRD OD-41) and representative authority rules (BRD
  OD-42) are decided.
* ID numbering differs between BRD and PRD; every trace must name the
  document.

## Alternatives considered and rejected

* A separate case-passport or scheduling service: adds a store and an
  authority boundary before the hypotheses are validated.
* A new journey assistant with scheduling or disclosure authority: conflicts
  with the retained assistant limits and consent boundaries.
* Deferring all journey requirements: leaves resident-control and remedy gaps
  identified in the atlas without a testable requirement.

## Open items

* Owner acceptance of BRD v0.17.0 and PRD v0.15.0, and a fresh independent
  quality review of both.
* BRD OD-41 and OD-42, and the deferred PRD disposition of the BRD FR-037
  challenge refinement.
* DPO decision on representative data retention and minimisation.
* Atlas-owner confirmation of the bundle to opportunity mapping in the PRD.
* The 2026-10-27 source-only choices and public price scenario are recorded in
  `infra/README.md` for issue 140. Actual subscription quota, billing currency,
  aggregate cost headroom, live what-if, sender-role propagation and private
  transport remain unverified/unexecuted; no provisioning is authorized.
* BRD OD-43 inventory, lawful basis, DPIA, record retention, thresholds and
  operational ownership; actual device credential provisioning remains #185.
* Completion of research phases R1 to R5 in the analytics research plan before
  any derived rule other than a clearly labelled exercise rule is used.

## Related documents

* [Customer journey atlas](../reference/research/ux/customer-journeys/customer-journey-atlas.md)
* [BRD v0.17.0](../brds/agentic-retrofit-programme-brd.md)
* [PRD v0.16.0](../prds/zava-forward-retrofit-programme-demonstrator.md)
* [In-use monitoring analytics research plan](../reference/research/iot-sensor-analytics-research-plan.md)
* [ADR 0001](./0001-azure-architecture.md) and [ADR 0002](./0002-pilot-readiness-architecture.md)

## Implementation status

The owner accepted this ADR with the scoped Basic-tier amendment above.
Separately owner-authorized issue 110 engineering
implements a [finite constructed offline API consumer](../../src/api/README.md#finite-offline-sensor-ingestion-110)
with SQL stable-key append, independent exercise controls and owned DQ metadata.
It reuses sensor_reading, not the generator's intentionally exact-replay loader.
Local actual SQLite/SQL Server processing is not authenticated Hub transport,
Azure SQL application acceptance or additional operational approval. No live IoT Hub
identity, provisioning, SDK, deployment, derived analysis, review task or screen
follows from that slice. Whole PRD AC-066, actual-model/Azure and human/live gates
remain unmet. Acceptance of the ADR and exercise tier does not satisfy those gates.
