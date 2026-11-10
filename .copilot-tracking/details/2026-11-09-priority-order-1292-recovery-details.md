<!-- markdownlint-disable-file -->
# Details: issue 1292 recovery validation (2026-11-09)

Phase 1 merge main. Phase 2 SQLite/in-memory tests. Phase 3 owned SQL Server: container labelled `zf.task=1292-sql-disposable`, published only on 127.0.0.1:14392, random password, private 0600 manifest via `sqlguard.write_manifest`; `ZF_SQL_TRUST_CERT=1` for the self-signed certificate; removed afterwards. Phase 4 static checks. Admission: no other SQL container was running; no queueing, no Docker prune.
