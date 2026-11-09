<!-- markdownlint-disable-file -->
# RPI Research: source-preserving current-main preparation (#1298)

* Task slug: main-preparation-1298 (child of chat-schema-sql-selector-1298)
* Date: 2026-11-09
* Research disposition: executed (read-only git inspection; no merge yet)
* Planning Readiness: Ready

## Scope

Prepare the frozen candidate for `main` by an ordinary local merge of current `origin/main`, without changing source. The approved candidate is HEAD `dadcd6da8cd939ffd54c259ed36c36077b249da3`, tree `daa47968359d8a2654bd2ba4f19f30c778279a23`, whose first independent Functional review (verdict approve, 0 findings, local-source only) is recorded in the coordinator file `independent-1298-final/` and was made against base `9f9aacc8b`, not current main. The review lane could not execute ancestry or main-side compatibility, so this lane must.

## Evidence

* C1. Fetched `origin/main` is `ef28d4da42d83b111d48f14df9b70e3c4932a477` (commit). `git rev-list --count HEAD..origin/main` is 3: `ba5cc74b8` (rubric score), `8d6f029ca` (SQL priority ordering and index bootstrap, #1308) and `ef28d4da4` (rubric score). The merge base with HEAD is `9f9aacc8b`, the candidate's introduction base.
* C2. `8d6f029ca` is an ancestor of `origin/main`. Main-side non-documentation paths: `.github/rubric/scores/latest.json`, `src/api` (server.py, web/app.js, tests/test_case_journey.py), `src/core` (README.md, pyproject.toml, continuity.py, mssqlstore.py, sqlstore.py, store.py, tests/sqlguard.py, tests/test_priority_order.py, tests/test_resident_decisions.py).
* C3. `git diff HEAD...origin/main --name-only -- tools` is empty, as are `.github/workflows`, `src/README.md`, `chatthreads.py` and the sensor fixture. The candidate edits only `tools/rpi-checks.py` and `tools/test_rpi_checks.py` plus tracking records. The candidate and main paths do not overlap; the tools files on main equal the base versions.
* C4. `git merge-tree --write-tree HEAD origin/main` reports a clean tree `a6e09b242ae1f0bdef00b1d71a979b19ed8b9b5d` with no conflicts.
* C5. The selector premise still holds on main: `origin/main:mssqlstore.py` line 20 still imports `MEMORY_ADDED`, `MSSQL_DDL`, `MSSQL_INDEX` from `.chatthreads`, and `chatthreads.py` is unchanged. Main changed `mssqlstore.py` and `sqlstore.py` but the candidate does not depend on their content.
* C6. No candidate receipt exists. Synthetic receipt fixtures in `tools/test_rpi_checks.py` exercise verification logic only and are not gate passes.
* C7. Tool pins: Ruff 0.17.1 and mypy 2.4.0 appear in `tools/rpi-checks.py`. Existing owned environment `~/.venvs/zf123-pinned` (Python 3.12.3) reports exactly ruff 0.17.1 and mypy 2.4.0, so no installation is needed. The gate's lint args are `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` for check and `--isolated --line-length 100 --check` for format over `RUFF_GROUPS[-1]` (both tool files); the mypy command is `--strict tools/rpi-checks.py tools/test_rpi_checks.py`.
* C8. The earlier lane's logs live in `/tmp/i1298-fresh.PsO6Ge`. This lane uses its own owned directory `/tmp/i1298-mainprep.syPvb5`.

## Constraints

* No source modification, no productive correction, no SQL behavioral change, no actual-SQL, full-gate or hosted claim, no push, PR or board action, no Docker or heavy run.
* Original old-branch (`fef352e0`) adverse findings (1 High, 3 Medium) and the fresh critique (Revise, 0 High, 3 Medium, 4 Low) and Review (Residual work) records stay unchanged.
* The literal full-gate acceptance criterion stays unmet; deliverable is `Refs #1298` only.

## Planning Readiness

Ready. The merge is expected to be clean and source-neutral for the two tool files.
