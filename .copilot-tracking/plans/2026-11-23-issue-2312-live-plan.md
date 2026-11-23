---
title: Issue 2312 live plan (2026-11-23)
ms.date: 2026-11-23
---

## Plan

Details: [details](../details/2026-11-23-issue-2312-live-details.md). Tier: FULL only if src changes; this change adds src code, but the owner brief fixes the focused tier with targeted tests, mypy and ruff; `rpi-checks.py --all` is not run.

* [x] Phase 1: write `eval_harness.py` (`validate_manifest`, `run_eval`, `verify_recorded`).
* [x] Phase 2: add `src/agents/evals/eval-manifest.schema.json`, `synthetic-eval-manifest.json`, `synthetic-eval-predictions.json`.
* [x] Phase 3: add `test_eval_harness.py` covering the four criteria; run tests, mypy, ruff.
* [x] Phase 4: README note, changes record with per-criterion table, review.
