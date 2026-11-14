# Plan: #162 generator pipeline

* [x] Add `GeneratorConfig` (name, version, seed, as_of, params) with a canonical digest.
* [x] Add `build` (generate then validate in memory), `run` (write only after validation; `seed-manifest.json` with seed, config version, config digest, generated_at, file and output digests) and `verify` (regenerate and compare).
* [x] Keep `generated_at` outside every digest so identical runs match.
* [x] Unit tests in `src/core/tests/test_generator_pipeline.py`.
* [x] Run ruff check, ruff format (line length 100) and focused tests.

Critique (single pass): timestamp must be timezone-aware and excluded from digests; applied directly.

## Cycle 2

* Trigger: mypy `no-untyped-def` at `src/core/tests/test_generator_pipeline.py:23` (`clock_at`) plus two Low review comments (unused `cohort_rng`, `complete` vs `partial_records` summary count).
* Finding: `cohort_rng`, `complete` and `partial_records` do not exist anywhere in this branch (`git grep` empty); the comments target other code, so no change is made for them. Reviewer to confirm.
* Planning readiness: Ready.
