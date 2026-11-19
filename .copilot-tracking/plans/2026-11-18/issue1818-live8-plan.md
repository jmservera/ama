<!-- markdownlint-disable-file -->
# Issue 1818 live8 plan: land the held sensor_register receiver fix (Refs #1818)

Tier: FULL (SQL and receiver grants). The full gate runs only when `/tmp/ama-rpi-heavy.lock` is free; it was held at 2026-11-18T17:45Z, so this candidate stops after focused tests.

1. Port the three source files and the infra grant text from held commit `7bde5f149` onto a fresh branch from `origin/main` (`2cd131da5`); do not carry its stale artifacts.
2. Run the new unit test, the core sensor consumer suite, the SQL Server grant test where a server is available, mypy and ruff.
3. Write a research note with a per-criterion proven or unproven table, reusing round 7 live evidence already on main.
4. Record changes, review, commit locally; no push.
