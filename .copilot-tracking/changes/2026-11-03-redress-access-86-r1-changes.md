# Changes: redress access under holds test (Refs #86, R1)

* src/core/tests/test_resident_decisions.py: add one test (21 lines). No production code, README or knowledge-base change, so no log.md entry.

Validation run: `python3 -m unittest tests.test_resident_decisions` (217 tests OK, 80 skipped, SQL Server variants skipped); ruff check and format; mypy --cache-dir=/tmp/mypy-86. Not run: gate, full suites, benchmarks, API tests, MSSQL variants.
