---
title: "Research: #432 safety path under a stopped AI request"
ms.date: 2026-11-02
---

Disposition: executed (direct read). Planning Readiness: Ready.

* Core ledger already enforces root call/depth bounds with a workflow-only alert (`test_loop_fanout_exact_calls_depth_and_owned_workflow_stop`).
* The criterion clause "hazard response and statutory clocks are unaffected" had no test or doc statement.
* `hazard`, `workflows` and `taskqueues` import no model module; `Store.raise_hazard` is deterministic.
* Considered and rejected for this slice: capstone deck regeneration (protected cost slides, heavy build), resident-demo ledger joins (SQL procedures and deployment change).
