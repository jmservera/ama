# Details: issue 954 composed-source browser validation (2026-11-09)

Plan `.copilot-tracking/plans/2026-11-09-issue-954-composed-browser-plan.md`.

## Step 1: pre-run record

In `~/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/evidence-954-composed-browser/`: `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git status --short` (must be empty), `git rev-parse HEAD:src/api/checks/photo_flag_stale_browser_check.py`, `sha256sum` of the checker, `python3 -V`, `pip list` playwright version, chromium asset directory listing.

## Step 2: admission

`fuser -v /tmp/ama-rpi-heavy.lock` (holder check), then once, from the worktree root:

`ZF_OBSERVATION_DIR=<evidence>/obs PYTHONPATH=<worktree-first api/src, core/src, agents/src, api/tests, core/tests, agents/tests> flock -n -E 99 /tmp/ama-rpi-heavy.lock python3 src/api/checks/photo_flag_stale_browser_check.py`

Create `<evidence>/obs` first (the checker does not create it). Exit 99 from flock means a lock conflict: record unadmitted and stop. Any other nonzero exit is a failed execution. Capture stdout, stderr, exit and start and end times.

## Step 3: classification

Pass requires checker exit 0 and, in stdout, exactly 83 `PASS` lines and exactly one `FAIL` line, which is the expected negative-control FAIL immediately followed by `PASS negative control`. The 83 are the C2 count on the same logic; the detector group prints 14 (13 fixtures plus `empty alert receipted`), verified by reading the source. Labels are compared with the C2 output (`evidence-954-c2/browser.out`); the typing change must not alter them. Also required for each of 503 and 403: the behavioural and quiet assertions, the actual client-flag true then false transition, the identity sentinel, no additional photo request, and a receipt JSON under `obs` with `quiet_per_owner_definition` true, no page error and no dialog. Any other count, unexpected FAIL, traceback or receipt deviation is a failed outcome, never waived.

## Step 4: after-run record

Checker `sha256sum` and blob after (must equal before), `git status --short` (the run must leave the worktree clean; observation output goes outside the repository), `MANIFEST.sha256` over every raw file. Then changes, review, state and handoff under the tracking and session paths.
