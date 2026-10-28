# Plan: remove the obsolete synthetic proof case (issue 360)

Date: 2026-10-25, written after the research file and before the critique and any live write. Details: `.copilot-tracking/details/2026-10-25/remove-synthetic-example-360-phase-details.md`.

## Decision
Physical, guarded, single-row DELETE of case id `CUTOVER-SYNTHETIC-ONLY` plus one appended audit entry, in one transaction, through the existing app runtime. Then reload the serving replica so its in-memory cache drops the case. No source change, image, deploy, scaling configuration, RBAC, network, Graph or new resource. Documentation and RPI evidence only on the PR branch.

## Phases
1. Pre-write proof and private backup (done in research; repeat the guard inside the transaction).
2. Independent critique of this plan and the details (once). Accepted findings are applied before any write.
3. Execute the guarded transaction (one run). Success needs the persisted post-checks, not an exit code.
4. Make the replica reload and verify map and list exclusion, health, auth refusals, revision, image and env unchanged.
5. Record evidence externally (`/tmp/ama-360-remove-example-live.md`), comment on issue 360 (aggregates only), then changes, review, docs, gate, PR (Refs 360).

## Rollback
* Before commit: any failed guard rolls back; nothing is written.
* After commit, if the owner wants it back: re-insert the saved row (private backup `/tmp/ama-360-rm/base-out.txt`, mode 600, contains only the synthetic case row) with an audit entry. The audit entry for the removal stays, because the ledger is append-only.

## Stop conditions
Match count not exactly 1, id in the seed set, audit chain or head mismatch, referencing audit or recommendation rows found, rowcount not 1, authority expired (16:02Z), or any unavailable verification. Report; never widen the delete.

## Cost and authority
No new resource. Existing S0 only. USD 50 cumulative cap not reset; USD 700 RG `ama` ceiling unchanged; cost API lag is not a cap proof; allowance USD 1 for the exec, restart and reads.

## Success criteria
As listed in the research file. The word "removed" is used only after the persisted checks pass.

## Critique outcome (appended about 12:32Z per file times, original text above preserved)
One independent rubber-duck critique ran on the three files above. Verdict: FAIL as drafted, six findings, all accepted and applied as amendments before any write.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | `UPDATE meta SET value=seq+1` is invalid (`seq` is a meta key, value is text) | Accepted: read the current `meta.value` for key `seq` under the transaction, write `str(cur+1)` with parameters, require rowcount 1 |
| 2 | Blocking | Raw connection does not give the `BEGIN IMMEDIATE`, placeholder and rowcount behaviour | Accepted: use `mssqlstore._Conn`; audit via the store's own ledger entry mechanics (`ledger.make_entry` with the captured head, ISO timestamp) |
| 3 | Blocking | Reference checks incomplete (chat tables, meta documents, other cases, staff, external documents) | Accepted and done read-only live at about 12:32Z: a generic scan of every non-history table found 0 references outside the case row itself (chat, assistant, time, notice, cutover_proof, meta, staff, recommendations, audit all 0; other cases 0; case has 0 documents). The transaction repeats the scan for `cases`, `recommendations`, `audit`, `meta`, `staff`, `chat_thread` and aborts on any hit |
| 4 | Blocking | A `meta.seq` bump does not evict a warm replica's cache | Accepted: restart the revision (all replicas) after commit, prove the replica set changed and verify exclusion from a fresh process and over HTTP behaviour; the scale-to-zero fallback is rejected as not a guarantee |
| 5 | Non-blocking | Prove ledger mechanics | Accepted: capture head before, assert count plus 1, head equals verified chain head, exactly one new `case_removed` entry whose `prev` equals the old head, prior 17 rows hash-equal |
| 6 | Non-blocking | Explicit mutation guards | Accepted: select by fixed id first, verify rowversion and body SHA-256, require rowcount 1 for delete, meta seq and audit head updates |

Amendment 5 status (correction, documentation only): partly applied. The executed script asserted the chain verifies, count plus 1 and head equals the verified chain head. It did not compare the earlier 17 audit rows byte by byte or by hash, and did not assert an explicit `prev` equality or a single new `case_removed` row beyond count plus 1. Preservation of the earlier rows is inferred from chain integrity and the append-only ledger, not proven by comparison. The "prior 17 rows hash-equal" wording in row 5 above was the plan, not the result. No runtime check was added afterwards.

Critique execution: once, about 12:32Z (earlier text in this file stated 12:44Z/12:45Z in error; file modification times are authoritative). No repeat critique for this task.

## Retention clarification (2026-10-28, documentation only)

The original decision and critique above remain historical. The single-row
`DELETE` is active-case removal, not data erasure: the live updatable ledger
`cases` table retains the prior body in system-managed history. Critique
amendment 3's non-history scan cannot establish absence from ledger history.
See the [dated research correction](../../research/2026-10-25/remove-synthetic-example-360-research.md#schema-correction-2026-10-28-pr-459-review).
No new plan, critique, runtime action or full RPI loop was started.
