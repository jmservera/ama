<!-- markdownlint-disable-file -->
# Phase Details: source-preserving current-main preparation (#1298)

Plan: .copilot-tracking/plans/2026-11-09/main-preparation-1298-plan.md. Log directory (uncommitted): `/tmp/i1298-mainprep.syPvb5`.

## Phase 1: Plan commit

* Stage only the five main-preparation-1298 records; commit with the repository-local noreply identity and the Copilot trailer.
* Gate: worktree clean and HEAD descends from `dadcd6da8` before merging.

## Phase 2: Merge

* `git fetch origin main`, confirm `origin/main` equals `ef28d4da4`, then `git merge --no-ff origin/main -m "merge: bring origin/main into the sensor chat-schema selector candidate"` with the trailer.
* Conflict means stop; do not resolve productively.

## Phase 3: Source-equivalence proof

* `git rev-parse HEAD:tools/rpi-checks.py dadcd6da8:tools/rpi-checks.py` and the same for `tools/test_rpi_checks.py`: pairs must match.
* `git diff --name-only dadcd6da8 HEAD` must list only main-side paths and the new records; `git diff --name-only dadcd6da8 HEAD -- tools` must be empty.
* `git diff origin/main HEAD --name-only` must list only the nine approved candidate paths plus the main-preparation records and this merge's records.
* `git merge-base --is-ancestor` checks for `dadcd6da8`, `ef28d4da4`, `8d6f029ca`, `9f9aacc8b`.

## Phase 4: Validation (owned venv `~/.venvs/zf123-pinned`, version check first)

* `python -m unittest discover -s tools -p test_rpi_checks.py -v` (103 expected).
* Targeted regression class from the earlier changes record, run by name.
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` on both tool files with `RUFF_CACHE_DIR` in the log directory.
* `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py` with `MYPY_CACHE_DIR` in the log directory.
* `git diff --check`; clean status.

## Phase 5: Records and handoff

* Write the changes record and review record with actual counts and exits; update state; commit; write the coordinator handoff.
