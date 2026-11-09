---
title: Plan for #185
ms.date: 2026-11-05
---

* Slice 1 (this PR): dry-run-by-default provisioning and teardown command over `device_identity`, adapters injected, `--apply` refused without owner and adapters.
* Slice 2 (stacked, later): Azure IoT Hub registry and Key Vault adapters, owner-run, needs credential owner decision and infrastructure gate.
* Slice 3 (later, #188): consumer accepting `live-sim-reading-v1`.
* Critique (single pass, self): adapters must stay out of the CLI so no Azure is reachable; errors fixed-code only; no secrets in output. Applied.
* Tier: focused. Slice 1 creates no credentials and touches no infrastructure.
