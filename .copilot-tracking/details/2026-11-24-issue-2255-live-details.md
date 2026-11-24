---
title: Issue 2255 live details
description: Phase details
ms.date: 2026-11-24
---

* Phase 1: write the seed tool. Open hazard (`released` not true) with no `aware_at` and no `response_due_at` and no `responded_at` gets `aware_at` = now minus a cycled offset (6, 30, 80, 200 hours) and `response_due_at` = aware + 168 hours (the operational 7-day reference), plus marker with original values. Skips counted by reason.
* Phase 2: tests (plan, apply, idempotent, skip, revert, projected clock text no longer unknown).
* Phase 3: ruff, mypy in src/core, run tests, research note with per-criterion table.
