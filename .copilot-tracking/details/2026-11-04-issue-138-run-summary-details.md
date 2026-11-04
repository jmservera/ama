---
title: Details for #138 run summary slice
ms.date: 2026-11-04
---

* `infra/scripts/pipeline.py`: new helpers; append markdown only when `GITHUB_STEP_SUMMARY` is set; ASCII only.
* `infra/tests/test_pipeline.py`: `test_run_summary_is_sanitized_and_absent_when_what_if_fails`.
* `infra/README.md`: PR what-if paragraph.
* `docs/reference/log.md`: appended entry.
