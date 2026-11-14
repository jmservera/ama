---
title: Issue 165 api and agents branch coverage floor plan
ms.date: 2026-11-14
---

## Plan

* [x] Phase 1: add `src/agents/tests/test_branch_floor.py` with synthetic fixtures for error and validation branches (see the [details](../../details/2026-11-14/165-api-cov-floor-0038-details.md)).
* [x] Phase 2: add `src/api/tests/test_auth_branch_floor.py` and register it in the existing `disallow_untyped_calls = false` mypy override in `src/api/pyproject.toml`, as other tests of untyped modules do.
* [x] Phase 3: validate with ruff check, ruff format --check, mypy, the new tests, the agents and api suites, and `src/core/tests/test_scenario_manifest.py`.
* [x] Phase 4: write tracking artifacts and commit locally without pushing.

## Critique

One final-candidate critique, performed inline: tests are deterministic (no sleeps, network, cloud or real PII; signal registration is patched; temp directories only), and no production code or gate changes. No finding conflicts with a decision. Verdict: proceed.

## Classification

Focused tier: test-only plus a mypy override for the new test module. No permissions, packages, images or gate semantics change.
