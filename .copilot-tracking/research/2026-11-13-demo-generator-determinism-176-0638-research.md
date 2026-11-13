<!-- markdownlint-disable-file -->
# Research: #176 generator determinism and manifest criteria (local frozen evidence)

* Date: 2026-11-13. Task: demo-generator-determinism-176-0638. Base/current main: `33c261a639b768e06bbd7fe0bd8840d71e3f05bd` (tree `5626e500605d82775ddbf5abf548da3a844bcdf3`), branch `test/demo-generator-determinism-176-0638`, clean at start.
* Research disposition: executed. Planning Readiness: Ready.
* Read: `docs/reference/memory.md`, `src/core/README.md` (reproducibility section, lines 3845-3890), issue #176 body (live), ledger facts (#176 comments: all available generators replayed; original private OSM inputs and universal historical manifests remain owner-owned). Both case studies and the knowledge-base index were read for context only; they hold no generator-determinism evidence beyond the README above.
* Not used: private datasets, `.env`, Azure, provider/model, credentials, SQL, browser, Docker, gate.

## Literal criteria

* C1: "Same seed and as-of date give byte-identical output for each generator, including the stock register and sensor data".
* C2: "Output manifests record seed, version and generator revision".

## Stale issue text, checked against current source

* "Pack builder writes wall-clock generated_at": stale. `generate_pack.py:291` derives `generated_at` from `--as-of` (help text line 245: never read from the clock).
* "Stock register generator is not in the repository": partly stale. A seeded fictional `stock_register.py` exists (PR #843). The original private OSM-anchored generator and its pinned inputs are still absent (`determinism_audit.UNAVAILABLE`, README 3875).
* Paths `mvp/` and `support/.../build_mvp_dataset.py` are old. Current tests are `src/core/tests/*`; generators are `src/core/src/zava_forward/core/synthetic/*` plus support generators.

## Per-generator matrix (blob ids at main 33c261a)

| Generator (blob) | C1 evidence | C2 evidence | Merged PR |
| --- | --- | --- | --- |
| scale_fixture.py 959ffff | `test_synthetic_determinism` scale a==b all files, seed/as_of change; audit `scale-fixture` | manifest seed, as_of, version 1.3.0, 64-hex revision, file_sha256 (`assert_manifest`) | #633 |
| sensor_backfill.py b381fba | sensor a==b incl. 3 shards; audit `sensor-backfill`; payload goldens | seed, as_of, version sensor-backfill-v3, 64-hex revision | #633 |
| sensor_scenarios.py cb6d917 | `test_sensor_scenarios` same seed repeats (object equality); audit byte-compares written files | audit manifest check: version sensor-scenarios-exercise-v1, 64-hex revision | #633 |
| sensor_stream.py 3977e7f | audit `sensor-stream` composed replay, register-backed, byte compare of frames.jsonl and manifest | `test_descriptor_records_seed_version_and_full_generator_revision`; version synthetic-stream-v2 | #1052 |
| stock_register.py 7913969 | `test_stock_register` a==b csv+manifest; audit `stock-register-fictional` | manifest seed, version 1.0.0, 64-hex revision, source_type | #843 |
| stock_fabric.py baee5d9 | `test_stock_fabric` CLI determinism, audit `stock-fabric` | version stock-fabric-v1, 64-hex revision | #633 |
| generate_pack.py 382fddb (support) | audit `public-pack` isolated replay (seed 1341953496; seed 7 fails its own validation); `test_pack_generator_is_byte_deterministic_with_manifest` | seed, version 2.0.0, 16-hex revision, key manifest too | #703 |
| zf_stock_epc.py 34b1aba (support) | audit `stock-epc`; `test_stock_fabric_and_epc_generators_are_byte_deterministic_with_revision` | version stock-epc-v1, 16-hex revision | #703 |
| build_mvp_dataset.py 108eeda (support) | `test_same_seed_date_and_register_are_byte_deterministic` (fictional register) | `test_mvp_output_and_receipt_record_seed_version_and_revision` | pre-core migration |
| Original private stock register generator | not in repository; no receipt possible | n/a | none |

## Observations and limits

* Existing audit `determinism_audit.py` (ae51000) replays its eight registered generators (scale, sensor backfill, scenarios, stream, stock fabric, fictional register, public pack, EPC) twice in separate temp directories, byte-compares every file of those eight, and does not register the MVP builder, document fixtures or live readings. It validates manifest seed, version and revision regex.
* Support generators record a 16-hex revision prefix; the audit accepts it by design (`SUPPORT_REVISION`). Literal wording "generator revision" is met, but at weaker collision resistance than the 64-hex core revisions.
* `sensor-scenarios` window is intrinsic (2024-01-01..2024-01-29), not as-of driven; seed is the determinism input there.
* The stock register item is satisfiable only by the fictional replacement; the original is an owner-owned gap, not an engineering defect found here.
* The prior 0630 note read only test names; this task executes them.

## Planning Readiness: Ready

Selected tests use constructed or fictional fixtures (test bodies read before execution: `test_stock_fabric` writes a constructed register into a temp dir and sets `ZF_DATA` to it; `test_generated_dataset` uses an in-file `register()`).
