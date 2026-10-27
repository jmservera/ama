---
title: IoT consumer and synthetic live streaming changes
ms.date: 2026-10-27
---

## Scope and Status

Task 110 / iot-consumer-110, full P01-P03 implementation scope.
Plan/details dated 2026-10-27. Research complete, one critique Revise preserved;
all six findings directly disposed without a second critique.
Implementation source scope executed; full delivery Partial. P01/P02 executed;
P03 local validation and one independent Review complete. Review outcome is
Not accepted, with three Medium defects routed to later implementation.
Gated publication remains blocked, not complete.
No Azure operations or secret/private-data reads.

## P01: Synthetic replay

Added core synthetic.sensor_stream and six owned tests. Exact existing
seasonal-generator comparison and odd/nonzero nominal-slot replay pass.
Synthetic-only stock validation, all declared fault modes, three/day default,
finite scale/bytes/quota controls and speed/pause/stop/cancellation pass.
Initial Ruff found one long assertion; formatter corrected it. Initial mypy
found calls to existing untyped generator; use the existing narrowly scoped
disallow_untyped_calls override pattern, not casts or ignored errors.

## P02: API transport

Source and test evidence complete for the executed local boundary; Review
findings remain open.
Pinned SDK witness: EventData.system_properties merges AMQP message properties
and annotations; EventData.properties exposes AMQP application properties.
Custom routed IoT properties are decoded only at the dedicated trusted
Hub-only sender endpoint; ambiguous bytes/string/annotation forms are refused.
Actual routed metadata remains a live verification gap.
Installed async SDK probe showed aiohttp absent and neither SDK declares it;
added an explicit pinned aiohttp dependency for asynchronous managed identity.
SDK PartitionContext.update_checkpoint without a store only warns/no-ops:
removed that misleading call. This run uses no checkpoint store and always
starts each new receiver at retained beginning (-1). SQL remains the only
durable restart state. Checkpoint-write failure is therefore not applicable.
Cancelled/timed-out shielded SQL work can still commit, but never checkpoint;
retain identities and replay to reconcile. The receiver's network wait deadline
is bounded; it cannot claim to roll back or forcibly stop a database operation.

## P03: Validation, Review and publication

Publication blocked. No full gate authorized; scoped checks cannot establish
complete repository final-publication acceptance.
Do not treat local/fake-SDK proof as actual Hub/Azure SQL or whole AC-066.

### Local validation completed so far

* Core configured Ruff check and format check: pass, 102 formatted files.
* Core configured strict mypy: pass, 155 source files.
* Core test_sensor*.py selector: 96 tests, pass, one existing opt-in SQL Server
  integration skip. Existing backfill tests emit unclosed-file ResourceWarnings.
* Core test_historical_backfill.py: 9 tests, pass.
* API configured Ruff check and format check: pass, 48 formatted files.
* API configured strict mypy: pass, 90 source files.
* New transport module: initially 16 tests, pass; final focused API transport
  and inherited sensor-ingestion selector: 62 tests, pass (17 new transport).
* Full existing API discovery: 1137 tests in 463.978 seconds, pass, 314 existing
  opt-in/integration skips. The additional distinct-device case was then
  covered by the final focused selector; no skipped integration is counted
  as Hub/Azure SQL success.
* Hashed runtime requirements dry-run: pass. Actual AioHttpTransport opens/closes
  locally without network; pip check passes.
* git diff --check: pass.
* New documentation section relative-file/heading links: pass.
* Existing migration authoring suite initially failed seven cases because
  system Python lacked python-pptx/Pillow. Installed the declared
  tools/rename-zava-requirements.txt in the external validation venv and reran:
  all 25 tests pass. No dependency pins were loosened.
* No SQL Server container, Azure, real AI, browser or deployment acceptance
  claimed from these local backend-only checks.

### Pre-Review reconciliation

Plan and phase details reflect the actual no-checkpoint strategy and shielded
SQL uncertainty, not the superseded warning-only SDK no-op. Source behavior,
documentation and test ownership agree. There are exactly two new test modules,
no existing test removals or workflow-name changes. Current fetched main equals
the branch base 09099ecd1a66ee9d37ad993707d1f2eda07cdfd4.
Required independent Review was unexecuted at that handoff and is now preserved
below. Publication gates remain unproven. A scoped gate is not full-gate evidence.

### Independent Review and parent closeout

Exactly one independent Review completed at
.copilot-tracking/reviews/logs/2026-10-27/iot-consumer-110-review.md.
Execution: Complete. Outcome: Not accepted. Original critique Revise unchanged.
Independent bounded probes reproduced three Medium findings:

* RV-001: a slow connect consumes a pre-reserved rate interval, permitting
  subsequent actual sends closer than the configured maximum rate.
* RV-002: the descriptor's full-register digest does not bind the selected
  subset or mutable selected model inputs.
* RV-003: receiver partial construction is outside cleanup/sanitized errors.

No finding is claimed fixed. Per the one-pass RPI contract, route to later
owner-selected implementation, not a second Review or silent closure.
The RPI loop is complete, but implementation acceptance and publication are
blocked. No issue criterion or human-review checkbox has been ticked.
Existing local tests do not overrule the independent adverse evidence.

### Local persistence and publication decision

Source and original RPI evidence were committed locally as 7cd2400f on
feat/iot-consumer-110, with authenticated-account noreply author/committer
and the required Copilot trailer. No source was changed after Review.
The allowed scoped heavy gate was not run: the independent Review already
blocks this candidate, and the complete final-publication gate is explicitly
not authorized. No lock contention or passing receipt is claimed.
No push, PR, issue closure or Azure operation occurred. This is a persistent
local handoff, not successful delivery of the requested published PR.
P03 publication remains incomplete. The three ranked concrete defect
follow-ups are recorded in state; existing credential/live/budget and OD-43
owner gates remain distinct.

## Amendments and Divergences

Legacy seasonal model selected explicitly; composed climate handover deferred.
Normal-device mutated unmapped identity is a transport refusal, not SQL DQ.
Fresh receivers replay retained history from -1; no new checkpoint store.

## Blockers and Remaining Work

Actual #185 credential lifecycle, #188 live acceptance and #189 active budget
verification remain deferred under the issue criteria. No issue closure claimed.
