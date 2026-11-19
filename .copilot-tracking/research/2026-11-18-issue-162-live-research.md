---
title: Research for #162 live break-glass proof
ms.date: 2026-11-18
---

* Task: prove unticked criterion 6 of #162 (administrator and break-glass access audited with purpose, policy decided) against the live synthetic demo, or state why not provable. Criteria 1 to 5 are already ticked.
* Owner decisions 2026-11-18: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). DPO/Legal approval, billing reconciliation and person-run AT testing not needed. Docs/evidence only, no src change; tier FOCUSED.
* Research disposition: executed. Prior evidence: docs/reference/research/chat-demo-breakglass-disclaimer-2026-11-03.md; src/core/.../chat_isolation.py `break_glass`; server route `POST /api/chat/.../breakglass`.
* Findings go to `docs/reference/research/chat-breakglass-live-proof-2026-11-18.md`.
