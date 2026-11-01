---
title: Changes for issue 219 release record invalidation
ms.date: 2026-11-01
---

## Changes

* `src/core/src/zava_forward/core/rai_release.py`: `TRIGGER_KEYS` and `changed_triggers`.
* `src/core/src/zava_forward/core/assistant_release.py`: `invalidate_changed`, called from `assessment` for non-legacy tasks; revocation writes a `release-revoked` event naming the triggers; a failed write denies dispatch.
* `src/core/src/zava_forward/core/assistant_release.py` (review fixes): revoked records keep `invalidated` (triggers, mismatched fields) so later denials name the cause without making revoked records selectable; `change()` writes status, cause and event under one savepoint (`SAVE TRANSACTION` on MSSQL) so an audit failure rolls the revocation back and dispatch stays denied.
* `src/core/src/zava_forward/core/assistants.py`: `ReleaseDenied(PermissionError)`; `review()` raises it and `transaction()` commits so an invalidation first seen by a denied review persists with its event.
* `src/api/tests/test_assistant_release.py`: independent scenarios install fresh constructed releases; added asserts that restoring a binding does not revive a revoked record and a denied-review persistence regression.
* `src/core/src/zava_forward/core/rai_release.py` (CI fix): `reference()` digest excludes `invalidated` so retained task references stay verifiable; `change()` stores the cause only on a valid non-empty release body so malformed bodies stay untouched.
* `src/api/tests/test_operator_suspension.py` (CI fix): `fresh_release` gives the retained-snapshot scope its own active release after earlier steps revoke it, without replacing other tasks' retained records.
* `src/core/tests/test_rai_release_invalidation.py`: cause-retention and audit-failure atomicity tests, plus the original four tests (matching record admitted, six triggers revoke and record, intended-use trigger, no false positive).

## Validation

* `src/core`: `python3 -m unittest discover -s tests -q` with `PYTHONPATH=../agents/tests`: 1646 tests OK (206 skipped).
* `ruff check .`, `ruff format --check .`, `mypy src`: clean.
* No local RPI gate by owner direction; CI is the evidence.

## Divergences

None from the plan.
