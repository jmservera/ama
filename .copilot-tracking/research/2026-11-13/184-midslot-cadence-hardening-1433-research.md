---
title: Issue 184 mid-slot cohort exit and cadence validation research
ms.date: 2026-11-13
---

## Scope

Refs #184. Child hardening of `e2bca0c5e` closing two non-blocking review comments.

## Findings

* Medium: `attempt_permitted` returns False on a mid-slot control cohort change (`src/api/src/zava_forward/api/live_simulator.py`). `_permitted` swallows errors, `send_slot` records `RUN_CONTROL_FENCED`, `run()` returns after a FENCED slot and `main()` returns 0. The `DEMO_COHORT_MISMATCH` refusal is lost.
* Existing test `test_sixth_home_added_mid_slot_fences_the_next_attempt` requires `attempt_permitted` to keep returning False, so the signature and result stay.
* Low: `lr.slot_floor`/`next_slot` divide by `seconds // 60` (ZeroDivisionError on 0, silent wrong floor on 30 or negative); `check_capacity` divides by `cadence_seconds`. Only `Generator` validates against `CADENCES`.

## Design

* In `run()`, after a FENCED slot, re-run `list_homes()` once; a `DEMO_COHORT_MISMATCH` StreamError is raised, other failures keep the current fenced return. `main()` already maps StreamError to exit 2.
* `slot_floor` and `next_slot` raise `LiveReadingError("INVALID_CADENCE")` unless `seconds in CADENCES`; `check_capacity` raises `ValueError` for a cadence outside (60, 300).

Planning Readiness: Ready.
