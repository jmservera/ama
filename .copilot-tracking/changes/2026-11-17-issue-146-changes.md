---
title: Issue 146 changes
ms.date: 2026-11-17
---

## Changes

* `infra/monitoring-runbooks.md`: added `### Job ranking` and a pointer in `### Job auth`.
* `infra/tests/test_alert_runbook_signal_matrix.py`: added `test_every_job_suffix_resolves_to_section_naming_it`; file reformatted with ruff at the file's existing 88-column style.
* `docs/reference/log.md`: appended entry.

## Reproduction

Before the runbook edit the new test failed for `rank` and `rank-publish` (resolved to `job-auth`). An `orchestrator` subtest failure was a test pattern error, corrected to accept `job-${applicationPrefix}-<suffix>` forms.

## Validation (FOCUSED tier)

* `python3 -m unittest discover -s infra/tests -p <file>`: test_alert_runbook_signal_matrix (8), test_monitoring_alert_coverage (5), test_ai_alert_runbook_ownership (4), test_monitoring_alerts (8), test_monitoring_workbook (5): all OK, run sequentially.
* `ruff format --isolated --line-length 100 --check`: the pre-existing file already failed at 100 columns (infra tests are outside src-ci); not applicable. mypy and src suites not applicable (no src change).
* Not run: rpi-checks.py (heavy lock held), Bicep build (no Bicep change), Portal/KQL rendering.

## Deferred

Bicep `jobFailures` ranking anchor: infrastructure change, FULL tier.
