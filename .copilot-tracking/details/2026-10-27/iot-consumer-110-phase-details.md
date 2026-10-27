---
title: IoT consumer implementation details
ms.date: 2026-10-27
---

## Metadata

Task 110 / iot-consumer-110. Plan:
.copilot-tracking/plans/2026-10-27/iot-consumer-110-plan.md.
Research: .copilot-tracking/research/2026-10-27/iot-consumer-110-research.md.

## Phase Index

| Phase | Status | Task |
| --- | --- | --- |
| P01 | Complete: six local tests | P01-T01 |
| P02 | Complete: seventeen local tests | P02-T01 |
| P03 | Local validation/Review complete; Not accepted; publication blocked | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Shared replay
<!-- rpi:task id=P01-T01 -->
### P01-T01: Finite seeded replay and pacing

Use sensor_stock.Selection granted synthetic rows and the existing backfill
generator. Generate the original complete finite model window before selecting
a replay suffix; never reseed at handover. Preserve scenario and timestamp IDs.
Default 480-minute cadence; any override is explicit run configuration.
Cap homes/slots/messages before generating. Truth records never enter telemetry.
Use injectable monotonic clock and wait function for deterministic controls.
Pacing checks stop/deadline even while paused; speed finite positive and bounded.
Failures are deterministic and declared, including transport disconnect/burst.
Tests: exact suffix equality, exclusion of unknown/declined selections,
forced AC-066 faults, count/quota/time/owner validation, pause/speed/stop.
Supported model is explicitly the existing legacy seasonal generator, not the
climate-backed composed model. Record stock digest/seed/origin/days/cadence/model.
Use nominal slot bounds before applying per-slot faults, including odd suffixes;
do not filter on a clock-skewed timestamp. Mutated unmapped IDs on a normal
device are transport refusals; SQL unmapped proof uses a separate exact binding
whose sensor is deliberately absent from SQL controls. Composed/live seam
acceptance remains deferred.

<!-- rpi:phase id=P02 -->
## P02: Azure adapters
<!-- rpi:task id=P02-T01 -->
### P02-T01: Managed identity receive and per-device publish

Use pinned azure-eventhub and azure-iot-device SDKs in the API workload.
Explicit activation record includes routing-ready, approval reference,
RG ama and endpoint outputs; no default connection or credential lookup.
Use ManagedIdentityCredential only for receive. Supply per-device X.509 context
for send; do not use service keys or device discovery.
One SYN-prefixed device per selected compact sensor ID and stock home.
Only Hub connection metadata is usable for identity binding; reject absent,
conflicting or wrong-origin identity before SQL. Preserve malformed primitive
observation handling in existing SQL DQ, but refuse invalid transport envelopes.
Return success only after SensorIngestion returns; on failure terminate receive
rather than rely on exceptions escaping SDK callbacks. Retry uses original
identities and SQL reconciliation, not fresh IDs. Cancel/close all SDK resources.
Pin azure-eventhub 5.15.1 and azure-iot-device 2.14.0. Inspect installed
EventData properties/accessors before the decoder. Trust only the dedicated
Event Hub whose sole sender is the IoT Hub identity; reject duplicate/conflicting
metadata, missing/wrong types and module identities. Never add guessed aliases.
Every fresh receiver explicitly starts at "-1" (retained beginning), without
a durable checkpoint store; SQL deduplication is the restart state. Retention
expiry is a disclosed recovery limit. Serialize callbacks within each partition
and stop global admission on first SQL/transport failure.
Use async SDK calls with absolute monotonic run deadline and reserved cleanup
allowance; disable device auto-connect/connection retry and Event Hub retries.
The installed SDK witness showed no-store checkpoints are warning-only no-ops,
so no checkpoint update is called. SQL admission uses a shielded thread task;
cancelling/timing out its wait cannot cancel the database commit. Observe the
eventual task outcome without acknowledging transport, retain stable IDs and
replay. Keep the SQL store available until in-flight work settles.
Test operation timeouts/stop, callback failure swallowed by SDK, checkpoint
uncertain commit and fresh-receiver replay across partitions.
Tests use real EventData objects where possible, fake clients and constructed
SQLite, never Azure. No actual Hub acceptance is inferred from fake metadata.

<!-- rpi:phase id=P03 -->
## P03: Delivery evidence
<!-- rpi:task id=P03-T01 -->
### P03-T01: Tests, documentation, one Review and publication

No test removals; maximum two new owned test modules, no new framework.
Use installed distributions in an external venv after missing-package probe.
Run focused sensor units, configured Ruff/mypy and API discovery; no cloud
fallback. Record commands/counts/failures. Update component guides and existing
IoT synthesis, knowledge-base index/log; no memory or original case-study edits.
Map each issue criterion as locally proven or deferred, never silently waived.
One independent Review after source completion; findings route to follow-up,
not a repeated Review. Commit original outcomes with Conventional Commit/trailer.
Run only the user-authorized changed gate once, timeout zero, new external
output; disclose busy/missing prerequisites. Push topic branch without force
and open one PR to main, default Refs for all incompletely proven issues.
Publication is conditional on applicable repository gates. Busy lock means
skip the sole changed attempt and disclose, never fabricate a receipt. A failed
or unavailable gate blocks publication; no second attempt or --all fallback.
