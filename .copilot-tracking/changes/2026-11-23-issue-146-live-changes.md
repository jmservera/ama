# Changes (2026-11-23), Refs #146

## Files

* `infra/scripts/monitoring_live_inventory.py` (new): offline classifier of `az` alert JSON for criterion 1.
* `infra/tests/test_monitoring_live_inventory.py` (new): 7 regression tests.
* `docs/reference/research/issue-146-live6-monitoring-2026-11-23.md` (new), `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

Focused tier (infra tool, no `src` change, no security control, workflow or manifest change). `python3 -m unittest discover -s infra/tests -p "test_monitoring*.py"`: 38 tests OK. `ruff check` and `ruff format --isolated --line-length 100` clean. Classifier run on live read-only JSON: ledger digest enabled; job, poison, IoT disabled; coverage partial. `rpi-checks.py --all` not run. Hosted CI for the exact head not observed. Azure: read-only; no resource created or changed.

## Per-criterion result

| Criterion | Result | Evidence or reason |
| --- | --- | --- |
| Alerts: job, poison, ledger digest, IoT | Unproven (partial) | Ledger digest enabled; job/poison/IoT installed, disabled; no firing drill permitted |
| Workbook: availability, errors, latency, cost vs budget | Unproven | Workbook installed; private-link workspace cannot be rendered from this host |
| Each alert has runbook entry with owner | Unproven | Proposed roles test-enforced; named person is a human decision |
| Tokenomics dashboard beside Azure cost, variance visible | Proven for demo (2026-11-18, not re-run) | `issue-146-live4-monitoring-2026-11-19.md` |
