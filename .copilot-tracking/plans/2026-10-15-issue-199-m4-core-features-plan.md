# Plan: M4 core features (refs #199)

Research: [research](../research/2026-10-15-issue-199-m4-core-features-research.md). Details: [details](../details/2026-10-15-issue-199-m4-core-features-details.md).

## Phases

* [x] 1. Record baseline on `main` (747 total).
* [x] 2. `git mv` four modules, the golden file and four tests to their target projects.
* [x] 3. Repoint imports and path strings in code, tests, registry, provenance pack and READMEs.
* [x] 4. Extend ruff and mypy exemptions, CI paths and installs, `mvp` image (agents wheel, golden file, `ZF_AI_GOLDEN`).
* [x] 5. Validate: `mvp` suite, every `src` project tests, ruff, mypy, wheels, CLI smoke.
* [x] 6. Update matrix, reference index, log.
* [x] 7. Commit, push, open PR (refs #199, not closes).

## Critique (executed once, final candidate)

* Accepted: one pull request; the set is small and acyclic.
* Accepted: `test_chat_isolation` stays in `mvp/tests` until M5 (same reason as the four M2 tests).
* Accepted: exempt the moved files from ruff and mypy instead of reformatting, to keep renames pure.
* Accepted: add `ZF_AI_GOLDEN` and image support because the golden file lives outside the package; no behaviour change when unset.
* Rejected: moving `recovery`'s `sqlite3` use behind the store; out of scope (behaviour change).
* No conflict with a confirmed owner decision; no significant divergence needing a user decision.
