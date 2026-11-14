<!-- markdownlint-disable-file -->
# Changes: issue 144 C1 rebase onto origin/main

Date: 2026-11-14. Branch `feat/demo-144-scale-probes-load-2315`, PR #1583, Issue #144. Original evidence: `.copilot-tracking/changes/2026-11-13/issue-144-scale-probes-load-restart-changes.md` (unchanged).

## Rebase

* Fetched `origin/main` = `b64ec641f89158b5d324cb7f8c522201278e2277`.
* Rebased the single feature commit (`cc64e90d6`) onto it; no conflicts. Append-only `docs/reference/log.md` and `.copilot-tracking/` additions kept on both sides.
* Rebased commit: `67470fa42`. No content changed by the rebase.

## Validation (focused tier)

Note: `/home/azureuser/source/ama/.venv` does not exist on this host; system `python3` with `~/.local/bin` ruff and mypy was used, with `PYTHONPATH` set to this worktree's `src/*` trees.

* `ruff check` and `ruff format --check` in `src/api`: pass (157 files formatted).
* `mypy` in `src/api`: no issues in 241 source files.
* `src/api` `test_scale*.py` via discover: 11 tests OK (includes the new load and restart test).
* `src/core/tests/test_scenario_manifest.py`: 8 tests OK. No tracked recipe or check changed, so `scenario-manifest.json` was not refreshed.
* `infra/tests/test_container_hosting_completeness.py`: 11 tests OK.
* Not run: full `src/api`, `src/agents` and `src/core` suites. The host was heavily loaded by other worktrees and the full api run exceeded 20 minutes. The change adds only tests, docs and a benchmark record, no source under `src/*/src`.

## Not done

Not pushed. Independent exact-head review and hosted CI remain required.
