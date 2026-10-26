# Issue 462 gate-failure correction cycle 1: changes (2026-10-25T23:25Z)

Prospective research and plan with one independent critique (request_changes, all four findings
accepted) were written before any edit:
`.copilot-tracking/research/2026-10-25/resident-azure-showcase-462-gate-correction1-research.md` and
`.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-gate-correction1-plan.md`.
Base head `289c0255`. Frozen candidate `/tmp/ama-462-candidate-581ebda0`, failed receipt
`/tmp/ama-462-local-final-gate1/receipt.json` (SHA-256 `17dc8ef8...da10a`) and all logs are untouched.

## Source changes

* `src/core/tests/test_resident_showcase_sql.py`: `mssql_python` is imported only when the SQL opt-in is
  on, so default collection no longer needs the driver and an opted-in run without it fails loudly. The
  class skip reason now reuses the existing allowlisted "opt-in loopback SQL Server"; the runner and its
  allowlist are unchanged. `setUpClass` drops the disposable database if setup fails part way.
* `src/api/src/zava_forward/api/resident_demo/web/demo.js`: sign-out reports success only on a 2xx
  response. A 403, 503 or network failure hides the home details and shows: "We could not confirm that you
  were signed out. Your session may still be active on this device and ends by itself within 30 minutes.
  Select Try again to check, then sign out again." Focus moves to the message heading; no false
  page-close claim; no response body or secret shown. Web guidelines were fetched; the change keeps native
  buttons, role=alert and focus handling. No conformance claim is made.
* `src/api/checks/resident_demo_browser_check.py`: new `check_logout_failure` with request interception
  for 403, 503 and abort.
* `src/api/checks/resident_demo_image_check.py` (new): builds the exact `Dockerfile.resident-demo`, checks
  uid 10001, refusal (no config, expired, missing verifier, session key or host list) without secret
  echo, then runs the container read-only, cap-drop ALL, no-new-privileges, loopback bind, against owned
  SQL: health, unlisted Host refused, forged 401, wrong password 401, fake sign-in, and own-home-only view.

## Commands and results (all under the shared heavy lock, `flock -n`, one task-labelled SQL container each)

Runner `/tmp/ama-462-correction1/run.sh` (copy retained in
`/home/azureuser/.ama462-evidence/correction1-2026-10-25/` with logs). Fake fixtures only; the throwaway
`sa` value is random per run and never stored.

* Old `demo.js` (source head `289c0255` plus the new check): opted-in `test_resident_showcase_sql` ran
  18 tests, OK, none skipped (the principal-deny tests executed). Browser check FAILED at the new 403
  case (`#error` never shown; the old code restarted the UI). This is the failing-before proof.
* After the fix: browser check exit 0 (55 PASS lines, 403, 503 and abort cases included); image check exit
  0 (22 PASS lines); opted-in SQL tests OK 18 tests, none skipped.
* Default (no opt-in) `test_resident_showcase_sql` and `test_resident_showcase`: 54 tests OK, 13 skipped
  with the allowlisted reason; with the driver import blocked it still collects (18 tests, skipped=13).
* `ruff check`, `ruff format --check` on changed files and mypy on the two check scripts pass; api
  `-k resident_demo` unit tests 34 OK. The full api unit suite was run once and printed only timing lines
  in its tail; it is not claimed as a pass here.
* Cleanup: only the task-owned containers (removed by exact ID) and the image tag the check built were
  removed; `ama-350-feedback-sql` and all other containers, previews, receipts were untouched.
  An earlier accidental `ruff format` of other check files was reverted with `git checkout` before commit.

## Receipt status and remaining coverage gaps

The `581ebda0` receipt is failed and is stale for any later head; no pass is claimed. A fresh full gate
needs coordinator capacity admission after this correction review. The generic runner still does NOT
select `test_resident_showcase_sql` for SQL tests, does not call `resident_demo_browser_check` or the new
image check, and does not build `Dockerfile.resident-demo`; those results here are targeted runs, not
gate coverage. Cloud G1 budget, G2 live provenance, G3 SQL and G4 write path remain open; no push.
