---
title: 1530 c2 rebase details
ms.date: 2026-11-13
---

## Details

* P3: before `scan(...)` in `populated_safety_panel`, set `open` on every `.safety-details` and `.safety-optional` element in `#case-safety` via locator evaluate_all, then assert at least one was opened. Axe then covers expanded content. Overflow check stays after.
* P2: run `python -m zava_forward.core.synthetic.cutover_audit` (see its README for write mode) and confirm the inventory is unchanged or regenerate.
* Evidence of conflicts: none, rebase clean.
