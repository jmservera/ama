# Changes: issue 114 live r3

No src change. Tier: FOCUSED (evidence and docs only; no src, SQL, infra or deploy change). rpi-checks.py --all not run.

Added: docs/reference/research/ledger-verification/ (raw run and evidence note), index and log entries.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| C1 Per-year audit and ledger digest verification proven by test before reliance | Proven (unit tests, 40 OK, local implementation) | docs/reference/research/ledger-verification/issue-114-per-year-ledger-verification-evidence-2026-11-18.md |
| C2 Load, latency, cost vs PRD | Ticked on the issue; the merged issue-114-live and r2 records hold that evidence; not re-examined in r3 | Issue closure review 2026-11-18 |
| C3 Backup, restore, deletion (DH-005) | Ticked on the issue; the merged issue-114-live and r2 records hold that evidence; not re-examined in r3 | Issue closure review 2026-11-18 |

Unproven for the demo: deployed image does not contain verify_ledger_before_reliance (owner image roll needed; no production change authorised).

Validation: unittest command in the evidence note, exit 0; link and diff review. mypy/ruff n/a (no code).
