---
title: Issue 212 home grouping changes
description: Changes delivering address-key home grouping for deterministic alerts
ms.date: 2026-11-01
---

Task: 212 / issue-212-home-grouping.

## Changes

* `src/core/src/zava_forward/core/rule_engine.py`: `_home_key` derives `home-<hash>` with
  `home_scope="address_key"` from normalised postcode and address when `home_id` is absent;
  `case_only` fallback retained.
* `src/core/tests/test_rule_engine.py`: three tests (derivation and cross-case grouping, fallback,
  recorded id precedence).
* `src/core/README.md`: criterion 7 audit row updated.

## Validation (focused tier)

* `tests.test_rule_engine` in src/core: 23 tests OK.
* `tests.test_rule_alerts` in src/api: 6 tests OK.
* ruff check, ruff format --check and mypy (strict) clean in src/core.
* No heavy local gate; CI is the evidence.

## Divergences

* None from the plan. Test uses breach-risk hazards because attention alerts for the same
  home/card/step/item are rate-limited by design.
