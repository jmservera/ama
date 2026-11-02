---
title: "Research: #432 remaining criteria and owner gates"
ms.date: 2026-11-02
---

Disposition: executed (direct read). Planning Readiness: Ready for a status reconciliation only; no further implementable slice.

Evidence read: issue #432 body and comments (latest 2026-10-31), `docs/reference/resources/ai-tokenomics.md` criteria table, `src/core/src/zava_forward/core/ai_consumption.py`, `docs/capstone/source/README.md`, merged PRs #602, #660, #709 and #765.

Source-only mechanisms on main: per-call joins (`CallContext`, `reserve`, `complete`), root call and depth bounds, token, money, expiry and unknown-price or liability holds with an owned alert, billing reconciliation with tolerance, accepted-outcome report with quality failure, capacity-not-cash, held-out batch spread under recorded authority, and the safety-path test.

Why no further slice is implementable without a human decision or live evidence:

| Criterion | Blocker |
| --- | --- |
| 1 Per-call joins | Historical and resident-demo calls use independent accounting and SQL procedures; joining them is a deployment and data change needing owner scope |
| 2 Bounds and safety | Live governed stop and statutory-clock observation need live identity admission (#612 blocked) |
| 3 Limits and alerts | Named alert owners and approved budgets are BRD OD-51 |
| 5 Reconciliation | No attributable Azure cost record or owner-set tolerance |
| 6 Report | OD-51 denominator, quality floor and complete Total Cost of AI inputs |
| 8 Held-out batch | Owner spend authority is not recorded; none is assumed |
| 9 Pitch | Slide 52 (B25) is a protected cost slide; placement and deck rebuild are owner-controlled work |

Already ticked: criteria 4 (dated price source metadata, rates Unknown) and 7 (capacity, not cash).
