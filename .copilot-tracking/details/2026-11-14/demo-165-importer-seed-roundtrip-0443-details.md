<!-- markdownlint-disable-file -->
# Details: Epic 165 importer seed round-trip (2026-11-14)

## Phase 1: test file

* Declared `synthetic-cohort` structure with property, archetype and resident-preference fields.
* Rows built from seed 165 and 40 homes using `scale_fixture`, `stock_register` and `stock_fabric`.
* Cases: per-seed determinism; round-trip fidelity and synthetic markers; idempotent re-import (versions, supersession, row counts, empty compare); independent stores; changed seed reports differences without duplicates.

## Phase 2: validation (focused tier)

* `src/importer`: `python3 -m unittest discover -s tests`, `ruff check .`, `mypy`.
* `src/core`: `test_epic165*`, `*synthetic*`, `test_generat*`, `ruff check .`, `mypy`.
* Use `PYTHONPATH=src:../core/src`.
