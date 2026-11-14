# Review: authority rotation guard (Refs #107)

Execution: one self-review of the diff, run once. Outcome: no blocking findings. Independent exact-head review and human approval remain required.

## Findings routed to later work

* An operator who legitimately needs a larger allowance has no approved path; rotation now inherits the lowest stored ceilings, consistent with the existing same-token rule. A deliberate ledger reset needs its own decision.
* The brief cites `consumption_allowance_version`; no such field exists in code, so the guard keys on the persisted allowance ledger.
* Tests cover SQLite only; the MSSQL path uses the same SQL shapes but was not exercised.

## C1 correction revalidation

Execution: formatting-only correction, whitespace removal in one test file, no behaviour change. Outcome: no new findings. `ruff check .`, `ruff format --check .` and `mypy` pass in `src/api`; 14 restart non-replenishment tests pass. Hosted CI on the new head, independent exact-head review and human approval remain required. Refs #107 only.
