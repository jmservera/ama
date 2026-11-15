<!-- markdownlint-disable-file -->
# Task Research: Issue #165 criteria 3 and 5 (coverage status, synthetic labelling and PII guards)

* Task ID: 165-synth-coverage-pii-2244 (slug `synth-coverage-pii-2244`), mode manual-sequenced RPI, Research disposition: executed
* Branch `test/demo-165-coverage-synthetic-pii-2244`, base `origin/main` 9c8c89890ce783cf78761af0698e42c928dbca2f, target `main`
* Tier: Focused (documentation plus local unit tests, ruff and mypy; no infra, deployment, SQL or security-control change)

## Scope

* `[ ] Every need has a recorded generator coverage status: covered, partial or missing`
* `[ ] All generated data is labelled synthetic and carries no real personal data beyond the documented OpenStreetMap map anchors`
* Allowed paths: `src/core/src/zava_forward/core/synthetic/`, `src/core/tests/`, `docs/reference/research/retrofit-synthetic-data/` if needed. Excluded: `infra/`, `monitoring_coverage.py`, `ai_consumption.py`, `server.py`, `orchestrator/ranking_publish.py`. No private data (`support/`, `~/.zava-forward/`) was read.

## Evidence

* Inventory: `docs/reference/research/retrofit-synthetic-data/needs-inventory.json` v1.3.0, 13 needs SN-01..SN-13, coverage 2 covered, 11 partial, 0 missing. Every row has `coverage`, `note`, `dataset_ids`, and `gap_closure.note`.
* `coverage.build_baseline` validates `coverage` value, closure kind and issue routing, but does not require the per-row `note` (rationale) or `dataset_ids` (evidence). Only `tests/test_needs_inventory.py` checks them, against the committed file, not as a reusable validator. Mutations that blank them are accepted by the validator. Gap G1.
* Generator outputs and labelling:

| Output | Label | PII guard | Finding |
| --- | --- | --- | --- |
| `scale_fixture` homes, households, events | `is_synthetic` | `privacy.snapshot_issues` (snapshot) | Covered; only `TE[0-8] 1ST` postcodes exempt |
| `sensor_backfill` rows, manifest | `source_type=SYNTHETIC` | `snapshot_issues(kind=sensor)` | Covered |
| `live_readings.Reading.row` | `source_type=SYNTHETIC`, `label` | none at emission | Labelled; no guard |
| `sensor_stream.wire` frames | inherits row | none at emission; size only | Gap G2: an unlabelled or PII-bearing row is serialised |
| `sensor_stream.descriptor` | `source_type=SYNTHETIC` | none | Labelled |
| `device_provision.report` | none | none | Gap G3: unlabelled, carries free-text `credential_owner` (operator supplied, could be a real person's email) |
| `stock_register` and OSM anchors | `building_form_osm`, `SYN-` ids | register guard in `sensor_stock` | The documented OSM anchors; no personal data |

* Guard behaviour: `privacy.pattern_issues` detects email, UK phone, NI number and postcode; `record_issues` requires a synthetic label. Both exist but are not applied at the stream and provisioning emission points.

## Gaps selected for closure

1. G1: make the coverage status and its rationale/evidence a validated, reportable property (`coverage.coverage_evidence_issues`, called by `build_baseline`, count surfaced as `coverage_evidence_validated`).
2. G2: guard `sensor_stream.wire` so a frame without `source_type=SYNTHETIC` or with an email, phone, NI number or postcode pattern is refused with a fixed code.
3. G3: label `device_provision.report` (`source_type=SYNTHETIC`, `contains_real_data=false`) and refuse a `credential_owner` that matches a personal-data pattern.
4. Add a generator-output audit test across every emitter listed above.

## Non-goals and limits

* Pattern checks are bounded, not a universal personal-data guarantee. Names such as the fixture `Alex Example` are not detected by patterns and rely on the fixture being constructed.
* Private register regeneration remains outside this task; coverage values are not changed (all stay `partial` or `covered` as recorded) and owner approval remains `not-established`.

## Planning Readiness

Ready. No open question requires the owner; the inventory values are unchanged.
