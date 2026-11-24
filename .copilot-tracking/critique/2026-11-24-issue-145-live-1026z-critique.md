---
title: Issue 145 live critique (2026-11-24 10:26Z run)
ms.date: 2026-11-24
---

Executed once on the final candidate plan.

Verdict: proceed with amendments applied.

* Per-admission blob write for allowance: rejected (hot path, new outage mode). Applied: fail-closed reapply after restore instead.
* Closing the ledger can block legitimate assistant calls after a restore: accepted, deliberate and documented; the manual owner route remains and an operator re-seeds under authority. Applied: say so in runbook and README.
* Must be idempotent and touch only rows with headroom: applied.
* Must not claim live proof: it is SQLite emulation, lower-tier; live restore remains unproven and no drill is authorised. Applied.
* Scope: no change to admission code, Bicep or Azure estate. Applied.
