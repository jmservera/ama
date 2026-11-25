---
title: Plan issue 2303 r73
ms.date: 2026-11-25
---

* [x] Phase 1: memoize `projection.withheld_scope_values` per distinct case set within `ai_tasks.live_report`.
* [x] Phase 2: add a core test that counts calls (recommendations over repeated case sets) and checks reasons are still held back.
* [x] Phase 3: run targeted core tests, mypy and ruff for src/core; record the evidence note and per-criterion table.

Tier: FULL applies because src changes. The full local gate and external receipt belong to the coordinator (this worker must not run rpi-checks.py --all).
