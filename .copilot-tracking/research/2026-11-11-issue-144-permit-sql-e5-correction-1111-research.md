---
title: Issue 144 permit SQL E5 correction research
description: Research for the one admitted E5 correction of the single test module
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e5-correction-1111
---

## Disposition

Research executed (read-only) on frozen aff1befd (tree b0026d7e). Planning Readiness: Ready.

## Evidence

* Independent report `independent-144-permit-sql-code-aff1-1111.json`, read in full: approve_with_comments, 2 Medium, no application defect.
* Finding 1 (module lines 228-233, 267-268, 298-310): `finish_worker` joins any non-None thread, so a failed `Thread.start()` makes cleanup raise "cannot join thread before it is started" and replace the primary; `failure[]` is read only on the normal path.
* Finding 2 (lines 86-98): `assert_isolated` takes `TMPDIR.parent` as scratch; `TMPDIR=/tmp` makes scratch `/`, so the check is vacuous.
* Case 3 receipt gap: the permitted marker is a durable event `kind=permitted` with `issued_at=now` (assistants.py issue_permit); `Assistants._markers(db, tid)` is the existing reader (used by `complete_result` and reclaim). No new API is needed.
* Environment: old V (paho-env-1111) is reusable only after a binding probe; current source bytes (699 files) equal the old snapshot manifest.

## Boundaries

E5 is counted, none remain. Only the one module plus new dated E5 records change. No SQL, container, lock or mutant run.
