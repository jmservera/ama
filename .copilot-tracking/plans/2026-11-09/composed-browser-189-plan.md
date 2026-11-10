<!-- markdownlint-disable-file -->
# Issue 189 composed browser check plan (2026-11-09)

Research: [research](../../research/2026-11-09/composed-browser-189-research.md). Details: [details](../../details/2026-11-09/composed-browser-189-details.md). Critique: [critique](composed-browser-189-critique.md). Parent: `current-main-integration-189` (C1 to C4 spent, one of five remains; this validation-only task consumes and resets none). Refs #189 only.

## Objective

Run the existing synthetic `simulator_control_browser_check` once, with its established variants, delayed-Stop assertions and axe, on the merged head `825abaa4c` (source-equal to the tested merge), inside one nonqueued holder of the shared heavy lock. This closes the single browser gap recorded in the integration review. No source change.

## Phases

* [ ] P1 Commit this research, plan, details and critique (one) before any validation (frozen).
* [ ] P2 Preconditions: clean tree, HEAD is the frozen records commit and source-equal to `825abaa4c` for `src tools infra`, local noreply identity, fresh fetch and main qualification (`3a9767d5c` to current main, rubric data only), pinned axe sha256 verified.
* [ ] P3 Actual holder check and one nonqueued admission (`flock -n`); if busy, stop fail closed, record NOT RUN with the holder, no queue, no retry loop.
* [ ] P4 Inside the one holder: fresh owned `mktemp -d` venv (CI install profile, pip, project-local only), `python -m checks.simulator_control_browser_check --axe /tmp/axe-4.10.3.min.js` from `src/api`, then the delayed-Stop probe old/new as in C3. Raw cmd, exit, stdout, stderr and sha256 manifest outside the repository.
* [ ] P5 Source and tested SHA before and after; changes record, one original Review, state, records-only commit, handoff `handoff-189-composed-browser.md`.

## Success criteria

* Check exit 0 with every required state, 0 axe violations, delayed-Stop old exit 1 and new exit 0 (synchronisation intact), source unchanged before and after, holder released.
* A failure is a recorded blocker, not waived, not retried silently, and no correction is made (a correction would need separate authorization).
* Skips and prerequisites that were absent are reported unverified.

## Out of scope

Source or test edits, merge or rebase of current main, push, PR, issue or board write, `rpi-checks --all`, SQL services, cloud, models, global installs, cleanup of evidence needed for later hash verification.

## Stop rule

Busy lock, missing prerequisite or any failure stops the task with the exact blocker; no cycle is started.
