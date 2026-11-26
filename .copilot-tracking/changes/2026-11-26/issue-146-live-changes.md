---
title: Issue 146 changes, live (2026-11-26)
---

Refs #146. Tier: focused (no `src/` change; infra Bicep, runbook and infra test). Basis: opt-in rule, no deployment, no gate or permission change.

## Planned files

* `infra/live-simulator-job.bicep`: opt-in `failureAlert`.
* `infra/monitoring-runbooks.md`: `Job live simulator` entry with owner.
* `infra/tests/test_monitoring_alert_coverage.py`: coverage of the new rule.
* `docs/reference/research/issue-146-live10-monitoring-2026-11-26.md` and `docs/reference/log.md`.

## Validation

* `az bicep build --file infra/live-simulator-job.bicep`: OK.
* From `infra`: `test_monitoring*` 44 OK; `test_alert_runbook_signal_matrix`, `test_bicep_policy`, `test_ai_alert_runbook_ownership` 77 OK. First run failed on the matrix test (rule name `${job.name}`); fixed to `${jobName}`.
* `ruff check` clean. Not run: deployment, hosted CI, `rpi-checks.py --all`.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Unproven as a whole (ledger digest proven) | Live inventory in the live10 note; others disabled or uninstalled, enabling needs named-human approval |
| Workbook with availability, errors, latency, cost vs budget | Unproven | Deployed copy stale; no Portal render; redeploy not authorised |
| Each alert has runbook entry with owner | Partly proven (roles proposed, no named person) | New `job-live-simulator` entry; tests pass |
| Metered AI usage beside Azure cost record, variance visible | Proven for the demo (live8) | Not re-run |
