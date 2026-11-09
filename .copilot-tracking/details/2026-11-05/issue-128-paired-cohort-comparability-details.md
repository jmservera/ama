<!-- markdownlint-disable-file -->
# Details: #128 paired cohort comparability (2026-11-05)

## Design

* `CONTRASTS[dimension]` maps dotted paths to `(reference, subject)` values, fixture-local and predeclared independently of the pair data.
* `_flatten` turns nested mappings into dotted leaf paths; empty mappings stay a leaf so structural changes are visible.
* `_same` compares type and value, so `1` is not `True`.
* `_comparability` diffs reference and subject (excluding `id`, which keeps the existing `pair_ids_differ` check). Outcomes: `None` (valid), `no_contrast` (no difference), `confounded` (declared contrast present plus other changes), `wrong_contrast` (anything else, including partial bundles, wrong values or a mislabeled dimension).
* In `evaluate`, an invalid comparison adds blocker `<pair>:invalid_comparison:<reason>`, an `invalid_pairs` entry, and is not counted in `tested` or `failed`.

## Unchanged

Deterministic ranking path, per-dimension accounting, seeded-defect accounting, input immutability, `activation_allowed=False`, `fairness_evidence=False`.
