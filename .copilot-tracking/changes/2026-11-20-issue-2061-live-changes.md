# Changes: issue 2061 (2026-11-20)

Refs #2061. Owner option A, demo only. Nothing pushed or deployed; read-only Azure only.

## Files

* infra/main.bicep, modules/identity.bicep, modules/containerapps.bicep, modules/guard.bicep: `demoSingleEnvironment`, guard, internal identity, jobs moved to it.
* infra/role-assignments.json, scripts/create-sql-users.py: internal roles and SQL grants.
* infra/tests (4 files): expectations and 3 new profile tests; guard count 33.
* infra/demo-single-environment-runbook.md, infra/README.md, docs/adrs/0008, docs/reference research note, README index and log.

## Validation

* `az bicep build --file infra/main.bicep`: OK.
* `python3 -m unittest discover -s infra/tests -q`: 740 tests, 1 error (`src/agents/tests/test_dispatch.py` imports missing `opentelemetry`; the same single error occurred before the change), 4 skipped.
* ruff check and format on changed Python: 14 findings, identical before and after the change (pre-existing).
* what-if on group `ama` (reconstructed parameters): 0 Delete.
* Tier: infra change classified FULL, but the full gate (`rpi-checks.py --all`) was forbidden for this run and was NOT run; no receipt exists. Hosted CI not observed.

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | ADR | Proven (Proposed; owner approvals open) |
| 2 | Bicep and what-if | Proven (0 Delete; parameters reconstructed) |
| 3 | Delete list | Partly proven (LB and public IP ids unreadable, managed group access denied) |
| 4 | Entra table and sign-in | Unproven (Graph denied, no deploy) |
| 5 | Identities and negative test | Partly proven (matrix and tests; negative test needs deploy) |
| 6 | End-to-end demo | Unproven (no deploy) |
| 7 | Production build and gate receipt | Partly proven (build and tests; no gate receipt) |
| 8 | Rollback | Written, not exercised |

Details: docs/reference/research/issue-2061-demo-single-environment-profile-2026-11-20.md
