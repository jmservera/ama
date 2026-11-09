# Issue 1292 E4 details (2026-11-09)

Prospective: committed before any edit.

1. `src/core/tests/test_priority_order.py`, `MssqlBeginRecovery.adapter()` (about lines 1488-1489): build `fake_driver = types.ModuleType("fake_mssql_python")`, install `Error` as `self.Error` through `vars(fake_driver)["Error"]`, keep `conn.driver = fake_driver`. Remove `Any` annotation on the local; `Any` remains imported only if still used elsewhere (the method return annotation uses it).
2. Static: from `src/core` with `/tmp/e3venv/bin/python -m mypy`, `ruff check .`, `ruff format --check .`.
3. Typed context: create owned `/tmp/e4typed`, `pip install -e ".[dev]"` and `mssql-python` there, run mypy; do not touch shared installs or the primary checkout.
4. Runtime: print `zava_forward.core.__path__` in `/tmp/e3venv`, then `python -m unittest discover -s tests -p test_priority_order.py` from `src/core`.
5. Record exits individually; write changes and review artifacts after the edit, in order.
