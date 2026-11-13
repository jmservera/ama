# Plan: 165 sensor and stock seed trace

Tracking-only write surface; Focused tier. No edits to `src/` or `docs/`.

1. Critique plan (independent) before any execution.
2. Create `/tmp/venv-165-1105` (system-site-packages), pip install --no-deps -e src/core and src/api; verify paths inside worktree.
3. Run `test_sensor_backfill`, `test_sensor_stock`, `test_stock_fabric`, `test_stock_reconciliation`, `test_generated_dataset` (unittest).
4. Run read-only probe `/tmp/probe-165.py` (copy hash recorded): build seed 20260901 as-of 2026-10-13 with the tests' fictional register; for the five runbook ids report anchor, `stock_epc.conflict_type`, `stock_reconciliation`, sensor-key presence, whether anchor is in a sensor-backfill register selection (consent granted); list case IDs with non-empty conflict_type and open state.
5. Record findings, hashes and exit codes in changes file; remove venv and probe; review; commit.
