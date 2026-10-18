---
title: Issue 126 RAI evidence register plan critique
ms.date: 2026-10-18
---

## Metadata

* Task ID: 126
* Slug: issue-126-rai-evidence-register
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-126-rai-evidence-register-phase-details.md
* Critique execution status: Complete
* Execution: exactly one rpi-plan-critique activation and one assessment of the final candidate. No workers, implementation, second critique or implementation Review.
* Inspected HEAD: ab0613f3336109ff9b96560a16758ee842232715, matching the pinned base.

## Inputs and Criterion Boundary

The caller's narrow direction controls this assessment: append-only constructed,
unverified claims in the existing governance document; all 22 residual/unassessed
baseline findings, not the eleven AI tasks. No acceptance, closure, evidence
promotion, role grant, new source module, service, UI, private data, live Azure or
inference. Existing task-release admission remains untouched.

The assessment covers the supplied plan, phase details and research, their
requirements, evidence, task dependencies, acceptance criteria, decisions and
failure modes. Source inspection was limited to their referenced contracts:
governance.py, change_provenance.py, SqlStore transaction/document/lock paths,
MssqlStore, existing governance and progress-event tests, API governance handlers,
the existing Dockerfile, core/API guides, the original RAI report and the
historical PRD v0.16.0 contract at
7a8b1fe65475752fcf242ed52acab8e7e43b58d3.

Project context was read from docs/case_study_48_original.md,
docs/case_study_48_addendum.md (relevant purpose and RAI sections),
docs/reference/README.md and docs/reference/memory.md. The task state and earlier
issue-126 Review were inspected only to establish lifecycle/provenance. Research
C1's live issue retrieval is supplied evidence, not independently refetched here.
No new regulatory research or current legal assertion is made.

P01 must establish semantics before P02 validation/documentation. P03 follows
evidence reconciliation and the single original implementation Review. Publication
is a normal pinned-lineage push and non-closing PR, not merge or acceptance.
Current-source comparison is explicitly caller-declared, never deployed-version
attestation; missing context remains Unknown.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| All 22 findings; C2/C6; P01-T01 | Covered | Original report principal tables contain eleven PARTIAL and eleven NOT_ASSESSED findings; literal inventory and immutable status/verdict tests are planned. |
| Append-only constructed provenance; P01-T01/T02 | Covered | Server actor/time/revision, retained history, closed claim action, constructed-fixture and unverified labels; no acceptance authority. |
| Exact source/task/release or explicit nonapplicability; C7; P01-T02 | Partial | Exact declared context and baseline-history rule are present; completeness must use distinct matching finding IDs, PC-001. |
| Completeness versus adequacy/closure; P01-T02 | Partial | Unknown acceptance and Open findings are explicit, but details say completeness counts records, PC-001. |
| Bounded inert input; P01-T01/T02/T03 | Partial | Closed keys, tiers and no-fetch boundary are explicit; concrete primitive/limit/cross-field contract is missing, PC-002. |
| Fresh registered manager read/write; C4; P01-T01/T02 | Covered | _actor, existing manager roles and change_validation under writer transaction; forged, removed and demoted actors included. |
| Checked-document CAS/audit and failure outcomes; C5/C9; P01-T02; P02-T01 | Covered | Existing shared document CAS, pending-audit quarantine, recovery, immediate post-COMMIT witness and committed/reload outcome are planned. |
| Detached deterministic no-write GET; C3; P01-T01/T03 | Covered | No defaults, detached snapshot, unchanged bytes/audit/data, strict assessment query validation and absent-context Unknown. |
| Existing governance/task-release preservation; P01-T03; P02-T01 | Covered | Narrow route changes and existing protocol, release, breach and task-release regressions; no admission changes. |
| SQL parity and hardened image; P02-T01/T02 | Covered as planned validation, not observed evidence | Actual disposable loopback MSSQL and installed-distribution UID10001/read-only image execution, or explicitly unmet outcomes. |
| Documentation and evidence honesty; P02-T03; P03-T01/T02 | Covered | Current dated engineering section, immutable historical report, append-only log, one original Review, hash originals, non-closing publication. |
| Change budget and exclusions | Covered | Zero new source modules, extend existing core governance tests and at most one HTTP test module; no generic persistence rewrite. |

Inventory cross-check, preserving original status/verdict:

* PARTIAL / DOWNGRADED: GOVERN-AUDIT-02, GOVERN-AUDIT-01, MAP-02, MAP-01,
  MAP-04, MEASURE-01, MN-4.3, MN-4.1, MN-3.2.
* PARTIAL / CONFIRMED: T-RAI-001, T-RAI-002.
* NOT_ASSESSED / UNCHANGED: GOVERN-AUDIT-04, GOVERN-AUDIT-05, MAP-05,
  MEASURE-02, MEASURE-03, MEASURE-04, MN-2.3, T-RAI-005, EU-COND-01,
  EU-COND-02, EU-COND-04.

These are 22 distinct findings. The report's seven PASS checks are not additional
open-register entries; neither the report's historical planning acceptance nor
its DOWNGRADED verdicts authorize closure.

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 2; Low 0.
* Rationale: The candidate has a credible narrow implementation approach, but
  two directly correctable contract gaps affect reproducible aggregate and
  validation tests. Neither requires a new user decision or expanded scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Define completeness by distinct matching findings, not claim-record count

* Related IDs: binding/completeness acceptance criteria; C6/C7; P01-T01/T02.
* Evidence: .copilot-tracking/details/2026-10-18/issue-126-rai-evidence-register-phase-details.md:25-29 says aggregate completeness "counts records". The plan at .copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md:62-65 requires exactly 22 unique inventory IDs and separates completeness from evidence adequacy, but does not define the numerator or context eligibility.
* Concern: An append-only history can contain many claims for one finding and stale/baseline claims for others. Counting records does not establish that dispositions were supplied for all 22 findings in the requested comparison context. No-query Unknown must not become apparent completeness merely because history exists.
* Impact: Duplicate or mismatched history could inflate a coverage summary even while acceptance correctly remains Unknown and closure Open. The planned tests lack an unambiguous oracle for this case.
* Smallest useful change: Specify separate history-record count and disposition coverage. Coverage counts each known finding at most once and only for claims eligible under the exact declared assessment and original baseline identity. Explicitly define the Unknown/no-context and historical-baseline cases without crediting history as current coverage. Do not change evidence adequacy or closure.
* Action owner: Planning parent, with implementation/tests owned by that same parent.
* Exact resolving evidence: Revised P01-T01/T02 specify the numerator, denominator 22 and context eligibility; tests show repeated claims for one finding count once, changes to each source/task/version/release component do not transfer coverage, baseline replay remains history, absent context remains Unknown, and 22 distinct eligible dispositions can be complete while all findings remain Open and acceptance Unknown.
* Decision route: Direct planner correction. Existing caller direction already resolves the authority and scope boundary; no user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Complete the bounded primitive and cross-field claim contract

* Related IDs: inert bounded input and invalid/promotional-body acceptance criteria; P01-T01/T02/T03.
* Evidence: .copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md:46-60,75 lists keys, commit syntax and some enums but only says to bound text/list lengths. .copilot-tracking/details/2026-10-18/issue-126-rai-evidence-register-phase-details.md:25-28 requires closed primitive validators without specifying their limits or the remaining field relationships.
* Concern: The candidate leaves references' shape/cardinality, individual text limits, result representation, revision type/range and decision-maker-status/reference consistency undefined. The task/release branch also needs an explicit rule for nonapplicability_reason when task fields are populated. These are observable request contracts, not formatting preferences.
* Impact: Failing-first tests and implementation can independently choose incompatible rules; a closed outer key set alone does not prevent nested/unbounded values or contradictory structured authority labels. Free-text supplied results must never become computed acceptance.
* Smallest useful change: Add one compact schema/validation matrix within the existing details: primitive types, required/null/empty behavior, finite text/item limits, reference item shape, strict nonnegative integer revision excluding booleans, task-versus-nonapplicability exclusivity, and status/reference consistency. Preserve existing tier names and unverified claim semantics; bounded supplied result text may remain text if explicitly specified.
* Action owner: Planning parent, with implementation/tests owned by that same parent.
* Exact resolving evidence: Revised P01-T01/T02 contain the matrix and tests at each chosen limit plus one beyond, wrong primitives/nested values, boolean/negative revisions, mixed task/nonapplicability fields, and inconsistent decision-maker references. Direct and HTTP tests reject invalid requests without a claim or success audit; valid inert references cause no fetch and never grant authority.
* Decision route: Direct planner correction. Choose conservative engineering limits within the confirmed scope; no significant or divergent user decision is required.

## Strengths and Residual Risk

* The plan correctly reuses the existing checked governance document. SqlStore.save already checks change_validation inside BEGIN IMMEDIATE and writes the shared document and audit in one transaction.
* The immediate post-COMMIT witness is necessary: existing hooks run before snapshots refresh, and exception paths can otherwise attempt rollback after commit. Pending-audit quarantine and committed/reload handling are explicitly planned rather than inferred from save success.
* Detached GET addresses the real _gov setdefault/live-reference behavior without rewriting unrelated governance writers.
* SQL atomicity is not generalized to JSON cross-file crash atomicity. Human competence, current-source qualification, staff-data/privacy review and live acceptance remain outside this claim register and unmet.
* Actual disposable MSSQL and hardened non-root image execution are required evidence tasks. Neither was executed in this plan critique; opt-in skips, authored tests and Dockerfile inspection cannot satisfy them. If unavailable, report explicitly unmet rather than passed.

## Questions or Blocking Evidence Gaps

No user question is required. This assessment is decision-capable for the supplied
planning boundary. The two findings require planner-owned clarification before
implementation. Real deployment, legal approval and qualified acceptance are not
planning evidence gaps to resolve by broadening this task.

## Limitations and Artifact Integrity

Only the requested critique artifact was written. No source, plan, details,
research, state or prior review was changed. No tests, container execution,
private datasets or live services were used. This is a plan critique, not code
review, deployment verification or compliance acceptance.

Input SHA-256 values captured before assessment:

| Artifact | SHA-256 |
| --- | --- |
| .copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md | a8da9df0533fceeb344afadbb979fdccb3e0b33c54d669b160215e2511e2ad21 |
| .copilot-tracking/details/2026-10-18/issue-126-rai-evidence-register-phase-details.md | 872a47ccd503c932090e91f72e032fcf2495d757319be25e3eea4cdc5bc13df2 |
| .copilot-tracking/research/2026-10-18/issue-126-rai-evidence-register-research.md | 57cdb2706ec0bb522ebf753939e94c744488306cba22e3c06f010628c3fb1812 |
| .copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md | 15134ff64d335b57954967c7b84a13c5f6d15f7119c453814534f1403c3cd84a |
| .copilot-tracking/reviews/2026-10-15/issue-126-frozen-protocol-gates-review.md | 836c2f02a7a5587ec8d41714ca3df06f56cb1394ebfade9933da57993eca1e4c |

This original adverse critique must itself remain byte-identical. Its SHA-256 is
returned separately after writing, avoiding a self-referential digest. Record
dispositions in the parent-owned plan/change evidence, not by altering this file.
The full actionable set for this assessment is PC-001 and PC-002; no separately
withheld late findings or second critique are prescribed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define distinct/context-bound completeness and the bounded schema matrix; record direct dispositions for both PC IDs in parent-owned planning evidence.
* User response required: No.

| [.copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md](.copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-18/issue-126-rai-evidence-register-phase-details.md](.copilot-tracking/details/2026-10-18/issue-126-rai-evidence-register-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-18/issue-126-rai-evidence-register-research.md](.copilot-tracking/research/2026-10-18/issue-126-rai-evidence-register-research.md) | Supplied research |
| [.copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md](.copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md) | Immutable baseline inventory |
| [.copilot-tracking/reviews/2026-10-18/issue-126-rai-evidence-register-plan-critique.md](.copilot-tracking/reviews/2026-10-18/issue-126-rai-evidence-register-plan-critique.md) | Original single critique |

## Next Steps

Active planning parent revises directly and records both PC dispositions without
another critique. Preserve this adverse original and its returned digest. No user
action is required. This worker stops here; it does not implement, run Review,
change state or publish.
