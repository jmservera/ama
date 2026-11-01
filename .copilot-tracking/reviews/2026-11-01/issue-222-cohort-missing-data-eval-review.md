---
title: Issue 222 cohort and missing-data evaluation review
ms.date: 2026-11-01
---

## Review

Executed once after implementation. Outcome: conformant for the slice; one criterion unmet.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Paired constructed cohorts vs approved manifest | Proven (synthetic) | fixture, `test_clean_run...` |
| All seeded defects detected | Proven | `test_all_seeded_defects...`, `test_undetected...` |
| Counts, errors, review burden, uncertainty reconcile | Proven | `test_per_cohort_counts_reconcile`, `test_reconciliation_failures_block` |
| Small or missing samples insufficient | Proven | `test_small_or_missing_samples...` |
| Exceeded or unapproved thresholds block, not averaged | Proven | `test_threshold_exceeded_is_per_cohort...`, `test_unapproved...` |
| Owner approval before live use (OQ-018) | Unmet | Needs named owner approval of real cohorts, fields and thresholds; synthetic results are not fairness evidence |

## Follow-ups

1. Feed ranking golden-set outputs (#108) and #174 fixtures into `evaluate`.
2. Persist the record and surface it in the release gate.

PR uses Refs, not a closing keyword.

## Post-review corrections

Eight Copilot review findings on PR 636 (threshold validation, missing-observation counting, duplicate IDs, missing outcomes, empty cohorts, rounded comparisons, human rejection, input digests) were valid and fixed; see the changes artifact. The original review outcome is unchanged.

A second round of four Copilot findings (expected-outcome validation, required task and version identifiers, fairness evidence only for measured evaluations, linear duplicate-ID detection) was valid and fixed. The original review outcome is unchanged.

A third round of three Copilot findings (malformed case IDs matching each other, required missing-data treatment, conservative synthetic flag) was valid and fixed. The original review outcome is unchanged.
