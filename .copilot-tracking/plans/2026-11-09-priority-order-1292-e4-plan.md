# Issue 1292 E4 plan (2026-11-09)

Prospective: committed before any edit. Fourth of five additional cycles; one remains after E4.

* Replace E3's `fake_driver: Any = types.SimpleNamespace(Error=self.Error)` with a test-owned `types.ModuleType` fake that exposes `Error` via a constant attribute install accepted by ruff and mypy, then `conn.driver = fake_driver`.
* Preserve every assertion, the BEGIN-failure and recovery behavior, the other ignore on `conn.state`, and E2's real SQL source bytes. No production, dependency, CI, unused-ignore or transaction changes; no `Any`, `cast` or `# type: ignore` for the driver.
* Choose the attribute install by trying `vars(fake)["Error"]` first (no B010, no attr-defined); fall back to the next candidate only on an actual tool failure and record it.
* Validation (demo typing-only tier), each producer exit captured separately without pipeline masking: import origin printed first; `/tmp/e3venv` mypy, ruff check, ruff format --check, priority module (expect 142 run, 65 skipped); mypy in a typed optional-driver static context (owned venv with mssql-python) if installable; no full Core, SQL or matrix rerun.
* If the typed context cannot be built, record it as not performed.
* Then independent-style original Review (still a self review, not the independent assessment), local commit, handoff.
