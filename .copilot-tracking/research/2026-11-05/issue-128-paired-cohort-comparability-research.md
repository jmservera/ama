<!-- markdownlint-disable-file -->
# Research: #128 paired cohort comparability (2026-11-05)

Task slug `issue-128-paired-cohort-comparability`. Research disposition: executed (bounded, source-level). Planning Readiness: Ready.

## Scope and provenance

* Worktree `/home/azureuser/source/ama-wt/issue-128-comparability`, branch `fix/paired-cohort-comparability-128`, base `3d7ad2fe`. Declared target `feat/discovery-assurance-integration-123` (parent #123), a local topic at the same base. No push, PR or merge.
* Read: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md` (context only), `src/core/README.md` paired_equity section, `src/core/src/zava_forward/core/paired_equity.py`, `src/core/tests/test_paired_equity.py`, `journey_register.human_review_route`.
* Process deviation (disclosed): the backlog manager wrote a tracking brief in the primary dirty main checkout. It was not moved, deleted or staged; only the bounded evidence in the task statement was consumed. These artifacts are original to this worktree.

## Findings

* Source blob `paired_equity.py` is `d29768d5e603db7703410bf7f8a2625638bd4784`, matching the confirmed reproduction.
* `_check_pair` only checks id equality, rank position and review-route rank effect. Nothing checks that exactly the declared attribute differs. The docstring states the invariant but code does not enforce it.
* Red reproduction (adverse evidence, preserved): existing `pairs()`, `pairs[0]["subject"]["days_in_stage"]=30`, `evaluate(pairs, ANCHORS)` returned `status=pass, tested=3, failed=0, blockers=[], activation_allowed=False`. A confounded comparison was admitted.
* Existing fixture contrasts: `sensor_data` present to declined; `resident.priority_support` False to True together with `resident.adjustment` `"None"` (string in the fixture) to `"Large print"`; `appointment_history` confirmed to `prior_no_access`.
* Environment finding: the shared editable installs point at the primary checkout (`/home/azureuser/source/ama/src/core`), so tests in this worktree would silently import primary source. An external venv (`/tmp/rpi128-venv`, system site packages, `pip install --no-deps -e src/core`) was used; no shared environment change, no `PYTHONPATH`.

## Constraints and unresolved gaps (not closed by this work)

* Fixture-local contrast only; not a production field mapping or approved policy. No inference of protected characteristics. No alternatives, directions, partial bundles or equivalence exceptions invented; ambiguous new semantics would need a named decision.
* Open and preserved: actual-model run, independent expected-pair and threshold approval (OQ-018), keyboard and screen-reader testing, user research, lawful-field decision, named human acceptance. No population fairness or activation claim.

## Planning Readiness

Ready. Smallest change: predeclared per-dimension contrast table plus a comparability check that rejects confounded, no-contrast and mislabeled pairs before they count as tested.
