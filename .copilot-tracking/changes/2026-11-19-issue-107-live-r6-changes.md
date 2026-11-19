# Changes: issue #107 sixth live pass (no source change, Tier FOCUSED)

Stop reason: the only buildable criterion is already delivered at HEAD; the other needs a human appointment and real-AI authority.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Independent SQL worker/race tests for material mismatches, revocation, restart; old images cannot restore approval or refill | Proven (local actual SQL Server 2022, r4 note); SQLite re-run this session: 30 OK, 15 skipped. Azure SQL/old image from private ACR not proven, not needed for demo | `docs/reference/research/issue-107-live-r4-criteria-2026-11-19.md` |
| Approved exercise record permits bounded proposals only; delivered-build real AI, SQL, Azure acceptance | Unproven | OQ-017 holders unappointed; real AI not authorised; approved side not fabricated |

## Validation

* `python3 -m unittest tests.test_assistant_restart_non_replenishment` in src/api: Ran 30, OK, skipped 15.
* No src change: mypy, ruff and rpi-checks not applicable; `--all` not run. No Azure resource created; credentials not read.
