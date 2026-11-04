---
title: Issue 193 round 6 research
ms.date: 2026-11-04
---

Research disposition: reused (issue comment, merged PR history and a fresh code check).

* Delivered: criteria 1 and 2 (scenarios and exercise labels, #505 and #635). #700 added `test_retrofit_scenario_consumers.py`, which uses test-local oracle helpers, not production code.
* Gap: criterion 3 needs the scenarios used by #133 and #111 tests. Production consumers exist on main: `sensor_analysis.derive_signal` (#111) and `AftercareRegister` (#133). No test drove the retrofit scenarios through them.
* Planning readiness: Ready. Test-only slice in `src/core/tests`; no production change, no SQL, no infrastructure. Focused tier.
* Note: the worktree was on `feat/issue-193-r5`; `feat/agent-chat-skills-530` is checked out in another worktree.
