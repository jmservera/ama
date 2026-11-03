---
title: "Research: #432 re-check after #790"
ms.date: 2026-11-03
---

Disposition: reused (2026-11-02 owner-gate research) plus a direct read of main at a1f18a12d. Planning Readiness: no implementable slice.

* Merged work: #602 (source-only metering), #660 (demo walk-through), #709 (held-out spread), #765 (safety-path test), #790 (status reconciliation). Nothing new has merged for #432 since #790, and no new issue comment records an owner decision, spend authority, billing period or live admission.
* A search of src/agents for discarded provider usage found only the validated chat path (`chat.py`, `dispatch.py`); the legacy draft and image paths named in the issue are not source-joinable without the deployment and SQL scope the 2026-11-02 research already routed to the owner.
* Unmet criteria: 1, 2 (live clause), 3, 5, 6, 8, 9. Ticked earlier and unchanged: 4, 7. Blockers are those in the 2026-11-02 table (OD-51, spend authority, attributable Azure billing, live identity admission, protected slide 52).
