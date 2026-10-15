# Plan: M1 isolated leaves

Task: issue-199-m1-leaves. Research: [research](../research/2026-10-15-issue-199-m1-leaves-research.md). Details: [details](../details/2026-10-15-issue-199-m1-leaves-details.md).

* [x] Phase 1: record baseline on main (719 tests, 92 skipped).
* [x] Phase 2: `git mv` three modules and three tests to `src/core` and `src/agents/tests`.
* [x] Phase 3: repoint imports in `mvp/` modules and tests; no shim.
* [x] Phase 4: lint and type exemptions for the unchanged moved files in `src/core` and `src/agents`.
* [x] Phase 5: `mvp-ci`, `mvp-validation` install `src/core`; image builds from the repository root with a core wheel and `mvp/Dockerfile.dockerignore`.
* [x] Phase 6: matrix, index, log, READMEs updated.
* [x] Phase 7: run all suites, record evidence, push and open the PR (refs #199).

Critique: executed once (self-critique). Verdict: accepted. Direct dispositions: keep renames pure (adopted); keep hashed lock untouched (adopted); root build context needs an allowlist ignore (adopted).
