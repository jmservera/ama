---
title: Issue 80 round 2 changes
description: Changes made
ms.date: 2026-11-04
---

Changed: server routes, two screens, README, two test files. No divergences from the plan.

## Validation (focused tier)

Ran from src/api with PYTHONPATH to this worktree: test_list_export_api and test_role_endpoint_inventory (21 OK); ruff check and format check on the project; mypy (cache /tmp/mypy-80, tests included, as CI does) clean; node --check on both JS files.
Not run: gate, benchmarks, full suites, browser or accessibility check of the new links, hosted CI.
