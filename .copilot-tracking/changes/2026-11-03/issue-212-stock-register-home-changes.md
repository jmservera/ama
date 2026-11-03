---
title: Issue 212 register-linked home grouping changes
description: Changes delivering stock register home grouping
ms.date: 2026-11-03
---

## Changes

* `rule_engine.py`: `_home_key` adds the `stock_register` scope from a linked, valid
  `stock_link.stock_home_id`.
* `test_rule_engine.py`: `test_stock_register_link_groups_cases_and_outranks_address`,
  `test_unusable_stock_link_is_ignored`, `test_recorded_home_id_wins_over_stock_link`.
* `src/core/README.md`: criterion 7 row and grouping paragraph updated.

## Validation (focused tier; no gate, benchmarks or full suites run)

* core `tests.test_rule_engine`: 30 tests OK (run with `PYTHONPATH=src`; the installed editable
  package points at another worktree).
* core `tests.test_source_monitor`: 29 tests OK.
* api `tests.test_rule_alerts`: 7 tests OK.
* `ruff check` and `ruff format --check` clean in src/core; `mypy --cache-dir=/tmp/mypy-212`
  clean (199 files).
* Slice does not touch security, infrastructure, SQL or deployment; the coordinator still owns
  the gate.

## Divergences

* None. `ENGINE_VERSION` deliberately not bumped (see plan critique).

## Acceptance criteria still unmet

* Criterion 7 remains unticked: no real staff precision or false-positive trial, and no case
  source writes a verified dwelling `home_id`. Hosted timer, real card approvals and a workbench
  alert component are also undelivered. PR uses `Refs #212`.
