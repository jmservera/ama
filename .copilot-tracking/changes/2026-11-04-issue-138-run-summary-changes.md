---
title: Changes for #138 run summary slice
ms.date: 2026-11-04
---

* `infra/scripts/pipeline.py`: `publish_step_summary`, `what_if_lines`; calls after what-if and successful deploy.
* `infra/tests/test_pipeline.py`: one new test.
* `infra/README.md`, `docs/reference/log.md`: updated.
* Run: `unittest test_pipeline.py` (30 tests; 29 pass; the existing `test_installed_local_api_denies_unauthenticated_requests` errors because the `src/api` package is not installed here and also errors on unmodified main), ruff with the CI flags, format, mypy strict with `--cache-dir=/tmp/mypy-530`.
* Not run: gate, benchmarks, full suites, Azure, Docker, Bicep, hosted CI.
* Area is deployment pipeline: complete gate is the coordinator's job.
