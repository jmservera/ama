---
title: IoT Hub RV-001 Implementation Addendum
description: Later local correction evidence without changing the original Review verdict
ms.date: 2026-10-27
---

## RV-001: Resolved in later implementation

PR #498, Refs #140. The module now derives one namespace hostname without
HTTPS scheme, port or trailing slash, exports it for the SDK and constructs
`sb://<hostname>/` for routing. Compiled regressions evaluate four provider
forms, including `https://eh-fixture.servicebus.windows.net:443/`, module output,
main forwarding and both routing states. Mutations reject port leakage and
wrong forwarding; the new regressions reproduced the defect before the fix.

`REQUIRE_AZ_BICEP=1` full infra discovery passed in an external isolated pip
venv: 461 tests, zero skips (109.451s). Module/main Bicep build/lint, scoped
Ruff lint/format and diff checks passed. No uv, Azure deployment, what-if or
secret access occurred.

This note records implementation resolution, not a second Review or acceptance.
The [original Review](../logs/2026-10-27/iot-hub-bicep-module-review.md) remains
byte-for-byte unchanged, **Complete / Not accepted** at its original boundary.
Detailed evidence and publication/live residual gates are in the
[changes record](../../changes/2026-10-27/iot-hub-bicep-module-changes.md#later-implementation-rv-001-2026-10-27-pr-498).
