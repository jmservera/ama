# Details: issue 2244 live re-verification

## Phase 1: probes

* `az containerapp revision list`, `replica list` (restartCount, state), `show` (latest ready, scale rules, probes).
* `curl /healthz` x13 over about 2 min.
* `az containerapp logs show --type console` filtered for tracebacks and the lock message.
* `az containerapp exec` with a pty to count `startup_retries` in the installed mssqlstore.py.

## Phase 2: record

* docs/reference/research/issue-2244-live-r54-2026-11-22.md plus live-probe.txt; README index entry; log entry.

## Phase 3: close-out

* Changes record with per-criterion table, review, one commit with Refs #2244. Issue stays open.
