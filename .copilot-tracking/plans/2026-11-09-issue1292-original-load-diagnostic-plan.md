---
title: Issue 1292 original-load diagnostic plan
ms.date: 2026-11-09
task_id: 1292-original-load-diagnostic-1109
---

## Task metadata

* Research `.copilot-tracking/research/2026-11-09-issue1292-original-load-diagnostic-research.md` (executed, Ready). Details `.copilot-tracking/details/2026-11-09-issue1292-original-load-diagnostic-details.md`. Critique `.copilot-tracking/plans/2026-11-09-issue1292-original-load-diagnostic-critique.md` (one pass only).
* Branch `test/demo-startup-diagnostic-1292-1109`, frozen `72ca1c9aac6396e19174352a3503f9b5e4ee8643`, base `ef28d4da42d83b111d48f14df9b70e3c4932a477`, pinned runtime source `8d6f029ca`. Local only: no push, PR, issue, board, cloud, merge, rebase or amend. Refs #1292 only; every criterion stays unticked.
* Tier: owner-selected demo-targeted focused diagnostic. It is not a release, not the complete local gate and not independent review. No `rpi-checks`.

## Authority and counters

* Not an E5 source fix and not extra correction authority. E4 history is immutable; E5 and the one remaining productive source correction are neither spent nor changed. No source, test, assertion, observer-semantics or harness behavioural fix. No injected failure, load, I/O or sleep.
* New diagnostic counters: at most TWO exact original paired selections (pair = one Core selection process plus one API selection process), at most 420 s per process, ONE actual holder check and ONE nonqueued admission of `/tmp/ama-rpi-heavy.lock` for the whole campaign. Prior campaign counters (6 attempts, one non-counted harness defect) stay as they are and are not reused or reset.

## Requirements

* R1 Exact originals: Core `tests.test_priority_order tests.test_resident_decisions tests.test_sqlstore tests.test_journey_store` from `src/core` with `PYTHONPATH=tests`; API `tests.test_case_journey tests.test_auth tests.test_entra_authoritative tests.test_role_endpoint_inventory tests.test_role_matrix tests.test_assistants` from `src/api` with `PYTHONPATH=../core/tests:../agents/tests:tests`; both with `env -u ZF_TEST_MSSQL -u ZF_SQL_TASK_MANIFEST` and `python -m unittest -v`; owned venv with editable installs as in the original profile.
* R2 Provenance before any attempt: full import origins for `zava_forward.core`, `.api`, `.agents`, `zava_forward.core.store`, `.sqlstore`, `.mssqlstore`, `zava_forward.api.server`, `zava_forward.agents.queue_azure`, `mssql_python`, `pyodbc`; sha256 of `store.py`, `sqlstore.py`, `mssqlstore.py`, the ten selected test files and the harness scripts; Python and `sqlite3` versions; installed package versions; producer commands; environment profile as variable names and non-secret values only (no secrets, no fixtures). This corrects the FR1 gap prospectively and does not repair past import provenance.
* R3 Timing record per process: real start and end (UTC `date +%s.%N`), exit, command, overlap interval, load average before and after, tests discovered, executed and skipped, full stdout and stderr in separate external files.
* R4 Plain versus OBSERVER stay distinct everywhere. Test processes run under a cleared environment (`env -i` with `PATH`, `HOME`, `LANG` and owned `PYTHONPATH`, `PYTHONDONTWRITEBYTECODE`, `PYTHONPYCACHEPREFIX`, `TMPDIR`, `ZF_DATA`), so no provider, credential, cloud or private-data variable or path is reachable; provenance lists variable names and only allowlisted non-secret values. The observer perturbs timing and failure semantics and is never claimed equivalent.
* R5 If the failure reproduces, preserve the full exception traceback, type, message, `sqlite_errorcode` and `sqlite_errorname`, and stop after a smallest confirmed root-scope proposal; otherwise keep cause UNKNOWN, with no proposed source fix and no flake or necessary-load claim.
* R6 New additive records only: the 14 existing original and qualification records, the 29-member raw packet and the original Reviews stay byte-equal (baseline sha256 before, re-hashed after). No amend, no history rewrite; the final handoff may cite the actual record commit.

## Phases and acceptance criteria

* P0 Planning commit: research, plan, details, one critique and state, committed BEFORE any environment creation, probe or attempt.
* P1 Profile probe and environment: chosen profile A is the system `python3` with the worktree source directories on `PYTHONPATH` and no installation. Run only an import probe; if it fails for missing packages (expected: the API package dependencies), create ONE owned venv (otherwise profile A is the runtime, recorded as a deviation) under `mktemp -d /tmp/i1292old-XXXXXX` and install exactly as the original (`pip install -q -e src/core -e src/agents -e src/api`). No global installs. Do not use `venv-440-1109` (another lane).
* P2 Provenance: write the provenance file and its sha256 manifest to the external directory `/home/azureuser/source/ama-demo-wt/logs-1292-original-load-diagnostic/` before the holder check. Criterion: every item of R2 recorded, or recorded as unavailable.
* P3 Admission: one `fuser`/`lsof` holder check; if a holder exists, stop with status UNADMITTED (no admission attempt, no retry, no queue, no signal to another holder). Otherwise one `flock -n` on `/tmp/ama-rpi-heavy.lock`, held for the whole campaign by a single driver process; if `flock -n` fails, stop UNADMITTED.
* P4 Pair 1 (PLAIN): start the API process, then immediately the Core process (the original listing order), each under `timeout 420`; wait for both; record. Pair 2 (OBSERVER on Core only, API plain) runs in the same admission only when the structured gate in the details holds (both processes finished without the 420 s cap, both logs have `Ran N tests` with N>0, API exit 0, Core PASS or REPRODUCED, no profile mismatch or driver fault). Stop-rule interpretation, stated before any attempt: a plain reproduction answers RQ-1 but cannot preserve the exception traceback (the test prints only the `errors` list), so the stop-after-preserved-trace rule is not yet met and pair 2 (still inside the two-pair cap) is the single attempt to capture the trace; this ordering and reading is a disclosed plan decision, not a claim that plain and observer runs are equivalent. A reproduction in the OBSERVER pair stops the campaign at once.
* P5 Classification per pair: REPRODUCED = the target test fails with `OperationalError('database is locked')` in `errors`; PASS = Core exit 0 with all selected tests run; CAPPED = exit 124; OTHER-FAILURE = any other failure or error; HARNESS-ERROR = observer or driver fault, recorded separately and counted neither as a pass nor as reproduction. Counts discovered (loader count, or `Ran N tests` where plain), executed (`Ran N`) and skipped (verbose `skipped` lines) are reported with their derivation; a difference from 421 and 263 is reported, not forced.
* P6 Implement record: one changes file with commands, timestamps, exits, counts, skips, outcome, counters and limits; new additive qualification of prior records (prohibited amendment disclosure, first post-wait traces qualified, no overclaim, process not fully conforming). Cleanup only the exact owned scratch path after raw evidence is copied; confirm the worktree clean.
* P7 Review: one authored Review (not independent), then final state; commit the records once (no amend); write the external handoff, which may cite the actual record commit.

## Stop conditions

* UNADMITTED (busy), missing original witness (not the case), environment install failure that cannot be completed with owned dependencies, a pair cap exceeded, reproduction with preserved trace, two pairs used. No retries, no third pair, no widening to the whole project, a full gate, multi-image, scanner, stress or load campaign.

## Validation

* Read-only git checks: `git diff --stat ef28d4da4 HEAD -- src infra tools .github pyproject.toml` empty before and after; `git status --short --ignored` clean after cleanup; sha256 baseline comparison for the 14 records, the original handoffs and `sha256sum -c SHA256SUMS` 29 of 29 for the prior raw packet.
* Link and ASCII review of the new records. No hosted CI was read; independent actual-head review remains later.

## Risks

* The editable-install package versions may differ from the original venv; recorded, not claimed equal (RL-1).
* Observer overhead on a 421-test selection is small outside the target test (tracing is installed only on connections opened while the target test is current) but timing still differs; reported as OBSERVER only.
* Zero of two does not show absence: frequency is unknown (RL-2).
