---
title: Issue 1828 CI correction cycle 2 plan
description: Plan to correct the mypy patch target in the viewport premise test
ms.date: 2026-11-16
ms.topic: reference
---

## Plan

Research: [research](../../research/2026-11-16/issue-1828-ci-correction-research.md). Details: [details](../../details/2026-11-16/issue-1828-ci-correction-details.md). Critique: [critique](../../critiques/2026-11-16/issue-1828-ci-correction-critique.md). Tier FOCUSED.

* [ ] Phase 1: change `patch.object(check_module.time, "monotonic", monotonic)` in `src/api/tests/test_map_viewport_premise.py` to `patch("checks.map_fullscreen_browser_check.time.monotonic", monotonic)`; no other line changes.
* [ ] Phase 2: verify with bare `mypy` from `src/api` (CI parity), the focused unittest, map sensor, role and browser harness regressions, `ruff check` and `ruff format --check`.
* [ ] Phase 3: if `/tmp/ama-rpi-heavy.lock` is free, run the full `checks.map_fullscreen_browser_check` with pinned axe twice on the new head and keep external logs; otherwise state the check is pending.
* [ ] Phase 4: changes record, one review, commit with the jmservera noreply identity and trailers. No push, PR or merge.

Not changed: harness logic, assertions, virtual clock, application, authorization, consent, map and keyboard behaviour.
