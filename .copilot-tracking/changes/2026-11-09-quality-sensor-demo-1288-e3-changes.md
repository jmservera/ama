---
title: Changes - issue 1288 E3
---

# Changes: issue 1288 E3

Plan: [plan](../plans/2026-11-09-quality-sensor-demo-1288-e3-plan.md).

## Commits (local, no push)

* `ed6f14f1b` test(quality-sensors): type E2 test helpers without suppression. Files: `src/api/tests/test_quality_sensors.py`, `_c7.py`, `_e1.py`, `_e2.py`, `test_assistants.py`. Diagnostic-level result: 141 new to 0 new against `c772364`, same pinned tool and config; no `ignore`, stub or `cast` added.
* `4b8d87801` merge of pinned main `23e944c1f` (IoT 1304). Single conflict in `core/sensor_consumer.py` imports, both kept.
* E3 candidate commit: regression test `Boundary.test_no_spoofed_simulation_claim_releases_captured_readings_to_a_real_ai` in `test_quality_sensors_e2.py` plus these RPI artifacts.

## Divergences and honest notes

* Part 2 was frozen, not implemented (see research Conclusion); no source, switch, store, token or web file changed.
* The new test passed on first run (green, no red): it locks existing E2 behaviour against spoofed claims. It is not model, live, real-AI or AT evidence.
* The test was drafted before the plan and critique were written (disclosed in the critique).
* E2's "126" untyped-test count could not be reproduced; the same-tool comparison found 141 before the fix. Both are preserved.
* First nonqueued shared-lock attempt for owned SQL found the lock held by another worktree; the retries are logged in `logs-1288-e3/e3-sql-lock-busy-124054.txt`.

## Validation record

Filled in at review from `logs-1288-e3/` (coordinator files, not committed).
