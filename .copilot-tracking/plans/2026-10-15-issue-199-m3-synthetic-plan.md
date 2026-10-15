# Plan: M3 synthetic tools and data governance (refs #199)

Research: [research](../research/2026-10-15-issue-199-m3-synthetic-research.md). Details: [details](../details/2026-10-15-issue-199-m3-synthetic-details.md).

## Phases

* [x] 1. Record baseline on `main` (742 total).
* [x] 2. `git mv` four modules, three fixture files and seven tests to their target projects.
* [x] 3. Repoint imports and path strings; add `core/synthetic/output_dir`; local role names in `chat_fixture` with a `mvp` guard test.
* [x] 4. Extend ruff and mypy exemptions, CI paths and `PYTHONPATH`, READMEs.
* [x] 5. Validate: `mvp` suite, every `src` project tests, ruff, mypy, wheel contents, CLI smoke.
* [x] 6. Update matrix, reference index, log, provenance register and data dictionary.
* [x] 7. Commit, push, open PR (refs #199, not closes).

## Critique (executed once, final candidate)

* Accepted: one pull request; the set is small and has no cycle.
* Accepted: local `ROLE_NAMES` plus a `mvp` equality test instead of importing `mvp.auth` from `agents`; it disappears when `auth` moves (M5).
* Accepted: do not repoint `build_mvp_dataset.py` (owned by #200) and do not touch the real `mvp/data/`.
* Rejected: moving `document_control_fixtures` readers out of `mvp/tests` (`test_document_controls` is M2-group and stays until M5).
* No conflict with a confirmed owner decision; no significant divergence needing a user decision.
