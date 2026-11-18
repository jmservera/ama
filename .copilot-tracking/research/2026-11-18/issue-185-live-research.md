---
title: Research for issue 185 live device identity proof
ms.date: 2026-11-18
---

Refs #185. Scope: demo hub `iot-cutover-test-rzsrg` (B1, private only, local auth disabled), hub-generated symmetric keys, no X.509.

Disposition: executed. Unticked criteria: credentials issued and stored without appearing in source or logs; teardown removes all simulated identities. Repo adapter `device_registry_azure.py` is X.509-only, so the proof uses an out-of-repo driver and changes no source.
