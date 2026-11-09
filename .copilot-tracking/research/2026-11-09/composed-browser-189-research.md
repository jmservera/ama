<!-- markdownlint-disable-file -->
# Issue 189 composed browser check research (2026-11-09)

Task `composed-browser-189`; parent `current-main-integration-189`. Refs #189 only. Research disposition: executed (prospective, read-only inspection, no source change). Validation-only continuation: it satisfies the already planned browser check that the integration record left NOT RUN.

## Pinned facts

* Worktree `/home/azureuser/source/ama-demo-wt/issue-189`, branch `feat/demo-simulator-control-189-1109`, clean at `825abaa4c2454dd484211ee197b84ab1bccb9a65`, tree `6b26925be77a321f051ae8236e0837996deb277d`. Repository-local noreply identity set.
* Source-equal to the tested merge `0dea95876`: `git diff 0dea95876 HEAD -- src tools infra` is empty. `src/api` equals C4 head `b933c2f60` (integration record).
* Fetched `origin/main` is now `700bf11e188a9fce05177385019b3d10ba5bb92f` (`chore(rubric): record score 78/100`). `3a9767d5c` (the base merged in `0dea95876`) is its ancestor. `git diff 3a9767d5c origin/main` is one file, `.github/rubric/scores/latest.json` (4+/4-); under `src`, `tools` and `infra` the diff is empty. Movement is rubric data only: no API, Core or tools source moved. Historical base remains `3a9767d5c`; current main `700bf11e1` is only qualified, not merged (no unnecessary merge or rebase). Prospective merged source equality: a merge of `700bf11e1` would change no source tree, so the tested `src`, `tools` and `infra` equal the current-main merged result.
* Heavy lock `/tmp/ama-rpi-heavy.lock` was held by the 1292 diagnostic driver (pid 3083388) during the integration run, so the browser check was not run. A read-only `flock -n` probe at research time shows the lock free (released at the stated 17:01). Another tmux session (1292 review) is a model review, not a lock holder; the real admission is decided at implementation by `flock -n`.
* Chrome and Playwright browsers exist (`/usr/bin/google-chrome`, `~/.cache/ms-playwright` chromium 1248). Pinned axe asset `/tmp/axe-4.10.3.min.js` exists with sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`, equal to `AXE_SHA256` in the check.
* The C3 command (capture-189-type-applicability `browser1.cmd`): `python -m checks.simulator_control_browser_check --axe /tmp/axe-4.10.3.min.js` from `src/api`, 13 axe scans, 0 violations, five passes; delayed-Stop probe `probe_delayed_stop.py old|new` (old exit 1, new exit 0). The probe file is an owned evidence file in the coordinator capture directory, not in the repository.
* The check imports `test_auth` and `test_mvp` (tests directories on `PYTHONPATH`), `playwright` and the API with `azure.iot.device` lazy (C4). Previous owned venvs were removed, so a fresh owned venv is required.

## Constraints carried

No source, config, schema or test edits; no amend, rebase, force, push, PR, issue, board, cloud, model, private data or other users' resources; no filesystem-wide scan, global install, new credentials or live-app activation. C1 to C4 are spent and one of five remains; no source change means no correction cycle. Not run in this lane: full gate, SQL services; Source 19 and the 110 Core SQL/Azure opt-in skips remain disclosed, unverified. Owner demo tier: targeted, nonqueued, fail closed if busy. Independent Functional review of the head only after this check passes.

## Planning Readiness

Ready. Unknowns are the holder state at admission and the browser outcome, recorded prospectively in the plan.
