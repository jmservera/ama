---
title: Issue 2254 live research (2026-11-23)
---

Planning Readiness: Ready (disposition: executed).

Findings so far: the source fix (hazard column compared in `SqlStore._repair_identity_columns`) and its test (`src/core/tests/test_sqlreads.py`) are on the branch. The 2026-11-22 live note records API counts 23/23/23. The unproven item is the on-screen All cases text with Show only = Safety issue open (the issue's own symptom), which was read from the API only. Plan: capture it live with Playwright.

Result: live capture done, tile 23 and All cases "23 cases" with Safety issue open. Note: [issue-2254-ui-2026-11-23.md](../../../docs/reference/research/issue-2254-ui-2026-11-23.md). Planning Readiness: Ready. No source gap found.
