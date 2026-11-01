# Changes: issue 225 finance and grants screens (2026-11-01)

* `src/api/src/zava_forward/api/web/role-screens.js`: registers "Invoice queue" (`finance-invoices`) and "Funding route and claim pack" (`finance-funding`) for FINANCE_ROLES; reuses the #226 helpers and `assetCost`. Read-only, no controls, no server change.
* `src/api/tests/test_finance_grants_screens.py`: 6 node-harness tests (line comparison, unknowns, conflicts, evidence, no controls, AI economics Unknown).

Validation: new and existing role-screen tests pass; ruff check, ruff format --check and mypy clean for src/api. Full discovery not run (focused tier). No heavy gate by owner direction; CI is the evidence.
