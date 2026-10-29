<!-- markdownlint-disable-file -->
# Review: Cohort and missing-data evaluation manifest preparation (#222)

## Scope and Evidence

* Task ID: 222
* Review date: 2026-10-20
* Review scope: full task (P01 to P03 implementation; P04 validation and Review)
* Assessed boundary: preparation-only slice; uncommitted worktree versus base 993a7b88 (HEAD equals base); no evaluator, runtime, model, participant, live data or threshold approval; no acceptance criterion ticked
* Plan: .copilot-tracking/plans/2026-10-20/cohort-manifest-222-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/cohort-manifest-222-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-10-20/cohort-manifest-222-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-20/cohort-manifest-222-changes.md
* Other evidence considered: research record; ranking.py, stock.py, policies/ranking-v1.json, ai_eval.py; docs and README diffs; re-run tests and Ruff

## Opening Review State

* Interpreted review goal: adversarially verify claims, arithmetic, non-overclaiming, leakage and approval-inference risk, scope and traceability
* Evidence readiness: all artifacts present; local gate not yet run (outside this Review)
* Acceptance basis: plan AC-P1 to AC-P3 and owner decision for #222
* Active read-only boundaries: this record only

## Execution Status

* Execution status: Complete
* Review execution evidence: unittest `test_cohort_manifest_draft test_eval_registry` 14 tests OK; Ruff check passed; Ruff format check clean; ASCII scan of manifest, pack and added diff lines clean; index, PRD and addendum anchors resolve; the complete local gate was not run or assessed here

## Outcome

* Outcome: Defects found (no High or Critical; two Medium, four Low). Preparation boundary is honoured and no approval or fairness overclaim was found.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 | Manifest, registry, test | Reconciled with gaps | Plan FR-2 says IDs `CM-P01...` and a single varied factor; delivered IDs are `CM-S/A/H/C/M/T` and CM-C01 varies two fields. Not recorded as an implementation-time update (RV-003) |
| P02 | Review pack | Reconciled | Content matches phase details; custody wording differs slightly but is sound |
| P03 | Index, log, README | Reconciled | Additions only; log appended |
| P04 | Pending | Partial | Local gate and receipt (AC-P3) outstanding by design |
| Follow-Up Items | Listed in both | Reconciled | None |

## Completed Work Assessment

| Marker | Files | Assessment |
| --- | --- | --- |
| P01 | src/agents/evals/cohort_manifest_draft.json; src/agents/evals/registry.json; src/agents/tests/test_cohort_manifest_draft.py | Counts verified: 12 scenarios (8 pairs, 4 aggregate), 6 seeds. Arithmetic verified: RC-T01 pooled 8/90 = 8.9% under 0.10, ARM-B 6/30 = 20% breach, ARM-A 2/60; RC-M03 ARM-A 1/40; identities hold. Status literals, `fairness_evidence` false, held-out NOT CREATED, unlabelled AI expectations, all AC Not met |
| P02 | docs/reference/research/evaluation/cohort-evaluation-review-pack.md | Frontmatter, no H1, `*` bullets, ASCII. Adverse evidence retained. Protocol sound (custodian, two blind reviewers, adjudicator, leak retirement, no participants) |
| P03 | docs/reference/README.md; docs/reference/log.md; src/agents/README.md | Index row and append-only log present; README says no harness reads the draft |

Code claims checked: ranking.py reads only hazard, support (`support_status == "Yes"`), days, stage, id (verified); `support_status` returns Unknown for missing or non-None adjustment cases while only Yes sorts first, so Unknown ties with No, and `reasons` adds `support_unknown` (verified); policy 1.0.0 status text and owner "to be named" (verified); PR-03 mirrors ai_eval.py zero critical misses (verified).

## Implementation-Time Plan and Detail Update Assessment

| Area | Assessment |
| --- | --- |
| Test invocation path, Ruff format | Disclosed and reasonable; reconciled |
| ID scheme and multi-field pair divergence | Not disclosed (RV-003) |

## Critique and Material Revision Assessment

* Latest critique: Revise (3 High, 5 Medium, 2 Low), all ten dispositioned Applied; spot checks confirm PC-001 (dataset_role, banned words), PC-002 (SD-01 unconfirmed, two proposals), PC-003 (registry/literal cross-check), PC-004 (acceptance_trace) are present in the deliverables.
* Material revisions: none after critique; no second critique needed.
* Justification assessment: supported, except RV-001 and RV-002.

## Plan Follow-Up Assessment

| Item | Route |
| --- | --- |
| Owner review, cohorts, thresholds, labeller | Open; owner decision, distinct follow-up |
| Per-cohort reporting after approval | Open; later authorised implementation |
| Support Unknown policy decision | Open; policy owner |

## Findings

| ID | Severity | Finding | Destination |
| --- | --- | --- | --- |
| RV-001 | Medium | The deterministic expectations (invariant, proposed_difference, SD-01 behaviour) are asserted in prose but never checked against `rank()`, although `zava_forward.core` is importable in the test path. The test only proves internal consistency, so a policy change or a wrong claim would pass silently. The "same relative rank" wording is also undefined: the baseline and variant carry different ids, so case-id tie-breaks can reorder them; the comparison basis (same id in two runs, or a fixed neighbour set) is not stated. | rpi-implement: add a small test that ranks constructed pairs and asserts the claimed invariance, A01 difference and A02 Unknown ties with No; define the comparison basis in the manifest |
| RV-002 | Medium | CM-A03 declares the contact-need pair an invariant "by construction" with support false, but `support_status` treats any non-None, non-Unknown `adjustment` as support Yes, so a large-print need stored in `adjustment` would move the variant ahead. The manifest notes the coupling yet still states an invariant and keeps SD-04 as a negative control the deterministic ranker cannot be tested with until a representation is chosen. Overstates realisability. | rpi-implement: restate expected as conditional on a separate contact field, or mark the pair representation-pending; owner checklist already asks to split pairs |
| RV-003 | Low | Plan FR-2 names `CM-P01` IDs and a single varied factor; delivered IDs differ and CM-C01 varies two fields. No implementation-time update in the changes record. | rpi-implement: add a descriptive update to the changes record (plan edit via rpi-plan only if desired) |
| RV-004 | Low | CM-C01 says dropping an open safety case is always critical and stays in the "top set". ai_eval.py treats a run as non-critical when hazards exceed top-k and the picks are all hazards. The manifest omits this nuance. | rpi-implement: add the top-k exception wording |
| RV-005 | Low | The pack's checklist cites #223 as a separate authorisation route; no research record supports the link (issue exists: human-review effectiveness test, open). | rpi-research or reword to avoid implying dependency |
| RV-006 | Low | ASCII and link checks are claimed in the changes record without persisted output (this Review re-verified them). Test regex `\bAPPROVED\b` is case-sensitive and only guards the exact status word; weak but acceptable. | Note only; no action required |

## Leakage, approval and scope assessment

* Leakage: dataset_role, pack and README all say development draft, not held-out; no oracle or gold wording. Agent labels remain unlabelled. No issue found.
* Approval inference: all AC Not met, proposals flagged invented, `requires_approval` true. No inference found.
* Scope: no evaluator, API, UI, model or data; only listed files changed. No creep. The untracked rpi-sessions state file is RPI bookkeeping and not listed in the changes record (trivial).

## Recommended Next Steps

* Run `/rpi-implement` for RV-001 to RV-004, then rerun the focused tests and the complete local gate; no second Review is required.
* Owner decisions remain open as listed in the pack.
