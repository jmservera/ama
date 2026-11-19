# Issue 114 live r3 changes

No source change. Artifacts only. Tier FOCUSED (no src edit; mypy and ruff not applicable).

Validation: from src/core, `PYTHONPATH=src:tests python3 -m unittest test_recovery test_sqlstore test_ledger_digest_blob -q`: 62 tests, OK, 76.8 s.

| Criterion | Ticked | Status for the demo |
| --- | --- | --- |
| Per-year audit and ledger digest verification proven by test before reliance | No | Proven by test on repository code; unproven on the deployed image (needs image roll and multi-year data, outside owner authorisation) |
| Measured load, latency and cost against PRD targets | Yes | Previously proven (docs/reference/research/sql-ledger-live-2026-11-18.md); not re-run |
| Backup, restore and deletion re-application (DH-005) | Yes | Previously proven, same note; not re-run |

Remaining work is production-only (deployment change). Nothing buildable for the demo.
