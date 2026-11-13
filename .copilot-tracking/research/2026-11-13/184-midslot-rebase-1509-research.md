---
title: Issue 184 mid-slot rebase research
ms.date: 2026-11-13
---

Research disposition: executed (read-only inspection).

Scope: replay be4013d4ec (sticky mid-slot DEMO_COHORT_MISMATCH exit 2 and require_cadence checks, PR 1524) onto origin/main 8ca5685b71 (post-1518) using `git rebase --onto 8ca5685b71 e2bca0c5eb`.

Findings:

* Branch head be4013d4ec sits directly on e2bca0c5eb (one-minute five-home cadence commit, delivered on main via 1518).
* Commit touches live_simulator.py, live_readings.py, three test files and tracking artifacts.
* Main moved from dafed6a27 with tracking-only changes plus the 1518 landing; conflicts are expected only in src/api live_simulator.py or tracking files, if at all.

Planning Readiness: Ready.
