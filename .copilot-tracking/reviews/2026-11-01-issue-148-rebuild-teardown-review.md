# Review: issue 148 rebuild and teardown automation (2026-11-01)

Changes: [changes](../changes/2026-11-01-issue-148-rebuild-teardown-changes.md)

Execution: one pass, self-review of the diff against the acceptance criteria. Outcome: conformant for criteria 1-3 at unit level; criterion 4 partial.

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 Scripted rebuild, checks between steps, no secret on argv | Met (unit) | `run_rebuild`, `assert_no_secret_argv`; tests `test_full_sequence...`, `test_secret_argv_rejected`, token only in child env |
| 2 Dependency-ordered teardown with budgets, empty inventory | Met (unit) | reused `teardown`; `test_dependency_order_budgets_last_and_empty_inventory` |
| 3 Seeding and staff reconciliation, synthetic only | Met for scripted sequence | `assert_synthetic`, seed and staff stages; roster guard checks email-like values only |
| 4 Dry-run and disposable-environment test | Partial | dry-run proven; tests use a fake `az`, no real disposable Azure run |

## Findings routed to later work

1. Run an authorised disposable Azure rebuild/teardown (closes criterion 4).
2. Add scripted probes for `workload-sql`, `model-standard`, `model-capable` (currently operator-gated, exit 2).
3. The synthetic guard cannot prove directory object IDs in a roster are synthetic; owner must supply a synthetic roster.
4. Teardown treats any group lock as blocking all deletion (conservative).
