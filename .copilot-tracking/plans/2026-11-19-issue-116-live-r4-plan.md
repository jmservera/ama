---
title: Issue 116 live round 4 plan
ms.date: 2026-11-19
---

## Phases

* [x] Phase 1: `reason_roles()` drops `Contractor` from any `ZF_REASON_ROLES` override; docstring records the demo confirmation.
* [x] Phase 2: add focused tests (override cannot grant contractor; defaults pinned to the confirmed set; unset/empty behaviour kept) in `src/api/tests/test_role_matrix.py`.
* [x] Phase 3: research note with the per-criterion proven/unproven table under `docs/reference/research/`, index and log entries.
* [x] Phase 4: targeted tests, mypy for `src/core`, ruff format check; one commit.

Critique: `.copilot-tracking/critiques/2026-11-19-issue-116-live-r4-critique.md`. Details: `.copilot-tracking/details/2026-11-19-issue-116-live-r4-details.md`.
