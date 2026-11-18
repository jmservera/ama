---
title: Plan for issue 110 live IoT Hub identity proof
ms.date: 2026-11-18
---

Refs #110. Docs/evidence only; no source change; focused tier.

1. Phase 1: grant temporary roles (Registry Contributor on hub, Event Hubs Data Receiver on `sensor-readings`) to `id-cutover-test-api`; create throwaway job `job-110-probe` in `cae-cutover-test-demo` with the demo API image.
2. Phase 2: run driver (outside repo): create 3 SAS devices, send 2 generator readings each plus one duplicate resend and one wrong-key contrast, read from Event Hub, verify hub-stamped device id, schema version, message id equals reading id; delete devices.
3. Phase 3: delete job and roles; verify hub stats 0 devices; write research note, changes and review records; commit.
