# Research: IoT ingestion issue 110, round 1 (fleet identity evidence slice)

Date: 2026-11-03. Branch: feat/issue-110-r1. Base: main at b855aec86. Research disposition: executed (repository and issue evidence only).

## Already delivered (not redone)

* #411 (100ead1ba): bounded offline consumer, SQL stable-key idempotent append, visible data-quality outcomes (criteria 2 and 3).
* #508 (768c006e4): opt-in finite IoT receiver and synthetic publisher; Hub-only authority, per-device X.509 binding, no public ingestion route (criteria 4 and 5).
* Device identity plan/provision/teardown in `src/core/src/zava_forward/core/synthetic/device_identity.py`; Bicep tracked in #140.
* Closure audit 2026-10-31 (issue comment): criterion 1 unmet because no real Hub identity was issued and no live stream was sent.

## Unmet criterion

* Criterion 1 (distinct IoT Hub identity per simulated device with schema version and stable reading ID) is unmet as a live claim. It needs a provisioned Hub, a credential owner and cost, network and tier approval, none of which this slice may do.

## Gap found

Existing tests prove client-per-device and one-home binding, but no test asserts across a multi-home fleet that every frame carries a device ID unique per sensor, a non-empty schema version, a non-empty reading ID unique per sensor, deterministic reruns, and that the receiver refuses a reading sent under a different device's identity.

## Planning readiness

Ready for a test-only slice. No security, infrastructure, SQL or deployment surface touched; focused tier applies.
