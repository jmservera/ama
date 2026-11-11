---
title: Issue 1259 failing-first verification research
description: Evidence audit for the literal regular-file, dangling-link and absent-directory failing-first proof gap (source unchanged)
ms.date: 2026-11-11
---

## Scope and base

* Task `1259-ranking-archive-path-health-failing-first`, branch `test/archive-path-regression-proof-2122`, base and head at start `077ad5ad20293a1d79932ea14e9f639dd11e5a22`, target `main`. Research disposition: executed (read-only audit of issue, comments, original RPI records and current source).
* Source delivered: #1325 into the #1258 topic (`fbf0a0ab`), then #1328 into main (`cd687abad`). This task changes no source, test, tool or workflow and does not rebuild #1325.

## Issue 1259 state (read 2026-11-11)

* Criteria 1 to 3 ticked, criterion 4 (regressions for regular file and dangling link across schedule, verify, publish, plus absent-directory coverage, "demonstrate failure before fix") and criterion 5 (original RPI, current FULL receipt, independent exact-head assessment, hosted checks) unticked.
* Comment 2026-11-09T20:24 withholds closure: the literal failing-first evidence and the FULL receipt are not replaced by the demonstration-targeted policy.

## Existing durable evidence

| Record | What it durably holds | Limit |
| --- | --- | --- |
| [changes 2026-11-08](../changes/2026-11-08-ranking-archive-path-health-1259-changes.md) "Red before fix (raw)" | Command, 6 tests, 7 failures, the failing assertions, absent-directory controls passing, the earlier wrong-control test error | Prose summary. The raw `red.log` is an external scratch log, not in the repository |
| [recovery changes 2026-11-09](../changes/2026-11-09-ranking-archive-path-health-1259-recovery-changes.md) | Scratch re-run with pre-fix source `6d793bc3a` and the then-HEAD tests: exit 1, 6 tests, 7 failures; current selectors green | Also an external `red.log`. Source then was the pre-Blob child; the current main source and tests are Blob-era |
| [parent-c5 changes 2026-11-09](../changes/2026-11-09-ranking-archive-path-health-1259-parent-c5-changes.md) | Failing-first probes for the Blob listing shapes only (8 failures of 12) | Concerns Blob shapes, not the literal local regular-file or dangling-link cases |

## Exact gap

Regression classes `UnusableArchivePathTests` (regular file, dangling link, dangling ancestor, mocked stat failure, absent-directory and link-to-folder controls) exist on main at `cd687abad` and pass. What is absent from the repository is a durable raw observation (command, exit, source blob, import origin, test output) that those exact main tests fail against the old implementation and pass against the repaired one, with the absent-directory controls passing in both. Existing records are summaries or external logs. No record shows the replay against the old source that main actually had before #1328.

## Candidate old sources and constraints

* Candidate A: `2be660e9d` (main parent of #1328), the real pre-fix main source (`isdir` guard), pre-Blob.
* Candidate B: `6d793bc3a`, the pre-fix 1258 parent used by the original red.
* Current main tests import `ranking_blob_fixture` and Blob-era `test_ranking_publication`; compatibility with old source is unknown and is established only by the replay. If neither old source can load the current tests, that is the recorded limitation and no test is written or adapted.
* An editable install resolves `zava_forward` under `/home/azureuser/source/ama`; the replay must prove module origin from the export instead.
* No existing local record shows execution dated before the fix implementation, so any result is labelled as executed on 2026-11-11.

## Not in scope

Production or private data, models, credentials, Azure, containers, SQL, FULL gate, new issues, knowledge base and the cutover files, acceptance-criterion ticks, closure.
