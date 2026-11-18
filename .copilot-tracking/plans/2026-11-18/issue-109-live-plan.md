---
title: Issue 109 live plan
ms.date: 2026-11-18
---

Tier: FOCUSED, no source changes (evidence note and tracking only). Azure actions stay in resource group `ama`.

1. Create throwaway job `job-109-probe`; grant `id-cutover-test-api` IoT Hub Registry Contributor on the hub (temporary).
2. Probe: create SAS device, read identity (before), connect and send simulated humidity and temperature, read identity while connected, disconnect, read after, delete device.
3. Create a throwaway Azure Monitor metric alert on `devices.connectedDevices.allProtocol`, observe its evaluation and fired state, delete it.
4. Remove job, role assignment and alert; confirm hub settings unchanged.
5. Write evidence note with per-criterion table; changes, review, commit.
