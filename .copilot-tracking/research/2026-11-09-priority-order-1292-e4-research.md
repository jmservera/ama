# Issue 1292 E4 research: typed fake-driver fixture (2026-11-09)

Prospective: written and committed before any test or source edit in E4. Authorized: fourth of five additional cycles; E1 to E3 spent; one remains after E4.

Baseline: branch fix/demo-recovery-1292-1109 at ee4dfc5fd5e9, clean. PR #1308 head remains 31464e65c (E3 local commit unpublished). Fetched origin/main is daf45a46ca85, unchanged since E3.

Findings (observed in the files, not re-run yet):

* `mssqlstore._Conn.__init__` is unannotated and executes `import mssql_python` then `self.driver, ... = mssql_python, ...`. The module has `ignore_errors` in core `pyproject.toml`, but the inferred attribute type is still used by importers.
* With `mssql_python` installed and typed, `conn.driver` is the module type, so assigning a `types.SimpleNamespace` is an `assignment` error (the reason for the E2 ignore). Without it, the import is covered by the `ignore_missing_imports` override, `conn.driver` is `Any`, and the same ignore is unused (the hosted failure).
* E3 replaced the ignore with `fake_driver: Any = types.SimpleNamespace(...)`. It works but adds an unneeded `Any` to the fixture and its plan/critique were written after the edit (admitted process divergence, preserved, not rewritten).
* The accurate fake is a module-shaped object: `types.ModuleType` carrying the `Error` class the production code catches with `except self.driver.Error`. It is valid whether `conn.driver` is `ModuleType` or `Any`.
* Ruff selects `E,F,I,B,UP`: `setattr(obj, "Error", ...)` with a constant triggers B010. Direct `fake.Error = ...` is likely a mypy `attr-defined` error because `ModuleType` has no `__setattr__` stub. Candidate constant-attribute installs to be tried against the real tools: `vars(fake)["Error"] = ...` / `fake.__dict__["Error"] = ...`.
* Other fake-driver prior art in this module: `types.SimpleNamespace(_Conn=..., ...)` at line about 1556 is a patched `mssqlstore`-like namespace, not assigned to a typed `conn.driver`; no shared helper exists.
* Environments: `/tmp/e3venv` is clean CI-equivalent (mypy 2.4.0, ruff 0.17.1, no mssql_python, editable install of this worktree's core). Operator Python has mssql-python 1.15.0 and imports the dirty primary checkout, so it is only usable for static typing checks with explicit worktree paths and never for runtime tests.

Unknowns: whether a typed-driver static context can be built without altering shared installs (plan: an owned venv `/tmp/e4typed` with core editable plus mssql-python; if installation is impossible, record it as unperformed).

Planning Readiness: Ready.
