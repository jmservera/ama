# Plan and details amendment: gate tier correction (#1292)

Dated 2026-11-08. Prospective correction. The original focused-tier plan
(`2026-11-08-priority-order-1292-plan.md`) and details
(`2026-11-08-priority-order-1292-details.md`) are preserved unchanged.

## Correction

The fix adds an immutable creation-order column (`created_ord`) and a SQL
migration with a backfill. These are SQL schema and migration changes. The
repository instructions and coordinator policy require the FULL local gate
(`python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory>`,
then `--verify-receipt`) before publication. The original focused tier
(`--changed`) is insufficient for this candidate.

## Evidence classes

* Focused SQL evidence (this continuation): native disposable SQL Server
  red/green for the two original #1292 selectors and the `MssqlPriorityOrder`
  class. This is targeted behavioural evidence, not the complete gate.
* Complete gate: NOT run here. #184 has priority on the shared heavy
  resource. The coordinator routes a separate clean exact-head full gate,
  receipt verification, independent exact-head review and hosted CI.
* Ledger-enabled SQL Server migration: unproven unless separately tested.
* Human and legacy-data decisions are unchanged: a named data owner decides
  whether a live database needs ordering review after backfill.

## Added steps

1. Confirm head, tree and tracked status; no product edits.
2. Inspect the lock holder, disk and memory; use `flock -n` for the whole
   disposable SQL operation; never queue.
3. Run red (base source plus new tests) then green (candidate source) with
   `ZF_RESIDENT_MSSQL=1` on a newly created task-owned container only.
4. Commit a dated changes and review addendum plus state update.
