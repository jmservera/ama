---
title: Issue 440 post-1500 plan critique (0240)
description: Independent one-pass critique of the post-1500 provenance annex plan, with dispositions
ms.date: 2026-11-13
ms.topic: reference
---

## Execution

Executed once by an independent rubber-duck subagent (fresh context, read-only, no file edits, no test runs) against the research, plan and details. Verdict: Revise, four Medium findings, no High. No second critique is run. Planner-owned corrections were compatible and applied directly; none conflicted with a confirmed decision and none required a user decision.

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| CR-1 | Medium | Details cited scorer run `43351173644` as the post-merge push scorer; it is a pull_request run at head `4961`. | Applied. Details and research now identify it as a pull_request run with unverified checkout, and require the actual push run id to be queried (`gh run list --commit`) or stated as not yet observed. |
| CR-2 | Medium | The 19 contexts could be read as all verified on the merge-ref tree; only Source CI checkout identity was verified. | Applied. Research, details and the allowed-claims list separate Source CI merge-ref checkout evidence from PR rollup successes of Scorer and status contexts. |
| CR-3 | Medium | Input-equivalence claim overreached: C4 changed an API test that Ruff covers, so the earlier types lane is not equivalent. | Applied. Plan and research limit equivalence to lanes whose own named inputs are unchanged and attribute final API lint, format and type status to the fresh canonical C4 check. |
| CR-4 | Medium | Counts-only re-read cannot support named test outcomes. | Applied. P1 now requires re-reading the specific named `ok` and `skipped` lines and the checkout line, and omitting any named claim that cannot be re-read. |

## Not verified by the critique

All 72 individual hosted core outcomes, the original C4 phase files and a post-merge push scorer run. These stay explicit limits; the implementation stage must re-read only the named lines it cites.

## Preserved

The recommendation (docs-only annex, no fresh observation) stood after critique. Original critique and dispositions are not to be replaced retrospectively.
