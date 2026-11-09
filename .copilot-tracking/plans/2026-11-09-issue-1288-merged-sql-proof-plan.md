# Plan: issue 1288 merged-main SQL contract verification

Task `issue-1288-merged-sql-proof`; research `.copilot-tracking/research/2026-11-09-issue-1288-merged-sql-proof-research.md`. Plan phase read-back: `date -u` 2026-11-09T23:21:35Z, before any observation. Verification only: no source, test, schema or workflow change; no correction cycle is spent or reset (E11 succeeded, E12 and E13 unused). Refs #1288 only.

## Objective

Decide, with source-identified evidence, whether the merged tree (checkout `a8593a7a8`, executable provenance Quality merge `1b7a1719b`, tree `dd2bedcb8...` equal to reviewed E11 `f995774ca`) satisfies these contracts, and state exactly what stays unproven:

* C-A durable authorized sensor and flag source IDs, and the role projection that exposes them, persist across restart and a fresh connection on SQL Server; duplicate and stale proposals are not promoted to a current flag.
* C-B the database control guard rejects a direct write for a home with a live gate (the persistence integrity that protects the authorized sensor set).
* C-C a refused send (`fence_send`) records its `send-refused` event in a committed transaction before the `DispatchWithdrawn` raise, visible from a fresh connection, with durable allowance, slot and counters consistent, and nothing sent (meter, token, socket zero).

## Decision: reuse versus observe

* C-A and C-B: the 5827 receipt (`sql-1288-e6-run`, API 605 OK with 1 SQLite-only skip) is an exact-scope historical receipt for unchanged code. The shared `store.py` changed since, so a minimal exact-source refresh of the named tests is chosen rather than relying on the older head alone. It is labelled a refresh at the merged tree and does not replace or overwrite the 5827 receipt.
* C-C: no SQL Server observation exists. One external disposable harness is planned.

## Single SQL exercise (ONE heavy admission)

One non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission, once. Occupied lock or failed non-blocking attempt: record the holder from the actual process list and lock state, stop SQL work, finish only light research, and return the exact pending step (no retry loop, no wait, no kill, no queue). The holder is inspected (`fuser`/`ps`) and never reused or terminated.

Inside the admission: one fresh container from the already present image `mcr.microsoft.com/mssql/server:2022-latest` (no pull), `127.0.0.1` random port, random per-run SA password (never logged), label `zf.task=1288-merged-sql-proof-1109`, memory 3g, removed in a trap. Scratch directory is a fresh issue-qualified `mktemp` (`/tmp/ama-1288-sqlproof-*`); the venv inside it was created because this worktree had no environment (the older `.venv-1288` editables point at another worktree; the generic `/tmp/e8venv` is not used). Dependencies came from the hash-pinned `src/api/requirements.txt`, then `pip install --no-deps -e src/core -e src/agents -e src/api`; import paths verified to resolve into this worktree.

Selected existing tests (exact methods, run with `-v`, `ZF_TEST_MSSQL=1`):

* `test_quality_sensors.MssqlHttp`: `test_sensors_api_role_matrix`, `test_same_ids_and_values_reach_model_and_proactive_flag`, `test_stale_proposal_is_not_a_flag`, `test_exact_a_b_a_return_requeues_the_stale_task_within_the_allowance`, `test_sensor_churn_before_claim_is_one_task_one_dispatch_and_survives_restart`, `test_request_marks_missing_sensor_evidence_as_unknown`.
* `test_quality_sensors.MssqlReadModel.test_latest_is_in_the_captured_source_and_citations`.
* `test_quality_sensors_e1.MssqlDirectControlWrites` (whole class, 9 tests).
* `test_quality_sensors_e2.MssqlBoundary` (whole class, 12 tests; the one SQLite-only skip is expected and not waived).
* `test_assistants.MssqlDurabilityTests` is NOT selected unless a selected test fails in `fence_send` or the slot lifecycle (it would then be the next impacted check, recorded as a gap rather than run as a campaign).

External harness `merged-sql-proof-1109/harness_refusal.py` (coordinator session files, not committed; its identity is the SHA-256 recorded in the evidence): class `MssqlRefusalHarness(ta.MssqlFixture, lane.Lane)` reuses the existing fixtures; tests:

* H1 admission: `begin_call` with a short future authority expiry admits and takes the physical slot; allowance row and attempt row read from a fresh raw connection.
* H2 refusal: after the expiry passes, `ticket.send_fence()` raises `DispatchWithdrawn`; a fresh raw `_Conn` (separate from the service's per-transaction connections) sees exactly one new `send-refused` event, the attempt still `reserved` (not `sending`), `peer.accepts == 0`, `meter.reserved == 0`, no token minted.
* H3 settlement: `ticket.end({"outcome": "not-sent"})` ends the attempt (`active_until = 0`), the allowance debit stays recorded as liability, the physical slot is reacquirable, and a new `begin_call` after expiry is refused before any meter or socket. All values read back from a fresh connection.

The harness uses the real `Assistants`, `MssqlStore`, `fence_send` and `CallTicket`. Its only test double is the existing local counted TLS peer and counting meter fixtures; it does not call a model. It does not patch the code under test, so a failure would be a real observation. A stub is not a model or release approval.

## Pass, fail, and record rules

* Failure or error of any selected test or harness check: preserve the full trace, smallest reproduction, requirement and current owner; no source fix, no schema change, no retry, no E12/E13 use. A harness error that is the fixture's rather than the product's is classified as inconclusive, not as a pass.
* Skips are listed with reasons; no skip is waived into a pass.
* Raw output, container id, image id, server version, exit codes and command lines go to `logs-merged-sql-proof-1109/` in the coordinator session files; only summaries with identities are committed in the `.copilot-tracking` changes record.
* Nothing from hosted CI, 5827 or c160 is relabelled as fresh. The refresh run is described as exactly what it covers.

## Out of scope and explicit limits

Real provider simulation stays OFF (`send_fence_supported=False`); no model, provider network, live IoT or Azure, real receiver or real data; no new permission, spending, production privacy or legal approval, or human acceptance. Ordinary post-fence suspension race, local-only socket cancellation, hosted interleaving and final audit persistence under an actual model remain limits. The sibling unmerged 891 changes are excluded. No cutover pack, reference index, log or shared documents are edited.

## Amendment after critique (2026-11-09T23:25Z; the original text above is retained)

The critique `.copilot-tracking/plans/critiques/2026-11-09-issue-1288-merged-sql-proof-critique.md` is applied:

* Selected tests add `test_quality_sensors_e2.MssqlCursor.test_the_cap_is_unchanged_and_a_long_history_completes_over_scans_and_restarts` and `test_quality_sensors_e1.MssqlManualAndProactive.test_a_completed_manual_request_after_a_restart_does_not_allow_another_call`. The churn test name is not treated as restart proof of IDs.
* Harness methods are selected by explicit id only (no inherited lane test runs on SQL Server): H0 restart of sensor and flag IDs and role projection through a second `Assistants` over a new `MssqlStore`; H2a direct `fence_send` transaction contract; H2b real `Ai.evidence` path through the lane request with a bounded SQL-clock wait at the meter `before` hook so the transport fence refuses on authority expiry (lease 60 s, no suspension), asserting meter/token 1 each (the fence follows them), peer accepts 0 and bytes 0, the committed event reason equal to the expiry text, the attempt `reserved`; H3 settlement and durable allowance via a fresh raw connection, with the physical slot checked in process and labelled as such.
* The simulation lane store stays SQLite by design; only the working store is SQL Server.
