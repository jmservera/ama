---
title: Law Store Azure SQL and Blob Phase Details (retrospective)
ms.date: 2026-10-15
---

## Metadata

Task ID: law-store-azure-sql-2026-10-15. Retrospective: describes work already
committed in d175a29.
Plan: .copilot-tracking/plans/2026-10-15/law-store-azure-sql-plan.md.
Research: .copilot-tracking/research/2026-10-15/law-store-azure-sql-research.md.

## Phase Index

| Phase | Direction | Status |
| --- | --- | --- |
| P01 | Backend interfaces and Azure implementations | Complete (retrospective) |
| P02 | Tests, CI, documentation | Complete (retrospective) |
| P03 | Review against issue acceptance criteria | Complete |

<!-- rpi:phase id=P01 -->
## P01: Backend Interfaces

<!-- rpi:task id=P01-T01 -->
### P01-T01: Database and snapshot interfaces

SqliteDb and MssqlDb share all, run, many, insert_ignore, limited, commit,
rollback and close. LocalSnapshots and AzureBlobSnapshots share put and get.
LawStore takes db and blobs, with from_env choosing by ZF_LAW_STORE. MssqlDb
creates tables when absent, verifies ledger tables are append-only ledger
tables, else installs INSTEAD OF UPDATE/DELETE triggers. Seeding rolls back on
failure.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Server wiring

server.main calls LawStore.from_env().

<!-- rpi:phase id=P02 -->
## P02: Validation and Documentation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Tests and CI

test_lawstore.py covers write-once snapshots, the Azure interface with a fake
container, and MssqlStoreTests; the CI mssql job runs test_lawstore.MssqlStoreTests.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Documentation

mvp/README.md law store section and a docs/reference/log.md entry record the
backends and the unverified infrastructure items.
