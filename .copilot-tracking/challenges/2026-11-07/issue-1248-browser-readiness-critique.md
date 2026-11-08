---
title: Issue 1248 saved-call History browser readiness critique
description: Single prospective critique of the issue 1248 plan and details
ms.date: 2026-11-07
ms.topic: reference
---

## Execution

* Critique executed once on the prospective plan and details. Verdict: proceed with amendments applied below. Not repeated for this task.

## Findings and Dispositions

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | The root cause is a hypothesis; a repair before the held-read observation would be speculative. | High | Applied: Phase 2 cause gate precedes any repair; H2 stops the test-only scope. |
| 2 | The old condition must demonstrably fail under delay; "fails under old condition" cannot rest on reasoning alone. | High | Applied: the held read records the old one-shot observation before release. |
| 3 | Reproducing in-check via the existing held-route idiom keeps scope small, but a pass under hold does not reproduce R4's natural timing. | Medium | Accepted: R4 is recorded as bounded "not reproduced" unless it recurs; controlled proof covers the mechanism. |
| 4 | Waiting on workspace detach is a signal of completed refresh, not of content; it alone could still pass an absent call. | Medium | Applied: detach wait is paired with the web-first exact-text expectation. |
| 5 | Tab selection persistence across the swap is unknown. | Low | Applied: History is selected after detach. |
| 6 | Reading hidden-panel text may differ by method. | Low | Recorded as a Phase 1 verification item with `text_content()`. |
| 7 | Browser execution contends for the shared heavy lock. | Low | Applied: execution only at separate admission under the sole non-queued lock. |
| 8 | Scope could drift into application changes. | Medium | Applied: application repair is routed to separate scope. |

## Conflicts With Confirmed Decisions

* None. No retry, sleep, blanket timeout, skip or weaker assertion was advised.
