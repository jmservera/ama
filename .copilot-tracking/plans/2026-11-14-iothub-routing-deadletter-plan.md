# Plan: IoT Hub routing contract tests (Refs #145)

Tier: Focused. Critique: executed once inline; an enabled fallback or quarantine route conflicts with the confirmed prior contract, so it is rejected and routed to follow-up.

* [x] Add `infra/tests/test_iothub_routing_deadletter_bicep.py` (dedicated group, fallback disabled, gated identity route, no shared-key auth).
* [x] Leave `infra/modules/iothub.bicep` unchanged.
* [x] Run the new and existing IoT tests, isolated ruff check and format.
