---
title: Issue 189 live research (2026-11-19)
ms.date: 2026-11-19
---

Task: first unticked criterion of #189, "Run has an owner, a time limit and a budget alert". Research disposition: reused plus fresh read-only re-observation. Planning Readiness: Ready.

Existing evidence: [first pass](../../docs/reference/research/issue-189-simulator-run-controls-live-evidence-2026-11-18.md) and [second pass](../../docs/reference/research/simulator-run-controls-live-189-2026-11-18.md). Code and tests for owner, bounded duration, budget alert and Bicep contract already exist in `src/core` (tests `test_simulator_run_controls_189`, `test_simulator_run_budget_controls`) and `src/api` (`test_simulator_admin`).

Remaining gap: a live owned run observed with its time limit. It needs a deployed simulator job or the `ZavaForward.ApplicationAdmin` role, both production or identity changes outside the 2026-11-18 owner authorisation. No new code is warranted.
