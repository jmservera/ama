---
title: Inventory and staff intake current-main checkpoint plan critique (Refs 440, 131, 132, 1362)
ms.date: 2026-11-11
task_id: 440-inventory-intake-main-1111
---

## Execution

One independent read-only critique pass by a `rubber-duck` subagent over the research, plan and details, at 2026-11-11 about 00:16Z to 00:17Z (actual clock), before any observation. It was asked to verify claims against the repository. It is not repeated for this task. Verdict: revise (five findings, all compatible with confirmed owner decisions; no user decision required).

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Core selectors O1 and O2 lack `PYTHONPATH=tests`; the module imports `dataset` and `sqlguard` from the Core tests directory | Applied directly: `PYTHONPATH=tests` added to O1 and O2 in the details |
| 2 | Blocking | O5 and O6 commands were incomplete (`...`) and Playwright, imported by O6a, was not handled | Applied directly: complete commands written; Playwright is a declared dev dependency restored only after an actual import failure, otherwise the affected check is blocked |
| 3 | Non-blocking | Research claimed the return path calls the resident guard; `return_quality` does not | Applied directly: research now says `accept_quality` and `hand_over_quality` are guarded, `reinspect_quality` passes through accept, return is not guarded |
| 4 | Non-blocking | Trace omitted PRD FR-015 (hazard) as a separate row | Applied directly: a separate hazard row, explicitly not satisfied by the household hold |
| 5 | Non-blocking | Presence claim for the inventory-managed predicate was too broad | Applied directly: exact predicate at `resident_decisions.py:249` recorded; an empty `tenure_reports` list or false `tenure_review_required` alone does not opt in |

## Residual

No finding conflicts with a confirmed decision. The critique did not question the no-new-test boundary, the Focused tier, or the combined-journey gap statement. This critique is an author-commissioned plan check and not an independent assessment of the final record.
