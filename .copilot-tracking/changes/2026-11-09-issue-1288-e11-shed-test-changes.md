---
title: Issue 1288 E11 changes and review
ms.date: 2026-11-09
---

# E11 changes and review

## Changes (one file: `src/api/tests/test_resident_demo_api.py`, +87/-2)

* `own_every_slot(owned, wait)`: acquires each of `MAX_CONCURRENT` slots with a bounded blocking timeout, asserts success, records only real acquisitions. `test_shed_signed_in_view_carries_retry_guidance` uses it and releases only owned slots; all 503, JSON retry, Retry-After and signed-in assertions unchanged.
* `DelayedReleaseSlots` (labelled test double, `BoundedSemaphore` subclass) holds handler-thread releases until a gate opens; regression `test_shed_view_owns_every_slot_despite_delayed_login_release` proves the delayed post-response release ordering (contention observed, then release, then all eight owned, 503, full re-ownership).
* `test_slot_ownership_helper_releases_only_what_it_acquired`: forced partial acquisition raises, only seven owned, no over-release, semaphore fully recovered.
* No runtime, cap, config, web or sibling test change. Siblings assert `all(held)` on a fresh app and lack the root cause.

## Evidence (`.venv-1288`, from `src/api`, PYTHONPATH=../core/tests:../agents/tests:tests, logs in session `logs-1288-e11/`)

* Red (controlled; helper temporarily in the old unchecked non-blocking form): 2 tests, 1 failure, 1 error ("acquisition never met a held worker slot", "AssertionError not raised", over-release).
* Green: 3 targeted tests OK; whole `test_resident_demo_api` module 47 tests OK, no skips; 20 repetitions each of the 3 tests all exit 0 (60 repetitions, 3 unique tests).
* `ruff check .` 0, `ruff format --check .` 0, `mypy` 0 (211 files).
* Not run: Core, Agents, full 2546, SQL, browser. Quality code unchanged; earlier Quality browser results are historical reuse, not WCAG or AT acceptance.

## Review (original, direct)

No web edit, so web guidelines not applicable. No sleeps, skips or weakened assertions. The helper's blocking wait is bounded (5 s) and fails loudly. Residual: the exact hosted interleaving remains unproven; hosted CI on the new head is required. Real-provider route OFF. Budget: E11 spent, E12 and E13 remain. Whole #1288 open (Refs only).
