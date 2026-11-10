<!-- markdownlint-disable-file -->
# Changes: issue 1288 H1 restart-context diagnostic (blocked, not executed)

Readback `date -u` 2026-11-09T23:38Z. Refs #1288 only. Verification, not a correction cycle: E11 succeeded; E12 and E13 unused and not consumed. No source, test, schema, workflow or shared-doc change.

## What was done

* Research, plan, details and the one independent critique (Revise, 3 blocking, all applied) were recorded before any observation, committed as `bf94ac0ba`.
* The external harness `harness_h1_restart_context.py` (sha256 `fbec7186270b...`) and wrapper `sql-run-h1.sh` (sha256 `2e9f7f832b22...`) were written; the harness imports and the test id resolves against an owned fresh venv (`/tmp/ama-1288-h1-*`, hash-locked requirements, editable core/agents/api from this worktree). Import check is not SQL evidence.

## Admission result

One non-queued `flock -n /tmp/ama-rpi-heavy.lock` attempt at 2026-11-09T23:37:50Z returned exit 1. Holder: issue-1238 manual verified SQL run (pids 3391368 bash, 3391370 `flock -n`, 3391371 `run-mssql.sh`, scratch `/tmp/issue1238-manual-verified-1109.134hqa`), about 58 s old. No queue, spin, retry, kill, container reuse or waiver. No SQL container was started. Record: `logs-h1-restart-context-1109/sql-run/admission-attempt.txt`.

## Status

H1 is NOT observed. H0 stays failed-inconclusive (33 selected, 31 ok, 1 skip, 1 FAIL, exit 1), unchanged and not retroactively passed. The source-based hypothesis in the research record (second service had a default `Ai` and no release context, so `release_denial` or release reference mismatch makes `actionable` false and the flag `not-current`) is unconfirmed.

## Exact unexecuted step

When the heavy lock is free, make one non-queued admission of `flock -n /tmp/ama-rpi-heavy.lock sql-run-h1.sh <fresh OUTDIR>` using a fresh owned venv written to `/tmp/ama-1288-h1.path`. Then record `h1.json` against the plan's pass definitions.
