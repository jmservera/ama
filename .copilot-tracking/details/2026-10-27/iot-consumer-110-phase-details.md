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

## Correction Cycle 1 (110-correction-1)

Date: 2026-10-27. Scope and phase IDs are the correction section of the existing
plan; original P01-P03 evidence remains historical. Current state is the
separate iot-consumer-110-correction-1-state.json. No unresolved owner decision.

<!-- rpi:phase id=P04 -->
### P04 / P04-T01: RV-001

Keep model interval/speed waiting separate from actual send admission.
Move rate reservation to the send coroutine immediately before the SDK await,
after client connect, message construction and the required attempt truth sink.
No await or truth callback may occur between reservation and SDK invocation.
Retain one global limiter across device clients and the cleanup-reserved
absolute deadline. Tests record actual fake SDK timestamps after delayed connect
and delayed truth preparation; include multi-device and paused/stopped/timed-out
admission. Core tests cover deterministic admission/cancellation controls.

<!-- rpi:phase id=P05 -->
### P05 / P05-T01: RV-003

Initialize optional resource/task ownership before setup. Keep callback
definitions outside setup if useful, but construct credentials, client and
receive/wait tasks inside the same try/except/finally. Close only resources
successfully returned; cancel/observe only created tasks. Use one bounded
cleanup call for tasks/client/credential. Preserve StreamError and cancellation;
sanitize unexpected setup/receive errors as IOT_RECEIVE_FAILED. Cleanup failures
remain explicit IOT_CLEANUP_FAILED. Tests cover credential failure, client
failure after credential, synchronous receive startup failure, and close failure.

<!-- rpi:phase id=P06 -->
### P06 / P06-T01: RV-002

Use the same canonical-validation helper for descriptor and replay. Hash the
validated selected copy with select's canonical digest; retain original
stock_sha256 separately. Include selected count/IDs and granted count in the
descriptor and selected digest on each Frame outside row telemetry. Copy this
field when the publisher snapshots frames. Tests distinguish one/two-home
subsets from the same register, fabric/consent mutation and old/new frame
provenance, invalid selected input and canonical ordering/normalization.
Do not redesign Selection globally or change historical model/reading IDs.

<!-- rpi:phase id=P07 -->
### P07 / P07-T01: Validation and publication

Use the two existing test modules only (<=12 additional methods, no removals).
Commands: core sensor selectors plus historical backfill; full API discovery
with PYTHONPATH=../core/tests:../agents/tests; both configured Ruff, format check
and mypy. Install declared distributions/dev tools with pip into an external
venv after the confirmed system missing-dependency probe. No manifests change.
Update guides, synthesis/index/append-only log and existing RPI artifacts.
Reconcile all correction markers before the one independent Review; write
reviews/2026-10-27/iot-consumer-110-review-addendum.md without modifying the
original log. Review findings route to later work, not a second Review.
No heavy/full gate planned for this bounded correction. Commit required
evidence and trailer, push same branch, update draft PR #508 with Refs and
explicit local-only/deferred criteria. Hosted/human approval and merge remain
separate; no issue closure.

### Correction Execution Status

P04/P04-T01, P05/P05-T01 and P06/P06-T01 are complete with focused passing
regressions. Model-time wait and actual send admission are distinct; constructor
ownership extends through receive task startup; shared canonical selected
snapshots bind descriptor, Frame and restricted truth provenance. Seven added
methods in two existing tests, no removals. Observation bytes/IDs are unchanged.
P07/P07-T01 local validation is complete: core 99 sensor tests (one existing
opt-in SQL skip), 9 historical backfill tests and configured lint/format/mypy
pass; API focused 66 tests pass. Full API discovery passes 1142 tests in
458.785 seconds with 314 existing integration/opt-in skips. Configured API
lint/format/mypy pass (48 formatted/90 checked files); core 102/155.
Pre-Review reconciliation is complete; source/tests frozen for the one
correction Review, now Complete / Conformant in the requested addendum.
P07 authorized commit/push and PR evidence update are complete: d553b1a5
was pushed non-force to feat/iot-consumer-110, existing draft PR #508's head
was verified at d553b1a51bcac5bcac884772581fa554cd5f8d68 and its body updated.
Source/tests remain unchanged after Review. This final evidence-only closeout
does not claim hosted/live/human acceptance or owner merge.
