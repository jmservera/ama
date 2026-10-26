<!-- markdownlint-disable-file -->
---
title: Issue 350 checker correction 1 plan
description: Surgical checker and test correction for two review defects
ms.date: 2026-10-25
---

* [x] Phase 1: failing regressions (deep nesting, admin-only `/api/me`, admin negative cases) in `tools/test_check_demo_feedback.py`.
* [x] Phase 2: explicit `RecursionError` handler in `load_evidence`; separate admin branch in `check_me` (empty counts and staff, `app_admin` true, work_queues contract); `identity` added to the runtime namespace.
* [x] Phase 3: one independent review, record, commit, full gate, normal push.

Out of scope: application or auth changes, Azure, Graph, roles, live AI. Critique was not run before implementation (see research disclosure); the post-implementation review is the only independent gate.
