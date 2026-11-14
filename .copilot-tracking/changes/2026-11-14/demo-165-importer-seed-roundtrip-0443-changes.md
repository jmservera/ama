<!-- markdownlint-disable-file -->
# Changes: Epic 165 importer seed round-trip (2026-11-14)

Refs #165. Focused validation tier (test-only, non-gate).

## Added

* `src/importer/tests/test_epic165_synthetic_seed_importer_roundtrip.py` (5 tests).

## Validation

| Check | Result |
| --- | --- |
| New test file | 5 passed |
| `src/importer` full discovery | 121 run, 1 error: `tests.test_version` `PackageNotFoundError` (importer not pip-installed; also fails on the unmodified tree). Others passed |
| `src/importer` ruff, mypy | passed (after import-order fix) |
| `src/core` epic165 (27), synthetic (41), generator tests | passed |
| `src/core` ruff, mypy | passed (308 files) |

Not run: the complete local gate (`rpi-checks.py --all`) and hosted CI; not required for this tier. No push was made.

## Divergences

None.
