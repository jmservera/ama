# Changes: issue 225 finance and grants screens (2026-11-01)

* `src/api/src/zava_forward/api/web/role-screens.js`: registers "Invoice queue" (`finance-invoices`) and "Funding route and claim pack" (`finance-funding`) for FINANCE_ROLES; reuses the #226 helpers and `assetCost`. Read-only, no controls, no server change.
* `src/api/tests/test_finance_grants_screens.py`: 6 node-harness tests (line comparison, unknowns, conflicts, evidence, no controls, AI economics Unknown).

Review round 2 (4 Copilot threads, all valid): invoice amount labelled "line total"; milestone_ref shown as supplied, unverified reference with acceptance Unknown; unchecked invoices show "Unknown. Not checked yet" in the queue instead of 0 exceptions; unreadable /form-review keeps claim-pack readiness and holds Unknown. Added test_unchecked_queue_row_and_unreadable_review_stay_unknown.

Validation: new and existing role-screen tests pass; ruff check, ruff format --check and mypy clean for src/api. Full discovery not run (focused tier). No heavy gate by owner direction; CI is the evidence.
