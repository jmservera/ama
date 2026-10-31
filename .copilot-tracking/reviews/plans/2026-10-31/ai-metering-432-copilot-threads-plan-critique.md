---
title: AI metering Copilot threads final-candidate plan critique
description: One evidence-grounded assessment of the five PR 602 corrections
ms.date: 2026-10-31
---

## Metadata

* Task ID: 432-copilot-threads
* Branch and PR: feat/ai-metering-432, PR #602, open against main
* Inspected HEAD: 736f20d8
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-copilot-threads-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/ai-metering-432-copilot-threads-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate critique; no delegated or second critique.
* Write boundary: This artifact only. Existing untracked parent planning/research/state inputs were not modified, moved or committed.

## Inputs and Criterion Boundary

* Caller requirements: Preserve CURRENT for nested look_at calls; validate report timestamps/ranges before SQL availability branching; persist unlinked legacy and priority rejection with Unknown economics; atomically create an ineligible assistant output link and rejection after a pending provider failure; persist MAX_EVENTS-held assistant withdrawal with unresolved financial attribution.
* Validation direction: Core/API unit tests, Ruff, configured format checks and mypy; CI is the publication gate, without waiting for the full local gate. Maximum eight additional test methods across the two canonical test modules, no removals. No paid calls, private data, secrets, UI changes or nested agents.
* Supplied inputs: The three dated task artifacts above; C1-C7 source pointers and W1-W5 review-comment pointers in the research.
* Source evidence considered: src/core/src/zava_forward/core/ai.py; src/core/src/zava_forward/core/ai_consumption.py; src/core/src/zava_forward/core/ai_tasks.py; src/core/src/zava_forward/core/store.py; src/core/src/zava_forward/core/assistants.py; src/api/src/zava_forward/api/server.py; src/core/tests/test_ai_consumption.py; src/api/tests/test_ai_consumption_api.py; both component READMEs and pyproject.toml files.
* Context considered: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md, docs/reference/research/sector/housing-association-primer.md and docs/reference/resources/ai-tokenomics.md. No legal-currentness or live financial assessment is made.
* Read-only GitHub inspection confirmed the branch/PR relationship and retrieved all five supplied unresolved review comments, IDs 4431875217, 4431875235, 4431875253, 4431875268 and 4431875281. No unrelated remote research was performed.
* Decisions and dependencies: P01 implementation precedes P02 validation and independent implementation Review; publication must retain Refs #432, original adverse evidence and the requested trailer. Thread resolution depends on actual fix/regression evidence, not this critique.
* Assessment boundary: Credibility of the supplied source-correction plan, including rejection/acceptance safety, durable evidence, report cohort/as-of semantics and feasible test ownership. This is not an implementation Review, test execution, CI result, full-gate receipt, operational approval or whole-issue acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| W1 / C1 / P01-T01: CURRENT preservation | Covered | Mirror run's existing-context branch; _request changes only actual configuration. Planned real local text-provider call/depth thresholds are appropriate. |
| W2 / C2 / P01-T01: pre-branch period validation | Covered | Shared timestamp/range helper before ledger availability selection addresses JSON and unavailable-schema bypass. Extend the existing HTTP method to exercise all branches. |
| W3 / C3-C4 / P01-T02: orphan legacy/priority reject | Partial | Reject-only persistence and original-link recovery are correct; orphan cohort review accounting is not specified sufficiently. PC-001. |
| W4 / C5 / P01-T02: pending assistant reject | Partial | Original root, immutable eligibility and authoritative transaction are specified; read/write staging and fallback boundaries need definition. PC-002. |
| W5 / C6 / P01-T02: capacity-held withdrawal | Partial | Unresolved marker and durable task history are appropriate; chronological precedence and unresolved accounting remain underdefined. PC-002 and PC-003. |
| P01-T03 / acceptance safety | Partial | Existing output-link matrix retains accept/edit refusal, but new root-repair and held paths need explicit negative assertions without widening acceptance. PC-004. |
| P01-T03 / bounded test ownership | Partial | Canonical modules, no removals and eight-method limit are stated, but no method-level allocation covers all failure/temporal branches. PC-004. |
| P02-T01 / static and component validation | Covered | Focused then full core/API suites; existing Ruff/format/mypy configurations and opt-in skips retained. Tests remain implementation-owned. |
| P02-T02 / independent Review | Covered | One implementation Review is separate from this one plan critique; adverse outcomes remain historical, not relabelled. |
| P02-T03 / publication and thread evidence | Covered | Non-force topic publication, privacy-safe local commit identity, five evidence-backed replies/resolutions and no merge/issue closure or hosted approval claim. |
| User-selected exclusions | Covered | No full-local-gate wait, no paid/private/UI work, no schema migration or broader historical/resident attribution project. These are not reopened as user questions. |

## Verdict

* Verdict: Revise
* Severity summary: 3 High, 1 Medium; 0 Critical, 0 Low.
* Rationale: All five corrections have credible source targets. The candidate nevertheless leaves decision-critical implementation contracts implicit at the intersection of missing links, bounded reads, unresolved markers and report accounting. The planner can resolve the four findings directly within existing user direction and the eight-method budget.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Orphan reviews need cohort attribution without inventing an output join

* Related IDs: W3, C3-C4, P01-T02, P01-T03.
* Evidence: src/core/src/zava_forward/core/ai_consumption.py:26-41 defines review/review-intent fields without root; :664-735 currently requires an output record; :826-849 constructs cohort_outputs only from linked outputs and counts only pending intents whose output is in that set. src/core/src/zava_forward/core/ai_tasks.py:375 and src/core/src/zava_forward/core/store.py:941 create intent before a separate domain save. Phase details require orphan rejection and unresolved cohort-review counting but do not define their association.
* Concern: Removing reject-only missing-output guards allows persistence, and unjoined_outputs already keeps the call cohort incomplete. It does not make the orphan review visible to unjoined_reviews, however. Neither review nor intent alone identifies the original call root. A global count would contaminate unrelated periods; counting only existing cohort_outputs misses exactly the new orphan case. A completed orphan rejection must not be mistaken for repaired output economics.
* Impact: Reporting can undercount unresolved review evidence or block unrelated cohorts, and original-link repair can leave stale or double-counted gaps. The requested rejection works superficially without a defensible report contract.
* Smallest useful change: Specify a content-free original-root association for orphan rejection, supplied from the authoritative legacy record by both legacy and priority paths. Use a compatible closed event representation without changing the required shape of already-written v1 events or introducing DDL. Define unresolved cohort reviews as distinct outputs in the call-root cohort with pending disposition and/or missing output attribution, counted once. Retain the original missing output, reject-only admission, authoritative-save retry rules and explicit matching original-link repair; do not fabricate an ineligible legacy output to hide the gap.
* Action owner: Planning parent for contract; P01-T02 implementer for source; P01-T03 test owner for assertions.
* Exact resolving evidence: Revised P01-T02 describes original-root association, legacy-v1 read compatibility and de-duplicated cohort rules. The existing ConsumptionApi.test_legacy_and_priority_reviews_recover_only_committed_matching_links matrix proves persisted rejection on SQL and JSON for both paths, unchanged accept/edit refusal, incomplete/Unknown economics and a visible orphan review gap; explicit original-link repair removes the gap without a second audit, save or disposition. A focused core case distinguishes an in-cohort orphan from an unrelated-root orphan, including a pending intent after save failure.
* Decision route: Direct planner correction. The user already chose rejection persistence with unresolved economics; no divergent user decision or new attribution project is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Define the transaction boundary before catching DispatchHeld after potential writes

* Related IDs: W4-W5, C5-C6, P01-T02.
* Evidence: src/core/src/zava_forward/core/ai_consumption.py:600-634 makes output read then append; :698-751 makes review independently read then append. _read at :167-178 holds above MAX_EVENTS. src/core/src/zava_forward/core/assistants.py:425-441 rolls back only exceptions escaping the transaction; :1059-1068 writes task state and human history before metering. Phase details propose supplying a missing root inside Consumption.review and catching DispatchHeld to append a marker in that same transaction.
* Concern: A naive composition of output(..., db=conn) and the current review write path can read N records, append an ineligible output as record N+1, then hold on its next read when MAX_EVENTS=N. Catching inside the outer transaction commits that partial normal-attribution write together with the unresolved fallback. The plan does not say whether this mixed state is intended or how it is accounted for. A catch around the whole authoritative transaction could also confuse metering holds with unrelated failures.
* Impact: The implementation may satisfy persisted withdrawal but produce an untested partially repaired financial link, inconsistent completion/retry evidence, or accidentally suppress a database failure. Atomic linkage-and-disposition is a specific user requirement, not merely using the same connection.
* Smallest useful change: Stage and validate metering reads, immutable-link conflicts and disposition decisions before normal financial writes, preferably using one bounded record snapshot. Define two complete outcomes: normal link/disposition, or unresolved withdrawal marker without leaked partial normal-attribution writes. If partial writes are deliberately retained, specify their exact invariant and report/retry handling instead of leaving it implicit. Catch only DispatchHeld from the metering operation for action reject; SQL/event/update failures still escape and roll back. Retain authorization/revision checks before either outcome.
* Action owner: Planning parent and P01-T02 implementer.
* Exact resolving evidence: Revised details name the catch location, read-before-write staging and outcome invariants. A boundary regression sets the limit to the actual existing record count on an unlinked metered pending task and inspects persisted task, human history and raw ledger records after rejection. It proves either complete normal attribution or the explicitly specified complete fallback, never unexplained partial writes. Fault injection during the output/disposition or fallback-marker insert proves arbitrary SQL failure rolls back task revision/state and every new event. A stale revision and unauthorized actor commit nothing.
* Decision route: Direct planner correction. This is failure-atomic implementation design under the existing requirement, not a request to relax capacity or swallow SQL failures.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Unresolved markers need explicit chronological, sticky and cohort-scoped semantics

* Related IDs: W5, C3, C6, P01-T02, P01-T03.
* Evidence: src/core/src/zava_forward/core/ai_consumption.py:163-178 sorts bounded reads by at,id; :642-662 and :719-748 use revision ordering for normal reviews/intents; :813-825 selects reviews as-of cutoff by revision. Reconciliation at :871 requires no unjoined outputs or reviews. The proposed marker is new, scan-independent metadata, so no valid next financial review revision can be assumed during a hold. Phase details say to preserve historical acceptance but do not define marker fields, precedence, persistence after normal reads resume or de-duplication.
* Concern: Treating a marker as an ordinary review with a guessed revision can lose against the old accept record. Considering every marker without its cutoff can rewrite historical acceptance. Considering only the most recent normal disposition can silently clear unresolved financial attribution after capacity recovery. A same-timestamp accept/withdrawal is realistic at SQL clock precision and cannot safely depend on random event-ID order.
* Impact: The central W5 safety claim can fail: a withdrawn proposal remains financially accepted, a past report changes retrospectively, or a later report produces a reconciled ratio while withdrawal attribution is still unresolved.
* Smallest useful change: Define the closed marker fields and validation, including opaque original root/output, reject disposition, event time and authoritative task revision or another deterministic ordering rule that does not scan the consumption stream. Apply markers only when at <= as_of and their root belongs to the call-time cohort. A relevant unresolved withdrawal must suppress acceptance despite older financial accept records, count once in unresolved review coverage and prohibit reconciliation/financial ratios. State that successful reads, repeated rejection and ordinary later ledger events do not themselves clear the unresolved state. No automatic repair/clear operation is in this task; preserve pre-withdrawal as-of acceptance. Keep normal immutable output eligibility and authorization unchanged.
* Action owner: Planning parent for temporal contract; P01-T02 report implementer.
* Exact resolving evidence: Revised P01-T02 defines marker schema compatibility, ordering, stickiness and cohort rules. Tests begin with a linked eligible human-accepted proposal and a complete matched bill, persist a held withdrawal, then restore read capacity without deleting events or changing production limits. Before-withdrawal cutoff still counts acceptance; at/after cutoff excludes it, reports incomplete coverage, nonzero de-duplicated unresolved reviews, Unknown token_cost/cost_per_accepted_proposal/quality-qualified cost and unreconciled status. Equal-time withdrawal precedence, repeated markers and an unrelated-root marker do not change the wrong cohort or double-count. A restarted Consumption instance preserves the result.
* Decision route: Direct planner correction. User direction already forbids stale accepted economics after withdrawal and recovery; no financial-approval or retrospective-history decision is needed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Allocate the eight-method budget to the failure contracts and negative acceptance cases

* Related IDs: P01-T01, P01-T02, P01-T03, P02-T01, all five acceptance criteria.
* Evidence: Plan Test Ownership and Candidate Lock fixes the canonical modules and maximum eight additions but gives no method-level allocation. Phase details list several additions without ownership or budget consumption. Existing test_ai_consumption_api.py:392-620 already contains the SQL/JSON, legacy/priority, accept/edit/reject fault matrix; :848-884 contains the actual HTTP period test. test_ai_consumption.py already covers capacity admission, normal chronological rejection and missing-link refusal, but not the new mixed/fallback states.
* Concern: Filling the budget with only positive thread examples can leave PC-001 to PC-003 failure cases and rejection-only safety unproved. Extending a core method name alone also does not establish that the new original-root repair path rejects accept/edit requests or that capacity fallback never bypasses revision/authorization controls.
* Impact: Implementation can appear test-complete while missing the exact boundary where new behavior changes acceptance or fails atomically. Late test proliferation would conflict with the explicit eight-method/no-removal constraint.
* Smallest useful change: Record a bounded ownership matrix in P01-T03. Extend the two existing composed methods for orphan/recovery and HTTP validation rather than replacing/removing them; use subtests for SQL/JSON/unavailable-schema and invalid/naive/reversed/as_of-before-end periods. Allocate no more than these eight additional methods:
  1. API: local text look_at shared call/depth threshold, standalone-root behavior and CURRENT restoration.
  2. API: actual failed-provider pending-task rejection, ineligible linkage, no redispatch and unchanged existing eligibility.
  3. API: accepted-proposal MAX_EVENTS-held withdrawal, durable task/history marker and post-recovery Unknown economics.
  4. API: exact-capacity link boundary, SQL insert failures and unchanged authorization/revision/acceptance controls, using subtests.
  5. Core: reject-only orphan intent/disposition, cohort gap accounting and original-link recovery.
  6. Core: original-root assistant link repair, immutable root/output/eligibility conflicts and reject-only repair admission.
  7. Core: unresolved marker cutoff/equal-time precedence, restart and sticky recovery behavior.
  8. Core: unresolved marker cohort isolation and distinct-output de-duplication.
* Action owner: Planning parent and P01-T03 test owner.
* Exact resolving evidence: Revised details associate each behavior with one named existing/new method and identify which assertions cover PC-001 to PC-003. Implementation diff has at most eight added test methods across the two canonical modules and zero removed/renamed methods; preserved cases still exercise accept/edit refusal on missing links, no acceptance repair/fallback, immutable existing eligibility, source verification, stale revision, authorization and SQL rollback. Focused modules, full core/API suites and both components' ruff check, configured ruff format --check and mypy pass with actual counts/skips recorded. No test/static-check success is claimed by this critique.
* Decision route: Direct planner correction. The allocation stays within the user's test cap and validation direction; no additional methods or expanded scope need approval.

## Strengths and Residual Risk

* CURRENT preservation and report-period helper reuse are surgical corrections to existing code paths; no new provider, UI or deployment is needed.
* The supplied direction correctly distinguishes human withdrawal from incomplete economics, while preserving fail-closed provider dispatch and human acceptance.
* Legacy cross-store intent/save/disposition recovery and assistant authoritative SQL transaction are recognized as different guarantees. Do not claim cross-store atomicity after these changes.
* Existing component configurations exempt some migrated modules from strict typing/formatting. Passing configured checks is useful but does not prove those source paths fully typed or accessible.
* Historical/resident joins, actual Azure billing, Finance authority, OD-51 and paid held-out evidence remain outside this source-only correction. None is inferred from synthetic billing or local HTTP tests.
* CI-only publication direction is already selected by the user. This critique does not demand a full-local-gate wait, fabricate a receipt, waive hosted/human approval or recommend a protection change.

## Questions or Blocking Evidence Gaps

* No user response is required. All actionable findings are direct planner corrections under current explicit direction.
* No decision-critical supplied evidence gap blocks this assessment. The absence of implementation/test results is expected at planning time and is not a claimed result.

## Limitations

* Read-only source and supplied-review assessment; no application execution, core/API tests, Ruff, mypy, paid calls, private data access, source edits or GitHub thread mutation.
* Source failure paths are established by inspected code, not newly executed reproductions. Future marker/link implementation risks are identified as unspecified contracts, not asserted as existing marker bugs.
* Caller planning/research artifacts were untracked at inspection; inspected source HEAD alone does not identify a committed planning candidate. Parent must preserve dated original evidence and bind later validation/Review to the implemented head.
* No second critique is requested or authorized. Planner disposition and the separately planned one implementation Review are the next stages.

## Recommended Next Action

* Highest-impact finding: PC-003, because stale accepted-output reconciliation is the central financial failure W5 requires preventing.
* Action owner: Planning parent.
* Smallest next action: Specify the marker's closed fields, deterministic as-of precedence, cohort de-duplication and sticky unresolved rule in P01-T02; dispose PC-001, PC-002 and PC-004 in the same direct revision before implementation.
* User response required: No.

## Relevant Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/ai-metering-432-copilot-threads-research.md](.copilot-tracking/research/2026-10-31/ai-metering-432-copilot-threads-research.md) | Supplied C1-C7 and W1-W5 evidence. |
| [.copilot-tracking/plans/2026-10-31/ai-metering-432-copilot-threads-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-copilot-threads-plan.md) | Final candidate assessed once. |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-copilot-threads-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-copilot-threads-phase-details.md) | Planner-owned contracts and test allocation to revise. |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-copilot-threads-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-copilot-threads-plan-critique.md) | Complete critique and all four findings. |

## Next Steps

Active planning parent revises and records disposition of PC-001 through PC-004 directly, then finalizes the plan without a second critique. Proceed to implementation and the separately planned validation/one implementation Review only after those contracts are explicit. No user action is required.
