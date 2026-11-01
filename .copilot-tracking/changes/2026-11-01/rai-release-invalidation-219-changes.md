---
title: Changes for issue 219 release record invalidation
ms.date: 2026-11-01
---

## Changes

* `src/core/src/zava_forward/core/rai_release.py`: `TRIGGER_KEYS` and `changed_triggers`.
* `src/core/src/zava_forward/core/assistant_release.py`: `invalidate_changed`, called from `assessment` for non-legacy tasks; revocation writes a `release-revoked` event naming the triggers; a failed write denies dispatch.
* `src/core/tests/test_rai_release_invalidation.py`: four tests (matching record admitted, six triggers revoke and record, intended-use trigger, no false positive).

## Validation

* `src/core`: `python3 -m unittest discover -s tests -q` with `PYTHONPATH=../agents/tests`: 1646 tests OK (206 skipped).
* `ruff check .`, `ruff format --check .`, `mypy src`: clean.
* No local RPI gate by owner direction; CI is the evidence.

## Divergences

None from the plan.
