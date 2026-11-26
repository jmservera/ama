---
title: Issue 146 live changes (2026-11-26)
ms.date: 2026-11-26
---

Status: complete. Tier: focused (documentation only; no src, Bicep or workflow change; `rpi-checks.py --all` not run).

## Files

* `infra/monitoring-runbooks.md`: live-note paragraph in Status and Authority.
* `docs/reference/research/issue-146-live10-monitoring-2026-11-26.md`: evidence note.
* `docs/reference/README.md`, `docs/reference/log.md`: index and log.

## Validation

* 43 infra monitoring tests pass (`unittest discover -s infra/tests -p "test_monitoring*.py"`).
* Live read-only Azure queries as recorded in the note; hosted CI not observed.

## Per-criterion table

| Criterion | Status | Why |
| --- | --- | --- |
| Alerts: job failures, poison, ledger digest, IoT | Unproven as a whole | Enabled for all classes; 2 of 6 jobs uncovered; no firing or delivery observed (drills not authorised) |
| Workbook: availability, errors, latency, cost vs budget | Unproven as a whole | Queries execute; errors and latency real; availability 0 rows; cost Unknown; no Portal render |
| Each alert has runbook entry with owner | Unproven | 18 of 22 name role and runbook; 4 legacy rules lack both; no named person |
| Tokenomics: AI usage beside Azure cost, variance visible | Proven for the demo | Executed live, variance unreconciled |
