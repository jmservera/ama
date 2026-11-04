# Issue 110 research (2026-11-04, r2)

* Disposition: executed. Planning Readiness: Ready for a records slice.
* Merged delivery checked: #411 (offline consumer, stable-key idempotent append, visible data-quality outcomes), #508 (bounded IoT streaming candidate, per-device X.509 publisher and consumer binding), #910 (offline fleet identity evidence). Open, not merged: #1088 (live simulator container, Refs #184); it is not counted.
* Ticked and preserved: C2 idempotent append, C3 duplicate/out-of-order/unmapped/wrong-unit/clock-skew/uncalibrated handling, C4 no public unauthenticated endpoint, C5 no device key or connection string in source or telemetry.
* Unmet: C1 (distinct IoT Hub identity per simulated device with schema version and stable reading ID). Offline code and tests exist (core device_identity.py, api iot_stream.py, test_iot_stream.py, test_device_identity.py), but no real Hub identities were issued and no live stream was observed.
* Remaining work is human or Azure: Hub provisioning (#140), tier, sizing, cost, network exposure and a named device credential owner. No coherent offline slice remains; more tests would duplicate #411, #508 and #910.
