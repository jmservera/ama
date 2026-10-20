<!-- markdownlint-disable-file -->
# RPI Changes: Cohort and missing-data evaluation manifest preparation (#222)

## Metadata

* Task ID: 222
* Related plan: .copilot-tracking/plans/2026-10-20/cohort-manifest-222-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/cohort-manifest-222-phase-details.md
* Implementation date: 2026-10-20

## Execution Status

* Status: Complete for implementation scope P01 to P03 and focused validation; the single Review (P04) follows
* Declared invocation scope: full plan
* Completed scope markers: P01, P02, P03 (P01-T01 to P03 tasks)
* All remaining active-plan markers: P04 (Review execution and local gate, recorded after this record)
* Status basis: all planned files exist, focused tests and lint pass; no evaluator, runtime, model or data work was done

## Execution Summary

Prepared a DRAFT, UNAPPROVED, NOT EXECUTED wholly synthetic manifest registered in
the existing eval registry, an owner review pack with the proposed human
protocol, a structural test, index/log entries and an agents README pointer. No
acceptance criterion is claimed met.

## Completed Work

### Manifest, registry entry and structural test

* Related phase or task: P01-T01, P01-T02, P01-T03
* Files: src/agents/evals/cohort_manifest_draft.json; src/agents/evals/registry.json; src/agents/tests/test_cohort_manifest_draft.py
* What changed and why: 12 scenarios (8 single-factor pairs, 4 sample/aggregation cases) across the three factor families, 6 defect seeds (1 critical, 1 unconfirmed candidate), illustrative reconciliation templates, 3 labelled proposals, AC1 to AC6 trace all Not met. Registered as cohort-manifest-draft. The test checks status literals, registry agreement, forbidden wording, ASCII, pair isolation, seed links, arithmetic and threshold states, proposal labelling and AC status only.
* Completion evidence: files present; all ten critique findings dispositioned in the plan
* Validation: `PYTHONPATH=../core/src:src:../core/tests:tests python3 -m unittest test_cohort_manifest_draft test_eval_registry -q` from src/agents: 14 tests OK; Ruff 0.17.1 check and format on the new test: clean

### Review pack

* Related phase or task: P02
* Files: docs/reference/research/evaluation/cohort-evaluation-review-pack.md
* What changed and why: held-out custody, independent reviewer and adjudication proposals, leakage boundary, small-sample and critical-error handling, review-burden and uncertainty plan, AC traceability, owner checklist, unresolved decisions and retained adverse evidence. New folder justified because no existing KB page can hold an evaluation protocol.
* Completion evidence: frontmatter, no H1, `*` bullets; ASCII scan clean; relative links resolve
* Validation: local ASCII and link scan run and passed

### Index, log and pointers

* Related phase or task: P03
* Files: docs/reference/README.md; docs/reference/log.md; src/agents/README.md
* What changed and why: index row, append-only log entry (earlier entries untouched), agents README pointer stating no harness reads the draft.
* Completion evidence: git diff shows additions only
* Validation: diff reviewed

## Implementation-Time Plan and Detail Updates

### Test invocation path

The details give the install-based command; the checkout had no installed packages, so the equivalent source-path invocation was used locally. The complete gate installs the projects itself.

### Ruff formatting

The first draft of the test failed E501 and format checks; it was auto-formatted with Ruff 0.17.1 (the gate pin) and rechecked.

### Divergences recorded after Review (RV-003)

* Delivered scenario IDs are `CM-S01..`, `CM-A01..`, `CM-H01..`, `CM-C01`, `CM-M01..` and `CM-T01`, not the `CM-P01...` pattern in the plan.
* CM-C01 varies two related completeness fields together by design; its justification says the reviewer may split it.

## Post-Review Disposition (original review preserved unchanged)

The single Review (`.copilot-tracking/reviews/logs/2026-10-20/cohort-manifest-222-review.md`) found no High or Critical issues. No second Review was run.

* RV-005: the review pack's #223 authorisation reference was reworded to name only #108 and a separate owner authorisation.
* RV-001, RV-002, RV-004, RV-006: not changed in this slice; routed to the follow-ups below. RV-002 is already disclosed in the CM-A03 justification.

## Gate-Found Corrections (first gate run, external dir /tmp/ama-222-rpi-20261020-manifest-01, failed receipt retained)

* project-core: the privacy checker requires every public eval payload to be registered; added dataset DS-COHORT-MANIFEST-DRAFT (root_label) to `docs/reference/research/retrofit-synthetic-data/provenance-register.json`. `test_synthetic_provenance` now passes (12 tests).
* project-agents: strict mypy required `-> None` on the six test methods; added.
* browser: Playwright timeout on `#wf-mode`, outside the changed files; to be re-observed on the fresh gate rather than assumed flaky.
* The first gate also needed ignored scratch caches (ruff, pycache) removed from the checkout.

## Follow-Up Items

* Before manifest-dependent execution: bind deterministic expectations to `rank()` and define "same relative rank" (RV-001); add the `ai_eval.py` hazards-exceed-top-k exception to CM-C01 (RV-004); separate contact need from `adjustment` once a field exists (RV-002); strengthen the APPROVED test guard (RV-006).

* Owner review of the checklist in the review pack; per-cohort reporting and fail-closed thresholds only after manifest approval.
* Policy owner decision on candidate defect SD-01 and on approving ranking policy 1.0.0.

## Validation Summary

Focused tests, lint, ASCII and link checks passed. The complete local gate is run after the commit.
