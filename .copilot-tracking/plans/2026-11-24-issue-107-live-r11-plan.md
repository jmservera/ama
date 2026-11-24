# Plan r11 (Refs #107)

1. Worker: add `schema` (SCHEMA_VERSION + registry) variation moving `assistants.SCHEMA_VERSION`, and `registry` moving `assistants.VERSION`.
2. Tests: two `check_process_wide_binding` cases (trigger/field assertions determined by running); both separate processes, SQLite and actual SQL Server.
3. Validate: SQLite module, disposable SQL Server 127.0.0.1 (removed after), ruff, mypy, mutation check.
4. Research note, index, log; changes and review records; commit.

## Critique (executed once)

Verdict: accepted. Risk: process-wide module patching leaks; confined to the worker process. Do not duplicate r10 tests; only add the two unmoved fields. Tier FULL (src/api tests); no --all.
