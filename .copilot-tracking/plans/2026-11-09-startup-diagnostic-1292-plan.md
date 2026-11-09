---
title: Issue 1292 startup lock diagnostic plan
ms.date: 2026-11-09
task_id: 1292-startup-diagnostic-1109
---

## Task metadata

* Task `1292-startup-diagnostic-1109`. Research `.copilot-tracking/research/2026-11-09-startup-diagnostic-1292-research.md` (executed, Ready). Details `.copilot-tracking/details/2026-11-09-startup-diagnostic-1292-details.md`. Critique `.copilot-tracking/plans/2026-11-09-startup-diagnostic-1292-critique.md`.
* Branch `test/demo-startup-diagnostic-1292-1109`, base and target `main` `ef28d4da42d83b111d48f14df9b70e3c4932a477`. Source-equivalent to `8d6f029cac004506953f36606862168bbe9d9412` (diff is only `.github/rubric/scores/latest.json`).

## Executive summary

Localize, or fail to localize, the cause of one `database is locked` error by running the exact affected test a bounded number of times on unchanged source, with observer-only instrumentation to capture where and when the exception arises. Output is a diagnosis record, not a fix.

## User decisions and requirements

* Genuine RPI in order; research, plan, details and critique are committed BEFORE any attempt.
* Zero source or test edit, skip, timeout relaxation, retry-as-fix, transplanted test, baseline deletion, SQL service, cloud, model, private data, global install, `rpi-checks` or full gate.
* No push, PR, issue, board or publication. Local freeze and a handoff `handoff-1292-startup-diagnostic.md` in the coordinator files directory.
* A needed source correction is reported (smallest confirmed cause and scope with evidence); the coordinator decides whether E5 applies. Nothing is implemented here.

## Functional requirements and exact commands

* FR1 environment: an owned `mktemp -d` directory `/tmp/i1292sd-XXXXXX` holds a venv created with `python3 -m venv` (no system site packages) used only for third-party prerequisites. Project imports are worktree-bound through `PYTHONPATH` entries `src/core/src:src/agents/src:src/api/src` plus the component tests directories, with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPYCACHEPREFIX` in the owned directory, so no editable-install metadata or bytecode is written in the source tree. `pip install` of pinned `requirements.in` entries (`mssql-python==1.15.0`, `aiohttp==3.14.5` and others) happens only on an observed ImportError and is logged. The global `zava-forward-*` editables point at another checkout and are not used. Verified by an import-origin check that prints each `zava_forward.*` namespace `__path__` and the origin of `sqlstore.py`, all under this worktree, and the sha256 of `sqlstore.py`, `store.py`, `test_priority_order.py`.
* FR2 exact test command (cwd `src/core`): `PYTHONPATH=tests:../core/src:../agents/src:../api/src <venv>/bin/python -m unittest -v tests.test_priority_order.SqliteLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers`. Per attempt, wrapped in `timeout 180`, capture stdout, stderr, exit and wallclock with `date +%s.%N`, `/proc/loadavg` and `nproc` before and after.
* FR3 attempt matrix, at most six in total, in this order, stopping early on a localized result:
  * Isolated I1 (unmodified command above), I2 and I3 (observer harness, labelled `OBSERVER`). One at a time, nothing else of mine running.
  * Concurrent C1 (unmodified command), C2 and C3 (observer harness). Each starts one API companion first, then the Core test about 3 s later. Actual process intervals and the two opener-thread intervals are recorded; if the companion ends or fails before the opener interval the attempt is classified inconclusive for contention (still counted against the cap). The companion is the existing API module only: `cd src/api; PYTHONPATH=tests:../core/tests:../agents/tests:../core/src:../agents/src:src <venv>/bin/python -m unittest -q tests.test_auth`, `timeout 240`, output kept. No other load.
* FR4 observer (external, outside the repo, separately labelled `OBSERVER`): a runner imports the same test module and wraps `SqlStore._initialize`, `_migrate_recommendations`, `_audit_evidence`, `_backfill_zero_ordinals`, `_review_priority_order` (those that exist) and `SqlStore._open`. Wrappers only append small tuples (monotonic time, thread name, event) to an in-memory list and keep the raised exception object; all formatting, tracebacks, `sqlite_errorcode` and `sqlite_errorname` are produced after the test ends. Recording is guarded so a recorder failure cannot mask the original exception, which is re-raised unchanged. After `_open`, the observer calls `connection.set_trace_callback` with a recorder that keeps only statements starting with BEGIN, COMMIT, ROLLBACK, CREATE, ALTER, DROP or PRAGMA (first 80 characters). That yields lock acquisition and release boundaries without altering SQL. Method-level timing alone is not write-lock hold time and is not reported as such; hold time is derived only from the BEGIN IMMEDIATE and COMMIT/ROLLBACK trace events and labelled an inference. Observer runs perturb timing and are never used to claim the unmodified result.
* FR5 evidence: raw logs and hashes (sha256) in the owned external directory `/home/azureuser/source/ama-demo-wt/logs-1292-startup-diagnostic/` (not committed). Commit only concise records.

## Resource and stop caps (set before running)

* At most 3 isolated plus 3 concurrent attempts; no retry of an attempt, no re-run to obtain a pass or a failure beyond this matrix.
* Core attempt wallclock cap 180 s; API companion cap 240 s; overall diagnostic cap 30 min wallclock.
* At most two of my processes at once (one Core test, one API module); the test's own two opener threads are the subject. No stress tool, no whole Core or API suite, no Docker or SQL service, no shared heavy resource.
* Skip (do not queue) an attempt and record it when `loadavg1` exceeds 12 at start.
* Stop on: a localized result (exception location captured with a consistent mechanism), the attempt cap, a cap breach, or a need for broader or source investigation (reported, not performed).

## Phases

* Phase 1 environment and import origin (FR1). Phase 2 isolated attempts. Phase 3 concurrent attempts. Phase 4 analysis and unchanged-source proof (`git status --short --ignored` shows no new or ignored file in the tree before and after, and `git diff --stat ef28d4da4 -- src infra tools .github pyproject.toml` is empty). Phase 5 concise diagnostic record in the changes artifact, review, handoff.

## Success criteria

* Every attempt has command, identity, exit, duration, load and output retained with hash. Source and test unchanged and proven. The record states a localized cause with confidence, or states the cause remains unknown with the unknowns. No claim of a flake or fix without evidence.

## Risks

* Observer timing overhead is small but nonzero. Shared host load varies. No reproduction in six attempts is a valid, unresolved outcome.
