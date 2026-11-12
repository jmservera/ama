---
title: Issue 144 permit SQL E3 corrected plan P1
description: Corrected prospective recipe for real disposable-MSSQL validation of the worker-permit clock and lock boundary and stored-permit result attribution, resolving independent findings R1 to R7
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e3-plan-p1-1111
---

## Status and authority

* Phase gate: Research done, Plan correction done (this document, details and authored critique). STOP before Implement. Nothing here has been run: no database, container, test, install, download, scanner, provider, model or Azure command.
* This supersedes the recipe of `issue-144-permit-sql-1111-plan.md` (frozen at `1a29cfd67`, unchanged) wherever they differ; everything not restated here (objective, seven case intents, lock-holder shape, distinction of E1 versus E2, limits) is inherited unchanged from it.
* Counter: Nov 10 five-cycle extension, E1/E2 spent, E3 admitted and counted from this correction, two unadmitted. A later admitted implementation is part of this same E3. No new five, no E4, no reset. Original spent history and unknown minimum preserved.
* Root decisions applied: Option T (one new `src/api/tests/test_permit_sql.py` plus dated RPI records) only after (a) independent prospective clearance of this corrected plan and (b) Root's explicit admission to implement and execute. Direct-only local SQL regression: no workflow, `SQL_SELECTORS`, gate, pyproject, requirement, fixture-helper, production or infrastructure edit, and no promise of hosted MSSQL coverage or whole-#144 acceptance.
* Conditional future environment admission (not permission now): fresh own runtime and tool environment via pip only after an explicit missing-dependency probe fails and is preserved (X1 below).
* D4 stands: a valid-witness behavioral mismatch on fixed source stops for Root on existing #144; no source fix, no new issue.

## Resource layout (all external, new for this plan)

`X=<ROOT>/144-permit-sql-e3-1111` (never the earlier `144-permit-sql-1111` directory). Subdirectories: `logs/` (immutable unique `NN-name.out/.err/.exit`), `receipts/`, `scripts/` (driver, origin probe, mutant scripts, authored outside the worktree), `snap/` (source snapshot), `wheelhouse/` and `wheelhouse-tools/`, `venv/V`, `venv/M1`, `venv/M2`, `mut/n1`, `mut/n2`, `cache/{ruff,mypy,pip}`, and `scratch/{home,tmp,data,state,cwd}`. Logs, receipts and hashes live outside `scratch/`; only `scratch/` is ever deleted.

## R1 deterministic nonbillable serverless Ai fixture (finding 1)

The new fixture builds `inner = Ai()` after the allowlisted environment is in place (no `AI_*` variable present) and then sets, before any authority or request is built:

* `inner.endpoint = "http://127.0.0.1:1"` (explicit loopback; no server is started and no transport, token or evidence method is ever called),
* `inner.model_version = inner.model_version_strong = "test-model"`, `inner.fast = "test"` (as `permit_setup` also sets) and `inner.strong = "capable"`,
* `inner.consumption = service.consumption`.

The fixture asserts `inner.is_live("assessment-preparation") is False` and `inner.configured is True` immediately after construction, and asserts that the authority configuration equals `inner.configuration("test", 0, 600)` through the existing `authority` helper (deployment `"test"`). `store.ai` stays the fixture `Provider` and only `request_plan` and `is_live` are patched onto it from `inner`, exactly as `permit_setup` does; no `Provider.evidence` is wired, so no provider call is reachable. A failed assertion is INVALID SETUP.

## R2 negative-control matrix (finding 2)

Case labels (stable, used in `msg=` and `subTest`): `E1-MARGIN`, `E1-AUTHORITY`, `E1-ISSUED-AT` (case 3), `E1-FENCE`, `E2-STORED-ROOT` (5), `E2-CONFLICT-ROOT` and `E2-CONFLICT-ID` (6, two `subTest`s), `E2-FAILURE` (7). Case 6 asserts each conflict independently (rejection returns False, a `result-rejected` event, no `completed` or `output` record, task still `leased`), then the matching result still settles once.

| Case | Fixed source (V) | N1 stale clock | N2 pre-E2 attribution |
| --- | --- | --- | --- |
| 1 margin crossing | ok | FAIL at `E1-MARGIN` (AssertionError, permit granted) | ok |
| 2 authority crossing | ok | ok | ok |
| 3 valid window positive control | ok | FAIL at `E1-ISSUED-AT` (stale `issued_at` below the release time) | ok |
| 4 send-fence refusal | ok | ok | ok |
| 5 root-omitted attribution | ok | ok | FAIL at `E2-STORED-ROOT` (AssertionError) |
| 6 conflicting attribution | ok | ok | FAIL only in `subTest` `E2-CONFLICT-ROOT`; `E2-CONFLICT-ID` ok |
| 7 failure without root | ok | ok | ok |

A control is CONFIRMED only when its exact failing set matches the row set, every failure is an `AssertionError` carrying the expected label, `Ran 7`, zero errors, zero skips and the full first-failure trace is retained. Any all-green control, extra or missing failure, `ERROR` where `FAIL` is predicted, skip, import or DMV error is INCONCLUSIVE/FAIL and blocks any success claim; evidence is preserved and the work stops with no assertion tuning, retry or widened timeout.

Mutant construction: N1 copies the snapshot `src/core` to `X/mut/n1/core` and moves the single statement `now = self.now(db)` of `issue_permit` to before the `UPDATE assistant_tasks SET revision=revision+1` (the shape at frozen `a482d787`, `assistants.py` line 1047). N2 copies it to `X/mut/n2/core` and reverts the exact hunk of `d28fcd356` (restores the pre-E2 marker condition, removes `_permitted_root` use and the envelope rebinding). Each mutant records `diff -u` against the snapshot file (must be a single hunk of the stated shape; N1 moves one line, N2 equals the reversed `d28fcd356` hunk) and sha256 of both files.

Each normal and mutant process runs the origin probe `X/scripts/origins.py` with the same interpreter and environment as the test run. It prints and asserts `zava_forward.core.assistants.__file__` and `zava_forward.core.ai_consumption.__file__` resolve under `snap/src/core/src` (V) or `mut/nN/core/src` (mutants), that `zava_forward.agents` and `zava_forward.api` resolve under `snap/src`, and that no `sys.path` entry contains `snap/src/core/src` in mutant processes. Origins are logged next to each test run.

## R3 holder lifecycle, join and hard deadlines (finding 3)

Test body structure (every case with a holder):

* `holder = connect(); observer = connect()` before the `try`; `try:` begin holder transaction with plain `BEGIN TRAN` (no applock) then the task-row `UPDATE`; read `holder_spid = SELECT @@SPID` and `@@TRANCOUNT == 1`; start the claimant thread (`daemon=True`, exceptions captured into a list and re-raised by the test after the join); poll the observer; at the gated release time re-read `@@SPID` (must equal `holder_spid`) and `@@TRANCOUNT` (must be 1) and confirm `sys.dm_tran_session_transactions` has a row for the holder SPID, then roll back. A changed SPID, a dropped connection or `@@TRANCOUNT != 1` is INVALID (a reconnect never counts as the same holder).
* `finally:` unconditionally executes `IF @@TRANCOUNT > 0 ROLLBACK TRAN` and closes the holder (errors recorded, not swallowed), closes the observer separately, and only then `join(15)` the claimant. The holder is released before every join on every failure path, so a blocked worker always unblocks. A claimant still alive after the 15 s join is recorded INVALID and the original exception is re-raised.
* Outer deadlines: every SQL producer runs under `timeout -k 15 600` (TERM then KILL of only that python process group child it started) inside the driver, itself under `timeout -k 30 2400`. The driver installs `trap cleanup EXIT INT TERM` that removes only the exact captured container id (label and name verified first). Unowned processes are never signalled; killing is limited to children the driver started.
* Per-case bounded polling: 100 ms interval; the observation wait for blocking is capped at the headroom stated in R5 (not 30 s) and a timeout is INVALID, not a retry.

## R4 concrete typed fixture and lifecycle (finding 4)

Module shape (names bound to this recipe; code is written only in a later admitted phase):

* Imports as modules, not names: `import test_assistants as ta` and `import test_ai_consumption_api as base` (no helper TestCase class enters the new module namespace, so discovery finds exactly the class `MssqlPermitBoundary`). `SqlBase` is defined in the module as `class SqlBase(ta.MssqlFixture, ta.Base): pass` (zero test methods) and is not a test class.
* `class MssqlPermitBoundary(unittest.TestCase)` with typed attribute declarations `fixture: Any`, `service: Any`, `store: Any`, `provider: Any`, `inner: Any`, `pm: dict[str, Any]`, and the class decorator `unittest.skipUnless(os.environ.get("ZF_TEST_MSSQL") == "1", "needs disposable SQL Server (ZF_TEST_MSSQL=1)")`.
* `setUpClass` calls `sqlguard.require_task_owned_loopback(os.environ)` (module import, the existing helper in `core/tests/sqlguard.py`).
* `setUp` order: assert owned scratch identities (R7) and `tempfile.gettempdir()` under `X/scratch/tmp`; `self.fixture = SqlBase()`; register `self.addCleanup(self.fixture.doCleanups)` BEFORE calling `self.fixture.setUp()` so a failed setup still cleans created temp roots; call `self.fixture.setUp()`; only after it succeeds register `self.addCleanup(self.fixture.tearDown)` AFTER the doCleanups registration (unittest runs cleanups LIFO: tearDown first, then doCleanups); copy `service`, `store`, `provider`, `pm`; build `inner` per R1; never call `ConsumptionApi.setUp`, so no HTTP server and no `tempfile.tempdir` patch to `cwd`.
* Borrowed helpers: `helpers: Any = base.ConsumptionApi` and class attributes `authority = helpers.authority` and so on for the nine helpers. They are plain functions that run unchanged on the new instance because `self` there is `Any`-typed through the `Any` cast of the class; no `ConsumptionApi` subclassing (which would inherit its tests and `setUp`). `no-untyped-call` and incompatible-`self` diagnostics are avoided by this single narrow `Any` adapter; no `type: ignore` is planned except the existing convention for untyped imports if mypy requires it, each with a justification comment, no pyproject edit and no blanket ignore. If strict mypy cannot be made clean without a broader ignore, stop for Root rather than add one.
* Discovery proof: `python -m unittest -v test_permit_sql` prints `Ran 7 tests` (SQL flag set, OK) and, with the flag unset, `Ran 7 tests ... OK (skipped=7)` with the exact tolerated reason; a separate `unittest.defaultTestLoader.loadTestsFromName("test_permit_sql").countTestCases() == 7` check is logged.

## R5 actual clock witnesses with fixed coordination headroom (finding 5)

All thresholds are the source constants (`PERMIT_LEASE_MARGIN` 38.0, `PERMIT_WINDOW` 2.0, authority `end - 2.0`). Headroom values below are fixed in advance and are never widened after a failure. Every timestamp is stored or read database time (`service.now`); host `time.monotonic` bounds polls only.

One passthrough `service.now` wrapper records `(thread name, db time)` for every call; it changes no value. The observer queries `sys.dm_exec_requests` joined with `sys.dm_exec_sql_text` and `sys.dm_tran_locks`, recording the blocked claimant SPID, `blocking_session_id`, `database_id` (must equal the test database id), `wait_type`, `wait_resource`, current statement offsets (`statement_start_offset`, `statement_end_offset`, the statement must contain `UPDATE assistant_tasks SET revision=revision+1`) and the granted `APPLICATION` lock (lock order: applock first, task row second).

* Case 1 (margin, discriminates N1): `lease_until` is stored as `L0 + 42` and read back; `L0` derived from the stored value. Fresh deny threshold `L0 + 4`. Fixed headroom: holder lock acquired at database time `<= L0 + 1.5`; blocked claimant observed at `Th_obs <= L0 + 3.0`; release at database time in `[L0 + 4.5, L0 + 6.0]`. Under N1 the recorded pre-lock claimant read must be `< L0 + 4` (stale below threshold; otherwise N1 is INVALID). Under the fixed source every recorded claimant read is `>= release time`. A missed witness is INVALID/INCONCLUSIVE.
* Case 2 (authority, E1 guard; expected not to discriminate N1): `authority_seconds = 8` and the stored authority `end` read back. Deny threshold `end - 2.0`. Release in `[end - 1.5, end - 1.0]` database time, and the actual last claimant clock read before the refusal (the reservation read) must lie in `[end - 2.0, end)`, giving `authority-expiring`, not `authority-expired`; zero reservations, marker absent, `used_calls == before - 1`, one `permit-denied` event. If the reservation read is `>= end` the case is INVALID (coordination overrun), not a defect.
* Case 3 (positive control): lease 120 s, release `>= obs + 1.0` database seconds; `permit` True, `issued_at >= release time` (`E1-ISSUED-AT`), `lease_remaining == stored lease_until - issued_at`, one `reserved` record equal to `meter_id`, `permitted` marker with `issued_at`, `dispatch_within_ms >= 1`, then `duplicate-permit` with still one reservation.
* A KEY/DMV witness that is absent (other granularity, DMV permission denied, no blocked row within the headroom) is INVALID/INCONCLUSIVE and stops; a mismatch is called a source defect only when every setup witness above is valid.

## R6 executable subprocess recipes (finding 6)

Common: `W=<worktree>` absolute; `S=X/snap` (snapshot of the worktree source made by `git ls-files -z --cached --others --exclude-standard src | tar --null -T - -cf - | tar -x -C X/snap` and verified as the committed `HEAD^{tree}` plus exactly the one new test file whose sha256 is logged); `PYENV` = `env -i` allowlist from R7. Python and tool paths are venv-specific absolute paths (`X/venv/V/bin/python`, `.../ruff`, `.../mypy`). Every subprocess redirects `>X/logs/NN-name.out 2>X/logs/NN-name.err` and writes `echo $? > X/logs/NN-name.exit` on the very next statement; no `tail`, `tee`, pipe or `grep` participates in a producer; first-failure traces stay; reruns get new names; `set -x` is never enabled.

* X0 identity (cwd `W`): `git rev-parse HEAD`, `git rev-parse 'HEAD^{tree}'`, `git status --short --ignored`. Expected before Implement: clean.
* X1 missing-dependency/binding probe, expected to fail and preserved: `python3.12 -m venv X/venv/V`; then `X/venv/V/bin/python -c 'import zava_forward.core'`, `X/venv/V/bin/python -m ruff --version`, `X/venv/V/bin/python -m mypy --version`. Only if these fail (expected) do installs proceed.
* X2 install (conditional admission, pip only, no uv, no global install, no manifest edit): `X/venv/V/bin/python -m pip download --require-hashes -r S/src/api/requirements.txt -d X/wheelhouse` and `-m pip download ruff==0.17.1 mypy==2.4.0 -d X/wheelhouse-tools`; then `-m pip install --no-index --find-links X/wheelhouse --require-hashes -r S/src/api/requirements.txt`, `-m pip install --no-index --find-links X/wheelhouse-tools ruff==0.17.1 mypy==2.4.0`, and `-m pip install --no-deps -e S/src/core -e S/src/agents -e S/src/api`. Pins justified: runtime hashes from the repository requirements; `ruff==0.17.1` and `mypy==2.4.0` match `src/api/pyproject.toml` dev extras and CI. Mutant venvs M1/M2 repeat the hashed runtime install from the local wheelhouse (no new egress) and `-e X/mut/nN/core -e S/src/agents -e S/src/api`. `pip freeze` and wheel sha256 are logged; the only network egress is the two `pip download` steps, carrying package names only.
* X3 static, cwd `S/src/api`, config `S/src/api/pyproject.toml` explicit: `ruff check --no-cache --config pyproject.toml tests/test_permit_sql.py`, `ruff format --check --no-cache --config pyproject.toml tests/test_permit_sql.py`, `mypy --config-file pyproject.toml --cache-dir X/cache/mypy tests/test_permit_sql.py tests/test_ai_consumption_api.py`; run through the venv V binaries, three separate producers. cwd is the owned snapshot, not the worktree.
* X4 SQLite carry-forward, cwd `X/scratch/cwd` (owned, so `Path.cwd()`-based tempdir lands in scratch), `PYTHONPATH=S/src/api/tests:S/src/core/tests:S/src/agents/tests` absolute, flag unset, one producer invoking 15 fully qualified ids, no class-level selector: `V/bin/python -m unittest -v test_ai_consumption_api.ConsumptionApi.<id>` for each of:
  `test_permit_reserves_once_marks_and_fences_the_attempt`, `test_permit_denials_reserve_nothing`, `test_permit_reads_database_time_after_the_blocking_update_for_every_use`, `test_a_lock_wait_that_crosses_the_lease_margin_refuses_without_a_reservation`, `test_a_lock_wait_that_crosses_authority_expiry_refuses_without_a_reservation`, `test_a_short_authority_shortens_the_window_and_too_short_is_refused_unreserved`, `test_suspension_after_claim_denies_the_permit_and_refunds_once`, `test_consent_withdrawal_and_captured_readings_fail_closed_to_manual`, `test_an_unavailable_send_fence_refuses_without_a_reservation_or_a_marker`, `test_marker_blocks_reclaim`, `test_settlement_binds_to_the_marker_and_late_results_settle_the_meter_only`, `test_permitted_result_binds_attribution_to_the_stored_reservation_root`, `test_permitted_result_rejects_conflicting_attribution_without_settling`, `test_permitted_failure_without_root_settles_the_meter_and_publishes_no_output`, `test_result_without_a_permit_closes_the_task_against_a_later_permit`. Requirement: `Ran 15 tests`, `OK`, zero skips (the original red3/green11 bound is carried forward by byte identity of the source and is not re-executed beyond these selectors).
* X5 flag-unset skip proof, same cwd, `ZF_TEST_MSSQL` absent from the allowlist: `V/bin/python -m unittest -v test_permit_sql`; require `Ran 7 tests`, `OK (skipped=7)` and the exact tolerated skip reason, plus the discovery-count check.
* X6 heavy admission: `flock -n /tmp/ama-rpi-heavy.lock` held by the driver; busy means UNADMITTED, stop, no queue or spin, no other process touched. Probe actual holder, free memory (need >= 6 GiB available), free disk (>= 20 GiB), loopback port ownership (publish `127.0.0.1::1433`, random port), image id and digest equal the pinned values, local unix docker socket only.
* X7 container (inside the lock): `docker run -d --name zf-144-permit-sql-e3-1111 --label zf.task=1292-sql-disposable --label ama.rpi.owner=<token> --label ama.rpi.task=issue-144-permit-sql-e3-plan-p1-1111 --memory=3g --cpus=2 --publish=127.0.0.1::1433 --env=ACCEPT_EULA=Y --env=MSSQL_PID=Developer --env=MSSQL_MEMORY_LIMIT_MB=2048 --env MSSQL_SA_PASSWORD` with the random password exported in the driver environment only (never in argv, a log or xtrace); receipt via `docker inspect <id> --format` allowlist (R7); `sqlguard.write_manifest` private 0600; readiness: at most 40 probes of `SELECT 1` (not a test retry); version query.
* X8 real SQL, cwd `X/scratch/cwd`, same allowlist plus the `ZF_TEST_MSSQL=1` and the `ZF_SQL_*` variables for the owned container, interpreter V: `timeout -k 15 600 V/bin/python -m unittest -v test_permit_sql.MssqlPermitBoundary` preceded by the origin probe. Require `Ran 7 tests`, `OK`, no `skipped`, each of the seven ids `ok`, DMV and clock witnesses recorded for cases 1 to 3.
* X9 negative controls, same container, same test file bytes: N1 in venv M1 then N2 in venv M2 (cwd `X/scratch/cwd`, origin probe first, separate logs and exits, same bound). Evaluate the R2 matrix.
* X10 cleanup and readback: database readback (databases present, task rows and counts, no credentials) saved to `receipts/` BEFORE container removal; sha256 of every log and receipt written to `receipts/sha256.txt` outside scratch; then remove only the exact captured container id after label and name verification; `docker inspect <id>` must fail and `docker ps -a --filter label=ama.rpi.owner=<token>` must be empty; remove only the resolved owned manifest and `X/scratch/*` (realpath under X); verify the heavy lock is free; `git status --short --ignored` in the worktree shows exactly the intended Option T file(s) before commit and no egg-info (installs live under `X/snap`).

## R7 isolation and credential-safe receipts (finding 7)

* Allowlisted environment (`env -i`) for every Python subprocess, established before any import: `PATH=<venv bin>:/usr/bin:/bin`, `HOME=X/scratch/home`, `TMPDIR=X/scratch/tmp`, `ZF_DATA=X/scratch/data/zavaforward.json`, `ZF_STATE=X/scratch/state`, `LANG=C.UTF-8`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH` as absolute helper directories (R6), `RUFF_CACHE_DIR`/`MYPY_CACHE_DIR` under `X/cache`, `PIP_CACHE_DIR=X/cache/pip` for pip steps only, no `AI_*`, `AZURE_*`, `IDENTITY_*`, `ZF_AI*`, proxy or credential variable. For SQL steps add only `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_PORT`, `ZF_SQL_DATABASE=master`, `ZF_SQL_AUTH=password`, `ZF_SQL_USER=sa`, `ZF_SQL_PASSWORD` (from a 0600 file read inside the driver), `ZF_SQL_TRUST_CERT=1`, `ZF_SQL_TASK_MANIFEST`.
* Before tests: assert resolved `HOME`, `TMPDIR`, `ZF_DATA`, `ZF_STATE` and cwd are under `X/scratch`, that the default `~/.zava-forward` path is neither read nor created, and that `tempfile.gettempdir()` is under `X/scratch/tmp`. `Base` builds constructed `test_mvp.DATA`; no private dataset is read.
* `ConsumptionApi.setUp` (X4) sets `tempfile.tempdir` to `Path.cwd()` with no source edit: run from the owned external `X/scratch/cwd` so that scratch lands there; the new module never uses that setUp.
* Docker receipts only from `docker inspect <id> --format '{{.Id}} {{.Image}} {{json .Config.Labels}} {{json .NetworkSettings.Ports}} {{.State.Status}} {{.HostConfig.Memory}} {{.HostConfig.NanoCpus}}'` (id, image, labels, ports, state, limits). Never `.Config.Env`, a connection string, an environment dump or xtrace. A post-run scan of `logs/` and `receipts/` for the password token (as a literal held in memory only) must find zero hits; a hit makes the run unpublishable and is recorded.
* Retention: logs, receipts, hashes and the reports persist outside `scratch/`; only `scratch/`, the container and the manifest are cleaned.

## Assertions retained from the independent report (existing contracts only)

Case 5 (E2, root omitted): `complete_result` returns True; exactly one `output` record with `root == reserved[0]["root"]`, `output` reference present and `eligible` as stored; the permitted result envelope carries meter id equal to the stored `meter_id` and the stored root; ready task state; verify/review and `accepted_proposals == 1` from `consumption.report(start=START, end=END, as_of=END)`; one `completed` record with the returned `id` and `tokens`; a repeated postback with the same result does not settle twice (still one `completed`, one `output`).
Case 6: each conflicting `meter_root` and `meter_id` rejects independently with no output, no completion, no settlement and the task still `leased`, then the matching result settles once.
Case 7: `completed` record `outcome == "provider-unavailable"`, `tokens is None`, `charge is None`, `held is True`; no `output`, no review record.
No broader contract is added.

## Disposition matrix (independent report to this correction)

| Id | Report finding | Severity | Disposition | Where |
| --- | --- | --- | --- | --- |
| R1 | 1 nonbillable Ai fixture | High | Resolved in plan: explicit loopback endpoint, fixed models, consumption binding, `is_live` false, no transport | section R1 |
| R2 | 2 non-discriminating controls | High | Resolved: per-test matrix, labels, mutant diffs/hashes, origin proof, INCONCLUSIVE rule | section R2 |
| R3 | 3 join does not bound worker/lock | High | Resolved: unconditional holder rollback, release before join, SPID/@@TRANCOUNT continuity, outer deadlines, exact-container trap | section R3 |
| R4 | 4 typed fixture composition | Medium | Resolved: SqlBase MRO, instance, cleanup order, `Any` adapter, seven-test discovery proof | section R4 |
| R5 | 5 prelaunch clock checks | Medium | Resolved: recorded actual clock witnesses, fixed headroom, INVALID classification | section R5 |
| R6 | 6 recipe lacks tooling/selectors | Medium | Resolved: pinned tool install after probe, 15 fully qualified ids, per-process cwd/path/flag/origin | section R6 |
| R7 | 7 isolation and receipts | Medium | Resolved: allowlist env, scratch assertions, allowlisted inspect fields, retention | section R7 |

No finding is regraded, withdrawn or marked as an application defect. Closure of these dispositions requires independent prospective clearance of this plan by the same reviewer; the authored critique is not independent.

## Limits (unchanged and explicit)

Local SQL Server 2022 Developer only, not Azure SQL, hosted MSSQL, production or provider; no consent, spend, deployment or release activation; B-scope worker, queue, routes, publisher, date and backoff excluded; dispatch-time recheck not covered; consent/readings/operator-disable remain SQLite predicate-patched evidence; no full or `--changed` gate; no hosted CI selection of the new module; evidence for whole-#144 acceptance is not claimed. Unobserved: everything in X1 to X10 until Root admits.
