# Plan: issue 145 SQL pilot tier and recovery proof (2026-11-01)

Research: [research](../research/2026-11-01-issue-145-sql-pilot-recovery-research.md)

## Phases

* [x] 1. Parameterise `modules/sql.bicep` (tier, vCores, auto-pause, backup redundancy, retention) and thread through `main.bicep`; defaults preserve dev.
* [x] 2. Record pilot setting in `main.pilot.example.bicepparam`; explicit dev values in dev params.
* [x] 3. Add `infra/tests/test_sql_tier.py` (text contract plus `bicep build`).
* [x] 4. Add `infra/sql-recovery-runbook.md` (PITR, ledger verify, RTO/RPO undecided, evidence template); link from `infra/README.md`; knowledge log entry.
* [x] 5. Validate: new and existing infra tests, bicep build, ruff, mypy.

## Critique (single pass)

* Provisioned SKU must be `GP_Gen5` with no `autoPauseDelay`/`minCapacity` (invalid for provisioned); guard with conditional objects.
* Do not claim acceptance criteria 2 to 4 as proven: PITR not performed, RTO/RPO undecided, #121 retention undecided. PR uses `Refs`.
* Compatible findings applied directly; none conflict with confirmed decisions.
