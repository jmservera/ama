---
title: IoT consumer and live synthetic simulator research
ms.date: 2026-10-27
---

## Research Brief

Deliver #110 with #184 and its listed children in one topic PR, reusing merged
ADR 0003 infrastructure and ADR 0006 packages. Audience: implementer and owner.
Output mode: convergence. Posture: focused (bounded named issues).
Evidence root: `.copilot-tracking/`.

## Research Parameters and Direction Controls

Investigate existing core observation, backfill, SQL consumer and approved
keyless transport contracts before selecting changes. No private datasets,
secrets, `.env`, real devices, Azure deployment or billable activity.
Local tests only; at most one locked scoped changed gate, never `--all`.
The explicit full-loop request authorizes ordered phase advancement.
No interaction is available; unresolved owner/legal decisions remain blocked.

## Extension Registry and Provenance

* Selected: repository instructions, rpi-research, subsequent ordered RPI skills.
* Research specialist skipped: this is one coupled contract trace.
* Web, AI and legal-domain extensions skipped: no UI, inference or new legal claims.

## Research Questions and Prior Knowledge Gate

* Q1: What approved transport/identity authority exists after #498?
* Q2: How can live transport preserve the existing ingestion/replay contract?
* Q3: Which child criteria can local evidence prove, and which remain deferred?
* Existing issue comments distinguish merged offline #411 and schema #412 from
  unproven live Azure acceptance. Verify against current sources.

## Research Cycle Log

### Cycle 1: Wider

Completed inline: read #110, #184, #185-#189, knowledge-base index, baseline
specifications, ADRs 0003/0006, PRD FR-050/AC-066 and BRD FR-048/OD-43.
Reflection: the merged infrastructure is bootstrap source, not a deployed Hub.
Its custom Event Hub is mandatory for managed-identity consumption.

### Deeper

Completed inline: traced SensorIngestion -> SensorConsumer, canonical stock
selection and seeded backfill/fault packets. Compact stock sensor keys already
fit the consumer; no schema widening is necessary. A replay must generate from
the original seed/window origin before selecting its replay interval: restarting
the random sequence at handover would introduce a seam.
Reflection: retain the existing SQL validation and checkpoint only after its
durable receipt; wire SDKs in the API workload, not core.

### Contrarian

Completed inline: challenged built-in Hub keyless consumption, synthetic labels
as authentication, checkpoint-before-commit, fresh random state at replay,
unbounded SDK retries and cost alerts as spending stops.
Reflection: use the custom Event Hub, enforce an allowlisted authenticated Hub
device-to-sensor binding, finite runtime/message bounds, explicit transport
failure and unchanged SQL replay. A transport envelope failure stops without
checkpoint; it cannot invent SQL DQ ownership. Never use application-provided
home/device claims alone as authority. Current Azure quotas/headroom, credential
issuance/rotation/teardown and live SQL acceptance cannot be proven locally.
No second cycle needed: remaining gaps require live/owner action outside scope.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/110, retrieved 2026-10-27:
  offline consumer merged; full live acceptance remains open.
* W2: https://github.com/jmservera/ama/issues/184, retrieved 2026-10-27:
  children #185-#189; #186 closed; remaining criteria not yet proven.
* C1: `infra/README.md:3098`: B1/one unit, individual identities, named owner,
  private custom Event Hub, bootstrap no-send gate and USD60 monthly model.
* C2: `src/api/src/zava_forward/api/sensor_ingestion.py:17`: finite SQL adapter.
* C3: `src/core/src/zava_forward/core/sensor_consumer.py:134`: independent
  consent/calibration/mapping controls; durable replay and DQ.
* C4: `src/core/src/zava_forward/core/synthetic/sensor_backfill.py:109`:
  generator random state begins at series origin; stable timestamp reading IDs.
* C5: `src/core/src/zava_forward/core/synthetic/sensor_stock.py:69`:
  only granted synthetic selections produce collision-checked sensor identities.
* C6: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2162`:
  actual Hub, Azure SQL restart and registered AI are whole AC-066 gates.
* W3: https://learn.microsoft.com/en-us/python/api/azure-eventhub/azure.eventhub.eventhubconsumerclient?view=azure-python,
  retrieved 2026-10-27: token credentials, receive callbacks, checkpoints and
  explicit close; SDK retries may restart failed partition consumers.
* W4: https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-construct,
  retrieved 2026-10-27: Hub-set connection device ID, custom-endpoint body and
  properties, explicit JSON content encoding.
* W5: https://learn.microsoft.com/en-us/python/api/azure-iot-device/azure.iot.device.iothubdeviceclient?view=azure-python,
  retrieved 2026-10-27: per-device X.509 factory, send and shutdown.
* External search for routed Python property placement failed (504); verify
  pinned SDK object contracts locally and disclose unproven actual routing.

## Findings, Alternatives and Decision State

Selected: bounded opt-in SDK adapters in API plus pure synthetic replay/run
controls in core, tests outside packages, existing SQL admission unchanged.
Reject built-in endpoint SAS (C1), new public HTTP ingestion (C2/C6), a second
generator (C4) and automatic credential provisioning (C1).
Retain individual X.509 credentials under the already named exercise owner;
actual approved Key Vault issue/rotate/revoke/teardown is deferred (#185).
Defer live Hub/Azure SQL seam proof (#188) and actual budget/alert/headroom
verification (#189). Existing #186 remains delivered, not re-closed.
No installed device discovery, inference, resident workflow or approval changes.

## Planning Readiness

Ready for independent local engineering. Research disposition: executed, complete.
Live acceptance and credential operations remain explicitly deferred, not passed.
Self-check: three waves complete; source pointers and constraints recorded;
no source changes during Research. Parent action: advance to Plan.

## Correction Cycle 1: Research Brief and Opening State

Date: 2026-10-27. Task: 110-correction-1; parent: 110.
Status: In progress. Output: convergence; posture: focused, selected for the
owner's three named defects. Evidence root remains `.copilot-tracking/`.
Audience: implementer, independent reviewer and draft PR #508 owner.

Research questions: where must actual send admission occur (RV-001), which
partially constructed receiver resources need ownership (RV-003), and how can
descriptor and frames bind identical validated selected inputs (RV-002)?
Criteria: precise regressions at these boundaries, no model/consent/SDK retry
authority changes, preservation of original adverse Review.
Starting areas: the two stream modules, their existing test modules, stock
selection and the original review log. External research is unnecessary.

Selected extensions: repository instructions and ordered RPI phase skills.
Research specialists skipped because this is a single coupled source trace;
web/AI/legal extensions do not apply. Explicit full-loop/correction direction
permits automatic phase progression; no intake question is needed or available.
Scope excludes deployments, private data, secrets, new models and operational
approval. The owner explicitly authorizes same-branch commit/push to existing
PR #508 with local validation; no full gate is authorized. The optional
large-change scoped gate is not planned for this bounded correction.

Prior knowledge: original Review is Complete / Not accepted, with all three
findings open. Original loop state is retained unchanged as historical evidence.
Current branch is clean and PR #508 is open to main. Issue #110, #109, #184
and #185-#189 and their linked PRD/BRD/ADRs were retrieved/read before source work.

### Correction Research Cycle 1

* Wider (inline): traced original RV-001/003/002, current Pacer/publisher,
  receiver resource ownership and stock selection. Reflection: all three
  reproduced source relationships remain present; no external SDK upgrade or
  new model is necessary.
* Deeper (inline): model wait reserves rate before connect/truth; receiver
  constructors precede its cleanup try; select hashes the entire canonical
  register before slicing. Reflection: separate model pacing from send
  admission, own partial setup, and reuse select's canonical selected-row copy.
* Contrarian (inline): a second pre-send reservation outside the send coroutine
  still permits scheduling latency to consume the interval; hashing only home
  IDs misses fabric/consent mutations; independently recomputed descriptors
  cannot identify old frames after mutation. Reflection: admit immediately
  adjacent to the SDK send in the same coroutine, and attach the canonical
  selected-input digest to frames as well as descriptors. Keep the original
  full-register digest separately. Constructor and cleanup errors must both
  remain fixed codes, with cancellation propagated.

### Correction Evidence Log and Findings

| ID | Evidence | Finding |
| --- | --- | --- |
| C7 | src/core/src/zava_forward/core/synthetic/sensor_stream.py:223; src/api/src/zava_forward/api/iot_stream.py:355 | RV-001: reserved time precedes connect and preparation |
| C8 | src/api/src/zava_forward/api/iot_stream.py:208 | RV-003: credential/client construction lacks owned error/cleanup scope |
| C9 | src/core/src/zava_forward/core/synthetic/sensor_stock.py:135; src/core/src/zava_forward/core/synthetic/sensor_stream.py:184 | RV-002: full-register digest precedes subset and mutable selected-row replay |
| C10 | src/core/tests/test_sensor_stream.py:24; src/api/tests/test_iot_stream.py:330 | Existing owned tests can host all focused regressions without a new test module |
| W6 | https://github.com/jmservera/ama/pull/508 (retrieved 2026-10-27) | Existing draft PR on the requested branch; reuse, never create a second PR |

Accepted: minimal split send admission, outer lifecycle ownership and canonical
selected snapshot digest on descriptor/frames (C7-C10). Rejected: pre-reserving
another rate slot, home-ID-only digest, and relying on a frozen wrapper around
mutable dicts. Deferred: actual Hub/SQL, credential lifecycle and OD-43; unchanged
from the parent. Questions are answered; another cycle would be redundant.

### Correction Planning Readiness

Research disposition: executed; status: Complete; Planning Readiness: Ready.
Self-check: ordered three waves, questions/evidence/alternatives/limits present;
no source changed. Parent action: transition to Plan for this correction only.
