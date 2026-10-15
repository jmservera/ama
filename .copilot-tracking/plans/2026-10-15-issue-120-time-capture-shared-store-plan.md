---
title: Issue 120 time capture shared store plan
description: Plan for shared-store time capture and requester/enabler separation
ms.date: 2026-10-15
---

## Phases

* [x] Merge `origin/main`, keeping both sides of `docs/reference/log.md`.
* [x] Move `time_entry`, enabling records and `notice_ack` into the shared SQL store with per-dialect DDL, no SQLite-only SQL in shared statements, one connection per operation via `assistant_connection()`.
* [x] Add `time_request` and require `activate` by a manager whose role and identity differ from the requester; audit both actions; UI buttons.
* [x] Tests: separation, shared store (SQLite and SQL Server), portability scan of `timecapture.py`.
* [x] README and knowledge-base log updated.

## Decisions

* Only the JSON demo store (no database) keeps a local SQLite fallback, stated in status and README.
* Old local `time.sqlite` content is not migrated: the feature was off and gated on an unapproved DPIA.
* Critique executed once, compatible findings applied directly: references changing voids the request as well as the enabling record.
