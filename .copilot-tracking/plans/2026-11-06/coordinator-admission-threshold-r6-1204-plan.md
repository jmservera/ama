---
title: Plan, open-PR admission threshold correction r6 (issue 1204)
ms.date: 2026-11-06
---

## Objective

Smallest correction of the coordinator instruction so that more than 20 open PRs triggers a drain that lasts until 10 to 15 remain, with no unconditional 16-20 ban; directly coupled new fixtures; independent static review; contained behavior validation; author Review.

## Checklist

* [x] P1 Verify identity, read target, current main, finding.
* [ ] P2 Details, one independent critique applied; commit planning before any edit.
* [ ] P3 Edit target (one passage). Record new blob.
* [ ] P4 Independent static assessment of the diff (generic subagent, harness default).
* [ ] P5 Sandbox 010: independent designer, read-only executor, independent grader, harness defaults.
* [ ] P6 Report 011, changes, state; commit.
* [ ] P7 Author Review; commit and freeze.
* [ ] P8 One native FOCUSED gate at final HEAD with fresh base; verify receipt externally.

Details: .copilot-tracking/details/2026-11-06/coordinator-admission-threshold-r6-1204-details.md

## Follow-Up Items

* Coordinator independent exact-head assessment, hosted CI, human review and merge remain outside this work.
