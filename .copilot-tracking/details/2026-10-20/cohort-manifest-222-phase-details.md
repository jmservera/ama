<!-- markdownlint-disable-file -->
# Phase Details: cohort-manifest-222

Plan: .copilot-tracking/plans/2026-10-20/cohort-manifest-222-plan.md. Evidence: research C1-C13, W1-W4.

## Pinned artifact locations

| Artifact | Path |
| --- | --- |
| Manifest | src/agents/evals/cohort_manifest_draft.json |
| Registry entry | src/agents/evals/registry.json (id cohort-manifest-draft) |
| Structural test | src/agents/tests/test_cohort_manifest_draft.py |
| Review pack | docs/reference/research/evaluation/cohort-evaluation-review-pack.md |
| Index and log | docs/reference/README.md; docs/reference/log.md (append only) |
| Pointer | src/agents/README.md |
| Test ownership | Only test_cohort_manifest_draft.py is added; test_eval_registry.py is unchanged and must pass. Removals: none. Maximum additions: one test module. |
| Generated targets | none |

Placement note: no existing KB page can hold an evaluation protocol (README placement rules), so one new page is created under research/evaluation/ and indexed.

## P01 Manifest, registry and structural test

Evidence: C2, C3, C5-C9. Placement in `evals/` reuses the registry and its test (C3); no new schema package.

* P01-T01 Author manifest. Pairs cover three factor families: sensor/source completeness, accessibility/contact need, appointment history. Include invariance pairs for the deterministic ranking (C7), an expected-difference pair for the support-Unknown candidate (C6), AI-task expectations proposed as to-be-labelled, missingness and insufficient-sample scenarios (small cohort, zero denominator, missing cohort label), a critical-error seed for an open safety case, and a threshold-averaging seed where an aggregate passes while one cohort breaches. Add `acceptance_trace` and `dataset_role` fields; avoid the words oracle, gold and ground truth. Done when FR-1 to FR-5 and FR-9a hold.
* P01-T02 Register in registry.json. Done when FR-6 holds and test_eval_registry passes.
* P01-T03 Add structural test. Semantic coverage is the flag, link and reconciliation checks; no regression duplication. Done when FR-8 holds and the test passes.

## P02 Review pack

Evidence: W2, W3, C10-C13. Sections: status banner; purpose and non-goals; how the manifest is structured; proposed held-out custody and split (custodian separate from prompt authors; manifest IDs only in prompts; expected outcomes withheld until freeze; leakage boundary; agent-authored proposals are not independent labels); independent competent reviewer protocol and adjudication; small-sample and unknown handling; disaggregated critical error handling; review burden and uncertainty reporting plan; AC1-AC6 traceability (all Not met, with what would meet each); owner review checklist; unresolved decisions; adverse and limiting evidence. Done when FR-7 holds.

## P03 Index, log, pointers

Add index row under Research Syntheses and the registry dataset pointer in agents README; append a log entry; do not rewrite earlier entries. Done when FR-9 holds and relative links resolve.

## P04 Validate, record, Review

From src/agents run `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest test_cohort_manifest_draft test_eval_registry -q`; run Ruff on the new test with the repository configuration; the complete gate later discovers the agents tests, a local relative-link check and ASCII check, git diff review. Write the changes record, then run one rpi-review. Done when AC-P1 to AC-P3 hold.

## Critique inputs

Lock: test ownership above, removals none, additions one test module, validation evidence listed in P04.
