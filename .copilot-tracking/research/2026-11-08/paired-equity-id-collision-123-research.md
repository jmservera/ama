<!-- markdownlint-disable-file -->
# Research: paired-equity anchor ID collision correction (#128, Refs #123 #440), 2026-11-08

Prospective, written before any production edit. Correction cycle 1 for the new independent functional finding on `3c31fa9d`. The earlier records, the f14 receipt and the independent assessment are unchanged.

## Evidence (read-only)

* Starting HEAD `3c31fa9dba5ac4247c693fb346acc81918a571f5`, tree `8f0e4aff1a5d76ec94f485abc9bee9277930a736`, ignored-inclusive clean; `origin/main` `f548b65f`.
* Finding (Medium, high confidence by static inspection, not executed): `paired_equity._position` ranks `[*anchors, case]` and picks the first entry whose `id` equals `case["id"]`. An anchor sharing the pair's case ID can be selected instead of the tested case.
* Proposed example: add `case("p1")` to `ANCHORS`, use the test file's `penalise_missing` ranker. The anchor stays rank 1 in both runs, so the sensor pair may pass although the declined-sensor subject is lowered (rank 5 vs reference rank 2).

## Contracts read

* `evaluate(pairs, anchors, seeded_defects, rank)`: each pair is `{id, dimension, reference, subject}`. `_check_pair` compares positions only when reference and subject IDs are equal; differing IDs yield failure `pair_ids_differ` (existing, tested).
* Existing invalid-comparison prior art: `_comparability` returns a reason (`no_contrast`, `confounded`, `wrong_contrast`); `evaluate` appends blocker `<pid>:invalid_comparison:<why>`, adds `{pair, dimension, reason}` to `invalid_pairs`, and does not count the pair as tested. Pair-shape problems use `<pid>:invalid_pair`.
* A rankers' output carries `id` and `rank`; the default is `ranking.rank`. `ranking.py` is out of scope and unchanged.
* A pair whose reference and subject both lack an `id` currently reaches `_position` and raises `KeyError`, an unstructured failure; this is directly coupled to the same ID contract.

## Reproduction obligation

Add a focused regression with the finding's exact example and run it red against the unmodified code, preserving command, exit and output. If it does not reproduce, make no production edit and return the evidence.

## Intended minimal fix (if reproduced)

* New helper `_identity_problem(pair, anchors)` evaluated only when reference and subject IDs are equal (the case that is ranked). Reasons: `missing_case_id` (absent or non-string or empty ID) and `anchor_id_collision` (ID equals any anchor ID).
* Reuse the existing structured path: blocker `<pid>:invalid_comparison:<reason>`, an `invalid_pairs` entry, not counted as tested, no pass. No silent fallback, no change to ranking, thresholds, contrasts, joint support bundle, `fairness_evidence=False` or `activation_allowed=False`.
* Differing-ID pairs keep their existing `pair_ids_differ` failure (not reclassified).

## Tier

FOCUSED: bounded constructed metric tooling and test correction. No SQL, security, auth, infrastructure, deployment, ranking, store, publisher or API change. Reassess if scope grows; stop for coordinator disposition.

## Separate

* The old joint-support/contact bundle concern is historical and unconfirmed; this correction neither fixes nor downgrades it.
* New source or tracking changes invalidate the f14 receipt for the resulting candidate; a fresh gate follows the commit.

Planning readiness: Ready. Research disposition: executed.
