# Review: M4 core features (refs #199)

Review executed once after implementation. Outcome: conformant, with open follow-ups routed to later work. Assessed boundary: the M4 branch diff against `main` (`5546282`).

## Checks

* Scope: the five matrix rows marked M4 for code and data plus four of the five tests moved with `git mv` (9 renames); no file left or duplicated in `mvp/`.
* Imports: `mvp` code uses `zava_forward.core` and `zava_forward.agents`; dependency-rule tests pass in every project (`agents` imports only `core`).
* Behaviour: only import lines, path strings and the golden file location changed in the moved code.
* Tests: 747 equal to the 747 baseline; 92 skipped as before.
* SQL portability: no non-portable SQL added.
* Dependencies and check names: no dependency change; `mvp-ci`, `mvp-validation` and `src-*` names kept.
* Path strings: registry, provenance pack, DPIA, READMEs and test globs repointed; no `mvp/evals` reference remains in `src/` or the data pack.

## Findings routed to later work

| Id | Finding | Routing |
| --- | --- | --- |
| F1 | Docker image build and SQL Server jobs not run locally | CI on the pull request; owner checks |
| F2 | `test_chat_isolation` stays in `mvp/tests` | Moves with M5 |
| F3 | The `mvp` image now serves `/api/ai/report` (golden file copied); not run in a container | CI image job and owner check |
| F4 | Temporary ruff and mypy exemptions | Removed in M6 |
| F5 | `recovery` uses `sqlite3` for the local backup copy | Review when the backup path is rebuilt (#114) |
