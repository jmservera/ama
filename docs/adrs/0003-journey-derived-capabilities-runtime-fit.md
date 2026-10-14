---
title: ADR 0003 Journey-Derived Capabilities and IoT Hub Sensor Ingestion
description: Proposed decisions on carrying the customer journey atlas capabilities in the existing single-API, Azure SQL and five-assistant runtime, and on using Azure IoT Hub as the in-use monitoring ingestion product with deterministic analysis
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

## Status

Proposed. This ADR records a proposal by the AMA programme. It does not record
approval by the owner, the DPO, Legal, the Board, control owners or any
customer role. It applies the runtime of [ADR 0001](./0001-azure-architecture.md) and
[ADR 0002](./0002-pilot-readiness-architecture.md) to the requirements added by
[BRD v0.17.0](../brds/agentic-retrofit-programme-brd.md) and
[PRD v0.16.0](../prds/zava-forward-retrofit-programme-demonstrator.md).
Decision 6 amends the ingestion choice in ADR 0002's sensor section on the
AMA project owner's direction (2026-10-14) that Azure IoT Hub is the product
for IoT; the owner has not approved any other part of this ADR.

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
   * A server-side consumer in the existing API reads the hub (built-in
     endpoint or message routing), validates schema, device-to-property
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
   * Tier, region (`uksouth`), unit count, device provisioning (for example the
     Device Provisioning Service) and retention are open items. The basic tier
     supports device-to-cloud only, and the standard tier adds cloud-to-device
     messaging, twins and IoT Edge; message routing is on both (Microsoft
     Learn, retrieved 2026-10-14). Confirm the tier and pricing before
     provisioning. Event Hubs alone is
     not chosen.

## Consequences

* The journey capabilities add no infrastructure: they are schema, API and
  screen work inside the current runtime. Decision 6 adds one Azure IoT Hub
  resource, a consumer in the existing API and its cost, which is not yet
  estimated or approved.
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
* IoT Hub tier, sizing, cost estimate, device provisioning approach, network
  exposure and Entra role design and device credential ownership; BRD OD-43 inventory, lawful basis, DPIA,
  retention and thresholds.
* Completion of research phases R1 to R5 in the analytics research plan before
  any derived rule other than a clearly labelled exercise rule is used.

## Related documents

* [Customer journey atlas](../reference/research/ux/customer-journeys/customer-journey-atlas.md)
* [BRD v0.17.0](../brds/agentic-retrofit-programme-brd.md)
* [PRD v0.16.0](../prds/zava-forward-retrofit-programme-demonstrator.md)
* [In-use monitoring analytics research plan](../reference/research/iot-sensor-analytics-research-plan.md)
* [ADR 0001](./0001-azure-architecture.md) and [ADR 0002](./0002-pilot-readiness-architecture.md)

## Implementation status

Not implemented. No migration, API or screen change, IoT Hub provisioning,
test run or deployment follows from this ADR.
