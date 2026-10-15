# Research: issue #114 durable Azure SQL store with ledger audit

* Disposition: executed. Planning Readiness: Ready.
* Evidence: `mvp/zavaforward_mvp/{ledger,sqlstore,mssqlstore,store}.py` already provide the hash chain, count digests, append-only audit and the SQL dialect; no per-year digest, load harness or erasure/restore path existed. PRD DH-005 (backup restores re-apply deletions), NFR-002 limits (list/detail p95 1 s, write 2 s). ADR 0005 owner decision: synthetic fixtures only; ADR 0002 decisions 1, 2.
* Gaps by criterion: (1) per-year verification missing; (2) no measuring harness, no Azure access here; (3) no erasure operation or deletion register.
* Constraints: Azure for deployment, non-Azure only for local tests (SQLite harness local only); no real personal data.
* Open items (owner or Azure evidence needed): Azure SQL load run and cost; Azure SQL point-in-time restore drill; DPO/Legal approval of erasure semantics with ledger row history; remaining PRD classes (dashboard, import preview).
