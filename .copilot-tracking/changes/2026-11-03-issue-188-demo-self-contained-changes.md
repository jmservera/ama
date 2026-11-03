# Issue 188 changes (2026-11-03)

## Changed

* `src/api/checks/sensor_handover_demo.py`: self-locating fixture path.
* `src/api/README.md`: shorter demo command and note.

## Validation run (focused tier)

* Demo with `PYTHONPATH=src:../core/src:../agents/src`: exit 0; `--seam 1.5`: exit 1.
* `test_sensor_handover_demo` and `test_sensor_consistency`: 42 tests OK.
* ruff check and format check clean on `checks` and the demo test.
* mypy (`--cache-dir=/tmp/mypy-188`): one `no-any-return` error, identical on the base commit (pre-existing, not fixed here).

## Not run

Complete local gate, benchmarks, full suites, SQL Server, Azure SQL, live Hub. No knowledge-base file changed, so no log.md entry.

## Acceptance criteria

All three remain unmet (live Hub to Azure SQL only). Use Refs #188.
