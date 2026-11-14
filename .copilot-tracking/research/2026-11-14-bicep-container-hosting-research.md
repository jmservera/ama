---
title: Bicep container hosting invariants research (Refs #144, #136)
ms.date: 2026-11-14
---

* Existing test_container_hosting_completeness.py already covered limits, replica bounds, three probes, single revision mode and rollback docs.
* Gaps found: no test that deployed images are parameters (not literals), that the placeholder is limited to bootstrap defaults, probe timing bounds, or worker scale-from-zero caps.
* Placeholder quickstart image is a deliberate bootstrap default (4 sites in main.bicep); the guard publicSimulationRequiresRealApiImage and deploy.py handle real images.
* No Bicep change needed; scope is test strengthening only.
