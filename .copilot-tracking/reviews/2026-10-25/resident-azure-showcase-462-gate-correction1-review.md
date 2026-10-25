# Issue 462 gate-failure correction cycle 1: original independent review (2026-10-25T23:30Z)

One independent code-review agent run after implementation; output preserved as returned. The reviewer
ran nothing, so the run counts in the changes artifact are from the commands recorded there.

No significant issues found in the reviewed changes. Outcome: **Conformant**.

* Optional driver import: `mssql_python` is imported only when `ON` is true; its only uses are inside
  the opted-in `SqlBoundaryTests`. An opted-in run without the driver raises ImportError, so it still
  fails loudly. `setUpClass` now drops the throwaway database if its setup fails (unittest does not call
  `tearDownClass` after a `setUpClass` failure).
* `demo.js` sign-out: only `r.ok` is success; 403, 503 and network failures call `fail(...)`, which hides
  content and sign-in, shows the message and focuses the heading. "30 minutes" matches
  `SESSION_SECONDS = 1800`. No body or token is shown. The server returns 403 on CSRF or origin failure
  and 200 after revoking, so the 2xx gate is correct.
* `check_logout_failure` is meaningful: 403, 503 and abort; asserts hidden content, message wording, no
  "close this page" text, cookie still present, focus on the message, and recovery after Try again.
* Image check: `--network=host` with `ZF_DEMO_BIND=127.0.0.1` listens on loopback only; settings are
  passed by key name only; refusal output is checked for the fake password and the SQL password; cleanup
  is limited to the generated container names and the unique image tag.
* Changes artifact: no false claim found; it says the generic runner still does not cover the new
  checks and that no pass is claimed.
