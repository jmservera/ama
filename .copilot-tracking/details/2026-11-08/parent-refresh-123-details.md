<!-- markdownlint-disable-file -->
# Details: discovery parent refresh onto current main, 2026-11-08

Plan: [plan](../../plans/2026-11-08/parent-refresh-123-plan.md).

## Merge

* Pins: topic `5beb7ba7d50dda8435b6ca9f34a6f7b3a0cfd749` plus the planning commit; main `f548b65f4aa31eb92a2cc9cb801130e422daed7f`. Command: `git merge --no-ff origin/main` with a Conventional Commit message and Copilot trailer. Forecast: clean.
* Understood conflict rule: append-only pack, log or index conflicts keep both sides' lines in chronological order; the rubric JSON takes main's exact blob; source or test conflicts in `paired_equity.py` are not expected and stop work.

## Checks (light, no gate group)

* Environment: `PYTHONDONTWRITEBYTECODE=1`, external `XDG_CACHE_HOME`, `MYPY_CACHE_DIR` and Ruff `--no-cache`, tool versions from `src/core/pyproject.toml` (Ruff 0.17.1, mypy 2.4.0 in `/tmp/ci764b-venv`), `PYTHONPATH` set to this worktree's `src/core/src` and `src/core/tests`, with import-file assertions.
* Tests selected from the actual files present after merge: `test_paired_equity`, journey register, release and invalidation, `test_ranking_publication`, `test_ranking_publication_runner`, cohort evaluation.

## Gate

* Output path absent before start: `/home/azureuser/.local/share/ama/gates/c123-f14-1108` on the root filesystem. Lock `/tmp/ama-rpi-heavy.lock`: check holders with `fuser` and `lsof`, and logical owner records, before the run.
