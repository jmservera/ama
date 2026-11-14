# Research: #162 reproducible generator pipeline and seed manifest

Disposition: executed. Planning Readiness: Ready.

* Existing generators (`scale_fixture`, `sensor_backfill`, `sensor_scenarios`) use seeded `random.Random`, record seed, `as_of`, source revision and file hashes via `provenance.py`, and `determinism_audit.py` replays them twice.
* Gaps against #162: no common config version, no generation timestamp, no output digest independent of timestamp, and no validation gate before the output directory is created.
* Decision: add one generic `synthetic/generator_pipeline.py` rather than change each generator; existing manifests stay untouched.
* Reuse `provenance.prepare_output` (non-destructive output) and `provenance.file_hashes`.

## Cycle 2

* Trigger: mypy `no-untyped-def` at `src/core/tests/test_generator_pipeline.py:23` (`clock_at`) plus two Low review comments (unused `cohort_rng`, `complete` vs `partial_records` summary count).
* Finding: `cohort_rng`, `complete` and `partial_records` do not exist anywhere in this branch (`git grep` empty); the comments target other code, so no change is made for them. Reviewer to confirm.
* Planning readiness: Ready.
