<!-- markdownlint-disable-file -->
# Research: Epic 165 importer seed round-trip (2026-11-14)

Refs #165. Focused validation tier. Disposition: executed. Planning Readiness: Ready.

## Evidence

* Importer ingestion path: `zava_forward.importer.mapping.preview_bytes` with a declared `Structure`, then `QuarantineStore.stage` and `approve` (`src/importer/src/zava_forward/importer/quarantine.py`). Rows are stored as JSON payloads in `import_rows`; a re-import creates a new version and supersedes the earlier approved batch.
* Importer may import only `core` (dependency rule test), so the fixtures come from `zava_forward.core.synthetic`: `scale_fixture.homes` (address, postcode, stage), `scale_fixture.households` (preferred channel, adjustment) and `stock_register` plus `stock_fabric` (dwelling type, age band, construction, heating; the archetype metadata the fabric label says is not an EPC record).
* `CASE_LIST` has no archetype or preference columns, so the test declares its own `Structure`; no production code changes.
* `compare` in `export.py` gives a read-only difference report suitable for idempotency checks.
* Environment: importer is not pip-installed, so tests run with `PYTHONPATH=src:../core/src`; `tests/test_version.py` errors with `PackageNotFoundError` on the unmodified tree (pre-existing, environmental).

## Decisions

* Isolated store: per-test temporary SQLite file through `QuarantineStore(conn)` and `create_schema`.
* Claims stay synthetic-only; no EPC or PAS 2035 compliance is asserted, only that the archetype fields survive import.
