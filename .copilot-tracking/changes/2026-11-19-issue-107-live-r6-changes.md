# Changes: issue #107 r6 (2026-11-19)

Tier: FOCUSED. No source edits; mypy and ruff not applicable. Validation: `python3 -m unittest tests.test_assistant_restart_non_replenishment tests.test_assistant_release -q` from `src/api`: 95 tests OK, 22 skipped (need `ZF_TEST_MSSQL=1`).

Files: new `docs/reference/research/issue-107-live-r6-criteria-2026-11-19.md`; appended `docs/reference/log.md`; index row in `docs/reference/README.md`.

| Criterion | Status | Basis |
| --- | --- | --- |
| Independent SQL connection/worker and race tests (mismatch, revocation, restart; old images cannot restore or replenish) | Proven for the demo | SQLite run above; actual SQL in the r4 note (30 tests, 0 skipped) |
| Matching approved exercise record, bounded proposals only; delivered-build real AI, SQL, Azure evidence | Unproven | Needs OQ-017 release holders and real-AI authority (human) |

Refs #107.
