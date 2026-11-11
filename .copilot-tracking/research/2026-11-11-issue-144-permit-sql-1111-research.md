---
title: Issue 144 permit SQL boundary research
description: Research for the retained real-MSSQL validation gap of the worker-permit clock and lock boundary and stored-permit result attribution
ms.date: 2026-11-11
task_id: issue-144-permit-sql-1111
---

## Scope

Research and plan only, in `/home/azureuser/source/ama-demo-wt/issue-144-permit-sql-1111` on `test/worker-permit-sql-144-1111`, base `origin/main` `e691255ff7aae111ef32d585900cf82c3789a78c` (cwd and HEAD asserted before writes; status clean). Refs #144 only. Current main already contains E1/E2 through PR 1428 (`05f11ebe9c9c04b5b3d12bc4db5889dae3b01d46`). No source, test, config, runtime, database, container or GitHub action was taken. E1/E2 of the Nov 10 five-cycle extension are spent and three remain; this launch consumes none.

## Disposition

Research executed. Planning Readiness: Ready, subject to the Root admission items in the plan. No source defect was found by reading; none is claimed.

## Retained gap (actual records)

* The E2 handoff reported no ready SQL fixture and no MSSQL parameterisation. The permit tests in `src/api/tests/test_ai_consumption_api.py` (`ConsumptionApi`) build `test_assistants.Base`, whose `open_store` returns the SQLite `SqlStore`. Every permit, E1 clock and E2 attribution regression therefore ran on SQLite with a patched clock (`after_blocking_update` wraps `service.transaction` and `service.now`). They prove ordering in the routine, not a real lock wait.
* Hosted `mssql` job (`.github/workflows/src-ci.yml` lines 292-327) and `SQL_SELECTORS` in `tools/rpi-checks.py` name `test_mssqlstore`, `test_lawstore.MssqlStoreTests`, `test_assistants.Mssql*`, `test_assistant_release.MssqlUnleasedRevocation` and `test_resident_aoai_sql.AccountingSqlTests`. None calls `issue_permit` or `complete_result`. `grep` finds those two methods only in `assistants.py`, `test_ai_consumption_api.py` and `test_capacity_browser_check.py`. A broad hosted MSSQL pass does not prove these paths.
* The R15 read-only diagnostic (`handoff-144-r15-readonly-diagnostic-1110.md`, attempt 2) reproduced the original defect on a disposable SQL Server 2022: holder plain `BEGIN TRAN` plus task-row UPDATE, claimant blocked on the row lock (claimant SPID 68 blocked by holder SPID 66), permit granted with a stale `issued_at` after expiry. Attempt 1 used `BEGIN IMMEDIATE` (global applock) and is invalid for this boundary; it is retained as history and must not be repeated. No observation of the fixed source on real SQL exists.

## Actual current contracts (read from source at the base)

Constants in `assistants.py`: `PERMIT_LEASE_MARGIN = 38.0`, `PERMIT_WINDOW = 2.0`, `PERMIT_REQUEST = (body_sha256, model, deployment, temperature, configuration, max_tokens, input_bound)`.

### E1: clock, lock order, expiry at reservation and dispatch window

* `Assistants.transaction` (line 652): on MSSQL `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE`, then `BEGIN IMMEDIATE`. `_Conn.execute("BEGIN IMMEDIATE")` (`mssqlstore.py` 177) runs `BEGIN TRAN` plus `sp_getapplock 'zavaforward_write'` (Exclusive, Transaction owner, 15 s timeout). So the claimant always owns the global applock before it can wait on a task row. An independent holder must therefore be plain `BEGIN TRAN` plus a row UPDATE with no applock, which matches the R15 attempt 2 harness and the E1 brief.
* `issue_permit` (line 1626): first statement `UPDATE assistant_tasks SET revision=revision+1 WHERE id=? AND owner=? AND fence=? AND state='leased'` (this is the blocking point); `now = self.now(db)` is read after it returns. `now` is `DATEDIFF_BIG(MILLISECOND, 1970-01-01, SYSUTCDATETIME())/1000.0` on MSSQL (line 674). Then the margin check `task["lease_until"] <= now + 38.0` returns `lease-expiring` with no refund and no reservation.
* Later authority expiry is separate and is already read post-lock: `_fence_in` reads its own `self.now(db)`; `ai_consumption.reserve_in(..., min_window=PERMIT_WINDOW)` reads `self.port.now(db)` itself (line 566) and holds `authority-expiring` when `now >= min(authority.end, price.end) - 2.0`; `_refuse_attempt` then refunds the attempt (`used_calls-1`, outcome `permit-denied`) and commits a `permit-denied` event. `dispatch_window_ms` returns whole ms of `min(authority end - now, price end - now, 8 s cap) - 1 s`, and `issue_permit` raises if it is below 1 ms.
* Consequence for the negative control: the original stale read affected only the margin check, `issued_at` and `lease_remaining` (all three used the pre-lock `now`). The frozen R15 source `a482d787` (`assistants.py` 1047) shows `now = self.now(db)` before the UPDATE; its `reserve_in` already read its own clock. So an authority-crossing case guards E1 behaviour but is expected not to fail on the stale-clock mutant. The margin case and the `issued_at`/`lease_remaining` assertions are the discriminating ones. This is a prediction to observe, not to assume.

### E2: stored server-root and meter-id attribution

* `complete_result` (line 1535) reads the `permitted` marker; for a marker it loads the stored root through `_permitted_root` (`consumption._read`, kind `reserved`, id equal to the marker `meter_id`), refuses (`result-rejected`, returns False, no settlement) when the root is missing, owner or fence differ, caller `meter_id` differs, or caller `meter_root` differs; otherwise it copies the envelope with the stored `meter_id` and `meter_root`, calls `_settle_meter` then `complete`. Without a marker and a matching lease it writes `closed-without-permit`.
* This is not a lock-boundary property. Its real-SQL value is that the reservation record, marker events and ledger read round-trip through `MssqlStore` and the SERIALIZABLE transaction, plus the `output` and review attribution that the consumption ledger records.

### Preserved paths

Allowed (reserve once, marker, attempt outcome `sending`, duplicate refused), manual and denied (`request-mismatch`, `task-not-leased`, `lease-expiring`, `authority-expiring`, `suspended` family via `_permit_block`), consent (`consent-not-granted`) and captured readings (`captured-readings`) fail closed to manual with state `disabled` and a refund, an unavailable send fence (`send-fence-refused`) refuses with no reservation and no marker, and failed or no-output results settle the meter and publish no output. Today consent, readings and operator-disable cases are exercised by patching predicates (`_sensors_granted`, `_captured_sensors`, `disabled`). Those stay SQLite-only evidence and must not be presented as SQL proof.

## Existing SQL fixture tooling, ownership and prerequisites (read-only metadata)

* `src/core/tests/sqlguard.py`: `require_task_owned_loopback(env)` admits only a literal loopback `ZF_SQL_SERVER`, a local Docker engine, `ZF_SQL_AUTH=password`, a user-owned mode-restricted `ZF_SQL_TASK_MANIFEST` (`schema zf-task-sql/2`, at most 24 h old, password digest match) and a live container with label `zf.task=1292-sql-disposable`, loopback-only 1433 publish, the provisioned `MSSQL_SA_PASSWORD`, created within 24 h. `write_manifest` is the existing admitted-setup helper. The precedent plan `2026-11-11-priority-before-fix-1292-plan.md` (P1-P5) uses exactly this.
* `test_assistants.MssqlFixture` (line 1320) only checks `ZF_SQL_SERVER in (localhost, 127.0.0.1, sql)`, creates and uses database `zf_test_assistants`, drops the assistant tables each `setUp`, and builds `MssqlStore`. It does not call sqlguard. The plan therefore requires the new class to call `require_task_owned_loopback(os.environ)` in `setUpClass`.
* Documented SQL provisioning (`tools/rpi-checks.py` 1243-1260; R15 diagnostic `run2.sh`): `docker run -d --memory=3g --cpus=2 --publish=127.0.0.1::1433 --env=ACCEPT_EULA=Y --env=MSSQL_PID=Developer --env=MSSQL_MEMORY_LIMIT_MB=2048 --env=MSSQL_SA_PASSWORD` with the label. Driver: `mssql-python` 1.15.0 and `mssql-python-odbc` 18.6.2.1 were verified at R15 and are in the hashed `src/api/requirements.txt` install used by CI.
* Image (read-only `docker image ls`): `mcr.microsoft.com/mssql/server:2022-latest`, image id `cf8f0ab2ebe6`, digest `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`, 2.35 GB, created about five weeks ago, already local; no pull is needed or proposed. Licence is the existing documented `ACCEPT_EULA=Y` with `MSSQL_PID=Developer`; no new licence grant is requested.
* Host observation at plan time only: 15933 MiB total, 8018 MiB available, 727 MiB free, 96 GiB disk free on `/`; `/tmp/ama-rpi-heavy.lock` exists (0 bytes). No holder was probed and the lock was not taken. These are instantaneous facts, not admission.
* Python 3.12.3. The last own venv (`144-main-port-extension1-1110/venv`) imports `mssql_python` but its editable installs point at the removed worktree, and the R15 venv points at the R15 candidate. Neither may be reused or repaired. A new own venv with editable installs asserted at this worktree is required.

## Findings

* F1: no real-SQL execution of `issue_permit` or `complete_result` exists in current main tests or hosted CI. Confirmed by selector and `grep` inspection.
* F2: the lock-crossing boundary can be exercised deterministically on real MSSQL without a patched predicate: independent plain-transaction row-lock holder, observation of the blocked request through DMVs, release gated on the database clock.
* F3: the stale-clock negative control needs a mutated source copy, because the defect is inside the routine and cannot be injected from a test.
* F4: wiring a new module into hosted CI or `SQL_SELECTORS` edits a workflow or gate tool, which takes the full tier by repository policy. It is outside any test-only cycle and is a Root decision.

## Evidence limits

Local disposable SQL Server only; not Azure SQL (different engine edition and isolation defaults), not production, not a provider, model, consent, spend, deployment or release proof. Dispatch-side `dispatch_check` and the worker are B scope and are not covered.

## Sources

* `src/core/src/zava_forward/core/assistants.py` (lines 64-66, 652-677, 1491-1507, 1535-1623, 1626-1679).
* `src/core/src/zava_forward/core/ai_consumption.py` (lines 547-625, 688-700).
* `src/core/src/zava_forward/core/mssqlstore.py` (lines 73-76, 129-210, 284-285).
* `src/core/tests/sqlguard.py`; `src/api/tests/test_assistants.py` (1320-1346); `src/api/tests/test_ai_consumption_api.py` (50-160, 1629-2010).
* `.github/workflows/src-ci.yml` (292-327); `tools/rpi-checks.py` (39-49, 92-124, 1229-1293).
* Coordinator records: `handoff-144-r15-readonly-diagnostic-1110.md`, `handoff-144-extension2-attribution-1110.md`, `brief-144-permit-sql-plan-1111.txt`; repository records `.copilot-tracking/research/2026-11-10-issue-144-extension2-attribution-research.md` and `.copilot-tracking/reviews/2026-11-10/issue-144-extension2-attribution-review.md`.
