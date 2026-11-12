---
title: Issue 144 permit SQL E4 corrected plan P2
description: Amended executable recipe for real disposable-MSSQL validation of the worker-permit boundary, resolving the P1 independent findings (1 High, 3 Medium)
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e4-plan-p2-1111
---

## Status and authority

* Research done, Plan correction done (this document, details, authored critique). STOP before Implement. Nothing here has been run or observed: no database, container, test, install, download, scanner, provider, model, Azure or GitHub command.
* This amends `issue-144-permit-sql-e3-plan-p1-1111-plan.md` (frozen, unchanged) only where stated below. Everything else in the original plan and P1 (Option T single module `src/api/tests/test_permit_sql.py`, direct-only local scope, seven cases, R1 Ai fixture, allowlisted environment, receipts, heavy-lock admission, image identity, limits, D4) is inherited unchanged. Parent critiques and both independent reports are unchanged adverse history.
* Counter: Nov 10 extension; E1/E2/E3 counted; E4 admitted and counted from this correction; one unadmitted cycle remains; no E5, no new five, no reset. A later implementation belongs to this same E4.
* Gates: G1 is independent prospective clearance of this actual P2 delta by the same reviewer `9e2e122a-295f-46f8-af5a-9e28472a4d06`; G2 is Root's explicit admission of implementation, the conditional pip steps and the current nonqueued heavy-resource, container and SQL run. Neither is given here. A valid-witness fixed-source mismatch stops on existing #144 with no source fix and no new issue.

## F1 (High) N2 contamination: case 6 flow

Seven methods retained. Case 6 `test_permitted_result_rejects_conflicting_attribution_without_settling` uses ONE leased task and this exact order, with nothing after the last subTest:

1. Baselines before any caller result: `completed_n`, `output_n` (counts of `completed` and `output` records), `used_calls`, `reserved_tokens` (allowance row), task state `leased`, `result-rejected` event count `r0`.
2. `with self.subTest("E2-CONFLICT-ID")` first: `permitted_result(task, meter_id="a"*64)`. Labelled assertions: `assertFalse` (rejection), `result-rejected` count equals `r0 + 1`, `completed_n` and `output_n` unchanged, `used_calls` and `reserved_tokens` equal baselines, task still `leased`. The id branch is unchanged by E2, so it passes on fixed source and on N2 and runs on an unmutated task.
3. `with self.subTest("E2-CONFLICT-ROOT")` LAST, containing in order: (a) `assertFalse(permitted_result(task, meter_root="a"*64), msg="E2-CONFLICT-ROOT")` FIRST; (b) baseline-relative no-mutation checks (`result-rejected` equals `r0 + 2`, `completed_n`, `output_n`, `used_calls`, `reserved_tokens` unchanged, task `leased`); (c) only then the matching result `assertTrue(permitted_result(task, meter_id=permit["meter_id"]))`, exactly one new `completed`, and a repeated postback asserting counts unchanged (not that it returns True).
4. Nothing follows the root subTest, and the matching success lives only inside it.

Predicted flows. Fixed source: every assertion passes. N1 (stale clock only): case 6 passes. N2 (pre-E2): the id subTest passes before any mutation; in the root subTest (a) fails (the conflicting root is forwarded, the meter settles and an output is written, the task becomes `ready`), which aborts that subTest with the labelled `AssertionError`; its mutation cannot reach the already-finished id branch and there are no later checks. Matching success executes only on fixed source after the refusal and no-mutation assertions succeed.

Frozen matrix (unchanged from P1, now consistent with the flow): N1 fails exactly case 1 (`E1-MARGIN`) and case 3 (`E1-ISSUED-AT`); N2 fails exactly case 5 (`E2-STORED-ROOT`) and case 6 only in subTest `E2-CONFLICT-ROOT` (`E2-CONFLICT-ID` is not a failure). Zero errors, zero skips, `Ran 7`, labelled `AssertionError` only, full first-failure traces, no all-green control, no extra or missing failure; anything else is INCONCLUSIVE and stops with no assertion tuning or retry. In case 5 an N2 `IndexError` or other exception is INCONCLUSIVE (see case 5 below).

## F2 (Medium) Offline build backend

Facts: `src/core`, `src/agents`, `src/api` require `setuptools>=77`; the venv's bundled pip alone is not a usable build environment (the legacy ext1 venv has none, and it is not reused).

Prospective pins (availability UNOBSERVED until a separately admitted download; not a successful observation): `setuptools==80.9.0` (satisfies `>=77`, py3.12) and `wheel==0.45.1`. Runtime hashed requirements unchanged; tools `ruff==0.17.1` and `mypy==2.4.0` unchanged.

Amended X2, after the preserved X1 failing probe and Root's separate install admission only:

* X2a: `pip download` into `X/wheelhouse-tools`: `setuptools==80.9.0 wheel==0.45.1 ruff==0.17.1 mypy==2.4.0` (with their dependencies). Wheel sha256 of every file written to `receipts/wheel-sha256.txt`; any sdist-only or missing artifact is a blocked environment, not a relaxed pin. Runtime download into `X/wheelhouse` from the hashed requirements as before. These are the only network steps, so there is no hidden PEP 517 egress.
* X2b: in each of V, M1 and M2, offline install: `pip install --no-index --find-links X/wheelhouse-tools setuptools==80.9.0 wheel==0.45.1`; runtime `pip install --no-index --find-links X/wheelhouse --require-hashes -r requirements.txt` (the hashed file, unchanged); V also installs ruff and mypy offline from `X/wheelhouse-tools`.
* X2c: every editable operation is `pip install --no-build-isolation --no-index --find-links X/wheelhouse-tools --no-deps -e <dir>`; V uses `-e snap/src/core -e snap/src/agents -e snap/src/api`, M1 uses `mut/n1/core` plus `snap/src/agents` and `snap/src/api`, M2 uses `mut/n2/core` plus the same two. Build directories and `*.egg-info` land only under `snap/` and `mut/`; the worktree gains none (final `git status --short --ignored` must be empty of them).
* Hashes of installed wheels (`pip freeze` plus `pip list --format=json`) and import origins are logged. The Root install admission is still mandatory and not given here.

## F3 (Medium) Strict fixture boundary

Replace the P1 `class SqlBase(ta.MssqlFixture, ta.Base)` statement. Imports stay module-style (`import test_assistants as ta`, `import test_ai_consumption_api as base`), so no helper test class is a module attribute and none is inherited. Inside the local fixture boundary (`setUp`) the composite is built at runtime:

* `composite: Any = type("PermitSqlFixture", (ta.MssqlFixture, ta.Base), {})` and `self.fixture: Any = composite()`. A `type()` call is not a class-statement subclassing site, `ta.*` stay `Any` through the existing `ignore_errors`/`follow_imports = skip` overrides, and no `type: ignore` is added for it. The composite has no test methods of its own; `ta.Base`'s own `unittest.TestCase` machinery is exercised only through the instance, never discovered, because it is not a module attribute. This also keeps `Ran 7`.
* Kept unchanged: the single narrow `helpers: Any = base.ConsumptionApi` adapter for the nine borrowed helpers; `setUpClass` calling `sqlguard.require_task_owned_loopback(os.environ)` before any connection; LIFO order: `addCleanup(fixture.doCleanups)` is registered BEFORE `fixture.setUp()` and `addCleanup(fixture.tearDown)` AFTER the successful call, so tearDown runs first, then doCleanups; no `ConsumptionApi.setUp`, no HTTP server; exact seven-method discovery count, flag-unset `skipped=7` proof and static proofs per X3/X5.
* Reasoning only (mypy was not executed): the remaining strict diagnostics are `no-untyped-def`, `no-untyped-call` and `no-any-return`; all test methods get full annotations, calls into `Any` objects are not flagged, and the new module contains no subclassing of `Any`. If strict is not clean without a broader ignore or a pyproject edit, the work stops for Root; no blanket ignore is added.

## F4 (Medium) Independent cleanup

Replace the P1 sequence with an `ExitStack`-style protected structure. Each resource registers its cleanup immediately after acquisition, and the callbacks are registered so LIFO execution is: holder rollback, holder close, observer close, then thread join.

```text
errors = []                                   # cleanup errors, kept visible
worker = None
with ExitStack() as stack:                    # outermost
    stack.callback(finish_worker)             # registered FIRST => runs LAST (join)
    holder = connect_holder()                 # acquisition
    stack.callback(close_quietly, holder, errors)       # holder close, always attempted
    stack.callback(rollback_quietly, holder, errors)    # rollback FIRST at unwind
    observer = connect_observer()             # acquired inside holder's protected region
    stack.callback(close_quietly, observer, errors)     # observer close, independent
    ... BEGIN TRAN, UPDATE, SPID/@@TRANCOUNT, start worker, poll, gated release ...
```

* Callback ordering is explicit: `finish_worker` is registered before any connection callback, so at unwind the order is observer close, holder rollback, holder close, then `finish_worker`. The holder is therefore always released before the join; registering the join first guarantees it can never run first.
* `rollback_quietly` and `close_quietly` catch their own exceptions into `errors` (they never raise), so a failing rollback cannot prevent the holder close, the observer close or the join. After the stack unwinds, a test that already had a primary exception re-raises it with the `errors` list appended visibly (`raise primary` with a note; if none, a cleanup error raises an `AssertionError("CLEANUP-ERRORS: ...")`). Nothing is silently swallowed or abandoned.
* `finish_worker` joins only a thread that was actually started (`worker is not None and worker.is_alive()` checked before `join(15)`); a worker still alive after the join raises INVALID (`WORKER-STILL-LIVE`) even when no earlier failure occurred. The worker is a daemon, its exception is captured into a list and re-raised after unwind.
* Retained containment: SPID and `@@TRANCOUNT` continuity checks, hard producer deadline `timeout -k 15 600`, driver deadline `timeout -k 30 2400`, exact owned-container `trap`; only child processes the driver started are ever signalled, never an unowned process.

## Coverage-clarity items

* Case 5 flow: assert the complete `output` collection count equals 1 with label `E2-STORED-ROOT` BEFORE indexing; then the tuple `(root, output reference, eligible)` equals `(stored reserved root, reference(task["id"]), True)`; envelope `meter_id` equals the permit `meter_id` and `meter_root` equals the stored root; task state `ready`; verify/review; `accepted_proposals == 1`; the single `completed` record carries the returned id and `tokens`; a repeated postback of the same result asserts counts unchanged (completed, output, allowance) and does NOT assert it returns True. A missing output is then the labelled assertion, not an `IndexError`; any N2 exception remains INCONCLUSIVE.
* Case 2 clock: the plan records the actual `reserve_in` clock separately only if the passthrough `service.now` wrapper sees it (the reservation read is the second claimant read after the post-update `issue_permit` read). It therefore treats the last claimant clock read before the refusal as a conservative refusal-time bound, NOT as a directly observed reservation timestamp. Justification from call order: `issue_permit` reads `now` after the UPDATE, runs `_fence_in`, then `reserve_in` reads `now` again, and the refusal event follows; every recorded read is `>=` the release time, so `last_read < end` proves the reservation read was `< end`, and `release >= end - 1.5` plus read `>= release` keeps it in `[end - 1.5, end)`. The case is INVALID if `last_read >= end`.
* Snapshot manifest: byte identity is proved by a per-file listing of the snapshot (`git ls-files -z --cached --others --exclude-standard src`, sorted, one `sha256  path` line per file) written to `receipts/snapshot-sha256.txt`, compared with the same listing computed from the worktree immediately before snapshotting and again after the run, plus the committed `HEAD`, tree and the one new test file hash. Differences stop the run.
* Origin evidence: the companion probe `origins.py` and the test process itself (a module-level first-statement check in the test run wrapper, written under `X/scripts`, no source edit) print resolved `__path__`/module file for `zava_forward.core.assistants` and `.ai_consumption`. Namespace packages use `importlib.util.find_spec(name).origin` and `submodule_search_locations` (resolved realpath), not an assumed `__file__`. Mutant processes require the mutant core path and require that no `sys.path` entry or `__path__` contains the normal `snap/src/core/src`, so the normal core cannot shadow the mutant core.
* Safe allowlisted environment, scratch-data and private-data boundaries, password-safe receipts and scan, retention, literal loopback and SQLGuard before connection: unchanged. No claim is made that any future static, runtime, DMV, timing, mutant or wheel result was observed.

## Disposition matrix (P1 findings to this correction)

| Id | P1 report finding | Severity | Disposition |
| --- | --- | --- | --- |
| P2-F1 | N2 root-conflict mutation contaminates shared task | High | Resolved in recipe: id branch first, root branch last with all follow-on checks inside it, matrix refrozen |
| P2-F2 | Editable installs admit PEP 517 downloads | Medium | Resolved in recipe: pinned backend wheels in the existing wheelhouse download, offline installs, `--no-build-isolation --no-index --no-deps` for every editable |
| P2-F3 | Any helper adapter does not fix subclassing of skipped imports | Medium | Resolved in recipe: runtime `type()` factory typed `Any`, no class-statement subclass, no ignore, no pyproject edit |
| P2-F4 | Cleanup independence | Medium | Resolved in recipe: ExitStack ordering, failure-tolerant rollback and closes, join only a started worker, live worker INVALID, visible errors |

No finding is regraded; closure requires G1 by the same independent reviewer. The authored critique is not independent.

## Scope and limits (unchanged)

Option T, one new test file plus dated RPI records, direct-only local qualification, no hosted SQL coverage, no CI, workflow, `SQL_SELECTORS`, gate, source, helper, requirement or pyproject change, no blanket full gate, no production, legal, consent, spend or cloud authority, no whole-#144 acceptance.
