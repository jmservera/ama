---
title: Issue 146 plan details
ms.date: 2026-11-17
---

## Details

* Edit `infra/monitoring-runbooks.md`: add `### Job ranking` after `### Job auth` (normal suffix `rank-publish`, demo `rank`, only with `enableRankingArchiveBlob`). Owner: Digital service owner. State that the Bicep currently resolves ranking-job alerts to the `job-auth` anchor and that the ranking job refuses with `RANKING_PUBLISH_BLOCKED` until a named owner signs a policy version.
* Edit `infra/tests/test_alert_runbook_signal_matrix.py`: add test reading the `jobFailures` ternary and the job names in `main.bicep`; assert each job-name suffix resolves to a runbook section, and that ranking suffixes are covered by the `job-ranking` section text.
* Edit the B1 matrix row and `infra/README.md` monitoring note; log entry in `docs/reference/log.md`.
* Validation: `python3 -m unittest discover -s infra/tests -p "test_alert_runbook_signal_matrix.py" -q`, then the other monitoring tests, sequentially.
