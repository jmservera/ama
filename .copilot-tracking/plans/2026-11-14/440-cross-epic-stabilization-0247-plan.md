---
title: Cross-epic stabilization journey plan (#440)
ms.date: 2026-11-14
task_id: 440-cross-epic-stabilization-0247
---

## Plan

Refs #104, Refs #149, Refs #165, Refs #440. Validation tier: focused (test-only, no gate, workflow, dependency or deployment change).

* [x] Phase 1: add `src/api/tests/test_cross_epic_stabilization_journey.py`, fully annotated, mypy-strict clean. Details: [details](../../details/2026-11-14/440-cross-epic-stabilization-0247-details.md).
* [x] Phase 2: run `mypy`, ruff check and format check, and the targeted unittest module.
* [x] Phase 3: write changes and review records; commit locally with the Co-authored-by trailer; no push.

## Critique (one pass, final candidate)

Verdict: proceed. Compatible findings applied directly: do not scan the whole fixture for personal-data patterns because it holds invented phone and postcode values; assert a subset of listed cases; do not touch `pyproject.toml` or `docs/reference/log.md`.
