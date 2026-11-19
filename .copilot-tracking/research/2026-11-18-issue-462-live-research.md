---
title: Research for #462 live synthetic showcase proof
ms.date: 2026-11-18
---

* Task: prove the unticked #462 criteria against the live synthetic demo (`ca-resident-demo`, resource group `ama`) with Playwright at desktop width; defer production-only items.
* Owner decisions 2026-11-18: synthetic demo, desktop only, live Azure authorised (cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO/Legal approval and person-run assistive-technology testing are not needed.
* Research disposition: executed. Prior evidence: 2026-11-16 and 2026-11-17 threat models; infra/resident-demo.bicep; infra/scripts/resident_demo_deploy.py.
* Opening state: app Running, revision `ca-resident-demo--0000012`, external HTTPS-only ingress, min replicas 0.
* Findings are appended in `docs/reference/research/resident-showcase-live-proof-2026-11-18.md`.
