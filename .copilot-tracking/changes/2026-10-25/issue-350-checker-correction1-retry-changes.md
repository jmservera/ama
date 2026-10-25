<!-- markdownlint-disable-file -->
---
title: Issue 350 checker correction 1 retry changes
description: Changes recorded by the forward-ordered retry
ms.date: 2026-10-25
---

* No source change. `tools/check-demo-feedback.py` and `tools/test_check_demo_feedback.py` remain as in 16e6d12d, retained after the critique found no gap.
* Added retry research, plan, details, plan critique, review, state and this changes record under `.copilot-tracking/` (2026-10-25).
* Actual order: research (07:38:59Z), plan and details (07:39:09Z), critique (07:39:58Z), checks, review, then these records and the commit.
* Checks: 80 of 80 tests; CLI exit 2 on 10000-deep input; admin fixture pass, admin_account not-run.
