---
title: Issue 184 mid-slot hardening changes
ms.date: 2026-11-13
---

## Changes

* `live_readings.py`: `require_cadence` used by `Generator`, `slot_floor`, `next_slot`.
* `live_simulator.py`: `check_capacity` validates cadence; `attempt_permitted(refusals=)`; `run(fence_error=)` raises DEMO_COHORT_MISMATCH after a fenced slot; `main()` wires both so exit is 2.
* Tests: RED-first cases in `test_live_readings.py`, `test_live_simulator.py`, `test_live_control.py`.
