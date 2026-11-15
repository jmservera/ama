<!-- markdownlint-disable-file -->
# Research: Epic 165 IoT, cohort and scenario join parity (2026-11-14)

Refs #165. Focused validation tier. Disposition: executed. Planning Readiness: Ready.

## Evidence

* Canonical home identifier: `scale_fixture.homes` yields `ZF-{i:05d}` with a PAS 2035 `stage` drawn from `insights.STAGE_ORDER`. `households` carries `home_id`, `events` carries `case`, and `sensor_backfill.sensor_for` derives `SENS-SYN-{i:05d}` and `home_id` from the same home, with dwelling type and age band as a labelled synthetic fabric draw (not an EPC record).
* `sensor_backfill.write` emits `sensors.csv` and `readings-*.csv` (temperature and humidity, `home_id`, `source_type=SYNTHETIC`) plus a manifest; the same seed, window and cadence give byte-identical output.
* Property archetypes and EPC bands live in `docs/reference/research/retrofit-synthetic-data/property-register.csv` (`property_id`, `archetype_id`, `archetype_label`, `current_epc`, `epc_sap`); `resident-journey.csv` joins by `property_ref`. These use the `SYN-PROP-*` namespace; there is no committed stock-to-case link (README line 45 reports it as missing), so the test does not invent one.
* `scenario-manifest.json` carries `fixture_contract.case_ids` (`ZF-4`, `ZF-1`, `ZF-5`), which resolve to cases in `src/core/tests/dataset.py` (a separate, unpadded constructed-fixture namespace with PAS 2035 stages), and `inventory.reviewed_rows` that equal the `needs-inventory.json` ids; each need's `dataset_ids` resolve in `provenance-register.json`.
* `privacy.PATTERNS` and `pattern_issues` give the real-person PII scan (email, UK phone, NI number, postcode); scale homes use the allowed `TE[0-8] 1ST` postcode exemption.
* Existing neighbours (`test_epic165_deterministic_reproducibility`, `..._journey_needs_coverage_matrix`) cover determinism and manifest-to-need binding separately; none joins sensor streams to cohort and stage state.
* Environment: an editable `zava_forward.core` from another checkout is installed, so tests run with `PYTHONPATH=src:tests` from `src/core` and `PYTHONPATH=src:../core/src` from `src/importer`.

## Decisions

* Join on the padded `ZF-nnnnn` id for generated streams; check the manifest's unpadded fixture case ids against the constructed fixture and against `STAGE_ORDER`, and assert the two namespaces stay disjoint rather than fabricating a mapping.
* Property register join covers archetype to EPC band consistency and journey references; claims stay synthetic-only, no EPC or PAS 2035 compliance asserted.
* Test only; no production code change.
