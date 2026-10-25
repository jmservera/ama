# Research: seed the demo `retrofit` database (issue 360)

Date: 2026-10-25 (written 07:5x-08:0x Z). Task: seed-demo-baseline-360. Topic branch `feat/seed-demo-baseline-360` from origin/main 36996d70 (new worktree `issue360-seed-baseline`). Research disposition: executed, read-only, no live call and no source edit before this file.

## Requirement (owner, 2026-10-25T07:56Z)
Seed the existing demo `retrofit` database (Standard S0) with the continuing synthetic 980-case baseline so the app can be tested. Not allowed: drop/recreate, audit deletion, clearing tables, new paid DB, RBAC grants, network relaxation, provider activation, binding synthetic staff to real people. Preserve the existing 1 case, 1 recommendation, 2 audit rows and all meta/Entra configuration. Expected total is 981 cases (980 plus the proof case), reported exactly, not forced to 980.

## Prior diagnosis (this session, read-only)
Live counts through the app PTY exec: cases 1, open 1, staff 0, recommendations 1, audit 2, meta keys as_of, continuity, entra_people, queue_context, queue_generation, rank_policy, seq, support_encoding. Only `ca-cutover-test-demo-api` and `ca-cutover-test-api` point at this database.

## Existing store and seed facts (origin/main 36996d70)
* `SqlStore._seed` (sqlstore.py:404-432) inserts only when `SELECT COUNT(*) FROM cases` is 0, in one transaction. It never merges, so on a database holding the proof case it is a silent no-op. `MssqlStore` inherits it unchanged.
* The seed JSON keys the store reads: `cases`, `staff`, any of `DOCS` (procurement, governance, continuity, buildings, form_schemas, bulk_edits), optional `as_of`. It does not read `recommendations`.
* A normal write (`save`, sqlstore.py:571-) runs inside `BEGIN IMMEDIATE`: it validates, writes cases with `seq = meta.seq + 1` and `rowversion`, writes documents, calls `_refresh_queue_membership`, appends audit with `_append_audit` (hash chained from `audit_head`), updates `meta.seq`, then commits; any error rolls back. Other replicas reload through `seq`.
* `_refresh_queue_membership(None)` recomputes queue flags for all cases and bumps `queue_generation`.
* `_row(c)` builds the derived case columns; `CASE_COLS` insert pattern is the one `_seed` uses (`INSERT INTO cases (id, rowversion, seq, ...)`).
* The audit table is ledger or trigger protected, append only. Appending is permitted; update and delete are not.
* Searched for an existing merge, upsert or reseed route in src, infra and tools: none. `test_buildings.py:201` and `src/core/README.md` state populated stores are deliberately not reseeded. `private-cutover-proof.py` seeds only its one fictional case and asserts no staff.

Conclusion: there is no supported non-destructive route, so a minimal seed-merge operation is needed. The owner's rule allows this through the ordered RPI loop with focused tests.

## Baseline provenance
* Generator: `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py --seed 20260901 --as-of 2026-10-13 --out <private dir>/zavaforward.json` (research README lines 59-62). Reads the tracked stock-geography register as an explicit synthetic input; output has real OSM addresses with fictional people. Same seed and as-of give identical bytes (test_generated_dataset). It also writes `<out>.coverage.json`, a receipt.
* Expected counts from docs: 980 programme cases, 443 open, 38 booked visits, 11 staff, one procurement package with 601 orders (infra README 1486-1491, 3064). These are historical docs figures; the actual generator output is the authority and will be reported unforced.
* The 60,000-home register is a separate denominator (seed 4820260930), not SQL cases.

## Compatibility risks identified
1. Case id collision with the proof case (`CASE_ID` in private-cutover-proof). Expect none; the guard must abort rather than overwrite.
2. Seed documents (procurement, buildings, and others) versus an existing meta row: absent keys can be added; a present key with different content must abort, never overwrite. The existing `continuity` key must be preserved.
3. `as_of` meta exists already (init ran 2026-10-25). The fresh-seed path would set the seed's as_of; for a merge it must be preserved, and the difference reported. Consequence to report: 2026-10-13 visits will appear past relative to the live as_of.
4. Staff: the seed holds 11 synthetic staff rows with emails. Under Entra-authoritative access, staff rows are not login authority, and the proof verifier expects zero staff. Default: do not add staff; an explicit option only.
5. The recommendations table (1 row) and audit (2 rows) must be unchanged. One appended audit event for the merge is the only addition, hash chained from the current head.
6. Azure SQL ledger: inserts into cases and meta are normal DML; no DDL is needed, so the CHECK/default migration risk fixed in PR450 does not recur. The API identity has datareader, datawriter, ddladmin; the merge needs no new grant.
7. Queue refresh over 981 cases is heavy but bounded; it runs inside the transaction.
8. Transport: the VM cannot reach private SQL, and the deployed image 0769b52d lacks the new code and the seed. Existing PTY exec can run only what is inside the container. The route to run the merge live must be planned separately and may need a reviewed image or job; unresolved at this point.

## Open questions for the plan
* Merge location (SqlStore method versus a standalone module) and CLI shape.
* Local rehearsal target for SQL Server (the #350 container must not be touched; a separate throwaway DB or container is needed).
* How the generated seed reaches the live container without storing data in a public path.

## Limits
This research reads code and docs only. No generator run, no live write, no private data read.
