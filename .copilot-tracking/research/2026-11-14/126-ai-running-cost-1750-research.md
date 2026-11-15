---
title: Issue 126 AI running-cost line and release-gate research
ms.date: 2026-11-14
---

## Research disposition: executed. Planning Readiness: Ready

* Target: `src/core/src/zava_forward/core/governance.py` (`benefits_record`, `capture_gate`, `release_record`); no `src/api` change needed (the API passes the body through).
* Existing: `ai_running_cost` held denominator, quality floor, components and a price-source status; release records held `economics_report_ref`, `economics_limit_breach` and the breach decision (issue #1142).
* Gap 1: no `total_cost_of_ai`, `cost_per_accepted_outcome` or `named_denominator`; Unknown-not-zero was not enforced for figures.
* Gap 2: release records did not carry the register's AI running-cost line.
* Constraint: no price, budget or target is set (BRD OD-51 open); missing price or accepted outcomes stays `Unknown`.
