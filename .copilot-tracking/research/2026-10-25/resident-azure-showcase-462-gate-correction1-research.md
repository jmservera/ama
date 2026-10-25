# Issue 462 gate-failure correction cycle 1: research (2026-10-25T23:08Z)

Written before any edit. Frozen candidate `/tmp/ama-462-candidate-581ebda0`, failed receipt
`/tmp/ama-462-local-final-gate1/receipt.json` and all venvs, logs and worktrees are retained unchanged.
Gate PID 1377819 is confirmed exited (`kill -0` reports no such process; no `rpi-checks` process; heavy
lock has no holder). Capacity at 23:07Z: 11 GiB available memory, 17 GB disk free (94 percent used).

## Findings (evidence read in this checkout, HEAD `289c0255`)

1. Gate failure. `src/core/tests/test_resident_showcase_sql.py:18` runs `import mssql_python`
   unconditionally. The runner's core venv installs core without the optional SQL driver, so unittest
   discovery raises ImportError. No other core test imports the driver at module level (grep); other opt-in
   SQL test classes guard only with `skipUnless(<env flag>, "<reason>")` and import the driver lazily.
   The new class uses the skip reason "needs ZF_TEST_MSSQL=1 and a loopback ZF_SQL_SERVER container",
   which is NOT in the runner's `EXPECTED_SKIP_REASONS` (tools/rpi-checks.py:60). Once collection works,
   the generic gate would reject that skip as unexpected. The existing allowlisted reason "opt-in loopback
   SQL Server" fits exactly, so the fix reuses it; the runner is not changed and the allowlist is not
   widened.
2. Opt-in must stay real. If the driver import is needed only when SQL tests are opted in, import it only
   under the opt-in condition so that an opted-in run with a missing driver fails loudly instead of
   skipping. Targeted validation will run with the opt-in set against a task-owned SQL container and must
   show the `SqlBoundaryTests` ran, not skipped.
3. Logout. `web/demo.js:~194` ignores `res.ok`, so 403 (CSRF/origin) or 503 clears the UI and calls
   `start()`; the catch path says "Close this page to end the session", which is false because the
   `__Host-zfdemo` cookie has Max-Age 1800 and survives a closed page.
4. Runner gaps (read, not changed): `SQL_SELECTORS` (tools/rpi-checks.py:28) lists no resident showcase
   module; `checks.resident_demo_browser_check` is not invoked (only design_system and regulatory
   checks); the container step builds `<project>/Dockerfile` for IMAGES only, so
   `src/api/Dockerfile.resident-demo` is never built, run non-root or started by the generic gate.
5. SQL image `mcr.microsoft.com/mssql/server:2022-latest` is present locally, so no pull is needed.

## Constraints and boundaries

No runner edit, no allowlist widening, no skip of failing checks, no change to the #444 loopback guard or
SQL deny rules, no cloud, no push, no full gate (needs coordinator admission). Only a task-labelled
disposable SQL container, torn down by exact ID afterwards. The employee SQL container
`ama-350-feedback-sql` is not touched. Heavy work runs under the shared lock
(`/tmp/ama-rpi-heavy.lock`) with `--lock-timeout 0` semantics: if busy, stop.

## Planning readiness

Ready for items 0, 1 and 2. Item 3 needs a new check script because no existing helper builds or
starts this image.
