# Issue 185 research: simulated device identity and provisioning (2026-11-01)

Task: issue-185-device-identity. Mode: automatic. Research disposition: executed. Planning Readiness: Ready.

## Evidence

* PRD FR-050 / AC-066 and ADR 0003 decision 6: each simulated sensor is a distinct IoT Hub device identity; per-device X.509 or symmetric keys; no key or connection string in source or telemetry; credential issue and rotation need a named owner; DPS is a separate implementation item.
* Research plan lines 45-60 and 131: individual X.509 approach and named exercise credential owner (Juan Manuel Servera) already recorded; actual issue/storage/expiry/rotation/revocation and teardown remain owner work; no teardown success claimed.
* `src/api/.../iot_stream.py` `Binding`: `device_id == "SYN-" + sensor_id`, unique home per binding (1..100). `sensor_identity.sensor_key(home_id)` yields the compact stock sensor key; `sensor_stock.Selection.sensors()` yields sensor/home pairs.
* Criterion 2 (one device, one stock home) is already checked in the issue.

## Gaps for acceptance criteria

1. Decision recorded with credential owner: needs a durable decision section (docs) naming approach, owner, rotation, teardown.
2. Credentials issued/stored without appearing in source or logs: no issuance/storage abstraction exists.
3. Teardown removes all simulated identities: no teardown logic or verification exists.

## Decision for this slice

Individual enrolment (no DPS), per-device X.509 (matches existing `iot_stream` path), credential material only behind a store protocol (Key Vault reference), run-tagged manifest, teardown by manifest with post-delete verification. Live Azure not exercised: criteria 3 and 4 proven only against injected fakes, so the PR uses Refs.

## Scope

Core module `zava_forward.core.synthetic.device_identity` plus tests in `src/core/tests`; a short decision section in the research plan. No live Azure, no new dependencies.
