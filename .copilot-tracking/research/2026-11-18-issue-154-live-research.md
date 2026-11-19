---
title: Research for #154 live resident and representative UX proof
ms.date: 2026-11-18
---

* Task: prove the unticked #154 criterion ("No live resident contact; designs are validated through the usability programme before any use") against the live synthetic demo, desktop only, with Playwright.
* Owner decisions 2026-11-18: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO/Legal approval and person-run assistive-technology testing are not needed.
* Research disposition: executed. Planning Readiness: Ready.
* Apps: `ca-resident-demo`, `ca-cutover-test-demo-api`; Event Hub `evhns-cutover-test-demo`. Credentials are read at runtime only and never recorded.
* Findings are appended in `docs/reference/research/issue-154-live-resident-ux-evidence-2026-11-18.md`.
* Result: no live resident contact is observed on the showcase (proven for the demo); usability-programme validation and the representative view are unprovable for the demo (no participants or SA-010 agreement; no live case has a representative).
