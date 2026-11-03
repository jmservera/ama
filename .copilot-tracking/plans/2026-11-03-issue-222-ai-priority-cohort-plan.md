---
title: Issue 222 AI priority cohort plan
ms.date: 2026-11-03
---

## Plan

* [x] Phase 1: add `agents/cohort_ai_eval.py` reusing `cohort_ranking_eval.build`/`observe` and `core.cohort_eval.evaluate`.
* [x] Phase 2: tests for faithful, biased, unavailable, never-approved, reconciliation.
* [x] Phase 3: README note; ruff, format, mypy strict, focused tests.

Details: see [phase details](../details/2026-11-03-issue-222-ai-priority-cohort-details.md).

## Critique

Executed once, direct. Applied: the runner never approves; the AI task must leave ranking unchanged and Proposed; the unavailable mode checks the fallback reason. Stacked later slices: owner approval (external), approved AI-task manifest. Focused tier.
