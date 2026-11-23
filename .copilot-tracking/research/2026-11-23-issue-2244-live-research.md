# Research 2244 live (2026-11-23)

Task: issue #2244, API start-up crash-loop on the SQL write lock. Demo scope per owner decisions 2026-11-18. Disposition: executed. Planning Readiness: Ready.

The issue has no tick-box acceptance list. Criteria are derived from its "Suggested" and "Defect" text:

* C1 start-up retries a lock timeout with backoff instead of exiting.
* C2 start-up skips the write lock when the schema is already current (read-only check first).
* C3 the live API revision runs the fix and starts without a crash-loop.
* C4 a long concurrent writer no longer makes the demo unavailable.
* C5 lock holder identified (issue: not proven; Log Analytics not readable).

## Evidence

* Main already holds #2273 (42546c9221, 2026-11-22 21:58 UTC): `_Conn._begin` retries `could not take the write lock` up to 8 times, backoff 1..30 s, enabled only while `MssqlStore._initialize` runs; tests in `src/core/tests/test_mssql_startup_lock.py`. C1 proven in code.
* Live API revision `ca-cutover-test-demo-api--0000054` (created 2026-11-22T23:14:23Z, Healthy, 1 replica, replica restartCount 0, Running since 00:43:11Z). Via `az containerapp exec` (pty) the image file `/usr/local/lib/python3.12/site-packages/zava_forward/core/mssqlstore.py` has md5 07d00576e1d5e11e0efb1d86cfc1f92f, identical to the main checkout (4 `startup_retries` occurrences). The ACR is not readable by this client, so the image digest could not be mapped to a commit; the file hash is the proof.
* `GET /healthz` on the live FQDN: HTTP 200 three times (0.10 s). Last 300 console lines contain no `write lock` error.
* Live `ca-resident-demo--0000026` runs image `zava-resident-demo` (a separate resident app, not the SQL store); it is Healthy and not part of the defect path.
* Gap A (C2): `MssqlStore._create_schema`, `_migrate_chat_memory`, `_create_indexes` and `sqlstore._migrate_queues` always take the global lock even when nothing changes. `_migrate` and `_migrate_recommendations` also always lock but rewrite data (rank policy, ordinals, continuity gate), so they cannot be skipped by a pure schema read.
* Gap B (C4): worst case one `BEGIN` waits 15 s x 8 plus 91 s of sleeps (about 211 s) against a StartUp probe budget of 1 s + 40 x 3 s (about 121 s). A writer holding the lock longer than about two minutes still ends in a probe kill. The probe is a production Azure setting; not changed here (owner rule: no production changes).
* C3 stress proof (hold the lock with a second session, then start a revision) would be a drill on the live demo database; excluded by the owner decision (no drills). Unproven by design.
* C5: Log Analytics is still not readable; not proven.

## Selected approach

Add read-only "already current" fast paths in `MssqlStore` for `_create_schema`, `_migrate_chat_memory`, `_create_indexes` and `_migrate_queues`, each falling back to the locked path when anything is missing. Unit-test with fakes. Do not touch `_migrate` or `_migrate_recommendations`.
