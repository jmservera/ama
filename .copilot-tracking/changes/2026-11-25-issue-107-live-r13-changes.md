# Changes: issue 107 r13 (2026-11-25)

Tier: FULL (src/api code); rpi-checks.py --all not run. No tokens spent, no Azure change.

## Files

* src/api/checks/assistant_real_ai_acceptance.py (new): fail-closed capped harness, dry-run CLI.
* src/api/tests/test_assistant_real_ai_acceptance.py (new): 8 tests, OK.
* docs/reference/research/issue-107-live-r13-real-ai-harness-2026-11-25.md, docs/reference/README.md, docs/reference/log.md.

## Validation

Unit tests 8 OK; ruff check and format clean; `PYTHONPATH=../core/src:../agents/src python3 -m mypy` clean. Witness note: implement-start was recorded with the harness file already written (witness qualification: source dirty at implement-start); no test was written before it.

## Per-criterion table (unticked criteria)

| Criterion | Status | Basis |
| --- | --- | --- |
| Independent SQL/worker/race tests; old images and restarts cannot restore revoked approval or replenish allowances | Unproven | Only r12 evidence (11 of 13 fields in separate processes, SQLite and disposable SQL Server); no older packaged image run |
| Approved exercise record permits bounded proposals only; delivered-build real AI, SQL and Azure evidence | Unproven | No approved release (OQ-017), OQ-018/OQ-019 open, tokens not to be spent; harness ready and tested offline |
