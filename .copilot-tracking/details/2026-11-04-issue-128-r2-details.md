# Details: issue 128 R2

* `evaluate(pairs, anchors, seeded_defects, rank)`: per pair, subject rank position in an anchor pool must not exceed reference position; `human_review_route(subject).rank_effect` must be `none`; ids must match.
* Blockers: `{dim}:no_pairs`, `{dim}:unjustified_deprioritisation`, `{id}:invalid_pair`, `{id}:seeded_defect_undetected`.
* Tests: tests/test_paired_equity.py (8).
