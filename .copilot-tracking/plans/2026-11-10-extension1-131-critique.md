---
title: Issue 131 E1 missing households key (critique)
ms.date: 2026-11-10
task_id: 131-extension1-1110
---

## Execution

One final-candidate critique, authored by the implementing worker (not independent). Verdict: Proceed.

## Findings and dispositions

* PC-001: absent versus null must stay distinct, otherwise legitimate Unknown is rejected. Applied: the check is key presence only, and an explicit-null control is in the test.
* PC-002: the view's `latest["households"]` raises KeyError for the latest revision only; with the shared validator the whole history is rejected first, so positional accident disappears. Applied by test (earlier-revision case).
* PC-003: SQLite store must be covered. Applied: the existing mixin runs the tests on the JSON base and the inherited SQLite store; MSSQL is skipped and not claimed.
* PC-004: do not edit the README or the 3 earlier RPI chains; scope stays two files. Applied.
* PC-005: red evidence must come from the unfixed module with the new test only. Applied in Phase 1.
