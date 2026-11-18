---
title: Issue 222 decision criteria plan
ms.date: 2026-11-14
---

## Phases

* [x] 1. Add `zava_forward.core.ai_decision`: per-dimension ordered limits, worst-dimension outcome,
  fail-closed on invalid criteria, missing values, non-finite values and low sample count, advisory
  flag until approved_by and approved_on are set, `evaluate_all` pausing registered features
  without criteria.
* [x] 2. Add `tests/test_ai_decision.py` covering bands, inclusive boundaries, safety rule, fail-closed
  paths and per-feature isolation.
* [x] 3. Run mypy (strict), ruff check, ruff format (line length 100) and focused tests.
* [x] 4. Write changes and review artifacts; commit without pyc files; do not push.

## Critique (single pass, direct)

Compatible: keep module standalone and typed rather than editing excluded legacy `ai_registry`.
Deferred: wiring criteria into the registry, API and dashboards.
