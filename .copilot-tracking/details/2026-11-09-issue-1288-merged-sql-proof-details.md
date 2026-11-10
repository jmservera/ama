# Details: issue 1288 merged-main SQL contract verification

Plan: `.copilot-tracking/plans/2026-11-09-issue-1288-merged-sql-proof-plan.md`. Detail read-back `date -u` 2026-11-09T23:21:35Z. Verification only.

## Step 1: pins and environment (light, no heavy admission)

* Record `git rev-parse HEAD`, tree, branch, `git status --short`, `origin/main` before any write; confirm the base-versus-1b7 diff is rubric-only.
* Owned venv in `mktemp -d /tmp/ama-1288-sqlproof-XXXXXX`, hash-pinned requirements, editable core, agents and api; check that module files resolve inside this worktree. Pip is used because the worktree has no environment; no global change.

## Step 2: store boundaries read first (no invented schema)

* `Assistants.transaction()` opens a new store connection per call (`store.assistant_connection()`), uses SERIALIZABLE on SQL Server, `BEGIN IMMEDIATE`, `COMMIT` on a normal exit, `ROLLBACK` on any exception except `ReleaseDenied` (committed). It closes the connection in `finally`.
* `fence_send` (assistants.py around lines 1470-1491): inside one transaction it checks `disabled(capacity=False)`, reads the attempt row and, when refused, inserts a `send-refused` event; the `DispatchWithdrawn` raise happens after the `with` block, so the event commits. This is the behaviour to observe; no assumption about rollback or commit is made beyond reading it.
* `begin_call` takes the physical slot first, applies disabled/expiry/schema/release checks and the atomic reserve and debit in one transaction, and releases the slot on refusal or store failure. `CallTicket.end` settles once and releases the slot once.
* Tables: `assistant_events(id, task_id, at, body)`, `assistant_attempts(id, ..., outcome, active_until, reserved, actual, pool)`, `assistant_allowance(id, calls, tokens, expires, used_calls, reserved_tokens)`. The fixture drops and recreates the working tables in the disposable database `zf_test_assistants`.

## Step 3: heavy admission wrapper (external script, session files)

Modelled on the retained `sql-1288-e5.sh` and `sql-1288-e6-run` (read, not modified): `flock -n /tmp/ama-rpi-heavy.lock`; meta (UTC date, pid, head, status); container with random name/port/password; readiness loop of bounded 40 x 3 s; `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_PORT`, `ZF_SQL_AUTH=password`, `ZF_SQL_USER=sa`, password in the environment only, `ZF_SQL_TRUST_CERT=1`, `HOME` and `ZF_DATA` inside the scratch dir (no private dataset), `PYTHONDONTWRITEBYTECODE=1`; run unittest `-v` for the selected tests and the harness; record exits; remove the container in a trap; record the image id, server version, cleanup output. The password never appears in any record.

## Step 4: evidence and review

* Read back `date -u` before every evidence write. Summaries with identities, exit codes and counts go to the changes record; raw logs stay external.
* Direct review of the final diff (records only) against the plan; classify each contract as proven at exact source, proven historically, unproven or failed.
* Freeze: records only, committed with the GitHub-resolved noreply identity and the Copilot trailer; no push, PR, issue or board write.
