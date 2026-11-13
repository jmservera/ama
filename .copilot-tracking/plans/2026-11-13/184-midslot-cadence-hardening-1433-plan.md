---
title: Issue 184 mid-slot cohort exit and cadence validation plan
ms.date: 2026-11-13
---

## Plan

* [ ] P1 RED tests: `test_live_control.py` mid-slot six-home run raises DEMO_COHORT_MISMATCH and main exits 2; `test_live_readings.py` slot_floor/next_slot refuse 0, -60, 30; `test_live_simulator.py` check_capacity refuses 0, -60, 30.
* [ ] P2 Implement `run()` re-check after a fenced slot, and cadence validation in `slot_floor`, `next_slot`, `check_capacity`.
* [ ] P3 Run the listed tests, ruff check, ruff format --check, mypy; independent code-review; commit.

Details: see plan; no schema or signature change; `attempt_permitted` still returns False.

## Critique (rubber-duck, verdict Revise, applied directly)

* PC-001/PC-002: the re-list design is dropped. `attempt_permitted` keeps returning a bool but takes an optional `refusals` list and appends `DEMO_COHORT_MISMATCH` when the control cohort differs. `run()` gets an optional `fence_error` callable; after a fenced slot it raises StreamError for that code. `main()` wires both, so a restored cohort or a plain stop/expiry cannot misclassify. Tests: restore-before-recheck and stop-with-changed-store.
* PC-003: one `lr.require_cadence` helper (exact int in CADENCES) is used by `Generator`, `slot_floor`, `next_slot`, `check_capacity`; tests cover 0, -60, 30, 60.0, True, "60".
