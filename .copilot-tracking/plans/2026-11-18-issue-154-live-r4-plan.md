---
title: Plan for #154 live round 4, representative grants for the deployable demo
ms.date: 2026-11-18
---

## Plan

* [x] Phase 1: add `src/api/src/zava_forward/api/resident_demo/rep_grants.py`, a fail-closed loader for a local synthetic grants JSON file named by `ZF_DEMO_REP_GRANTS_PATH`.
* [x] Phase 2: wire the loader into `__main__.main()`; absent variable keeps current behaviour.
* [x] Phase 3: focused tests in `src/api/tests/test_rep_grants.py` including an HTTP round trip through `ResidentDemo`.
* [x] Phase 4: validate (unit tests, mypy, ruff), record changes and review.

Details: [details](../details/2026-11-18-issue-154-live-r4-details.md). Critique: [critique](../critiques/2026-11-18/issue-154-live-r4-critique.md).
