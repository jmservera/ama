---
title: Issue 110 device identity, schema version and reading ID research
ms.date: 2026-11-14
---

Research disposition: executed. Planning Readiness: Ready.

Scope: criterion 1 of #110 (distinct device identity, schema version, stable reading ID).

Evidence:

* `src/core/src/zava_forward/core/synthetic/device_identity.py`: `verify_envelope` binds `SYN-<sensor_id>` to the sensor/home pair, requires a live schema version and recomputes `reading_id_for(sensor_id, slot)`.
* `src/api/src/zava_forward/api/iot_stream.py`: the only caller; it reads the Hub-asserted device id and X.509 scope before calling `verify_envelope`, then checks the per-device binding.
* `src/core/src/zava_forward/core/sensor_consumer.py`: `_live_shape` re-derives the reading ID; `(sensor_id, reading_id)` is the primary key, giving idempotent append.
* `src/core/tests/test_iot_device_identity_schema.py`: existing envelope tests.

Finding: `verify_envelope` parsed `observed_at` with `datetime.strptime`, which accepts non-canonical text (`2026-11-14T9:5:00Z`, full-width digits, lowercase `z`). Such a message would pass the identity check although it is not the canonical slot text a device must send. The downstream consumer rejects it, so impact is defence in depth, not data corruption.

Unproven and out of scope: real Hub identities and live Azure SQL acceptance (open tier, cost, network and credential-owner decisions), so the criterion stays unchecked.
