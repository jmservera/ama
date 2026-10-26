# Research: hosted review findings on d91302ea (#462), 2026-10-26

* Threads 4382767658 (public default permissions rejected) and 4382878923 (ownership-derived access) on resident_showcase_sql.py; owner-flagged missing real-SQL coverage and keyboard sign-out focus.
* Evidence: the existing opt-in SqlBoundaryTests class (ZF_TEST_MSSQL=1, loopback) already creates a throwaway database; the SQL principal check had only been run against FakeCursor.
* Facts to confirm on real SQL: which public grants a fresh database has; whether a WITHOUT LOGIN user can exercise the rights predicates (external SID identity cannot be created in a container, so identity stays fake-tested).
* Planning readiness: Ready.
