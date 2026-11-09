<!-- markdownlint-disable-file -->
# Changes: post-policy validation of recovered #123, 2026-11-09

Plan: [plan](../../plans/2026-11-09/postpolicy-validation-123-plan.md). Refs #123, #128, #440.

## Implemented

* Phase 1: guarded local merge (HEAD `572fc4729b59e6d41c831536e3841251b860f263` and `origin/main` `9814cf6b236be1f2e86c4401973b8e834be927bc` confirmed immediately before, tracked tree clean). `git merge --no-ff origin/main` merged with no conflict; merge commit `01a1964cb3b084c2dab04dd5d188eb017eeedf94`, tree `5e71e6989f958e50d69e79e637df8119dbf5cee4` (equal to the pre-merge `git merge-tree` prediction). Parents: `HEAD^1` frozen candidate, `HEAD^2` main. Author and committer `8036360+jmservera@users.noreply.github.com` (repository-local config).
* Phase 2: `b46a9ad9a` (old base), `572fc4729` (frozen candidate), `cfd1bca` (old remote PR head) and `9814cf6b2` (main) are all ancestors of the merge. No `src/**/*.py` or `src/**/*.sql` path differs between the frozen candidate and the merge. The merge adds seven non-tracking paths (all documentation or agent text): `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.github/copilot-instructions.md`, `.github/rubric/README.md`, `docs/reference/log.md`, `docs/reference/method/tracking-retention-policy.md`, `docs/reference/research/delivery-bottleneck-analysis-2026-10-31.md`, `src/README.md`, plus main's `.copilot-tracking/` files. `git diff --check` over non-tracking paths: exit 0, clean. Inherited trailing-whitespace findings exist in main's tracking sandbox evidence (55 output lines); not edited.
* Phase 3 (from `src/core`, `PATH` with `~/.venvs/zf123-pinned/bin` first, Python 3.12.3, ruff 0.17.1, mypy 2.4.0, `PYTHONDONTWRITEBYTECODE=1`): `ruff check .` exit 0; `ruff format --check .` exit 0, 216 files already formatted; `mypy` exit 0, 269 source files, no issues; `PYTHONPATH=src:tests python -m unittest test_paired_equity test_cohort_eval test_household_conditions test_retrofit_effects test_monitoring_coverage test_rule_engine test_chat_privacy -q` exit 0, 146 tests OK, no skip lines. Import provenance: `zava_forward.core.paired_equity.__file__` is `/home/azureuser/source/ama-demo-wt/issue-123/src/core/src/zava_forward/core/paired_equity.py`. Counts match the pre-merge pinned run.
* Phase 4: relative-link existence check over eight merged policy files: 1043 links, 17 missing, all in `docs/reference/log.md` historical entries pointing at retired `mvp/` and `docs/capstone` paths. They are present identically in `origin/main` and the frozen candidate (66 matching lines each); the merge adds none. Log merge is append-only (no removed lines relative to the frozen candidate).
* Phase 5: this evidence only; no source, manifest or pin change.

## Not run

`rpi-checks --all`/`--changed`, SQL, API, browser, hosted CI, Azure, real model, private data. No main path requires them.

## Divergences

The first write of the critique file failed (missing directory) in the same batch as the guarded merge; corrected afterwards (see critique note). No source divergence.
