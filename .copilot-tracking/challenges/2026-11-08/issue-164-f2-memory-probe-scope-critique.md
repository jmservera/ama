---
title: Issue 164 F2 prospective critique
description: One independent prospective critique of the F2 plan, run before implementation, with dispositions
ms.date: 2026-11-08
---

Execution: Complete (one pass, rubber-duck agent, read-only, 2026-11-08, before any source edit). Verdict: proceed with changes. Original findings preserved verbatim in substance below; none is retracted.

## Findings and dispositions

* CR-001 (Blocker): deriving "no panel memory consumed" from zero true receipts also holds for zero receipts, an unsupported claim. Disposition: accepted. Serving coverage is `not exercised: no panel memory consumed` only when at least one receipt exists and every receipt carries `memory_used` false; zero or incomplete receipts report `unknown: no serving receipts`; any true receipt reports the deviation. Tests cover empty, incomplete and true cases.
* CR-002 (Significant): the gate scope overstated, because the memory-poisoning scenarios also exercise serving prompts and refusals. Disposition: accepted. The label qualifies the isolation memory assertions, not the whole gate or scenario; the gate row carries a count of probes actually executed and a scenario without a probe is tested.
* CR-003 (Significant): failure-path probe accounting. Disposition: accepted. The probe counter lives in a mutable holder created before the try block, so counts from completed turns survive a later exception or a constructor failure; tests cover both.

## Residual

No conflict with a confirmed user decision, no divergent issue needing a user decision. No second critique will run for this task.
