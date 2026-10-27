---
title: IoT consumer and live synthetic simulator plan
ms.date: 2026-10-27
---

## Task Metadata

Task ID: 110. Slug: iot-consumer-110. Planning completed after direct critique
dispositions. Post-implementation Review: Complete / Not accepted, three
Medium defects; final delivery and publication remain blocked.
Details: .copilot-tracking/details/2026-10-27/iot-consumer-110-phase-details.md.

## Executive Summary

Add a bounded, explicitly activated Azure SDK consumer and synthetic publisher
around the existing SQL admission contract. Reuse seeded backfill rather than
create a second model. Prove behavior locally and deliver one PR with honest
issue-by-issue evidence.

### What You May Not Know

The merged Hub module is not deployed and defaults to no routing. The keyless
consumer must use its dedicated Event Hub, not the built-in endpoint. Actual
credential issue/teardown, private routing, Azure SQL and whole AC-066 remain
unexecuted; no owner or privacy authority is inferred.

## User Decisions and Requirements

* Deliver #110 with #184/#185-#189 in one PR to main on the provided branch.
* Use ADR 0003 approved Free/B1 scope in ama; no deployment unless necessary.
* New code in src per ADR 0006, tests outside packages; preserve check names.
* Local tests only, at most one scoped changed gate under the heavy lock with
  timeout zero; never --all, uv, private data, secrets or real devices.
* Conventional commit and Copilot trailer; publish evidence, using Refs unless
  every issue criterion is proven. Preserve human/resident boundaries.

## Goals

* Connect device telemetry to existing idempotent SQL admission without a public route.
* Make replay, failure injection, pacing and run limits reproducible.

## Scope and Non-Goals

In scope: core synthetic streaming model, API SDK adapters, tests, package pins,
component and knowledge-base documentation, RPI evidence and one PR.
Excluded: Azure operations, automatic provisioning, real devices/data, derived
analysis, AI changes, legal decisions, issue closure based on mocks.

## Functional Requirements

* One canonical JSON observation per message; explicit SYN device mapping.
* Receiver uses ManagedIdentityCredential and custom Event Hub outputs.
* Bind Hub connection device metadata to independently configured sensor/home;
  never trust an application property claiming another home.
* SQL accepted or durable DQ outcomes precede successful receipt. No checkpoint
  store or checkpoint update is used; fresh receivers replay retained beginning.
  Failed/uncertain SQL, malformed envelopes or identity mismatch stop admission.
* Replay preserves seed, original model origin, cadence, stock IDs and reading
  IDs; three observations/day is the default, other cadence explicitly declared.
* Bounded speed/pause/stop, duplicates/order/skew/units/calibration/unmapped
  faults plus disconnect/burst exercise controls and separate truth records.
* Publisher accepts only explicit granted synthetic selection; no discovery.

## Non-Functional Requirements

* Limit payload to 4096 bytes, runtime <=3600 seconds, finite message count,
  finite replay model slots, finite send rate and no autonomous SDK reconnect.
* Validate quota/headroom and declared owner/alert/budget reference before send;
  B1 400,000 daily 4-KiB units, conservative per-message accounting.
* No secret-bearing repr/logging; sanitized transport failure codes and cleanup.
* Preserve original SQL validation, consent, calibration and property history.

## Acceptance Criteria

* Local fake-SDK tests prove wiring, metadata binding, durable checkpoint order,
  replay after failure, stopped-run behavior and no default cloud connection.
* Constructed actual SQLite tests prove same-home backfill/stream union and exact
  replay identity. Zero numeric difference on overlapping seeded windows is the
  declared seam tolerance; actual Azure SQL proof remains deferred.
* Relevant existing tests, Ruff and mypy run; no criterion ticked from unrun tests.
* All five #184 children get explicit delivered/deferred evidence in PR/docs.

## Sources

Research: .copilot-tracking/research/2026-10-27/iot-consumer-110-research.md,
C1-C6/W1-W5. Existing SensorIngestion, SensorConsumer and synthetic backfill.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Shared synthetic replay and controls
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement finite seeded replay and pacing

Core owns the pure model and truth records; no network dependency.

<!-- rpi:phase id=P02 -->
### [x] P02: API-owned Azure transport
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement managed-identity receive and per-device publish

API owns SDK dependencies and finite explicitly called runners; no HTTP route
or startup activation. X.509 clients are supplied from separately approved
credential mounts; this work neither issues nor retrieves secrets.

<!-- rpi:phase id=P03 -->
### [ ] P03: Evidence, validation and publication
<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Test, document, review and publish

Test ownership: add at most two modules, core/tests/test_sensor_stream.py and
api/tests/test_iot_stream.py; no removals. Core semantic coverage for replay,
faults and bounds; API semantic coverage for SDK lifecycle, metadata and SQL.
Regression coverage reuses existing sensor suites. Canonical targets are src
modules, pyprojects/requirements and READMEs; generated target only API hashed
requirements. Run local project commands and one independent Review.
Only one changed gate invocation, after commit, new external output,
--lock-timeout 0; busy lock means skip and disclose. No full gate.

## Dependencies

P02 depends on P01; P03 depends on P01/P02. Merged #498/#411/#412/#486 are
available source contracts, not actual Azure environments.

## Critique Disposition

Exactly one critique executed, original verdict Revise, preserved at
.copilot-tracking/reviews/plans/2026-10-27/iot-consumer-110-plan-critique.md.

| Finding | Disposition | Resolving contract |
| --- | --- | --- |
| PC-001 | Direct correction | Pin SDKs 5.15.1/2.14.0; inspect actual EventData representation before implementing metadata decoder; dedicated endpoint and Hub-only sender are the trust boundary; actual routing remains deferred |
| PC-002 | Direct correction | No checkpoint store/update: every new finite receiver starts at retained beginning (-1), serial callbacks per partition; SQL deduplication handles history; failures close admission globally |
| PC-003 | Direct correction | Async SDKs, absolute monotonic deadline including cleanup reserve, disabled reconnect/retry, shielded SQL uncertainty and first-failure channel; bounded network operations and external stop; SQL may still settle after cancellation |
| PC-004 | Direct correction | Mutated sensor ID on normal device is transport refusal, not SQL UNMAPPED; deliberately unmapped exact binding may be independently installed, never authorized by payload truth |
| PC-005 | Direct correction | Explicit legacy synthetic seasonal model only; canonical conversion, full-origin RNG, nominal slot selection before timestamp mutation; per-slot deterministic fault transformations support odd windows; composed climate handover deferred |
| PC-006 | Direct correction | Single permitted scoped attempt only; busy/failing/missing gate is recorded, never a successful receipt; publication remains conditional on applicable repository gates, no full fallback authorized |

These are compatible corrections within existing user constraints, not new
owner authority. Replay beyond the one-day configured retention is not promised.
Run descriptor binds stock digest, seed, origin, cadence, days, model version
and explicit fault mode. API live callers provide already configured SQL
controls, never infer them from simulator output.

## Follow-Up Items

* RV-001: later rpi-implement must enforce actual send spacing after connection;
  original Review's delayed-connect reproduction overrides passing pacing tests.
* RV-003: later rpi-implement must cover receiver partial-construction cleanup
  and fixed-error handling.
* RV-002: later rpi-implement must bind descriptor and replay to the same
  validated selected-input snapshot.
* #185: owner-approved credential issue, Key Vault storage, rotation and teardown.
* #188: live private Hub-to-Azure SQL acceptance and actual restart/seam evidence.
* #189: actual aggregate budget/quota headroom and active alert verification.
* OD-43 remains an operational gate, outside synthetic engineering.

## Handoff

Changes: .copilot-tracking/changes/2026-10-27/iot-consumer-110-changes.md.
The ordered RPI loop reached its one Review. Preserve the Not accepted outcome
and route the three defects to later owner-selected implementation. P03 remains
unchecked because publication is blocked; no second Review or live acceptance
is inferred. No push/PR is permitted while applicable final gates are missing.
