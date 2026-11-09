# Issue 1292 E3 details (2026-11-09)

1. `src/core/tests/test_priority_order.py` `adapter()` (around line 1488): replace the ignored assignment with the `Any`-typed local plus plain assignment.
2. Verify in the clean venv built by `pip install -e ".[dev]"` in `src/core` (mypy 2.4.0, ruff 0.17.1): `mypy`, `ruff check .`, `ruff format --check .`, `python -m unittest discover -s tests -p test_priority_order.py`.
3. Verify mypy and ruff under the operator-shell Python (mssql-python present) so the fix holds with a typed driver.
