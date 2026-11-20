# Critique: issue 120 live fix (single pass)

Candidate: on MSSQL add `notice_version` as a nullable column and read it with `COALESCE(notice_version, N'')`; keep NOT NULL DEFAULT for newly created tables.

* Verdict: proceed. Legacy rows read as `''`, which never equals the current notice version, so an old enabling record cannot satisfy the gate (fails closed). Matches SQLite upgrade semantics.
* Inserts always supply notice_version, so nullability never persists on new rows.
* Risk: SQL change requires FULL tier before publication; recorded, not run here (owner: never run rpi-checks.py --all).
* No conflict with confirmed owner decisions.
