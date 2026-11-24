---
title: Issue 2255 live plan
description: Plan and single critique for demo hazard clock seed
ms.date: 2026-11-24
---

Plan: add `src/core/src/zava_forward/core/demo_hazard_clock_seed.py` (inspect, apply, revert; mirrors `demo_handoff_due_seed.py`) plus focused unit tests in `src/core/tests/test_demo_hazard_clock_seed.py`. Details: [details](../details/2026-11-24-issue-2255-live-details.md).

Critique (executed once, verdict proceed):

* Risk: guessing a missing timestamp for real data. Direct disposition: touch only open hazards with neither `aware_at` nor `response_due_at`, mark each with `demo_clock_seed` so revert is exact, and state synthetic demo assumption.
* Risk: changing the hazard service. Disposition: no change to taskqueues; the tool writes only the recorded fields that service already reads.
* Risk: live write not authorised. Disposition: ship tool, prove locally, record live criterion as unproven with owner step.
* Tier: FULL because src changes (no `rpi-checks.py --all` run here; coordinator owns the gate).
