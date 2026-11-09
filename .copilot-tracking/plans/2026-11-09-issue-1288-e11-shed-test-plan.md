---
title: Issue 1288 E11 shed test ownership plan
ms.date: 2026-11-09
---

# Issue 1288 E11 plan (prospective)

* Scope: `src/api/tests/test_resident_demo_api.py` only. No runtime, cap, config or web change.
* Steps: (1) add a focused regression that delays the post-response worker release through an instrumented (labelled, test-local) semaphore wrapper and requires the shed test's slot-ownership helper to own all eight slots; run it failing-first against the old unchecked non-blocking acquisition. (2) Fix by a helper `own_every_slot` that acquires each slot with a bounded blocking timeout, asserts success, and returns the count actually acquired; the shed test releases only that count. 503, JSON retry guidance, Retry-After, signed-in GET and normal admission assertions stay. No sleeps, skips or cap change.
* Validation: entire `test_resident_demo_api` module; 20 bounded repetitions of the exact test and of the new regression (recorded as repetitions); API ruff, format, mypy from `src/api` with `.venv-1288`. No Core, Agents, SQL, browser or full runs: Quality code unchanged, so earlier browser results are historical reuse, not WCAG or AT acceptance.
* Budget: E11 spent after this; E12 and E13 remain under the owner authorization of 2026-11-09T22:14. Real-provider route OFF.
