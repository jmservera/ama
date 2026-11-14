<!-- markdownlint-disable-file -->
# Details: Epic 165 IoT, cohort and scenario join parity (2026-11-14)

## Phase 1

* Build a small cohort (n=12) from `scale_fixture` and write sensor readings with `sensor_backfill.write` for seeds 165 and 166.
* Assert sensors, readings, households, events and stages join one-to-one on `ZF-nnnnn` with zero orphan streams and no readings without a registered sensor.
* Assert stages are in `STAGE_ORDER`; property-register archetype ids map one-to-one to labels, EPC bands normalise to A-G, and journey rows join to properties.
* Assert manifest case ids resolve in the constructed fixture with valid stages, reviewed rows equal the needs inventory, and need dataset ids resolve.
* Scan every generated record and the pack for real-person PII patterns using `privacy.pattern_issues`.
* Assert byte-identical replay per seed and differing output across seeds.

## Phase 2

* Core: `PYTHONPATH=src:tests` unittest for the named suites; importer with `PYTHONPATH=src:../core/src`; ruff and mypy from `src/core`.

## Phase 3

* Commit with `Refs #165` and the Copilot trailer; no push.
