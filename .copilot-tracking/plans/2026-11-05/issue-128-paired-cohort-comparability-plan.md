<!-- markdownlint-disable-file -->
# Plan: #128 paired cohort comparability (2026-11-05)

Details: [phase details](../../details/2026-11-05/issue-128-paired-cohort-comparability-details.md). Research: [research](../../research/2026-11-05/issue-128-paired-cohort-comparability-research.md).

Validation tier: FOCUSED (pure constructed diagnostic; no SQL, security, infrastructure or deployment change).

## Phases

* [x] Phase 1: Red regressions and failing reproduction in `test_paired_equity.py`.
* [x] Phase 2: Add `CONTRASTS` and `_comparability` to `paired_equity.py`; route invalid pairs to blockers and `invalid_pairs`, not `tested`.
* [x] Phase 3: Update the existing `src/core/README.md` paragraph.
* [x] Phase 4: Focused validation: affected core tests, Ruff check/format, mypy including tests.
* [x] Phase 5: Single Review, commit with evidence, final checks on frozen HEAD.

## Critique (single pass, direct dispositions)

* Reuse of `ranking`, `journey_register`, `digest` unchanged; no new module, config or framework (accepted).
* Counting an invalid pair as failed would hide it in the dimension; instead it is an explicit invalid outcome and the dimension reports `no_pairs` if no valid pair remains (accepted, matches existing `invalid_pair` handling).
* Support bundle must be both fields together; a partial bundle is `wrong_contrast` rather than a new approved alternative (accepted).
* Seeded-defect accounting unchanged: an invalid pair is not a detected defect.
