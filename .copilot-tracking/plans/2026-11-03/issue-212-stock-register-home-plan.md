---
title: Issue 212 register-linked home grouping plan
description: Group deterministic alerts by a linked stock register reference before the address key
ms.date: 2026-11-03
---

Task: 212 / issue-212-stock-register-home. Plan status: Ready. Details:
[details](../../details/2026-11-03/issue-212-stock-register-home-details.md).

## Scope

* `src/core/src/zava_forward/core/rule_engine.py`: `_home_key` order `recorded_home`,
  `stock_register`, `address_key`, `case_only`.
* `src/core/tests/test_rule_engine.py`: three tests.
* `src/core/README.md`: criterion 7 row and grouping paragraph.

## Critique (single pass, executed)

* Risk: `ENGINE_VERSION` bump would invalidate source-monitor approvals bound to the version.
  Disposition: no bump. Unchanged cases regroup on their next revision or scheduled minute; the
  `alerts()` view already regroups from the latest check.
* Risk: stock reference read as verified dwelling identity. Disposition: distinct scope label
  `stock_register`, `stock-` id prefix, README states it is not verified identity.
* Risk: grouping implies shared consent. Disposition: grouping affects staff alert display only;
  no resident message, consent or approval path touched.
* Verdict: proceed.

## Validation (focused)

`tests.test_rule_engine`, `tests.test_source_monitor` (core), `tests.test_rule_alerts` (api),
ruff check, ruff format --check, mypy with `--cache-dir=/tmp/mypy-212`.
