<!-- markdownlint-disable-file -->
# Issue 189 C2 browser check changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/browser-check-189-c2-plan.md). Refs #189 only. Raw outputs, exit files and hash manifest are outside the repository in `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/capture-189-c2-browser/` (manifest 131 entries, `sha256sum -c` all OK; manifest sha256 `b72e5918a5fd056263d27489c6567b829b7de42dd114bf983599f9dbe31e5386`). The recapture directory `capture-189-validation-recapture` is retained unchanged and still verifies.

## Identities

* Frozen base `bd7a3fb8e28a1c61dae0aac5f0bcfa320b9d4c8c`, tree `eb95eaf45148b4abe68292d3aa163647031261df`; committed research/plan/critique `277705c4d` before any source edit.
* Source fix commit `e256766aa7063b4350768b63b81031a2b8e71903`, tree `e0c1530704b3342c4fb7c0e030b4a390cf8ac9fa`. Fetched `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477`; `src`, `infra`, `tools` unchanged on main since `8d6f029ca`.

## Change

One file, `src/api/checks/simulator_control_browser_check.py` (+9, -1): new `wait_for_stop_saved` waits for `#simulator-control-notice` containing `Stop saved and read back` (the completed stop response), then the check asserts the first State fact starts `Stopped.`, keeps the file assertion and the axe scan. No product, UI, sleep, retry, removed assertion or weakened state. Diff sha256 of the working change `224641dc0f581a5048cc5ee028c75dbdc8b0754a9068bc0822176662d98ccc23`.

## Evidence

* Cause: probe shows the non-exact `Stopped` match is the always-visible Stop help text before any stop (1 match, exact 0 matches), resolving while the control is still enabled.
* Deterministic regression (server-side 1.5 s delay of `live_control.write`): old wait exit 1 (control still enabled when the wait returned); new wait exit 0. An earlier first probe delayed with a blocking Playwright route handler, which stalls the Playwright dispatcher and did not reproduce (old wait exit 0); it is retained in `superseded-route-delay/`, not used as evidence.
* Unmodified baseline, 6 fresh runs: exits 0,0,0,0,1,0; run 5 failed at line 156 as before. Cumulative failure of the old check: 3 of 10 observed runs.
* After the fix, 10 fresh runs: 10 of 10 exit 0, each 13 state lines (13 axe scans, all `violations: []`: unavailable, rejected start, permitted, stopped after stop, permitted stop, expired enabled, invalid window, already stopped, already stopped after repeat, stale, write error, manual route not writable, view-only administrator) and the completion marker; no BrokenPipe line in any of them. Ten passes are evidence, not proof.
* Unit modules (`src/api`, verbose, exit 0, 0 skips): `test_simulator_admin` 27, `test_live_control` 34, `test_entra_authoritative` 36, `test_auth` 41, `test_content_standard` 18, `test_design_system` 8.
* `ruff check` and `ruff format --check` on the check file: exit 0. `node --check` of `app.js` and `simulator-control.js`: exit 0.
* Adverse, not waived: project `mypy` from `src/api` exit 1, 8 errors, all `no-untyped-call` on unchanged lines (`TrustedProxyProvider`, `App` at checks lines 123 and 125, six in `tests/test_simulator_admin.py`); not caused by this diff and not corrected here (scope). A bare single-file `mypy` run (exit 1, `import-untyped`) was a wrong invocation and is retained in `superseded-route-delay/`.
* Not run: core suites, case journey, workspace scripts (unchanged from the recapture capture), SQL, Azure, models, full matrix, rpi-checks. Manifest and needs-inventory: not applicable, no recipe, workflow or inventory file changed. Web guidelines: current source fetched before edits; the change touches no web markup, `simulator-control.js` was read only for text and live-region semantics (`role=status`, `role=alert`).

## Cycle ledger

C1 one of five spent (coordinator brief); C2 spent now (this productive source edit); three remain. No reset or extra grant.
