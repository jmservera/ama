# Issue 1292 E4 changes (2026-11-09)

Chronology: planning commit c5e242ca1873 (research, plan, details, critique) preceded the edit; edit applied 15:05:57Z after it; changes and review written after validation.

* `src/core/tests/test_priority_order.py` `MssqlBeginRecovery.adapter()` (+2/-1): `fake_driver = types.ModuleType("fake_mssql_python")`, `vars(fake_driver)["Error"] = self.Error`, `conn.driver = fake_driver`. Removes E3's `Any` seam. Assertions, BEGIN-failure/recovery behavior, the `conn.state` ignore, production, dependencies and CI untouched.
* Attribute install: first candidate worked; no fallback needed.

Validation (demo typing-only tier; each exit captured separately):

* Import origin (/tmp/e3venv): zava_forward.core path = this worktree `src/core/src/zava_forward/core`. /tmp/e4typed also resolves to this worktree.
* /tmp/e3venv (no mssql_python, mypy 2.4.0, ruff 0.17.1): mypy exit 0 (275 files); ruff check 0; ruff format --check 0 (222 files); priority module (from src/core) exit 0, 142 tests, 65 skipped; the two MssqlBeginRecovery tests ran and passed (not skipped).
* /tmp/e4typed (owned new venv, mssql-python installed): mypy exit 0 (275 files); ruff check 0. Probe showed `conn.driver` is `types.ModuleType` there (SimpleNamespace assignment errors) and `Any` in e3venv; ModuleType assignment is accepted in both.
* Not run: full Core, SQL contracts, matrix (no executable SQL change). E2 real-SQL evidence for the source bytes is preserved and not replaced by these skipped unit cases.
* The earlier operator-Python 32 failures + 76 errors (dirty primary import) remain invalid environment evidence, not waived or claimed passed.
