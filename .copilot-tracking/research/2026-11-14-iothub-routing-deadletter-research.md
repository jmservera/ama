# Research: IoT Hub routing, consumer group and dead-letter contract (Refs #145)

Date: 2026-11-14. Base: 59c53274c (stacked on PR #1672). Disposition: executed. Planning Readiness: Ready.

* Module is `infra/modules/iothub.bicep` (no `iot.bicep`). It already has the dedicated `api-consumer` group on the telemetry Event Hub, an identity-based route gated by `routingReady`, `disableLocalAuth` on hub and namespace, and `disableModuleSAS`.
* The fallback route is explicitly disabled and no built-in endpoint consumer group exists; `test_iothub_module.py` pins both as an owner-approved privacy posture (the built-in endpoint would retain device messages outside Event Hub RBAC).
* Enabling fallback quarantine or adding a quarantine Event Hub/route would break those existing tests, which are out of the permitted file scope. Dead-letter storage is therefore a recorded gap, not implemented here.
* Issue #145 body text describes SQL tier work; the IoT scope comes from the task brief. Refs only.
