---
title: Issue 146 live threshold approval plan
ms.date: 2026-11-14
---

Refs #146. Focused tier, `src/core` only.

* [x] Phase 1: add `named_human` and live approver gate in `rai_release.py`.
* [x] Phase 2: add `live`/`now` to `cohort_eval.evaluate` (constructed, non-human, expired blockers not disposable).
* [x] Phase 3: add `tests/test_rai_threshold_live_approval_guard.py`.
* [x] Phase 4: ruff, mypy, unittest, existing RAI and cohort suites.

Details: [details](../../details/2026-11-14/threshold-live-approval-guard-details.md). Critique executed once: compatible, no conflicts; default offline behaviour kept.
