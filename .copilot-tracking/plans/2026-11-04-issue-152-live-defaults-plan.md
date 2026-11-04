---
title: Plan, issue 152 live default queue check
ms.date: 2026-11-04
---

## Plan

* [x] Phase 1: add `src/api/tests/test_workbench_live_defaults.py` (real loopback API, constructed fixtures, password auth).
* [x] Phase 2: update `src/api/README.md` paragraph on the manifest.
* [x] Phase 3: focused tests, ruff, mypy (`--cache-dir=/tmp/mypy-530`).

Details: [details](../details/2026-11-04-issue-152-live-defaults-details.md).

## Critique (one pass)

Verdict: proceed. No UI, security, SQL, infrastructure or deployment change, so the focused tier applies. Do not claim full AC-034/043 or criterion 1. Use Refs #152. Later slices: scripts for deferred workflows, owner device decision, selection/focus and no-match checks.
