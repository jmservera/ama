---
title: Issue 165 acceptance criteria audit research
ms.date: 2026-11-13
---

## Scope

Audit the five literal acceptance criteria of issue #165 (Epic: Synthetic data programme: needs, generator and sensor simulator) against commit 34b11967b93df40b653d384ab3b136bb1fb842f9. Research disposition: executed. Planning Readiness: Ready.

Brief mismatch: the brief calls this an "EPC conflict / stock discrepancy" audit. The issue text contains no EPC conflict criterion. The stock-reconciliation modules (`src/core/src/zava_forward/core/stock.py`, `src/api/tests/test_stock_reconciliation_api.py`, `src/core/tests/test_stock_reconciliation.py`) are named in the brief and are run as requested, but only the synthetic stock register and fabric files bear on the criteria (SN-01, #168). The audit is of the literal criteria.

## Criteria (gh issue view 165, 2026-11-13)

1. #440 stabilization checkpoint completed before epic closure (reconcile, regression, dispositions, Azure residuals, owner pivot/defer decision).
2. Needs inventory and phase gate approved by the owner.
3. Every need has a recorded coverage status: covered, partial or missing.
4. All child features closed or deferred.
5. All generated data labelled synthetic with no real personal data beyond documented OpenStreetMap anchors.

## Evidence gathered

* Inventory: `docs/reference/research/retrofit-synthetic-data/needs-inventory.json` version 1.3.0, status `draft-awaiting-owner-review`, 13 rows SN-01..SN-13, coverage values covered/partial/missing, 5 open items including owner approval; tested by `src/core/tests/test_needs_inventory.py`.
* Children (gh, 2026-11-13): #176, #184, #185 open; #166-#175, #177-#183 closed. Epic comment 2026-11-04 confirms the open set and that #440 is human-blocked.
* Labelling: `stock_register.py` emits `source_type SYNTHETIC`; `privacy.py` offline checks are bounded and "never a universal personal-data guarantee".
* Related tests: `test_needs_inventory.py`, `test_stock_register.py`, `test_stock_fabric.py`, `test_sensor_stock.py`, `test_synthetic_provenance.py`, `test_generator_coverage.py`, `test_stock_reconciliation.py`, API `test_stock_reconciliation_api.py`.

## Planning notes

Proof table must mark criteria 1, 2 and 4 as NOT FULLY PROVEN (human or open-child gates). Criterion 3 is proven by inventory plus test. Criterion 5 is NOT FULLY PROVEN: only bounded automated checks exist; absence of real personal data in all data cannot be proven by unit tests.
