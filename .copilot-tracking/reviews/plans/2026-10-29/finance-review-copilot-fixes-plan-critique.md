<!-- markdownlint-disable-file -->
# RPI Plan Critique: Finance review Copilot fixes

## Metadata

* Task ID: finance-review-copilot-fixes-510
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/finance-review-copilot-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/finance-review-copilot-fixes-phase-details.md
* Critique execution status: Complete
* Assessment: one final-candidate assessment; this artifact preserves its complete original verdict and finding set.

## Inputs and Criterion Boundary

* Caller requirements: fix exactly the two supplied PR #510 findings; retain blank corrections/history without satisfying required inputs; preserve numeric zero and boolean false; isolate unavailable drafts without exposing their fields/history; keep tests outside installed packages.
* Research: .copilot-tracking/research/2026-10-29/finance-review-copilot-fixes-research.md, including Q1/Q2, C1-C7, alternatives, readiness and recorded environment limitations.
* Decisions and dependencies: P01 and P02 are independent; P03 follows both. Preserve existing test ownership, remove no tests, add at most four methods, retain the four requested core checks and focused staging/API checks.
* Lifecycle boundary: the caller authorizes the bounded full RPI loop and a local commit only. This critique does not continue phases, commit, push, use Azure or edit rubric scores.
* Direct corroboration: src/core/src/zava_forward/core/form_review.py; relevant portions of src/core/src/zava_forward/core/forms.py; src/core/tests/test_form_review.py; src/core/tests/test_form_staging.py; src/api/tests/test_form_staging_api.py; relevant core/API contract README sections and src/README.md local-gate guidance.
* Repository context: original case study, addendum, reference index and owner memory were consulted. These do not expand the two-finding implementation scope.
* Assessment boundary: planning credibility, existing code contracts, regression coverage, dependencies and validation/stop conditions. This is not implementation verification, operational approval, a fresh PR review or a full-gate result.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C2, P01-T01: blank required corrections | Covered | Details explicitly retain type validation and raw correction/history, then exclude stripped-empty strings from confirmed membership. form_review.py:44 and :239-294 support that separation. |
| C6/C7, P01-T01: conditional and typed inputs | Covered | Public-action coverage includes unconditional/active conditional blanks, blank controlling inputs, zero/false, diagnose and persisted reopen. Exact typed equality is retained rather than generic truthiness. |
| C3, P02-T01: sibling availability | Covered | Replace the whole-list failure with a per-draft DocumentUnavailable handler around the complete report, after authorization. Distinct retained sources and an unchanged readable sibling are explicit regression requirements. |
| C4, P02-T01: retained-data privacy and recovery | Covered | Exact three-key affected entries exclude fields, history, schema, attachments and snapshots. Existing retained-source/snapshot tests are updated, not removed; missing bytes, deleted metadata, pending/infected scans and recovery are covered. |
| C4, P02-T01: nonmutation and failure distinction | Covered | Preserve write denial, no saves/scans/source writes, per-report caches and real DocumentStoreError propagation. Existing outage and source-read tests remain owned by the core suite. |
| C5, P02-T02: HTTP contract and authorization | Covered | Intentional one-draft GET 403 changes to 200/per-entry Unavailable; unauthorized reads stay denied. A two-draft HTTP test fits the reserved fourth method, and both contract READMEs are targeted. |
| Locked change/test budget | Covered | Three core methods can parameterize the blank/conditional matrix, typed zero/false cases and two-draft availability matrix across the existing JSON/SQLite fixtures; one HTTP method remains available. No additional test module or package-owned tests are needed. |
| P03-T01: targeted checks and original Review | Covered | Four exact core commands are supplied; component READMEs provide staging/API fixture paths. Reconcile evidence before one independent Review and preserve its original outcome. |
| P03-T02: local candidate and gate boundaries | Covered | Commit only locally, preserve original evidence, fetch main, use a fresh external gate output and nonqueued admission. Missing prerequisites/foreign lock ownership remain explicit blockers, not successful validation or cloud fallback. |
| User scope and financial authority | Covered | No new routes, UI, approval, source-document behavior, Azure activity, push, manual rubric edits or unrelated issue closure. Held financial controls remain unchanged. |

## Verdict

* Verdict: Pass
* Rationale: The supplied plan and details credibly address both defects at the existing confirmed-input and authorized per-draft report boundaries. The regression matrix protects persistence, history, typed conditions, sibling availability and retained-source privacy without exceeding the locked budget. Existing intentional read-denial assertions are explicitly reconciled rather than silently weakened.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

* None. PC IDs: none. This is the complete actionable finding set for the supplied boundary; no findings are reserved for a later critique.
* Exact resolving evidence: not applicable because no actionable finding is raised. The coverage table identifies the existing planning commitments and corroborating contracts supporting the verdict.
* Disposition: no direct planner correction and no significant/divergent user decision required.

## Strengths and Residual Risk

* Keeping _valid type-only avoids falsely reporting blank strings as schema-type failures; filtering confirmed membership preserves the human correction and recorded lineage.
* Catching only DocumentUnavailable around a complete draft report prevents partial disclosure without disguising storage-service failures or weakening actor checks.
* Existing historical/snapshot coverage is retained alongside the new multi-draft case. The four-method limit is feasible with the existing parameterized store fixtures.
* The plan already recognizes missing full-gate prerequisites and shared heavy-lock ownership as possible blockers. Pass does not accept a missing gate as a successful gate, or establish hosted/human approval.
* Implementation and validation are still prospective. A later Review finding or failed command must retain its actual outcome; this critique does not pre-approve corrections or authorize another critique.

## Questions or Blocking Evidence Gaps

* None decision-critical for this bounded plan assessment.

## Limitations

* No tests, gate commands, GitHub queries or external research were executed for this critique.
* The supplied research's prior pull, PR lifecycle and dependency-installation claims were treated as recorded inputs, not freshly reproduced.
* Repository status showed the three planning/research inputs and session state as untracked on docs/finance-96. They were left untouched; no existing critique artifact was found.
* Only the caller-specified critique artifact was written. Plan, details, research, state and executable files remain unchanged.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record the Pass disposition and finalize the plan handoff for P01-T01 under the caller's existing bounded-loop authorization.
* User response required: no.
* Stop: critique complete; no phase continuation by this assessor.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/finance-review-copilot-fixes-plan.md](.copilot-tracking/plans/2026-10-29/finance-review-copilot-fixes-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/finance-review-copilot-fixes-phase-details.md](.copilot-tracking/details/2026-10-29/finance-review-copilot-fixes-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-29/finance-review-copilot-fixes-research.md](.copilot-tracking/research/2026-10-29/finance-review-copilot-fixes-research.md) | Supplied research and evidence |
| [.copilot-tracking/reviews/plans/2026-10-29/finance-review-copilot-fixes-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/finance-review-copilot-fixes-plan-critique.md) | Complete original critique |

## Next Steps

No user action is required. Return Complete / Pass to the planning parent for disposition and authorized handoff; stop this critique task here.
