# Research: remove the obsolete synthetic proof case (issue 360)

Date: 2026-10-25, written about 12:30Z before any plan, critique or live write. Worktree `issue360-remove-synthetic-example`, branch `fix/remove-synthetic-example-360`, from main 0245944a. Research disposition: executed. Planning readiness: Ready.

## Trigger and authority
Owner: one entry called "Synthetic Example" in the housing database is out of the map; it is an old proof entry and is no longer needed; remove it. Narrow authority: this exact obsolete synthetic proof entry and directly necessary dependent rows only. No broad reset, no seeded-case deletion, no identity, grants, Entra or audit destruction. OSM tile configuration (revision 0000006) must stay. Cumulative USD 50 and USD 700 (RG `ama`) caps unchanged; no new paid service.

## Identity (read-only, live app via PTY exec, 12:28Z, parameterised aggregate output)
* Exactly one case matches "synthetic example" (search, body or surname): id `CUTOVER-SYNTHETIC-ONLY` (the infrastructure proof case from the private cutover proof), stage "Contacting resident", open (`closed=0`), `Synthetic` area, address label "Infrastructure proof only", rowversion 1, seq 1, no building id, 0 documents, 0 appointments, 0 history entries, body length 820.
* Live totals before: 981 cases, 444 open, 7 recommendations, 17 audit entries (head count 17, chain intact), 0 staff rows, `meta.seq` 9, `as_of` 2026-10-16.
* Seed preservation: the SHA-256 of the sorted list of the other 980 case ids equals the SHA-256 of the reviewed seed's 980 id set (`a4be036a...3500b6`, computed from the private seed file). So the matched id is not one of the 980 seed cases and every seed id is present.
* Audit rows referencing the case id: 0. Recommendations whose body references the id: 0 (7 recommendations checked; they grew from 2 through user activity, so live state is not assumed unchanged).
* Aggregate digest of the other 980 rows (sha256 over id plus sha256 of each body): `536c4fca...57654d`. Used for before and after comparison.

## Schema and constraints (src/core sqlstore.py, mssqlstore.py)
* Tables: `meta`, `staff`, `cases`, `recommendations`, `audit`, `audit_head`. No foreign keys. Recommendations and audit reference cases by a text id only. Documents, appointments, history and funding live inside the case JSON body, so no dependent rows exist.
* Only `audit` is an append-only ledger (a ledger table with `APPEND_ONLY`, plus an `INSTEAD OF UPDATE, DELETE` trigger). `cases` is a normal table, so a physical DELETE is allowed by the schema. Audit rows and `audit_head` are never touched except for one appended entry.
* Queue flags (`queue_*`) are columns of each case row. Removing a row needs no refresh of other rows (the case has no building link and is not referenced by other rows).
* `SqlStore._append_audit` appends a chained entry and updates `audit_head` in the caller's transaction; `merge_seed` is the pattern (one `BEGIN IMMEDIATE`, chain verified against head, one audit append, `meta.seq` bumped).
* No existing delete or remove helper for a case exists (grep of `src/` found no `DELETE FROM cases`). Adding a broad delete API is forbidden.

## Serving-cache finding (decisive for the route)
`SqlStore._sync` loads rows with `seq > self._seq` into the in-process `self.cases` dict and never evicts. `/api/map`, lists and queues read `self.cases`. A physical DELETE by another process therefore leaves the case visible in a running replica until that replica restarts and reloads from the database. A database delete alone does not remove it from the map of a warm replica.

## Options
1. Physical DELETE of the single `cases` row plus one appended audit entry in one transaction, run through the existing app runtime (PTY exec, parameterised script), then make the serving replica reload (revision-preserving replica restart or scale-to-zero cold start). No source change, no deploy. Matches the owner's wording ("remove from the database"). History stays in the audit ledger.
2. Audited soft delete (closed or hidden flag). Rejected: closing would pretend completed work, and no existing hidden flag removes a case from lists and the map.
3. New store helper plus eviction in `_sync`. Rejected for this P0: needs code, an image build, a full gate and deployment authority. Recorded as a possible follow-up (stale-cache after external deletes).

## Risks
* Concurrent user activity: the transaction must verify, under the write lock, the audit chain and head, exactly one matching row with the recorded body hash and rowversion, zero referencing audit rows and recommendations, and `DELETE ... WHERE id=? AND rowversion=?` rowcount equal to 1. Any mismatch rolls back and nothing changes.
* After the delete the removed id must not be rewritten by the stale cache: `_save` writes only touched cases and uses the rowversion guard, so a stale replica cannot silently re-insert the row.
* Making the replica reload is a runtime action on existing resources. It is not scaling configuration, an image change or a deploy. It is a risk if the restart is slow (cold start about 40 s, health probes on `/healthz`).
* Cost: a transaction against an existing S0 database and one restart add no new resource and no measurable incremental cost; allowance recorded in the live report. The cost API is lagged and is not a cap proof.

## Verification the plan must prove
Exact match 0; total minus 1; all 980 seed ids present; digest of the other rows unchanged; map and list exclude the id after reload; audit chain intact with count plus 1 and the earlier 17 rows unchanged; recommendations and staff unchanged; `/healthz` 200, anonymous and forged-header API 401; revision 0000006, image 0769b52d and the two OSM tile env values unchanged; SQL users, grants, S0 untouched.

## Evidence gaps
* The app cache behaviour is from code reading; the post-reload map exclusion is verified live after the change.
* Owner browser view of the map after removal remains the owner's check.
