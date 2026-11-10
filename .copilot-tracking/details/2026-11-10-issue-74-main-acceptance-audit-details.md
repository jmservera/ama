# Issue 74 current-main acceptance audit: details

Plan: [plan](../plans/2026-11-10-issue-74-main-acceptance-audit-plan.md).

## Commands (relative to the worktree root; `V=/tmp/ama-74-venv-1110`)

1. Environment: `python3 -m venv $V`; `$V/bin/pip install -e` is not used. Install the declared distributions non-editable: `$V/bin/pip install ./src/core ./src/agents ./src/api "playwright==1.64.0"`. Verify with `$V/bin/python -c "import zava_forward.api, playwright"` and confirm module paths resolve to site-packages, not the source tree.
2. Core: from `src/core`, `$V/bin/python -m unittest discover -s tests -p test_home_case.py -v`.
3. API: from `src/api`, `PYTHONPATH=../core/tests:../agents/tests $V/bin/python -m unittest discover -s tests -p test_home_case_api.py -v` (the `tests` folders are not packages, so the discover form is required).
4. Browser: from `src/api`, `ZF_BROWSER_SCRATCH=/tmp/zf74-b flock -n /tmp/ama-rpi-heavy.lock $V/bin/python -m checks.home_case_browser_check`; `PYTHONPATH` for the client carries the worktree `src/core/src`, `src/agents/src`, `src/api/src` only if the installed distributions do not resolve; the server child always uses the worktree source through the runner.
5. Capture stdout, stderr and the exit status of each command in `phase74-main-acceptance-audit-evidence-1110/`, with sha256 sums, and record skipped tests and the `PARTIAL: axe scan SKIPPED` line verbatim.

## Field and role matrix definition

Fields: shared systems, dependencies, holds, works, costs (building); evidence documents, decision, cost allocation, outcome (home; outcome means `stage`/`closed` and quality states). Roles: Retrofit Programme Manager (finance view), Resident Liaison Officer (staff without finance view), Contractor and anonymous (refused).

Status vocabulary: `local-observed` (asserted by a maintained check that ran on this pinned main against a constructed fixture), `implemented-unverified` (present in pinned source but no maintained check asserts it), `blocked` (check could not run), `unknown`.

## Stop rules

* A failing check stops that check; failure output is preserved and no assertion is weakened.
* A busy heavy lock is recorded as a validation hold; no wait, queue, spin or kill.
* If a dependency is genuinely missing beyond the planned install, record it; no shared or global install.
* Chromium: use the already cached revision. If Playwright 1.64.0 does not accept it, record the browser check as blocked; do not run `playwright install` into the shared cache, and do not change `PLAYWRIGHT_BROWSERS_PATH` to download elsewhere without recording it as a deviation.

## Output files

* `.copilot-tracking/changes/2026-11-10-issue-74-main-acceptance-audit-changes.md`: changes record (prospective, then actual).
* `.copilot-tracking/changes/2026-11-10-issue-74-main-acceptance-matrix.md`: concise source-bound acceptance matrix.
* `.copilot-tracking/reviews/2026-11-10-issue-74-main-acceptance-audit-review.md`: the single post-implementation review.
* ROOT handoff `handoff-74-main-acceptance-audit-1110.md`, outside the repository.
