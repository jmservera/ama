---
title: Issue 81 missing capacity confirmation plan critique
description: Independent prospective critique of the research, plan and details, with dispositions
author: RPI agent (hve-core-all:rpi-agent); critic rubber-duck (read-only, independent)
ms.date: 2026-11-07
ms.topic: reference
task_slug: issue-81-capacity-unknown
parent_task: issue-81-realign-r2
status: executed once, prospectively, before any source or test change; not repeated
verdict: Revise
---

## Execution

* One independent read-only `rubber-duck` critique over the research, plan and details files, validated against current code. Static assessment only; the critic ran no tests. Verdict Revise. No user decision is required: all findings are compatible with the coordinator's direction.
* The critic confirmed the finding is real and the sole-item rule is sound, the regression fixture construction is feasible, the staff lookup follows the first commitment check, and the API still returns HTTP 400 without exposing the structured gate result.

## Findings and dispositions

| # | Severity | Finding | Evidence cited | Disposition |
| --- | --- | --- | --- | --- |
| 1 | Significant | Planned `unittest discover` over the whole core suite would run the 60,000-case queue benchmark, contrary to the no-queue boundary | details P4 command; `test_queue_benchmark.py:18` | Accepted. Plan Amendment 1 and the details replace discovery with explicit focused modules and exclude queue-scale modules |
| 2 | Significant | Regression assertions did not prove the full contract (state None, exact message, literal status dictionary, persistence) | details P1 steps 3-4 | Accepted. Amendment 1 requires `error.state is None`, exact message, literal status dictionary and a second-reopen snapshot |
| 3 | Significant | Widened callers (Booked appointment record, completion) lack targeted preservation tests and use a separate rollback context | `procurement.py:462-494` | Accepted. Amendment 1 adds refusal and no-mutation tests for both callers in the JSON flow and the existing SQLite-file flow where a fixture exists |

## Outcome

Dispositions are applied in the plan (Amendments) and details. Original findings are preserved verbatim in meaning above. No finding was rejected. The critique is not repeated for this task; implementation, when authorised, records its own review separately.
