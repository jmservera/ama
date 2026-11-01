---
title: "Research: #432 held-out batch spread slice (2026-11-01)"
ms.date: 2026-11-01
---

* Prior PRs: #433 (requirements), #602 (merged ledger, admission, price, billing, report), #660 (merged demo walk-through). All used Refs #432.
* Criteria marked delivered in the issue: dated price source, time-as-capacity.
* Remaining engineering-only gap: report gives min/max/mean tokens per proposal but no spread, and no recorded spend-authority field for a held-out batch (criterion 8).
* Still blocked (not attempted): live Azure billing, OD-51 owner decisions, real spend, pitch regeneration (B25 already states the gap).
* Research disposition: executed. Planning Readiness: Ready.

## Correction cycle 1 (PR 709 review)

* Two Copilot threads: null/empty authority or evidence reference, and allowance checked against measured totals instead of all roots. Both valid.

## Correction cycle 2 research

* Copilot thread PRRT_kwDOUU8JX86yY4nm (ai_consumption.py:1068): valid; only `batch_spread` was tested directly, not `Consumption.report(batch=...)`.
