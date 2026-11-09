# Issue 1292 E3 changes (2026-11-09)

* `src/core/tests/test_priority_order.py`: removed `# type: ignore[assignment]` on `conn.driver`; added `fake_driver: Any = types.SimpleNamespace(Error=self.Error)` and `conn.driver = fake_driver` (+2/-1 lines).

Results (actual):

* Pre-fix clean venv `mypy`: 1 error at line 1488, exit 1 (reproduced).
* Post-fix clean venv (mypy 2.4.0, ruff 0.17.1): `mypy` Success, 275 files; `ruff check .` pass; `ruff format --check .` 222 files formatted; priority module 142 tests OK, 65 skipped, ~112 s.
* Post-fix operator Python (mypy 2.4.1, ruff 0.17.3, mssql-python 1.15.0): mypy Success 275 files; ruff check and format pass.
* Operator Python priority run: 32 failures/76 errors, because it imports the primary checkout's older `zava_forward` (stale editable install), not this worktree. Not valid branch evidence; recorded, not waived. The worktree-bound venv run passes.
* Not run: full Core suite (2594), MSSQL contracts, blanket gate (not applicable to a typing-only test change; hosted CI will rerun).
