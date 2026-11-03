---
title: Issue 212 per-scope precision plan
description: Add by_home_scope to the precision block
ms.date: 2026-11-03
---

Plan status: Ready. Details: [details](../../details/2026-11-03/issue-212-precision-by-scope-details.md).

## Scope

* rule_engine.py: generalise per-card helper to `_precision_by`; add `precision.by_home_scope`.
* test_rule_engine.py assertions; core README audit row.

## Critique (single pass, executed)

* Risk: read as accuracy proof. Disposition: counts only; rate null until humans classify; trial stays unmet.
* Risk: suppression. Disposition: read-only, none.
* Verdict: proceed.

## Validation (focused)

core test_rule_engine, test_source_monitor, api test_rule_alerts, ruff check/format, mypy --cache-dir=/tmp/mypy-212. Not run: gate, benchmarks, full suites.
