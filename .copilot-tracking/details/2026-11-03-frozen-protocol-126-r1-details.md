---
title: Issue 126 round 1 details
ms.date: 2026-11-03
---

## Phase 1: governance code

* `benefits_record` requires `ai_denominator` (three allowed values), `ai_quality_floor`, `ai_cost_components`; optional `ai_price_source`, else cost status is Unknown.
* `capture_gate` adds a reason when the approved entry lacks `ai_running_cost`.
* `value_claim_record` (capacity only) and `value_claim_confirm` (different person, one of five destinations, budget owner reference). `governance_view` lists claims.
* Server: two new governance actions.

## Phase 2: tests and docs

* Two new tests in `src/core/tests/test_governance.py`; fixture updated.
* `src/core/README.md` section and knowledge-base log entry.
