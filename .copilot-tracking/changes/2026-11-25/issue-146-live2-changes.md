---
title: Issue 146 changes, live2
---

Refs #146. Tier: focused (no `src/` change; infra script and infra test only). Basis: read-only inventory tool.

## Files

* `infra/scripts/monitoring_live_inventory.py`: `--jobs`, `uncovered_jobs`, `partial` status.
* `infra/tests/test_monitoring_live_inventory.py`: partial/covered/unchanged and CLI name-only tests.
* `docs/reference/research/issue-146-live9-monitoring-2026-11-25.md`: live evidence.

## Validation

* `python3 -m unittest tests.test_monitoring_live_inventory` (from `infra`): 8 tests OK.
* `ruff check` and `ruff format --isolated --line-length 100 --check`: clean.
* Live run against resource group `ama`: coverage partial; six jobs lack an enabled failure rule.
* Not run: `rpi-checks.py --all`, hosted CI.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Unproven (only ledger digest enabled live) |
| Workbook with availability, errors, latency, cost vs budget | Unproven (deployed copy stale; availability has no data) |
| Each alert has runbook entry with owner | Unproven (no named person) |
| Tokenomics dashboard beside cost record | Proven for the demo in live8; not re-run |
