<!-- markdownlint-disable-file -->
# Changes: #176 generator determinism evidence (no source change)

* Date: 2026-11-13. Base/main `33c261a639b768e06bbd7fe0bd8840d71e3f05bd`. Plan: `.copilot-tracking/plans/2026-11-13-demo-generator-determinism-176-0638-plan.md`; research: `.copilot-tracking/research/2026-11-13-demo-generator-determinism-176-0638-research.md`.
* Source, tests, generators and policy: unchanged. Only `.copilot-tracking` artifacts added.
* Environment: Python 3.12.3, new exclusive venv `/tmp/gd176-0638-PeGX/venv` with `pip install ./src/core` (exit 0; build isolation may have used the network, no isolation claimed). `TMPDIR=/tmp/gd176-0638-PeGX/final/tmp`. Fixtures are in-file constructed or fictional registers; no private dataset, `.env`, Azure, provider, browser, Docker or gate. No SQL in the final selected runs; the discarded discovery run executed the temporary-SQLite restart test (see next bullet).
* Discovery runs earlier in Research (all exit 0) included the SQLite restart test via whole-module `tests.test_stock_fabric`; discarded. Final runs below follow the critiqued plan. Logs: `.copilot-tracking/changes/logs/2026-11-13-demo-generator-determinism-176-0638/` (`exits.txt` holds full argv, cwd and true exit per command).

## Final commands (true exit, counts, skips)

| Id | Command (python = venv) | Exit | Result |
| --- | --- | --- | --- |
| t1 | `-m unittest -v tests.test_synthetic_determinism tests.test_stock_register tests.test_determinism_audit` (cwd src/core) | 0 | 28 run, OK, 0 skipped |
| t2 | `-m unittest -v` stream descriptor test x2, `tests.test_sensor_scenarios`, `tests.test_live_readings.GeneratorTests` | 0 | 27 run, OK, 0 skipped |
| t3 | `-m unittest -v` three named `StockFabricTests` (legacy draws, CLI determinism, revisions); SQL test excluded | 0 | 3 run, OK, 0 skipped |
| t4 | `-m unittest -v` six named `GeneratedDatasetTests` (runbook cohort, MVP byte determinism, stock fabric, MVP receipt seed/version/revision, pack, fabric+EPC); SQL test excluded | 0 | 6 run, OK, 0 skipped |
| t5 | `-m unittest -v tests.test_document_form_fixtures.DocumentFormFixtureTests.test_deterministic_and_labelled_synthetic` (cwd src/importer) | 0 | 1 run, OK, 0 skipped |
| t6 | `-m zava_forward.core.synthetic.determinism_audit` (JSON in `t6.out`) | 0 | 8 PASS, all byte identical, no missing manifest field; `unavailable`: `stock-register`; identical to discovery output |

Audit manifest fields (seed 7, as-of 2026-10-15 except pack seed 1341953496): scale-fixture 1.3.0; sensor-backfill-v3; sensor-scenarios-exercise-v1; synthetic-stream-v2; stock-fabric-v1; stock-register-fictional 1.0.0 (all 64-hex revisions); public-pack 2.0.0 and stock-epc-v1 (16-hex revision `5d6374ffe2f7bcd1`).

## Corrected per-generator matrix

| Generator | C1 byte identity (what is actually compared) | C2 manifest fields | Note |
| --- | --- | --- | --- |
| scale-fixture | all files a==b, test and audit | seed, as_of, version, 64-hex revision, file hashes | proven |
| sensor-backfill | test: all files incl. 3 shards (patched shard size, 5 homes); audit: 3 homes at the default shard size, all files a==b | same | proven |
| sensor-scenarios | written files a==b (`test_snapshot_bytes...`), audit | version, 64-hex revision via audit | proven; window intrinsic, not as-of |
| sensor-stream | audit writes frames.jsonl and a manifest from `descriptor()` twice and byte-compares | descriptor records seed, version, 64-hex revision (test); the generator returns a descriptor, the audit writes the file | proven for the composed audit configuration only; fixed replay origin, not as-of driven |
| stock-fabric | CLI outputs a==b | version, 64-hex revision | proven |
| stock-register-fictional | csv and manifest a==b | seed, version, 64-hex revision, source_type | proven for the fictional replacement |
| public-pack | pack and key dirs a==b (audit, isolated interpreter) | seed, version, 16-hex revision, key manifest | seed 7 fails the generator's own validation (no output); audited at seed 1341953496 |
| stock-epc | outputs a==b | `summary.json` carries seed, version, 16-hex revision; `--manifest` conflicts CSV has none | provenance sits in the summary |
| MVP dataset builder | dataset JSON a==b only (test:97-103) | receipt records seed, version, revision (test at :204) | receipt bytes identity not tested |
| document form fixtures | `json.dumps(sort_keys)` equality of two builds | header: seed, generator_version, content_sha256, no revision | C2 gap |
| document control fixtures | not executed (no determinism test located) | header: seed, as_of, generator_version, content_sha256, no revision | C1 untested, C2 gap |
| live_readings | `test_same_seed_home_and_slot_is_reproducible`: lists of serialized `body()` bytes equal across two instances for seed 184, one home and the test slots; no written output files | no manifest at all | C2 gap; C1 byte-level only for the tested home/slots, no manifest or file replay |
| original private stock register | not in repository | none | owner-owned, unavailable |

Observation, not a red test (no existing permitted test asserts it): the committed fixtures `src/importer/evals/document_form_fixtures.json` and `src/core/evals/document_control_fixtures.json` have no `generator_revision` key (`c2-gap-observation.txt`); `zf_documents.py` and `zf_document_controls.py` contain no `generator_revision`.

## Criterion dispositions

* C1: proven for scale, both sensor generators, scenarios, stream (audit configuration), stock fabric, fictional stock register, public pack, EPC and the MVP dataset JSON. Not proven: original private stock register (absent, owner-owned), control fixtures (no replay found), MVP receipt bytes, live_readings beyond its one tested home and slot set. Not closure-ready.
* C2: proven for the core generators, public pack and EPC summary, MVP receipt. Confirmed literal gaps: document form and control fixture headers lack `generator_revision`; live_readings has no manifest. Support revisions are 16-hex prefixes. Not closure-ready.
* Refresh policy criterion untouched.

## Future initial-scope plan (not implemented, needs authorisation)

* Add `generator_revision` (existing `provenance.source_revision` pattern) to both document fixture generators; regenerate the two committed fixtures; add the missing key assertions and a control-fixture determinism test.
* Decide, with the owner, whether live_readings needs a descriptor or is out of "manifest" scope, and the status of the private stock register.
* No relabelling of #184 minute/v2 source; no private-input provenance change.

## Unperformed

Hosted CI, complete gate, deliberate SQL validation, browser, Docker, network isolation, whole-suite run, original stock register and OSM inputs.
