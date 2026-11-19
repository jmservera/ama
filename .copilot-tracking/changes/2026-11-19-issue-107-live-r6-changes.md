# Changes: issue #107 sixth live pass (no source change, Tier FOCUSED)

Stop reason: every remaining criterion is either already delivered at HEAD or needs a human appointment and real-AI authority; nothing further can be built for the demo.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Independent SQL worker/race tests for material mismatches, revocation, restart; old images cannot restore approval or refill | Proven on local actual SQL Server 2022 (r4 note); SQLite re-run this session at current head: 30 OK, 15 skipped. Azure SQL and a pulled old image are not proven and not needed for the demo | `docs/reference/research/issue-107-live-r4-criteria-2026-11-19.md` |
| Approved exercise record permits bounded proposals only; delivered-build real AI, SQL, Azure acceptance | Unproven | No approved release (OQ-017 holders unappointed); real AI not authorised; no approved side fabricated |

## Validation

* `python3 -m unittest test_assistant_restart_non_replenishment -q` in `src/api` with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`: Ran 30, OK, skipped 15.
* No src change: mypy, ruff and rpi-checks not applicable; `--all` not run. No Azure resource created; credentials not read. Nothing ticked on the issue.
* Witness: the first `plan-done` call was refused (artifacts not yet in the state file, my error); the retry succeeded. Original refusal preserved.
