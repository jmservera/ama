# Research: src-ci affected-project selection (2026-11-03)

Issue-less CI work. Owner priority: cut CI load.

* Source: `.github/workflows/src-ci.yml`. Every PR touching its path filter ran all five matrix projects, `src-namespace` and `mssql`.
* Branch protection depends on job names (`src-core`, `src-api`, `src-namespace`, ...). A job-level `if` on a matrix job leaves the unexpanded name `src-${{ matrix.project }}`, so the matrix must keep all five entries and gate steps instead. Jobs with static names (`src-namespace`, `mssql`) can use a job-level `if`; skipped jobs report success.
* Dependencies: api installs core and agents; agents, orchestrator and importer install core. api and agents tests use `src/core/tests` helpers, so a core tests change affects dependents.
* mssql installs core, agents, api, orchestrator only.
* Decision: unknown or ambiguous paths select everything; only provably unaffected work is skipped.
