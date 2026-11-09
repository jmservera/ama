# Details: issue 954 photo flag browser validation (2026-11-09)

## Phase 1: recovery

* Verify the planning commit's parent is `ef28d4da4`, its source tree equals the base source tree (`git diff --stat ef28d4da4 HEAD -- . ':!.copilot-tracking'` empty), clean status, then `git show chore/photo-service-evidence-audit-954:src/api/checks/photo_flag_stale_browser_check.py` into the path. Record the old blob and diff to the adapted file in the changes record. Do not merge the old branch (it predates main by thousands of files).

## Phase 2: checker adaptation

Keep the owned loopback server (trusted-proxy provider, synthetic store, no token) and the Playwright routes: only `/api/me` (real payload, `services.photo` overridden stale-true, then false, then true) and `/api/account/photo` (503 in one page, 403 in another, real JSON error body, never 200).

Per status, assert:

* startup `/api/me` said photo true; exactly one photo request, answered with the intended status;
* `me.services.photo` false afterwards; initials visible; photo image hidden;
* inline unavailable status text in `#photo-status` (role status), `#account-error` empty;
* no disruptive UI: no `[role=alert]`, `[role=alertdialog]`, `dialog[open]`, `.toast` or similar element appears, no JS dialog event;
* no application error: zero `pageerror`, zero `pageerror` and zero console `error`/`warning` events other than the native failed-resource diagnostic for the photo URL with the expected status. Every console event of every type is recorded unfiltered; benign non-error events are recorded but do not fail the owner-definition verdict;
* a false refresh sends no photo request: first assert the refresh `/api/me` response was processed (sequence of overridden flags true, false, true is recorded and the refresh response awaited) and that the flag was true before the false answer was served, so the check cannot pass vacuously; a true refresh retries exactly once; no further request;
* no full reload: a `window` marker set after load survives and no main-frame navigation occurs after the first load.

Record separately and unfiltered: all console events, native diagnostic count, application console count, page errors, `literal_no_console_event` (informational, expected false), and `owner_definition_quiet` (the asserted verdict). Receipt JSON goes under `ZF_OBSERVATION_DIR` when set and is written from a `finally` block per status (partial events, counts and the failure text), so an early failure stays diagnosable.

Current-main adaptations: assert at start that `zava_forward.api`, `zava_forward.core`, `test_mvp` and `test_auth` resolve to files inside this worktree (fail otherwise), keep `test_mvp`/`test_auth` fixtures from `src/api/tests` via `PYTHONPATH`.

## Phase 3: execution

Scratch owned dir (mktemp, recorded in `/tmp/zf954.scratch`). Commands, in order, each with raw exit:

* `ruff check` and `ruff format --check` on the checker (format applied before the run so that the executed file is the committed file);
* (`PYTHONPATH` below applies to every command, not only the browser run) `PYTHONPATH=<wt>/src/api/src:<wt>/src/core/src:<wt>/src/agents/src:<wt>/src/api/tests:<wt>/src/core/tests:<wt>/src/agents/tests flock -n /tmp/ama-rpi-heavy.lock python3 src/api/checks/photo_flag_stale_browser_check.py` (busy lock means independent work, no queueing);
* `python3 -m unittest discover -s tests -p test_photo_availability.py -v` in `src/api`;
* `python3 -m unittest discover -s tests -p test_scenario_manifest.py -v` and `-p test_needs_inventory.py -v` in `src/core`;
* source-equivalence: `git diff ef28d4da4 -- src/api/src` empty for product source.

## Phase 4: review

Fetch the guidelines again immediately before review, read the changed file, report `file:line` findings. Not run: axe, human assistive technology, live Entra, deployed environment, workflow wiring.

## Phase 5: records

Changes, review and state under `.copilot-tracking/`; handoff in the coordinator files directory as `handoff-954-demo-validation.md`. Commit with Conventional Commits and the Copilot trailer; author and committer are the repository-local noreply identity.
