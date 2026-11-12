---
title: Issue 144 permit SQL E5 correction phase details
description: Phase details for the E5 correction
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e5-correction-1111
---

## Phase 1 module edit

* `claim_behind_lock`: `running` thread variable set after successful `start()`; post-unwind handling of `failure[]`, notes via `traceback.format_exception`, `InvalidWitness ... from primary` for cleanup errors.
* `assert_isolated`: manifest-bound validation as in the plan; called in `setUp` before the fixture.
* Case 3: marker `issued_at` equality inside one transaction.

## Phase 2 probes

Probe script and old/new results live under the external directory `144-permit-sql-e5-correction-1111` (probe/, logs/), labelled HARNESS-ONLY.

## Phase 3 static and SQLite

Run from a new snapshot with the reused V and PYTHONPATH precedence so that all module files originate from the new snapshot.
