# Changes: issue 145 live (2026-11-23)

Tier: focused (test-only; no src, workflow or Bicep change; no `rpi-checks.py --all`).

## Files

* `infra/tests/test_sql_tier.py`: new `test_runbook_parameter_table_matches_bicep_defaults` (runbook table vs Bicep, main and pilot defaults); `re` import; ruff format of one pre-existing unformatted line.
* `docs/reference/research/issue-145-live-20261123-2026-11-23.md`: read-only Azure observation and criterion table.

## Validation

* `python3 -m unittest infra.tests.test_sql_tier`: 8 tests OK (7 before).
* Mutation: changing the Bicep retention default to 15 fails the new test; reverted.
* `ruff check` and `ruff format --isolated --line-length 100 --check` clean.
* Azure: read-only `az sql` only; nothing created, no drill, no secret read.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| SKU, auto-pause, redundancy parameters (ticked) | Proven | Existing tests, 8 pass |
| PITR restore and ledger result (ticked) | Proven earlier | Earlier research notes; not re-run, drills not authorised |
| Objectives stated or undecided (ticked) | Proven | Runbook |
| Backup redundancy and retention match #121 | Unproven | #121 open, no approved retention decision; deployed Local and 14 days only observed |
| R1 restore actual backup with document and audit state | Unproven | No drill authorised |
| R2 reconcile and reapply tombstones and holds | Unproven | Needs restore |
| R3 no resurrection of revoked or erased state | Unproven | Needs restore and release code |
| R4 DPO and record-owner approval | Waived for demo | Owner decision 2026-11-18 |
| R5 independent qualified witness | Unproven | Worker is not independent |
