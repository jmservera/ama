# Issue 1818 c2 changes

Status: complete.

* `src/api/tests/test_map_sensors.py`: `put` override now matches `Seed.put` (count, consent, home, offset, **kw) and forwards all; new typed `map_view()` wraps untyped `request` with one `type: ignore[no-untyped-call]`; `sensor` casts its return.

Validation: `cd src/api && mypy` and `cd src/core && mypy` clean; `ruff check` clean; `unittest tests/test_map_sensors.py` 13 tests OK (run with worktree PYTHONPATH because editable installs point at the main checkout).
