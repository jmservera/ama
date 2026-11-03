---
title: Plan, issue 152 per-profile default manifest slice
ms.date: 2026-11-03
---

## Plan

* [x] Phase 1: add `default` block (ids, count, order, selection, empty_reason) to each of the eight implemented profiles in `workbench-manifest.json`.
* [x] Phase 2: add a unit test comparing defaults with role queues and the manifest sort/selection; update `src/api/README.md`.
* [x] Phase 3: run focused unit test, ruff, mypy (`--cache-dir=/tmp/mypy-152`).

Details: [details](../details/2026-11-03-issue-152-workbench-ia-details.md).

Stacked slices after this one: scripts for deferred workflows (technical, procurement, QA, finance, operator); owner device decision.

## Critique (one pass)

Recorded in this plan. Verdict: proceed. Applied: defaults derive from role queues, not fixtures (safety and contractor differ); do not claim AC-034/043 or criterion 1; use Refs #152.
