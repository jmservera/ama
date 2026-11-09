---
title: Issue 86 focused-tier author review
description: Author review of the focused-tier execution against the critiqued plan; not an independent assessment
ms.date: 2026-11-08
---

Scope: issue #86 only. Author review, one pass, not independent exact-head assessment.

## Outcome: Findings open

| # | Severity | Finding | Routing |
| --- | --- | --- | --- |
| 1 | Medium | Core `MssqlResidentControls.test_challenge_edited_in_case_outside_generation_candidates` fails on MSSQL (`4 != 40`); unchanged from Main and outside the maintained selectors | Later user-selected work: either fix the fixture to seed through the store or add the class to the maintained selectors; coordinator to decide whether it blocks |
| 2 | Info | Maintained API SQL selectors passed (288 ok, 1 named JSON-only skip) incl. 3 `MssqlUnleasedRevocation` | None |
| 3 | Info | Interrupted FULL remains non-passing; manual SQL run is not a runner receipt | Coordinator |

## Plan criteria

Prospective records committed before execution: met. Critique amendments F1-F5 applied: met (database creation, owned-endpoint check, skip classification, hash-locked install and driver probe). Currency proof: met. Actual SQL feature tests completed for the API selectors; core resident SQL class completed with one failure. Container removed, no prune, no private data.

## Pending

Independent exact-head review of the `e888a499` delta, published `c5edb320` delta and Main-versus-final inherited hunks; hosted checks; human approvals; #1238; later #81 to Main FULL. No tick, closure or publication.
