---
title: Issue 133 aftercare criteria plan critique
task_id: 133-aftercare-criteria-2035
date: 2026-11-13
---

Execution: one independent rubber-duck pass over the plan, details, research and working diff. Verdict: proceed with changes.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Guard missed "The retrofit made the home colder" and "Your bills will be cheaper" | Applied: patterns added with tests |
| 2 | Baseline reported unknown when the full comparison is insufficient | Rejected: intentional, tested design (`test_insufficient_or_missing_comparison_is_unknown_without_partial_means`); coverage is stated separately. Recorded as a follow-up if the owner wants partial baselines |
| 3 | Neutral caveat "No claim of ... lower energy bills" rejected | Applied: narrow negated-claim exemption that ends at a comma or conjunction; "No claim of savings, but you could save money" still rejected |

No significant or divergent issue needed a user decision. Critique is not repeated.
