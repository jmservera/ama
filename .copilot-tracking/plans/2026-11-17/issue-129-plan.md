---
title: Issue 129 plan (2026-11-17)
description: Protocol-versus-scorer drift test and protocol doc refresh
ms.date: 2026-11-17
---

## Plan

* [x] P01 Add `test_protocol_bundle_table_matches_scorer` to `src/core/tests/test_learning_test_bundles.py`: parse the doc bundle table and compare title, atlas IDs, comparator, requirements and stop rule to `BUNDLES`. Verify it fails on a mutated doc copy (measure) before passing.
* [x] P02 Update the protocol doc: `ms.date`, Next slices (CLI slice #1374, scenario tests), keep criteria unmet.
* [x] P03 Run targeted core tests, ruff format, mypy; doc link test.

Details: `.copilot-tracking/details/2026-11-17/issue-129-details.md`. Critique: compatible; direct dispositions only. Out of scope: SQL, security, infra, #1818/#1641, live runs.
