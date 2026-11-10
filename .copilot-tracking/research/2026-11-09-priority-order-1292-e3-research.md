# Issue 1292 E3 research: hosted Core mypy unused-ignore (2026-11-09)

Scope: PR #1308 head 31464e65c, hosted run 42637488856 job 129229710625. Core
tests (2594 OK, 301 explicit skips), ruff lint and format passed; mypy (275
files) failed alone: `tests/test_priority_order.py:1488: error: Unused "type: ignore" comment [unused-ignore]`.

Findings (observed):

* Line 1488 was `conn.driver = types.SimpleNamespace(Error=self.Error)  # type: ignore[assignment]` on a `_Conn.__new__` instance. `_Conn.driver` is set in the unannotated `__init__` of `mssqlstore`, to `import mssql_python`.
* CI installs only `-e ".[dev]"` for core (no dependencies, so no `mssql_python`): mypy 2.4.0, ruff 0.17.1, CPython 3.12.16.
* Reproduced with a clean venv from that command (`/tmp/e3venv`, mypy 2.4.0, ruff 0.17.1): the identical error at line 1488, exit 1.
* The operator-shell Python has `mssql-python` 1.15.0 installed, mypy 2.4.1, ruff 0.17.3 and resolves `zava_forward` to the primary checkout (`/home/azureuser/source/ama/src/core`), not this worktree. There the ignore is used and mypy passes. This is an environment difference; the E2 local pass is preserved and not claimed to share CI's environment identity.
* Semantics: the ignore is needed only when the driver module is importable and typed; it is unused when it is absent. A fix must type-check in both.
* Side effect noted: priority tests run under the operator-shell Python import the primary checkout's older source and fail (32 failures, 76 errors); they are not valid evidence for this branch. Valid runs use the worktree-bound clean venv.

Fetch: origin/main is daf45a46ca85; no change to test_priority_order.py, core pyproject or mssqlstore between 31464e65c and main (no overlap), so no merge/rebase.

Planning Readiness: Ready.
