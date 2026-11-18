---
title: Cohort and Missing-Data Evaluation on the Synthetic Demo (issue 222)
description: Per-criterion proven and unproven record for issue 222 on the synthetic desktop demo, with the offline test run and the OQ-018 approval boundary
ms.date: 2026-11-18
ms.topic: reference
---

Refs #222. Scope: synthetic desktop demo under the owner decisions of 2026-11-18. The evaluation is offline and deterministic; no Azure, browser or live-data action was needed or taken. Synthetic results here are not fairness evidence.

## Evidence run

Head `e01b3d2152513f7a4a918e77e95c7e85b337423f`, from `src/agents`:

```bash
PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest \
  tests.test_cohort_ranking_eval tests.test_cohort_ai_eval tests.test_cohort_manifest_draft
```

Result: `Ran 36 tests in 2.329s`, `OK`. The evaluation output prints seven blockers: six `insufficient_sample` lines (for example `support_need/declared: n=6 below minimum sample`, `source_completeness/partial: n=6`, `appointment_history/missed: n=6`) and one `unapproved_thresholds` line stating that cohorts, lawful fields or thresholds lack named owner approval bound to the manifest digest (OQ-018). The run ends with the line `OQ-018: ... synthetic results are not fairness evidence.`

## Per-criterion status

| Criterion | Issue state | Demo status | Evidence |
| --- | --- | --- | --- |
| Paired cohorts evaluated against an approved expected-outcome manifest | ticked | Regression re-run passes | 36 tests above; manifest is a draft, so "approved" rests on the existing ticked review |
| Seeded unjustified exclusion or deprioritisation defects detected | ticked | Regression re-run passes | `test_cohort_ranking_eval`, `test_cohort_ai_eval` |
| Per-cohort counts, errors, review burden and uncertainty reconcile | ticked | Regression re-run passes | same modules |
| Small or missing samples remain insufficient | ticked | Observed in output | six `insufficient_sample` blockers |
| Exceeded or unapproved thresholds block activation | ticked | Observed in output | `unapproved_thresholds` blocker |
| Cohorts, lawful analysis fields and thresholds owner approved before live use (OQ-018) | unticked | UNPROVEN, deferred | see below |

## Why the last criterion cannot be proven for the demo

OQ-018 asks Data and Performance, Resident Engagement, the DPO and competent task owners to approve representative cohorts, lawful fairness-analysis fields, sample sufficiency and thresholds. That is a named-human approval for live use. The 2026-11-18 owner decisions exclude DPO and Legal approval for the demo and keep production use deferred to #1905 (legal) and #1906 (DPO). The criterion also says synthetic results are not fairness evidence, so no run can satisfy it. The gate correctly keeps the `unapproved_thresholds` blocker in force, which is the intended demo behaviour. The issue stays open with this one criterion; do not close it.

## Evidence limits

* An independent re-run reported nine blocker lines (eight `insufficient_sample` and one `unapproved_thresholds`), not the seven stated above; the 36 passing tests reproduce exactly.
* The head named in this note is the branch base, not the candidate head.
* Test output was not retained as a file. The OQ-018 owner approval stays unproven.
