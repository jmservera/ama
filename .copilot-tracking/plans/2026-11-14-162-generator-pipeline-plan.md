# Plan: #162 generator pipeline

* [x] Add `GeneratorConfig` (name, version, seed, as_of, params) with a canonical digest.
* [x] Add `build` (generate then validate in memory), `run` (write only after validation; `seed-manifest.json` with seed, config version, config digest, generated_at, file and output digests) and `verify` (regenerate and compare).
* [x] Keep `generated_at` outside every digest so identical runs match.
* [x] Unit tests in `src/core/tests/test_generator_pipeline.py`.
* [x] Run ruff check, ruff format (line length 100) and focused tests.

Critique (single pass): timestamp must be timezone-aware and excluded from digests; applied directly.
