---
title: Issue 1292 before-fix paired validation review
description: Author Review of the evidence-only paired validation; not an independent exact-head review
ms.date: 2026-11-11
---

## Review execution and outcome

One post-implementation Review, authored by the executing agent. It is not independent exact-head review. Outcome: conformant for the bounded scope, with the open items below routed to later work.

## Findings

| Id | Severity | Finding | Routing |
| --- | --- | --- | --- |
| R1 | Info | The prospective records were committed (`0ba32c2c2`) before SQL started; one critique was executed and applied | none |
| R2 | Info | The original arm reproduced the wrong-newest recommendation on real SQL Server in 4 of 5 methods; the current arm passed 14 of 14 with 0 skips | none |
| R3 | Medium | The red covers 4 selected methods, not the whole module against the old source, and one method failed before its incremental step | coordinator decides whether AC3 is met |
| R4 | Medium | The legacy-row transition heuristic still needs a named data-owner decision (AC2) | existing owner |
| R5 | Medium | Independent exact-head review, hosted CI and human approval of this candidate remain outstanding | coordinator |
| R6 | Low | Timeout bound is the outer bound only; image identity is local id only | stated limits |

## Not claimed

Source E5 or a fix, the startup cause, whole #1292, #81 or #440 acceptance, a full gate, Azure, live, human or approval evidence, and no criterion was ticked.
