<!-- markdownlint-disable-file -->
# Review: #128 paired cohort comparability (2026-11-05)

Execution: executed once, by an independent `code-review` agent on the uncommitted diff (reading only; it ran no commands). Outcome recorded as originally returned.

## Original verdict: NOT CLEAN (2 Medium)

1. Medium, `paired_equity.py` `_comparability`: Python `==` equates `False`/`0` and `True`/`1`, so a pair with `priority_support=1` satisfied the `(False, True)` contrast.
2. Medium (low likelihood), `_flatten`: an empty nested mapping produced no leaf, so adding or removing `{}` was an invisible confound.

No accounting regressions found (tested/failed counts, `invalid_pairs`, blockers, ranking path, `activation_allowed=False`, `fairness_evidence=False`, immutability).

## Disposition

Both findings are tightly coupled to this change and were fixed before freeze (`_same` type-aware comparison; empty mapping kept as a leaf) with test `test_type_coerced_values_and_empty_nested_change_are_rejected_...`. Per the one-pass rule no second Review ran; the fix is verified by tests, Ruff and mypy, not re-reviewed. The original NOT CLEAN verdict is not converted to a conformant verdict.

## Routed, not closed

Actual-model run, independent expected-pair and threshold approval (OQ-018), keyboard and screen-reader testing, user research, lawful-field decision, named human acceptance, hosted CI and human approval. Partial issue acceptance only: the comparability-validation criterion for the existing constructed fixtures. #128 and #123 are not closed or approved. No population fairness or activation claim.

## Correction 2 review evidence (2026-11-05, appended)

The original NOT CLEAN verdict above stands unchanged. The two earlier fixes (type-aware equality, empty mapping) were never independently re-reviewed, and this correction did not review them either. The coordinator's adverse findings (nested type masking, dotted-key shadowing) are recorded in the changes artifact and fixed with tests. No review approval is claimed; the independent exact-head assessment remains coordinator-owned. Self-check by tests only.
