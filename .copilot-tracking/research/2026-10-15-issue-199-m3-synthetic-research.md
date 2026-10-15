# Research: M3 synthetic tools, eval fixtures and data governance (refs #199)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 199 comment, ADR 0006 (Accepted, move-not-copy, private data relocation to `ZF_DATA`), parity matrix rows marked M3 (14 rows: 4 modules, 3 fixture files, 7 tests), merged PRs 296 (M1) and 297 (M2) and their divergences, `src/README.md`, `.github/copilot-instructions.md`, `docs/reference/README.md`.
* Baseline on `main` (`14b776c`): `mvp` Ran 551 OK (skipped=92); `src` core 167, api 8, agents 8, orchestrator 4, importer 4. Total 742 (matches the M2 total). Target: at least 742.
* Size: about 600 lines of Python plus three JSON files and seven tests. One pull request is safe, so no M3a/M3b split.

## Findings that shape the plan

* `chat_fixture` goes to `src/agents/tests` but imports `auth.DEFAULT_ROLE_MAP`, and `auth` stays in `mvp` until M5. `agents` cannot import `mvp`, so the role names are held locally and a `mvp` test keeps them equal.
* `test_chat_isolation` (M4), `test_recovery` and `test_document_controls` (M2, stays in `mvp`) use the moved files, so they are repointed and `src/agents/tests` joins the `mvp` `PYTHONPATH` (the M2 pattern for `src/core/tests`).
* Path-sensitive strings: tests that compute `ROOT` from `__file__`, the eval registry paths and glob, the provenance register locations, `data-dictionary`, needs inventory, generator usage strings, CI paths and `PYTHONPATH`, `mvp/README`.
* Data governance: generators defaulted to `mvp/data/` (via `parents[1]`). ADR 0006 puts working data in the per-user `ZF_DATA` folder, never under `src/`. The runtime treats `ZF_DATA` as a data file, so the helper accepts a folder or a file path. `build_mvp_dataset.py` repoint belongs to #200. The real `mvp/data/` copy is an owner action (not present in this worktree; no agent reads it).
* The SQL in `sensor_backfill` already uses `INSERT ... WHERE NOT EXISTS`; no `INSERT OR REPLACE/IGNORE`, `AUTOINCREMENT` or `PRAGMA` is introduced.
* Docker and SQL Server are not usable locally (docker socket permission denied); rely on CI.
