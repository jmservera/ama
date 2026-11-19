---
title: Issue 1847 research (delivery check on main)
---
# Research: nomination test bootstrap isolation (#1847), 2026-11-18

Disposition: reused plus delta check. Planning Readiness: Ready. Tier: FOCUSED per coordinator brief (issue text says FULL conservatively; the coordinator owns the full gate and receipt).

## Delivery check against base 20f0b166f

* `src/core/tests/test_nomination_route.py` already rejects foreign `zava_forward` modules with `ImportError` before any `sys.path` change and has no `sys.modules` purge (commit 7de4a8110, #1849, `Refs #1847`).
* `src/core/tests/test_nomination_bootstrap.py` has fresh-process regressions: source layout in both orders with `ConflictError`, `GateError`, `Store` and patch-target identity, foreign-copy-on-path with nomination first, and foreign-module-first rejection without purge.
* Earlier artifacts: `.copilot-tracking/research/2026-11-17-issue-1847-research.md` holds the measured original failure (failures=1, errors=20) and identity split.

## Criteria status

* Delivered: order tests (source and foreign-on-path layouts), identity observation, regression failing on the original, no whole-family purge, retained foreign checks.
* Unmet in the tree: supported/unsupported layout contract is not documented outside tracking artifacts; no noneditable-installed-first row in the tests is mislabelled.
* Unmet here by design: complete local gate and verified external full receipt (coordinator).

## Smallest delta

Document the layout contract in `src/core/README.md` beside the nomination section. No source or test behaviour change.
