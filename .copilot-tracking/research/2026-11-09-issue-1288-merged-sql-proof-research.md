# Research: issue 1288 merged-main SQL contract verification (no correction cycle)

Disposition: executed. Task `issue-1288-merged-sql-proof`, resumes the pending `integrate-quality-persistence` task. Research phase read-back: `date -u` 2026-11-09T23:20:29Z, before any SQL observation. This is a VERIFICATION continuation, not a correction: E1-E11 are spent or succeeded (E11 succeeded), E12 and E13 are unused and are neither spent nor reset here. No source, test, schema or configuration change is authorised. Refs #1288 only; whole 1288, #440 and the live-model criteria stay open.

## Identity pins

* Worktree `/home/azureuser/source/ama-demo-wt/issue-1288-merged-sql-proof-1109`, branch `test/demo-quality-sql-proof-1288-1109`, clean at start, HEAD equals `origin/main` `a8593a7a8670aab27329a81fedee605b4913e7e9` (tree `5113adcb220d250f0b99c1ab57024e0a2c87f68f`).
* Quality merge `1b7a1719b` (squash of PR 1331) is the executable provenance. Its tree `dd2bedcb8f4e73266e143be09bf72474c62db9fd` equals the independently reviewed E11 head `f995774ca` tree.
* Check of the claim "the new base differs only by rubric": `git diff --name-status f995774ca a8593a7a8` and `git diff --stat 1b7a1719b a8593a7a8` list one path, `.github/rubric/scores/latest.json` (21 insertions, 17 deletions). `src`, `infra`, `tools`, `.github/workflows` and `pyproject.toml` are empty in that diff. Both pins are therefore recorded; the executable identity is the 1b7 tree, the exact checkout identity is a8593.
* Unmerged source 891 Core/AI changes are excluded from this assessment.

## What hosted CI covers

`.github/workflows/src-ci.yml` lines 316-329 (and `mvp-ci.yml` 121-134) run one SQL Server step with a fixed list: `test_mssqlstore`, `test_lawstore.MssqlStoreTests`, `test_assistants.Mssql{Contract,Review,Durability,Api,Ledger}Tests`, `test_resident_aoai_sql.AccountingSqlTests`. No `test_quality_sensors*` Mssql class, no `test_assistant_release.Mssql*` class and no lane test runs on SQL Server in hosted CI. The hosted "MSSQL 6m41" pass therefore does not establish the Quality sensor/flag persistence contract. The hosted API job runs the Quality Mssql classes as skipped (no `ZF_TEST_MSSQL`), so they exercise SQLite only there.

## Where the Quality persistence contract is tested

Quality flag and sensor-ID behaviour is tested by Mssql subclasses over the `ta.MssqlFixture` (it drops and recreates the working tables in a disposable `zf_test_assistants` database, refuses any server other than localhost/127.0.0.1/sql):

* `test_quality_sensors.MssqlReadModel` and `MssqlHttp` (role matrix `test_sensors_api_role_matrix`; source IDs and values reaching model and flag `test_same_ids_and_values_reach_model_and_proactive_flag`; stale/duplicate handling `test_stale_proposal_is_not_a_flag`, `test_same_bucket_arrival_...`, `test_exact_a_b_a_return_...`; restart `test_sensor_churn_before_claim_is_one_task_one_dispatch_and_survives_restart`; unknown/missing sensor evidence `test_request_marks_missing_sensor_evidence_as_unknown`).
* `test_quality_sensors_c7.MssqlPerHome` and `test_quality_sensors_e1.Mssql{DirectControlWrites,ManualAndProactive,Adoption,Coalescing}` (database control-guard triggers rejecting direct update/delete/insert for a home with a live gate; restart behaviour).
* `test_quality_sensors_e2.Mssql{Boundary,Cursor,ForecastPurity,Rotation}` (captured readings refused before meter, token or socket; the one SQLite-only skip for the cross-process withdrawal).

## Retained source-qualified receipts

* `sql-1288-e6-run/` (outside this worktree, coordinator session files): head `5827ebede7cfbf1281bd23c46cd142535f39c4f4`, clean, one non-queued heavy admission, SQL Server 2022 Developer container, API `Ran 605 tests ... OK (skipped=1)` (the one skip is the SQLite-only cross-process withdrawal), Core 53 OK. Its verbose log names all 17 Quality and assistant Mssql classes above (205 Mssql-class tests).
* `logs-1288-e5/sql-run/` at `96da7bae0` (API 577/1 skip) and `logs-1288-e4/sql-run-141828` (509/1 skip) and the c8 logs are older, superseded by the 5827 receipt for this purpose and not used as the primary receipt.
* Historical c160 "319 tests / 1 skip" is a hosted CI count and ALONE does not establish any unexamined named contract; it is not used as contract proof.

## Source delta from the 5827 receipt to the merged executable tree

`git diff 5827ebede a8593a7a8` over `src/core/src` and `src/api/src`: 12 files. Relevance to the Quality persistence and refusal contracts:

* `assistants.py` (8 insertions, 5 deletions): `fence_send` now records the `send-refused` event inside the transaction and raises `DispatchWithdrawn` after the transaction block, so the refusal is committed rather than rolled back (E6 fix 5f44dc4e1). The persistence of that event on SQL Server was never observed: the refusal-event test `test_quality_simulation_lane...authority_that_expires_after_admission_stops_the_send` counts `send-refused` rows on the SQLite working store; no Mssql lane subclass exists; E7 recorded "SQL: none run" for this ordering.
* `sensor_consumer.py`: formatting only. Proof: `ast.dump(ast.parse(...))` of `git show 5827ebede:` and `git show a8593a7a8:` of the file is equal (checked about 2026-11-09T23:19Z).
* `sensor_view.py`, `sqlstore.py`, `mssqlstore.py`: unchanged since 5827 (absent from the diff).
* `ai.py`, `ai_transport.py`, `simulation_lane.py` (2 lines), `server.py`, `assistants.js`: E7 route-disabled and deadline work; not SQL persistence code.
* `ranking*.py`, `ranking_archive_blob.py`, `store.py`: main ranking-archive work (issue 1258), not Quality persistence; `store.py` is shared infrastructure, so a refresh run exercising the store is a reasonable guard but no contract change is expected.
* Tests: the Quality Mssql test files and `test_assistants.py` are unchanged since 5827; `test_quality_simulation_lane.py` (+87) is the SQLite lane and `two_process_worker.py` +1 line.

## Findings and gaps

* Sensor/flag source-ID persistence, role projection, duplicate/stale handling and restart: established at source `5827ebede` for unchanged code (`sensor_view.py`, `sqlstore.py`, `mssqlstore.py`) with `sensor_consumer.py` AST-identical. It is a historical receipt for the earlier head, not a fresh run at the merged tree, and shared `store.py` changed.
* Refusal-event transaction and fresh-connection visibility on SQL Server: genuinely unproven. The lane tests that count `send-refused` and exercise cross-process reuse run on SQLite only.
* No Mssql lane subclass exists, so lane-level (`/api/assistants/simulation/quality/request`) behaviour on SQL Server is unobserved. The simulation lane's own store is a separate SQLite file by design (`simulation_lane.provision`); this verification does not alter that.
* Real provider simulation stays code-disabled (`Ai.send_fence_supported=False`); the lane stub is a fixture, not a model or an approval.

## Planning readiness

Ready for a finite plan: one bounded disposable SQL Server observation under one non-queued heavy admission, a selected exact-source refresh of named existing tests, and one external disposable harness that observes the refusal-event commit and fresh-connection visibility through the real `Assistants`/`MssqlStore`. If the heavy lock is occupied, record the block and the pending step and stop.
