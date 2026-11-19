---
title: Issue 107 old-image SQL probe correction critique
description: One independent critique (rubber-duck) of the final correction plan, with dispositions
ms.date: 2026-11-17
---

## Execution

Executed once, read-only, by an independent rubber-duck subagent against the plan, details, research table and the actual code. Verdict: Revise (three major points, no blockers). Not repeated.

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Major | Precedence could classify a violation from missing or untyped evidence, or from a trigger that never happened | Accepted. Each adverse check requires typed present evidence and its own trigger readback (revocation or mutation read back, integer provider counter, boolean result, well-formed pool); otherwise it contributes an INSUFFICIENT reason only. Independent proven violations are still kept. |
| 2 | Major | Worker entries and `provider_calls` are assigned after later operations, so a dispatch followed by a failing readback loses the evidence | Accepted. The worker publishes `tasks`, `executed`, `reinvoked` and `provider_calls` into the output record before the risky operations and updates them in place; errors set `status=error` on the same record. Test: dispatch then failing state query keeps the counter and entry. |
| 3 | Major | A daemon-side create that completes after an empty reconciliation can outlive cleanup | Accepted. A create ended by timeout or OS error is marked ambiguous. Cleanup lists by exact name and labels, waits a bounded settle interval and lists again; an ambiguous resource is always reported as a containment error naming its expected name and labels even when no object is found, so the run cannot exit 0. |

## Amendments

The details file is unchanged; this critique supersedes the three affected items above. No finding conflicts with a confirmed decision.
