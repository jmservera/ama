# Profile-main checkpoint details (issue 440, 2026-11-10)

Plan: [plan](../plans/2026-11-10-profile-main-440-1110-plan.md).

## Observation commands (run from the worktree; raw outputs go to the Root session directory, outside the repository)

Evidence directory: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/profile-main-440-observation-1110/`.

1. Source identity: `git rev-parse HEAD HEAD^{tree}`, the four blob ids, `git status --short`, and the local `refs/remotes/origin/main` value with its observation time (a fetch is a read of the remote and is recorded; remote currency is claimed only as of that fetch).
2. Attempt A (no private environment yet, system `python3`): from `src/api`, `python3 -m unittest tests.test_specialist_keyboard_check`; from `src/core`, `python3 -m unittest tests.test_perspective_walkthroughs tests.test_journey_acceptance tests.test_scenario_manifest`. Record each selector's exit and `zava_forward` and `checks` module file paths (`python3 -c`, read-only). A result whose imported module path is not inside this worktree is classified as not current-main proof (blocked), whatever its exit.
3. Restore only for a selector that failed with an actual missing-dependency or wrong-path failure: `python3 -m venv /tmp/ama-440-profile-venv-1110`, then `/tmp/ama-440-profile-venv-1110/bin/python -m pip install -e src/core -e src/agents -e src/api` and `playwright==1.64.0` (the version pinned by `src/api/pyproject.toml`); record package versions. Prove by the venv interpreter that `zava_forward.core.__file__` resolves into this worktree.
4. Attempt B: only after step 3, and only the affected selector(s), using the venv interpreter. A selector that already passed with a proven in-worktree module path in Attempt A is not rerun. Every earlier outcome is retained. Expected totals: API 6 tests, Core 16 tests.
5. Browser admission (all required, else a blocked row and stop this check): `fuser -v /tmp/ama-rpi-heavy.lock` shows no holder; `MemAvailable` in `/proc/meminfo` read immediately before is at least 1.5 GiB (headless Chromium plus the owned local server, an engineering threshold chosen here, not a repository rule); the cached Chromium revision loads under the pinned Playwright without any browser download.
6. Only if admitted, one run: `flock -n /tmp/ama-rpi-heavy.lock` with `ZF_BROWSER_SCRATCH=/tmp/z440p`, from `src/api`, the venv interpreter, `python -m checks.specialist_keyboard_browser_check`, bounded by `timeout 900`. Record exit, PASS count, negatives, declared no-table walks. Afterwards confirm by PID that no process this run started remains; kill only such a PID.
7. Documentation checks: `git diff --check`, ASCII check of added lines, relative link resolution, `git diff --name-only` confined to the pack and own RPI files.

## Pack section structure (new, appended; no earlier section edited)

`## Specialist keyboard probe current-main checkpoint (2026-11-10, Refs #440 #134 #73 #108 #184)`: dated qualification paragraph; Identities, scope and exclusions; Source identity proof; Observed this checkpoint (commands, exits, environment); Historical retained observations; Requirement trace (document-qualified); Evidence classes; Gaps; Findings, owners and gates; Recommendation; Process record and limits.

## State and witness notes

* State file `.copilot-tracking/rpi-sessions/2026-11-10/profile-main-440-1110-state.json`; witness chain in Root `phase440-profile-main-evidence-1110/`.
* The review file is created only after `implement-done` and finalized before `review-done`; the pack must be at its committed content at `review-done`.
