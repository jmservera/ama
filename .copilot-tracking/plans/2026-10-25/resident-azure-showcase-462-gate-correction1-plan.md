# Issue 462 gate-failure correction cycle 1: plan and details (2026-10-25T23:12Z)

Prospective. Source of truth for scope: the owner's brief items 0 to 3. Research:
`.copilot-tracking/research/2026-10-25/resident-azure-showcase-462-gate-correction1-research.md`.

## Phase 1: test collection (item 0)

* `test_resident_showcase_sql.py`: move `ON` above the driver import; `import mssql_python` only when
  `ON` (an opted-in run without the driver raises ImportError, a loud failure); change the class skip
  reason to the allowlisted "opt-in loopback SQL Server". No change to any assertion.
* Validate: core venv without the driver (a throwaway venv outside the checkout) collects with the
  class skipped for the allowlisted reason and `RenderTests` still run; with opt-in and a task-owned SQL
  container the class runs (0 skipped) with the full principal-deny assertions.

## Phase 2: logout (item 1), tests first

* Add `check_logout_failure` to `src/api/checks/resident_demo_browser_check.py`: after keyboard
  sign-in, intercept `**/demo/logout` with Playwright `route` for (a) 403 JSON, (b) 503 JSON,
  (c) abort. For each: sensitive content hidden, sign-out row hidden, the error panel visible with text
  saying sign-out was not confirmed and the session may still be active, no text containing "Close this
  page", cookie `__Host-zfdemo` still present, focus on the error heading, "Try again" works: after
  unroute, retry shows the content (session still valid), and Sign out now succeeds and shows the
  sign-in form. Run it against the OLD `demo.js` first to prove failure, then fix.
* `demo.js`: sign-out handler reports success only when `res.ok`; otherwise and on network error call a
  new `signoutFailed()` that hides content, sets the honest message ("We could not confirm that you were
  signed out. Your session may still be active on this device and ends by itself within 30 minutes.
  Select Try again to check, then sign out again."), focuses the heading. No secret or response body in
  the DOM or console. Keep `retry` wiring, semantic buttons and focus order. Web guidelines are fetched
  and applied to this change (`web-design-guidelines` skill).

## Phase 3: SQL deny and browser under the heavy lock (item 2)

* One task-labelled disposable SQL container (published on 127.0.0.1, limits as the runner uses), fake
  `sa` password from `/dev/urandom` held only in the process environment of the commands, torn down by
  exact container ID.
* Run, from this worktree with the `ama462` venv: core `test_resident_showcase_sql` opted in (principal
  deny tests), then `python -m checks.resident_demo_browser_check`. Save command text and results (without
  the password) as dated logs under the tracking changes record with the exact source SHA.

## Phase 4: image controls (item 3)

* New `src/api/checks/resident_demo_image_check.py`: builds `Dockerfile.resident-demo` with context
  `src/` to a task-labelled tag; asserts the uid is 10001 and not root; runs with `--read-only`,
  `--cap-drop=ALL`, `--security-opt=no-new-privileges` and verifies a refusal (no configuration: exit
  non-zero, no secret in output, not listening); then starts it against the task-owned SQL fixture
  database (host network, loopback only, fake verifier/session key) and asserts `/healthz` with the
  allowlisted Host, `/demo/session` JSON, and a wrong-Host 4xx. Removes the container and image tag it
  created. It reuses `database()` and settings helpers from the browser check.

## Phase 5: validation, critique disposition, review, commit

Lint/format/type on changed files only; focused unit tests (core showcase, api demo, dependency rule).
One independent review after implementation. Local commit with the privacy-safe identity. The frozen
receipt is stale for any new head: stated, not hidden. A fresh full gate happens only on coordinator
admission, after this correction review. Coverage gaps remain until the runner is changed under its own
reviewed task: item 4 and 5 gaps above are reported, not claimed covered.

## Stop conditions

Lock busy or SQL container fails to start: stop, retain logs, report. No cloud, push or runner edit.

## Critique and dispositions (2026-10-25T23:20Z, one independent rubber-duck critique, verdict request_changes)

Findings are retained as returned in substance; no second critique.

* High, host network could expose beyond loopback: accepted. The image check sets `ZF_DEMO_BIND=127.0.0.1` explicitly for the host-network run and asserts the listening address is loopback.
* Medium, new controls not gate-enforced: accepted and already disclosed. Reported as a follow-up gate task needing coordinator admission; the runner is not changed here.
* Medium, setUpClass leak on partial setup failure: accepted. The correction adds an exception-safe drop in `setUpClass`, only for this test module.
* Medium, SQL fixture ownership of the image check: accepted. The image check takes the task-owned container settings from the environment (same container as Phase 3, which is torn down by exact ID at the end) and does not provision SQL.
