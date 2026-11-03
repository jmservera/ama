---
title: "Research: #432 round 2 re-check"
ms.date: 2026-11-03
---

Disposition: reused (2026-11-02 owner-gate, 2026-11-03 re-check and resident-usage research) plus a direct read of provider call sites on main a7effea1d. Planning Readiness: Ready for a records-only slice; no implementable source slice found.

* Merged for #432: #602, #660, #709, #765, #790, #832, #936. Nothing merged since #936 touches metering, limits, price, billing or the report.
* All three provider call sites (core/ai.py, resident aoai.py, resident assistant.py) now read and validate provider usage. The resident adapter sink is not instantiated by any host, and a ledger join for it needs an owner scope decision.
* Unmet and gated: 1 (host ledger join for the resident adapter), 2 (live clause), 3 (alert owners, budgets), 5 (attributable Azure billing, tolerance), 6 (OD-51 denominator, quality floor), 8 (owner spend authority), 9 (pitch placement; slide 52 protected). Ticked and unchanged: 4, 7.
* No security, infrastructure, SQL or deployment change: focused tier.
