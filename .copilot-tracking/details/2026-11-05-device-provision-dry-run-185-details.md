---
title: Details for #185
ms.date: 2026-11-05
---

* Phase 1: `build_manifest` reads the register, selects granted homes, calls `device_identity.plan`.
* Phase 2: `run` returns a report; dry-run by default; apply needs `owner_named` and both adapters.
* Phase 3: `main` CLI with fixed-code refusals and exit 2.
* Phase 4: tests with fakes from `test_device_identity`, README section.
