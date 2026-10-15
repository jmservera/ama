# Plan: M2 core hub move (refs #199)

Research: [research](../research/2026-10-15-issue-199-m2-core-hub-research.md). Details: [details](../details/2026-10-15-issue-199-m2-core-hub-details.md).

## Phases

* [x] 1. Record baseline on `main` (702 mvp tests).
* [x] 2. `git mv` the 25 modules, the policy file, eight test modules plus `release_support`, and `test_content_standard`; extract `dataset.py`.
* [x] 3. Rewrite imports in `mvp/`, `infra/` and `support/` to `zava_forward.core`; fix path-sensitive code.
* [x] 4. Update `src/core` and `src/api` lint and type exemptions, package data, CI, Dockerfile, READMEs.
* [x] 5. Validate: mvp suite, each src project tests, ruff, mypy, wheel contents.
* [x] 6. Update matrix, reference index, log, `src/README.md`.
* [x] 7. Commit, push, open PR (refs #199).

## Critique (executed once, final candidate)

* Accepted: keep one PR; put `ai_registry` and `assistants` in `core` and record the divergence from A1 rather than break the dependency rule.
* Accepted: leave the four server-bound tests in `mvp/tests` and say so in the matrix.
* Accepted: keep ruff and mypy exemptions so renames stay pure; they end in M6.
* No conflict with a confirmed user decision; no significant divergence needing a user decision.
