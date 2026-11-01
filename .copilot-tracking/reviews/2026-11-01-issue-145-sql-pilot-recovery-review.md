# Review: issue 145 SQL pilot tier and recovery (2026-11-01)

Execution: executed once. Outcome: partially conformant; open criteria routed to follow-ups.

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 SKU, auto-pause, redundancy as environment parameters; pilot recorded | Met | `sql.bicep`, `main.bicep`, pilot example, `test_sql_tier.py`, bicep build |
| 2 PITR performed, ledger result recorded | Unmet | Not performed; no authorized disposable Azure infrastructure |
| 3 RTO/RPO stated or undecided with owner | Met as undecided | Runbook objectives table names owners; NFR-004 |
| 4 Backup redundancy and retention match #121 | Unmet | #121 open; retention not decided; redundancy is an owner placeholder |
| RAI restore and erasure criteria | Unmet | Drill blocked on authority; offline tiers not claimed as restore proof |

Findings: none open in the changed code. Routed follow-ups: authorized disposable-server PITR drill with witness; owner RTO/RPO decision; align retention after #121; size vCores from load result.
Decision: PR uses `Refs #145` only.

Post-review addendum: three valid Copilot findings (weak compile test, `bicep` vs `az bicep` skip, invalid ledger verification input) fixed; the restore-ledger verification remains Not performed and is now explicitly blocked on native digest capture. Outcome unchanged.
