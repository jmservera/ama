<!-- markdownlint-disable-file -->

# Phase Details: issue-152-empty-queue-coverage-correction-3

Plan: .copilot-tracking/plans/2026-11-10/issue-152-empty-queue-coverage-correction-3-plan.md
Research: .copilot-tracking/research/2026-11-10/issue-152-empty-queue-coverage-correction-3-research.md

<!-- P01 -->
## P01: Integrate, bind and validate

* P01-T01 Commands from the worktree root: `date -u`, `git fetch origin main`, `git rev-parse origin/main`, then `git merge --no-ff origin/main -m "<conventional message>"` with the Copilot trailer. Do not use rebase, reset, stash, amend or cherry-pick. On conflict, resolve only inside the four slice paths preserving both intents; any other conflict stops with evidence.
* P01-T02 Verify `queueEmptyExplanation` and the `listView` empty call remain, and that main's changes to `app.js` outside those lines are byte-equal to main (`git diff origin/main -- src/api/src/zava_forward/api/web/app.js` shows only the slice hunks). Confirm no change to `server.py`, navigation, intake, shared persistence, finance or resident_decisions relative to main.
* P01-T03 Read `src/core/src/zava_forward/core/synthetic/scenario_manifest.py` and its tests, determine how the recipe hash is computed, compute the file hash, change only the `recipe` sha256 in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`. Update the knowledge-base index/log only if the repository rule requires for a material KB file change (a hash binding is a minimal edit; record decision in changes).
* P01-T04 Create throwaway venv outside the repo, `pip install -e` of `src/core`, `src/agents`, `src/api[dev]` from this worktree (declared dependencies only after a missing failure). From `src/api`: `python -m unittest tests.test_queue_empty_state tests.test_content_standard tests.test_workbench`, `node --check` for app.js, `mypy` (strict, API project config), `ruff check` and `ruff format --check` on changed Python files; Core scenario-manifest and needs-inventory tests; `python -m checks.workbench_browser_check` (served, loopback, synthetic, `ZF_STORE=json`). Record command, exit, counts, versions. Missing Chromium: follow the README install guidance only.
* P01-T05 Commit scoped local changes with repo-local noreply identity; review once (web guidelines refreshed); record final timestamp from `date -u`.
