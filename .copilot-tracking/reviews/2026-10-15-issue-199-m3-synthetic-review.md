# Review: M3 synthetic tools and data governance (refs #199)

Review executed once after implementation. Outcome: conformant, with open follow-ups routed to later work. Assessed boundary: the M3 branch diff against `main` (`14b776c`).

## Checks

* Scope: exactly the 14 matrix rows marked M3 moved with `git mv` (rename detection shows them as renames); no file left or duplicated in `mvp/`.
* Imports: `mvp` code uses `zava_forward.core.synthetic`; `chat_fixture` is a test-support module on `PYTHONPATH` (`src/agents/tests`), as the matrix target states. Dependency-rule tests pass in every project.
* Behaviour: only import lines, path strings and the default output folder changed in the moved code, plus the local role map in `chat_fixture`.
* Tests: 747 at least the 742 baseline; 92 skipped as before.
* SQL portability: no `INSERT OR REPLACE/IGNORE`, `AUTOINCREMENT` or `PRAGMA` added.
* Dependencies and check names: no dependency change, so no pip-compile run was needed; `mvp-ci`, `mvp-validation` and `src-*` check names kept.
* Data governance: tools default to `ZF_DATA` outside the repository; `.gitignore` entries `/mvp/data/` and `/src/**/data/` are asserted by tests; no working data tracked.

## Findings routed to later work

| Id | Finding | Routing |
| --- | --- | --- |
| F1 | Docker image build and SQL Server jobs not run locally | CI on the pull request; owner checks |
| F2 | `chat_fixture.ROLE_NAMES` duplicates `auth.DEFAULT_ROLE_MAP` until M5 | Guard test now; remove in M5 |
| F3 | `build_mvp_dataset.py` and the real `mvp/data/` still use the old location; the real data copy is an owner action | #200 and cut-over gate |
| F4 | `DS-SENSOR` is still `not-generated` in the provenance register (matrix reopen list for #175) | Data fix, separate follow-up |
| F5 | `ZF_DATA` is a file at runtime but a folder in ADR 0006 wording; `output_dir` accepts both | Align the ADR text in M6 or #200 |
| F6 | Temporary ruff and mypy exemptions | Removed in M6 |
