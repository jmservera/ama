---
title: Issue 470 core suite timeout critique
ms.date: 2026-11-17
---

* Execution: one final-candidate critique, performed by the implementing agent.
* Verdict: proceed. Raising the core ceiling to 3600 s leaves the hang fail-closed (exit 124). Sharding core rejected as larger and receipt-shape changing. Old receipts with 1800 s core timeout stop verifying; documented.
