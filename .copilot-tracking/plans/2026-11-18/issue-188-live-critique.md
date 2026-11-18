---
title: Issue 188 live plan critique
ms.date: 2026-11-18
---

One critique, executed before implementation. Verdict: proceed with constraints.

* The indoor backfill cannot be joined to a live stream; use a same-schema weather backfill and say so (accepted).
* The production receiver cannot run on the Basic demo namespace; claim only the demo path (accepted, recorded as unproven).
* Ledger rows cannot be removed; record as residue (accepted).
* Keep the verifier handover inside the window with at least 2 samples per side (accepted).
No finding conflicted with a confirmed owner decision.
