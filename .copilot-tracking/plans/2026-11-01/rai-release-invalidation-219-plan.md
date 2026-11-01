---
title: Plan for issue 219 release record invalidation
ms.date: 2026-11-01
---

## Steps

* [x] Add `changed_triggers` to `rai_release.py` mapping bound keys and contract fields to material-change triggers.
* [x] Add `invalidate_changed` to `assistant_release.py` and call it from `assessment` for non-legacy tasks before selection; revocation records an event with the triggers.
* [x] Tests outside the package in `src/core/tests/test_rai_release.py` (pure) and `test_rai_release_invalidation.py` (SQLite).
* [x] Validate: relevant unit tests, ruff check, ruff format --check, mypy for `src/core`.

## Critique (single pass)

Verdict: Revise-free. Risk: revocation is terminal, so a transient mismatch needs a new record; this matches the module rule that revoked or suspended is terminal. Legacy tasks excluded to avoid cross-deployment revocation. No change to approval authority.
