# Changes: issue 145 live (Refs #145)

Tier: FOCUSED, documentation only. No src, infra or workflow file changed. No Azure resource created or modified.

Files: docs/reference/research/issue-145-live-20261119T1024Z-2026-11-19.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry).

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| C1 | SKU, auto-pause, redundancy parameters | Proven (ticked) |
| C2 | PITR and ledger result | Proven (ticked; native verify denied) |
| C3 | Objectives stated or undecided with owner | Proven (ticked) |
| C4 | Backup redundancy and retention match #121 | Unproven: production-only, no approved decision (#1906) |
| R1 | Actual backup restored with documents and audit | Partly proven: no blob PITR, no drill authorised |
| R2 | Reconcile, reapply tombstones and holds | Partly proven: no legal hold state |
| R3 | No resurrection of release, suspension, allowance | Unproven: needs src fix at FULL tier, not permitted here |
| R4 | DPO approval | Waived for the demo |
| R5 | Independent qualified witness | Unproven: production-only |
| R6-R8 | Disposable limits, labelling, counts only | Proven (ticked) |

## Validation

Link and diff review of the three changed files. Unit tests, mypy and ruff not applicable (no code change).
