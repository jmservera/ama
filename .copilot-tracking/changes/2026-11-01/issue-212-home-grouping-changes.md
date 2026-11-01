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

## Amendment: upgrade-safe regrouping (PR #630 Copilot thread)

* `rule_engine.py`: `ENGINE_VERSION` 2 to 3 so unchanged data-change checkpoints are recomputed
  after upgrade (checkpoint key includes the version). `alerts()` now regroups open alerts by the
  latest check's `home_id` and `home_scope`; alert IDs, episodes and disposition events are untouched.
* `test_rule_engine.py`: regression starting from persisted v2 case-only alerts (one acknowledged),
  then an address appears at the same revision; asserts one shared group, same alert IDs and
  preserved acknowledgement history.
* Validation: `test_rule_engine` and `test_source_monitor` 53 tests OK; ruff check, ruff format
  --check and mypy clean in src/core. Full src/core discovery: 1644 run; 1 failure and 2 errors are
  subprocess tests that need the package installed (`No module named 'zava_forward'`), unrelated.
* Note: source-monitor approvals bound to engine version 2 must be re-approved by a human.

## Amendment: current-home throttle and latest-check regrouping (PR #630 Copilot threads)

* `rule_engine.py`: new `_homes()` maps each case to the home grouping of its latest check
  regardless of item. `_publish()` attention cooldown now compares prior attention alerts (same
  card, step and item) by their case's current home, so historical case-only throttles do not let a
  second case at the same address publish within 24 hours. `alerts()` regroups from `_homes()`, so
  held-card and removed-evidence snapshots (item `card` or `hazards`) still regroup. History is not rewritten.
* `test_rule_engine.py`: cross-case attention upgrade regression and held/missing-evidence regrouping
  regression; both fail without the change.
* Validation: `test_rule_engine` 26 tests OK; ruff check and format clean.
