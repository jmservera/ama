---
title: Issue 212 home grouping plan
description: Derive a deterministic home key so alerts group per home across cases
ms.date: 2026-11-01
---

Task: 212 / issue-212-home-grouping. Plan status: Ready. Critique: executed once, below.

## Scope

* `src/core/src/zava_forward/core/rule_engine.py`: add `_home_key(facts, case_id)` returning
  `(home_id, scope)`; use it where checks are built.
* `src/core/tests/test_rule_engine.py`: tests for derivation, cross-case grouping and fallback.
* `src/core/README.md`: update the criterion 7 audit row. No other files.

## Steps

1. Recorded `home_id` wins, scope `recorded_home`.
2. Else both `home.postcode` and `home.address` non-empty strings: `home-` plus first 16 hex of the
   SHA-256 of `postcode|address` lowercased with whitespace and punctuation collapsed, scope
   `address_key`.
3. Else `case_id`, scope `case_only`.
4. Tests: two cases at the same address group into one home; a different address stays separate;
   formatting variants match; missing address stays `case_only`; recorded `home_id` unchanged.
5. Validate: core unit tests for rule engine, ruff check, ruff format --check, mypy in src/core.

## Critique (single pass)

* Risk: address matching may merge distinct flats. Disposition: accepted and labelled
  `address_key`; address strings include the unit in the case model. Documented as not a
  registered home identity.
* Risk: changes existing checkpoint keys. Disposition: key hashes inputs, not home id, so replay is
  unaffected; existing tests confirm.
* Verdict: proceed.
