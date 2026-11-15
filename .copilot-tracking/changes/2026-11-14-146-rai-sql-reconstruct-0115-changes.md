---
title: "Changes: #146 RAI SQL restart reconstruction"
ms.date: 2026-11-14
task_slug: 146-rai-sql-reconstruct-0115
---

## Files

* `src/core/src/zava_forward/core/rai_metrics.py` (new): pure classifier and reconstructor.
* `src/core/src/zava_forward/core/assistants.py`: `Assistants.rai_metrics`.
* `src/api/src/zava_forward/api/server.py`: `GET /api/assistants/rai-metrics` (default last 24 hours).
* `src/api/tests/test_rai_restart_sql_reconstruction.py` (new, failing first on missing module) and an HTTP test in `test_assistants.py`.
* `src/api/pyproject.toml`: new test module added to the existing untyped-fixture mypy override.

## Validation

ruff check, ruff format --check and mypy clean for core, api and orchestrator; new tests, `test_monitoring_coverage`, `test_scenario_manifest` pass; see review for the assistant suites. Hosted CI not run.

## Divergences

None. Worktree runs used PYTHONPATH to the worktree sources.
