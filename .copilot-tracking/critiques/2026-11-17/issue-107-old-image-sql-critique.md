---
title: Issue 107 old-image SQL plan critique
description: Single independent critique of the final-candidate plan, with direct dispositions
ms.date: 2026-11-17
---

## Execution

Executed once by an independent rubber-duck agent (read-only) against the plan, details and research. Verdict: Revise. No confirmed user decision conflicts with any finding; all six are applied directly in the details (amendments section) and are not re-critiqued.

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | C1 to C3 could pass with zero calls for unrelated reasons (`execute` returns False for non-pending tasks) | Accepted. Every negative case needs SQL-verified preconditions (pending distinct task, active release before mutation), mutation readback, task identity and an intended gate outcome (release non-active and invoke state disabled); otherwise INSUFFICIENT. |
| 2 | Blocking | Allowance not tested after revocation or material mutation; larger restart config not compared | Accepted. Consume allowance first, then mutate, then restart and try a distinct otherwise-authorised task; compare ceiling and consumption before and after, including a larger restart config. The #1271 clamp for partially used claims is not duplicated. |
| 3 | Blocking | Image ID does not prove which modules were imported; script dir could shadow packages | Accepted. Mount only the worker in an isolated directory, run `python -I -B` with `PYTHONPATH` unset, report each loaded module path and SHA-256 in every action; host requires site-packages paths and equal hashes across actions. |
| 4 | Blocking | `sqlguard` checks env only, not Docker's persisted context | Accepted. Probe reads `docker context show` and the context endpoint with fixed argv and refuses unless default and a local unix socket, before any Docker mutation. |
| 5 | Blocking | Cleanup by generated name could remove an unowned container | Accepted. Remove only container IDs captured from this run's own creation after the run label is verified; a name collision aborts before creation. |
| 6 | Non-blocking | Raw errors may disclose credentials | Accepted. Redact every generated secret from all printed and persisted output; tested with driver-error and timeout text. |

## Outcome

Plan revised once; proceeding to implementation.
