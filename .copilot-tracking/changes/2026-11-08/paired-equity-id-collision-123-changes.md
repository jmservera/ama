<!-- markdownlint-disable-file -->
# Changes: paired-equity anchor ID collision correction, 2026-11-08

Plan: [plan](../../plans/2026-11-08/paired-equity-id-collision-123-plan.md). Research: [research](../../research/2026-11-08/paired-equity-id-collision-123-research.md). Critique: [critique](../../plans/2026-11-08/paired-equity-id-collision-123-critique.md). Refs #123, #440, #128.

## Order

* `b28d4a24d6d6e1d20384dd2798fb970f054a1f86`: planning commit (Research, Plan, details, critique, state) before any source edit.
* Then tests added, run red against the unmodified module, fix applied, green and static checks run. Implementation and these records are committed together afterwards; their identity is in the handoff.

## Red run (before the fix)

* Command: `cd src/core && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD/src:$PWD/tests /tmp/ci764b-venv/bin/python -m unittest test_paired_equity`. Import asserted to `src/core/src/zava_forward/core/paired_equity.py`. Output kept at `/tmp/collision-red-0811.txt`.
* Exit 1; `Ran 23 tests`, `FAILED (failures=5, errors=1)`.
* The finding's exact example reproduced: `ANCHORS + [case("p1")]` with `penalise_missing` and also with the default `ranking.rank` returned `status` `pass` (`AssertionError: 'pass' != 'blocked'`). This is an executed reproduction, not a static assertion.
* A pair whose reference and subject both lack an `id` raised an unstructured `KeyError`; empty and non-string equal IDs also did not block.
* Existing 16 tests plus the distinct-ID positive control, differing-ID and confounded-collision tests were unaffected.

## Source changes

* `src/core/src/zava_forward/core/paired_equity.py`: new `_identity_problem` (14 lines changed). Only when reference and subject IDs are equal it returns `missing_case_id` (absent, empty or non-string) or `anchor_id_collision`. `evaluate` uses `_comparability(...) or _identity_problem(...)`, so the existing structured path applies: blocker `<pid>:invalid_comparison:<reason>`, `invalid_pairs` entry, not counted as tested. `_comparability` keeps precedence. Differing-ID pairs keep `pair_ids_differ`. Ranking, contrasts, joint support bundle, flags unchanged.
* `src/core/tests/test_paired_equity.py`: 7 new tests (collision with two rankers, several anchors with a seeded defect, missing/empty/non-string IDs, confounded precedence, differing-ID retention, distinct-ID positive control).
* `src/core/README.md`: one sentence naming the new invalid-pair reasons.

## Green and static checks (current source, light)

* Focused: `test_paired_equity` 23 tests OK, exit 0.
* Coupled selection (paired equity, journey, cohort, RAI release and invalidation, ranking publication and runner): 177 tests OK, exit 0, no skips.
* Core Ruff check passed. The first Ruff run flagged one E501 line and `ruff format --check` flagged the test file; I applied `ruff format` to the two files, then check passed, format check 215 files, mypy 268 source files, all exit 0 (Ruff 0.17.1, mypy 2.4.0). `git diff --check` exit 0.

## Not changed

* `ranking.py`, store, publisher, runner, API, auth, policies, thresholds, fixtures. `fairness_evidence=False`, `activation_allowed=False`. The joint support/contact bundle concern is historical, unconfirmed, not fixed or downgraded. f14 receipt and the independent 3c31 assessment are preserved. The f14 receipt does not cover this candidate.

## Pending at commit time

* Fresh selected-tier gate (`--changed --jobs 2 --lock-timeout 0`), partial receipt verification, independent exact-head assessment, hosted checks.
