# Plan: seed the demo `retrofit` database (issue 360)

Date: 2026-10-25. Written after `research/2026-10-25/seed-demo-baseline-360-research.md` and before any source edit. Branch `feat/seed-demo-baseline-360`, base 36996d70.

## Decision
No supported non-destructive route exists, so add the minimum: a store-owned, insert-only `merge_seed` operation plus a thin CLI, delivered through the ordered RPI loop. Replace nothing; do not alter `_seed`.

## Design (clean architecture, small surface)
* `SqlStore.merge_seed(src, *, apply, include_staff=False, actor="seed-merge")` in `sqlstore.py`, using only the existing dialect hooks so SQLite and `MssqlStore` share it.
* One write transaction (`BEGIN IMMEDIATE`), rolled back on any error:
  * Cases: id absent, insert as `_seed` does with `seq = meta.seq + 1`. id present with an identical body, skip. id present with a different body, abort the whole merge (collision guard); never update or delete.
  * Documents (procurement, governance, buildings, form_schemas, bulk_edits, continuity): insert only when the meta key is absent. A present key is preserved and reported, never replaced.
  * Staff: not inserted by default (staff rows are not login authority and must not be bound to people). `include_staff=True` inserts missing emails only, off by default.
  * `as_of`, `rank_policy`, `support_encoding`, `entra_people` and all other meta rows are untouched; the seed's `as_of` is reported next to the stored one.
  * Then `_refresh_queue_membership(None)`, exactly one appended audit entry (`seed_merge`, counts and the seed SHA-256, chained from the current head) and `meta.seq` bump. If nothing is inserted there is no audit entry and no seq change, so a repeat run is a no-op (idempotence).
  * `apply=False` runs the same checks with SELECTs only and returns the report; nothing is written.
* Report returns counts only: seed cases, existing, to insert, identical present, conflicts, docs inserted/preserved, staff inserted, expected totals. No rows, names or emails.
* CLI `python -m zava_forward.core.seed_merge --seed PATH [--apply] [--include-staff] [--expect-added N]`: builds the store from `ZF_*` environment (same as the app), dry run by default, prints the report as JSON, exits non-zero on a conflict or on an `--expect-added` mismatch.

## Tests (focused, offline first)
1. SQLite: merge into a store holding one existing case, one recommendation and audit rows: counts, existing case body unchanged, recommendation unchanged, audit prior rows byte-identical with exactly one appended and the chain valid.
2. Dry run writes nothing (row counts, seq and audit head unchanged).
3. Idempotence: second apply inserts 0, appends no audit, seq unchanged.
4. Collision: a seed case with an existing id but a different body aborts with nothing inserted (all-or-nothing).
5. Injected failure after the case inserts (patch `_append_audit`): full rollback, restart shows the original state.
6. Documents: absent key inserted, present key preserved and reported; staff off by default and on by flag only; `as_of` preserved.
7. Real SQL Server (`ZF_TEST_MSSQL`, throwaway database, local-server guard as in tests/test_assistants.py): the same merge, rollback and idempotence on ledger-enabled and plain databases, including the audit ledger append.
8. CLI test: dry run default, `--expect-added` mismatch exits non-zero.

## Local rehearsal
Generate the deterministic seed (seed 20260901, as-of 2026-10-13) to an external private directory, record its SHA-256 and counts, then run dry run and apply on a throwaway SQL Server database that clones the live shape (proof case, one recommendation, two audit rows, meta keys). Use my own throwaway SQL Server container on a different port. The #350 container and the local sites are not touched.

## Live route (after tests, review and coordinator release)
Source needs the coordinator's exact-head release and a merge to main before it can run live. Planned route, no new paid resource and no new grant:
1. Build an ephemeral private image from the merged main using the existing kaniko build via `job-cutover-test-init` (the owner-approved route): core, the tracked generator and the tracked stock-geography inputs, with the entry `generate then merge`. Record digest and Dockerfile variant. Job definition backed up first and restored afterwards.
2. Run the merge with the existing job identity and the app's SQL settings: dry run first, then `--apply --expect-added <value from the dry run>`. The job needs replicaTimeout raised only for the run (restored afterwards).
3. Verify with the existing PTY exec: counts, unchanged proof case and recommendation, audit prior rows unchanged plus one new, idempotent second dry run, healthz 200, anonymous 401.
Backup before write: for rollback there is no delete by design; the pre-write evidence is the exact counts and the audit head hash plus the SQL point-in-time restore window of the database. A failed run rolls back in the transaction.
Authority: owner explicit seeding authority 07:56Z; original USD 50 cap and USD 700 ama RG limit unchanged; live window to 12:00Z, resources to 16:02Z. Cost: no new resources; a short job run and image storage only, to be stated with the evidence.

## Out of scope
Provider/map activation, DROP or recreate, audit deletion, staff binding, role grants, network changes, the Dockerfile variant fix, sensor migration, any change to `_seed`.

## Success criteria
Tests above pass including real SQL Server; independent review PASS; full gate on the exact head; live counts reconcile (expected total = existing 1 + generated cases) with unchanged proof/recommendation/audit and idempotent rerun.

## Independent critique (rubber-duck, run before implementation, 2026-10-25)
Verdict: PASS-WITH-CHANGES. Execution: executed once; not repeated. Original plan text above is unchanged.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Case collision compare must be semantic, not raw string | Accepted: normalise the seed case as `_seed` does, decode the stored body and compare canonical sorted-key JSON. Tests: reordered keys, whitespace, omitted defaults. |
| 2 | Document policy contradicted research | Accepted: absent = insert; canonical-identical = skip; differing = abort, except a documented allowlist of one key, `continuity`, which is preserved and reported (existing proof state; owner said preserve meta). |
| 3 | Audit chain unverified before append | Accepted: inside the write transaction recompute the chain over existing audit rows and require it to equal `audit_head` and the count; abort otherwise. Tests: stale head, corrupted prior row. |
| 4 | Dry run is advisory | Accepted: every guard is recomputed inside the apply transaction; documented. |
| 5 | S0 and job capacity | Accepted: one transaction, batched inserts (50), explicit timing per phase in rehearsal, fail before the replica deadline; measured in rehearsal before live. Raise job replicaTimeout only for the run if the measurement requires it. |
| 6 | Staff insertion weak | Accepted: remove `--include-staff` entirely. Staff are never inserted by this tool. |
| 7 | Idempotence and privacy | Accepted: live proof is a guarded second `--apply --expect-added 0` with unchanged audit count/head; log-capture tests assert no body, name, address or email on success, conflict and error paths. |
