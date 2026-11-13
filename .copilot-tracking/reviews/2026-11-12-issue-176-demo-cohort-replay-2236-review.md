---
title: Review, issue 176 five-home demo cohort replay regression
ms.date: 2026-11-12
---

* Execution: executed once, independent code-review agent, read-only, on the uncommitted diff. Outcome: Pass for the slice; #176 not complete.
* Findings: none blocking. Minor: the negative-control `.replace` strings in the parser test depend on exact runbook row text and fail loudly if reworded. The as-of 2026-12-01 observation is recorded in the [changes record](../changes/2026-11-12-issue-176-demo-cohort-replay-2236-changes.md); the reviewer did not read tracking files.
* Unmet acceptance criteria: criteria 1 and 2 stay unmet and unticked (original private register generator, untouched historical manifests). Criterion 3 unchanged.
* Routed follow-up: owner supplies or retires the original register generator and inputs. Optional later work: a check that the simulator control cohort file lists exactly these five ids (needs a separate source decision), and archetype codes if the seed ever records them.
* Use Refs #176, not Closes. No human approval, deployment or live acceptance is implied.
