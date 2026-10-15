---
title: Law Store Azure SQL and Blob Plan (retrospective)
ms.date: 2026-10-15
---

## Task Metadata

* Task ID: law-store-azure-sql-2026-10-15 (issue #210).
* Task slug: law-store-azure-sql.
* Retrospective: this plan describes what commit d175a29 built. It was written
  after implementation and was not approved before it. No critique was run;
  none is claimed.
* Research: .copilot-tracking/research/2026-10-15/law-store-azure-sql-research.md.
* Phase details: .copilot-tracking/details/2026-10-15/law-store-azure-sql-phase-details.md.

## Goals

* Make Azure SQL and Azure Blob the deployed target of the law store, keeping
  sqlite and a local folder as test doubles only.
* Preserve all existing behaviour for AC1 to AC6 of issue #210.

## Non-Goals

* Provisioning Azure SQL, Blob or the WORM policy (infrastructure).
* Legal review or approval of any provision.

## Acceptance Criteria Mapping

| Criterion | Where met | Status |
| --- | --- | --- |
| AC1 full source and provision records | reg_source and reg_version DDL in lawstore.py, both backends | Met |
| AC2 new version, snapshots immutable | append-only ledger or trigger; write-once snapshots | Met |
| AC3 partial sources say so | completeness field, tested | Met |
| AC4 gaps as no source held | reg_gap, tested | Met |
| AC5 read-only viewer without AI | /law.html and /api/law/* | Met |
| AC6 index rebuilt from SQL | rebuild_index, tested | Met |
| Azure SQL ledger and Blob target | MssqlDb, AzureBlobSnapshots | Met in code; deployment unverified |

## Phase Checklist

* [x] P01 Backend interfaces and Azure implementations (retrospective, done in d175a29).
* [x] P02 Tests, CI job, README and knowledge base log (retrospective, done in d175a29).
* [x] P03 Retrospective review against the acceptance criteria.

## Follow-Up Items

* Verify the Blob container immutability policy and Azure SQL deployment when
  infrastructure exists (not in this task).
* Run test_lawstore.MssqlStoreTests in the CI mssql job (not run locally).
