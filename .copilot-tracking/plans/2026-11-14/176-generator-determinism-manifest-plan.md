# Plan: issue #176 generator determinism and manifest fields

* Date: 2026-11-14
* Research: `.copilot-tracking/research/2026-11-14/176-generator-determinism-manifest-research.md`
* Critique: executed once; verdict compatible, no conflicting advice

## Phases

* [x] Phase 1: add `src/core/tests/test_generator_determinism_matrix.py`
  * Replay every `determinism_audit.GENERATORS` entry in three fresh interpreters with `PYTHONHASHSEED` 1, 2, 3 and banned `datetime.now/today`, `time.time`, `uuid4`; assert identical tree digests and manifest `seed`, `version`, `generator_revision`.
  * Assert stock register payload is independent of `as_of` while the manifest records it, and sensor backfill output changes with `as_of`.
  * Assert `scale_fixture` manifest fields per seed.
* [x] Phase 2: validate in `src/core`: targeted unit tests (including `test_scenario_manifest`, `test_needs_inventory`), `mypy .`, `ruff check .`, `ruff format --check .`.
* [x] Phase 3: write changes and review artifacts, confirm no tracked `.pyc`, commit locally without pushing.

## Decisions

* No generator source change: research found no leak.
* Only `src/core` is touched; importer has no generator.
* Tier: focused (test-only change).
