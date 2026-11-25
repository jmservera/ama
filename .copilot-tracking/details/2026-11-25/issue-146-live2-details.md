---
title: Issue 146 details, live2
---

Phase 1: in `classify`, when `jobs` is given, uncovered = jobs lacking an enabled rule named `alert-{job}-failed`. If class status would be `enabled` and uncovered is non-empty, status is `partial`; add `uncovered_jobs` to the job_failure entry. Top-level `coverage` stays `partial` when any class is enabled or partial.
Phase 2: tests in `infra/tests/test_monitoring_live_inventory.py`.
Phase 3: `python3 -m unittest` on that file, `ruff check` and `ruff format --isolated --line-length 100 --check`.
