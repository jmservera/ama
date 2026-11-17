# Research: issue #176 generator determinism and manifest fields

* Date: 2026-11-14
* Task: `176-generator-determinism-manifest`; Research disposition: `executed`
* Planning Readiness: `Ready`

## Scope

Remaining #176 acceptance criteria: (1) same seed and as-of date give byte-identical output for each generator including stock register and sensor data; (2) manifests record seed, version and generator revision.

## Findings

* Generators in `src/core/src/zava_forward/core/synthetic/`: `stock_register`, `stock_fabric`, `scale_fixture`, `sensor_backfill`, `sensor_scenarios`, `sensor_stream` (with `sensor_stock`, `sensor_faults`, `indoor_projection`, `climate_history`, `household_conditions`, `retrofit_effects`), all seeded through `random.Random(f"{seed}-...")` and `provenance.parse_as_of`.
* `provenance.source_revision` yields `sha256:<64 hex>` for each generator; every manifest records `seed`, `version`, `generator_revision` (and `as_of` where windowed). `sensor_scenarios` has an intrinsic window.
* `determinism_audit.audit()` replays each generator twice and passes for all eight replayable generators (six core plus two support generators); the original private register is reported unavailable.
* `scenario_manifest.py` validates the hand-maintained public coverage manifest against fixed source hashes. It is not a generator output, so it has no seed.
* `src/importer` contains no synthetic generator. Its `datetime.now` and `uuid4` use is runtime quarantine and exception state, not synthetic output.
* `resident_preview_fixture._today()` is wall-clock but feeds an in-memory test store, never serialized generator output.
* Grep of the synthetic package for `datetime.now`, `uuid4`, `date.today`, `utcnow`, `time.time` found no generation-path use.

## Gap

The existing audit and tests replay in one interpreter with one `PYTHONHASHSEED` on one calendar day. They cannot detect unordered-set iteration or clock/uuid leaks. No test proved determinism under hostile ambient state, or as-of independence of stock register payload.

## Environment note

Editable installs point at the main checkout, so validation here uses `PYTHONPATH` set to this worktree's `src/*/src`.

## Recommendation

No generator change is needed. Add a focused matrix test (fresh interpreters, differing hash seeds, wall clock and uuid made to raise) over `determinism_audit.GENERATORS`, plus as-of and manifest-field tests.
