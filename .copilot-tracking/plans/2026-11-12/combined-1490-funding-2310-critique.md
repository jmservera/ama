---
title: Issue 82 combined 1490 candidate critique
ms.date: 2026-11-12
task_id: combined-1490-funding-2310
---

## Execution

One independent read-only critique (rubber-duck agent) of the final candidate plan, run once before the RV01 cherry-picks. Verdict: needs changes; all findings compatible, applied directly. No second critique for this task.

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-01 | High | The plan deferred every Review finding, which could defer a gate regression. | Applied: the plan now stops on any material finding (gate weakening, regression, lost evidence) and defers only explicitly non-blocking findings. |
| PC-02 | Medium | Failing-first reproduction on the already-fixed head is meaningless. | Applied: reproduce in an isolated temporary worktree at the combined head with only the four reader source files (three readers and `taskqueues.py` revision) restored to their pre-RV01 content, record the expected failures, then run the fixed candidate; run the revision negative control separately and verify restoration. |
| PC-03 | Medium | No explicit failure stops or installed-package origin checks. | Applied: enumerate focused tests, verify imports resolve to the candidate worktree, record exit codes and skips, and stop on any unexpected failure. |

Reviewer confirmations: HEAD keeps both complete independent test_mvp methods; `advance` checks the stage before `gate_reasons`; RV01 source paths do not overlap the intervening 153 and 82 changes; no gate weakening identified in the proposed reader changes.
