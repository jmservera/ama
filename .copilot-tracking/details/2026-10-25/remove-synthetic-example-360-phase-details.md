# Phase details: remove the obsolete synthetic proof case (issue 360)

Date: 2026-10-25, before the critique and any live write.

> SUPERSEDED (correction about 14:25Z, documentation only). This is the pre-critique draft, kept as written for chronology. It is NOT a current runbook. Two parts were rejected by the accepted critique recorded in the plan (`plans/2026-10-25/remove-synthetic-example-360-plan.md`, section "Critique outcome"): step 8 below is invalid, because `seq` is a value under the `meta` key `seq` and not a column, so the corrected form is to read the current `meta.value` for key `seq`, write `str(cur+1)` with parameters and require rowcount 1; and the scale-to-zero fallback in "Replica reload" is rejected as not a cache-invalidation guarantee, so the revision is restarted and the replica set change is observed. The executed script was `/tmp/ama-360-rm/rm.py` (external, private), not this text.

## Transaction (script run through the app PTY exec, current revision, parameterised SQL only)
Inputs fixed in the script: id `CUTOVER-SYNTHETIC-ONLY`; expected rowversion 1; expected body length 820; expected other-rows digest recorded in research (re-computed inside the transaction; a change by user activity must abort and be re-evaluated, not ignored); expected seed id-set digest.

Order (no foreign keys, so child-first is only about the audit entry):
1. Open the store connection like the app (`mssqlstore.connection_string(os.environ)`); `BEGIN IMMEDIATE` (existing wrapper).
2. Verify audit chain intact and equal to `audit_head` (via `ledger.verify_entries`).
3. Select cases matching the search phrase: require exactly one and that its id is the fixed id; require rowversion 1 and the recorded body SHA-256.
4. Require 0 audit rows with this `case_id` and 0 recommendation bodies containing the id.
5. `DELETE FROM cases WHERE id=? AND rowversion=?`; require rowcount 1.
6. Require the id-set digest of the remaining cases equals the seed id-set digest, and the count is the prior count minus 1.
7. Append one audit entry via the store's chained-entry logic: who `owner-request-remove-synthetic`, action `case_removed`, case id the removed id, detail "obsolete synthetic proof case removed at owner request; cases_after=N" (no personal data).
8. `UPDATE meta SET value=seq+1 WHERE key='seq'` so syncing readers notice the change.
9. `COMMIT`. Any exception or guard failure: `ROLLBACK`, print counts only, exit non-zero.

## Output (aggregates only)
Before and after: total, open, recommendations, staff, audit count, audit head prefix, chain intact, other-rows digest, exact-match count.

## Replica reload
After the commit, make the serving replica reload from the database using the lowest-impact runtime action (restart of the single active replica of the current revision; fall back to waiting for scale-to-zero after the 300 s cooldown). No revision, image, env or scaling change. Verify revision name, image, the two OSM env values and traffic 100 percent before and after.

## Verification after reload
Cold start tolerance 60 s; `/healthz` 200; anonymous `/api/cases` and `/api/me` 401; forged header 401; a fresh PTY read shows exact match 0, total minus 1, seed ids all present, digest of the other rows unchanged, audit count plus 1 and chain intact. Map exclusion: in the new process, `store.map_view` (the serving projection) over the loaded store does not contain the id (script prints a boolean and counts only).

## Evidence locations
`/tmp/ama-360-rm/` (private, mode 700), `/tmp/ama-360-remove-example-live.md`, issue 360 comment (aggregates only).
