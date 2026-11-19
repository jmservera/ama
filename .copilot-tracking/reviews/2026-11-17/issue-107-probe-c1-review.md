---
title: Issue 107 probe correction review
description: Single correction Review of the execution-readiness fixes to the older-image SQL probe
ms.date: 2026-11-17
---

## Execution

* Review executed once after implementation, by a read-only `code-review` agent over the unstaged diff (probe, worker, README; the agent did not read the test file or README) plus the implementer's own self-review below. No Docker, SQL or full gate was run.
* The original implementer Review of db7ad278 and the independent execution-readiness findings (`evidence-107-c1/execution-readiness.json`, `functional-findings.json`) are unchanged and remain the adverse record for the opening candidate.

## Outcome

Conformant for the bounded correction within this runtime. NOT publishable: the actual old-image and disposable-SQL execution, the full gate receipt, independent exact-head assessment and hosted CI are missing.

## Independent agent result

No high-confidence defect in any of the eight corrections. One non-defect observation: a readiness login blocked past its 60 s bound ends the run as INSUFFICIENT instead of retrying (fails early, cannot pass wrongly or leak).

## Implementer self-review

| Finding | Result | Evidence |
| --- | --- | --- |
| 1 private network | Corrected; real attachment is unproved until an actual run (internal-network port publication assumption, `Created` container network listing) | `worker_create_args`, `Docker.attachments`, argv test |
| 2 complete protocol | Corrected | `PROTOCOL`, `check_step`, 14 mutation cases |
| 3 SPID reuse | Corrected | reused-SPID test |
| 4 adverse precedence | Corrected; worker partial record is covered only by the SQLite self-test | scenario and judge tests |
| 5 cleanup lifecycle | Corrected | fake-daemon lifecycle tests |
| 6 token ceilings | Corrected | pool tests |
| 7 deadlines | Corrected; a native-blocked call is abandoned, not killed | bounds tests |
| 8 output path | Corrected | symlink and traversal test |

## Residual items routed to later work

* Actual Docker/MSSQL run under the shared heavy lock (the holder must be checked live; the #1837 hold is historical).
* Assumptions an actual run must confirm: internal network plus bridge attachment of the SQL container, `hostname == container id[:12]` for the worker, and the `Created` container network listing.
* Full tier gate receipt, independent exact-head review and hosted CI.
* One worker edit and two later probe edits were applied with Python scripts rather than the edit tool (same content as the diff).
