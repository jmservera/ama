---
title: Law Store Azure SQL and Blob Research (retrospective)
ms.date: 2026-10-15
---

## Task and Disposition

Task ID: law-store-azure-sql-2026-10-15 (GitHub issue #210).
Retrospective record: the implementation (commit d175a29 on
feat/law-store-azure-sql) was written before this RPI loop ran. This research
was assembled afterwards from the issue and the existing diff; it did not guide
the implementation.
Research disposition: reused (issue text, ADR 0005 and the existing diff).
Planning Readiness: Ready.

## Issue Evidence

Issue #210 asks for a versioned law store in Azure SQL (ledger enabled) with
immutable Blob snapshots and a rebuildable retrieval index, seeded from the
dated local regulatory snapshots. Source references: ADR 0005 (Architecture 1,
Phasing 1), PRD FR-060/AC-104, BRD FR-051/AC-099, and
docs/reference/regulatory/README.md. ADR 0005 is a proposal; no owner, Legal,
Compliance or DPO approval is recorded.

Acceptance criteria (AC1 to AC6):

* AC1 source and provision records keep official URL, authority type, status,
  effective, retrieval and review dates, content hash, completeness and owner.
* AC2 a newer retrieval is a new version; snapshots are never changed.
* AC3 partial sources carry completeness partial and answers say so.
* AC4 missing sources (leasehold, complaints handling, TrustMark, licensed
  PAS 2035) are gaps returned as no source held.
* AC5 a read-only provision viewer works without AI.
* AC6 the retrieval index can be rebuilt from SQL.

## Existing Change Evidence

Diff origin/main...HEAD (one commit, six files):

* mvp/zavaforward_mvp/lawstore.py: the existing sqlite and local-folder store
  was already present on main (AC1 to AC6 largely met there). The commit adds
  a backend split: SqliteDb and LocalSnapshots (test doubles), MssqlDb (Azure
  SQL, append-only ledger tables when the database is ledger enabled, else an
  INSTEAD OF trigger), AzureBlobSnapshots (upload without overwrite), and
  LawStore.from_env selecting by ZF_LAW_STORE.
* mvp/zavaforward_mvp/server.py: uses LawStore.from_env.
* mvp/tests/test_lawstore.py: new snapshot and Azure interface tests plus
  MssqlStoreTests (skipped without a SQL Server).
* .github/workflows/mvp-ci.yml: adds test_lawstore.MssqlStoreTests to the
  mssql job.
* mvp/README.md and docs/reference/log.md: describe the backends and open items.

## Evidence Boundaries

* Azure SQL and Azure Blob behaviour is exercised only in CI against SQL
  Server and a fake container; no Azure deployment was observed.
* Blob container immutability (WORM) is infrastructure and unverified.
* Seeded versions are not_reviewed with owner to be named; no legal approval.

## Risks and Open Items

* Gap vs the issue wording: the issue says Azure SQL with ledger enabled; the
  code supports both ledger and trigger fallback.
* No infra/ Bicep change in the diff; the issue does not require one.
