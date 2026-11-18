---
title: C1 plan, wire run governance into RunPlan (#189)
ms.date: 2026-11-14
---

1. `run_governance.py`: `_gbp(allow_zero)`, validate projected and admit costs, pre-cap halt at `>=`, `halt_reason`.
2. `run_plan.py`: optional `budget_alert_gbp`, `budget_cap_gbp`, `planned_cost_gbp`; `RunPlan.governance()`, validation, `RunController.meter` and `admit()` (stops run on halt), CLI flags.
3. Tests in `test_simulator_run_budget_controls.py`; README note under #189.
4. Focused validation: core mypy, ruff, targeted tests (caches in /tmp).

Critique: executed once, no conflicts; owner and time limit reuse plan `owner` and `max_seconds`.
