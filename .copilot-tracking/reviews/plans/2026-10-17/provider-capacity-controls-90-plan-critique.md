<!-- markdownlint-disable-file -->
# RPI Plan Critique: Provider capacity and controlled orders

## Metadata

* Task ID: 90
* Critique date: 2026-10-17
* Candidate: final candidate, assessed exactly once
* Plan: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Caller requirements: exactly the four #90 criteria; tiny fictional local data; no private data, live authority, cloud, paid inference, new services/frameworks or mvp changes. Preserve #78 provenance, #97 forms and independent resident/safety/building controls. No implementation, nested agents or second critique.
* Exact issue text was read using read-only gh issue view 90. The criteria are: work is not scheduled or confirmed beyond evidenced committed capacity; each work-order change is a new version with its issuer; system drafts are never instructions; contractors read only their own orders. #89 is hierarchy, not an execution dependency.
* Primary evidence: .copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md, C1-C7, and its supplied manager pointer, .copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md. Manager recommendations are research hypotheses, not company approval or additional owner-approved scope.
* Requirement pointers checked: docs/prds/zava-forward-retrofit-programme-demonstrator.md:843-851 and docs/brds/agentic-retrofit-programme-brd.md:1436-1440. Full FR-016 acceptance, actual contractual enforceability and legal approval are outside this critique.
* Supporting supplied source contracts checked: src/core/src/zava_forward/core/procurement.py; src/core/src/zava_forward/core/store.py:514-548; src/core/src/zava_forward/core/sqlstore.py:468-659; src/core/src/zava_forward/core/change_provenance.py:15-132; src/core/src/zava_forward/core/mssqlstore.py; src/core/tests/test_quality_procurement.py; src/api/tests/test_role_matrix.py; src/api/tests/test_mssqlstore.py; component guides and validation configuration; existing capacity-screen source location.
* Required context checked: original/addendum, knowledge-base index/memory and sector primer. No new regulatory interpretation or external research was performed.
* Latest-main condition: feat/provider-capacity-controls-90 HEAD and origin/main both resolve to adedf1f232e567d3a22a623d9c871513fa6b7cdc. Read-only git ls-remote origin refs/heads/main returned the same SHA during this critique. No branch switch, fetch, rebase or remote write was performed.
* Dependencies P01-T01 -> P01-T02 -> P02-T01 -> P02-T02 -> P03-T01 are coherent. The existing untracked planning/research artifacts were left untouched.
* Test ownership, zero removals and the maximum of 35 additional test methods are binding. Findings below request bounded additions to the plan/details, not implementation or a larger test budget.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #90 criterion 1; C1, C2, C5 | Partial | Fixed home-order quota, exact homes, scope invalidation and recorded losses are sound; PC-001 through PC-004 identify unresolved authorization, evidence, progression and race oracles. |
| #90 criterion 2; C3, C7 | Covered at requirement level | Plan:44,56 expressly includes every appointment, reissue, completion, correction and withdrawal, stable identity, immutable snapshots and copied reads. PC-005 requires these to be assigned to exact runnable acceptance tests, including non-booked outcomes and rejected writes. |
| #90 criterion 3; C7 | Covered at requirement level | Plan:45,57 and details:36 require explicit not-an-instruction output and no execution on review; no new AI/send route. PC-005 locks offline template/proposal/review no-write evidence rather than paid inference. |
| #90 criterion 4; C4 | Covered at requirement level | Plan:45,58 specifies two contractors, direct and HTTP isolation, package isolation and write rejection. Existing HTTP package access is 403, which should stay denied rather than be broadened. |
| Named authorization; RULE-008; manager recommendation 1 | Partial | Trusted staff records and no self-grant are correct; the matching contract lacks explicit action, supplier/scope and revocation rules. PC-001. |
| Meaningful evidence/version/dates/units; RULE-007; manager recommendations 2-4 | Partial | Count/unit/case/scope fields are selected, but acceptance, freshness and temporal boundary semantics remain unspecified. PC-002. |
| SQL atomicity; C6, C7 | Partial | Reuse of checked documents and writer locks is correct; deterministic race/rollback acceptance is not assigned. PC-004. |
| P01-T01 / P01-T02 | Partial | Failing-first approach is credible, but must pin positive and negative progression rules and transaction interleavings. PC-003, PC-004. |
| P02-T01 | Covered at scope level | Narrow current API and Fluent 2 capacity-screen continuation only; fresh guidelines and local fictional browser required. Exact changed-file and browser checks belong in PC-005. |
| P02-T02; preservation of #78/#97 | Partial | Preservation is explicit, but actual regression selectors, inherited SQL coverage and validation invocations are not locked. PC-005. |
| P03-T01 | Covered | One implementation Review, Refs #90 main-targeting PR, no closing/merge/history rewrite. A failed check or adverse review must remain visible, not be reported as criterion acceptance. |
| Test ownership/removals/budget/canonical targets | Partial | Parent ownership, no removals and 35-method cap are explicit. Generic migrated Python/JS targets and component commands are insufficiently specific to function as the claimed execution lock. PC-005. |
| Latest main and local-only scope | Covered | Same local/remote main SHA verified. No operational authority, real data or hosted acceptance inferred. |

## Verdict

* Verdict: Revise
* Rationale: The candidate is architecturally surgical and has the correct four-criterion boundary. It is not yet an executable final plan: several consequential predicates and their deterministic acceptance evidence are still left for the implementer to choose. Correct those directly within the existing phases and test budget. No new research wave, user approval, implementation or second critique is requested.
* Severity summary: Critical 0; High 4; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Define the effective delegation match, not only its storage fields

* Related IDs: RULE-008; C1, C2, C7; P01-T01, P01-T02.
* Evidence: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md:41; .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md:24,28; .copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md:78-92. src/core/src/zava_forward/core/procurement.py currently uses broad _need_manager checks; src/core/src/zava_forward/core/change_provenance.py:15-43 provides identity freshness, not a procurement delegation predicate.
* Concern: The plan specifies contract reference/version/reference/validity in trusted staff records but never states the matching rules for the requested action, supplier, applicable package/scope or revocation. A current registered manager with any in-date contract entry could satisfy that underspecified contract even when not authorized for this supplier or action. It is also not explicit that all delegation fields come from the freshly resolved staff record, never the request or cached caller dictionary.
* Impact: Named identity alone can be mistaken for named instruction authority. A limited or revoked delegation could authorize consequential package/capacity/order changes, including through advance.
* Smallest useful change: Add one bounded exercise predicate and operation matrix to P01-T02: resolve current trusted staff; require the selected manager role plus an unrevoked, effective delegation for the exact contract/call-off version, supplier and requested action, with declared package/scope limits matched where present. Define missing/malformed required limits as unknown/denied. Define which checks apply before a package has an ID, using contract/action scope rather than granting authority during creation. Record the matched delegation snapshot, and rerun that same predicate at SQL commit. Do not add financial approval logic, an authority endpoint or real named permissions.
* Action owner: Planning parent.
* Exact resolving evidence: Revised details contain the predicate, required exercise fields and action matrix; P01-T01 assigns positive fictional delegation and negative wrong-action, wrong-contract/version, wrong-supplier/scope, revoked/expired, missing-entry and stale/spoofed-identity cases to named test methods/subtests. Commit-time revocation belongs to PC-004.
* Decision route: Direct planner correction. Existing user direction already preserves named authority and permits fictional local engineering; no actual appointment or new user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Specify what establishes commitment and the exact date/version validity rules

* Related IDs: #90 criterion 1; RULE-007; C1, C2; P01-T01, P01-T02, P02-T01.
* Evidence: .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md:26 says "current review and source ordering" without defining either. .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md:42-43 lists metadata and two intervals. Manager lane:94-122 distinguishes a source string or supplier assertion from accepted commitment, future-effective delivery from future-issued evidence, and the exercise review trigger from contractual expiry.
* Concern: A committed label plus populated source fields can still be only a decorated free-text assertion. The plan does not specify the bounded acceptance record tying that source/version to the named accepting manager and contract/call-off version. It also leaves the clock, future issue/review dates, exact freshness boundary, interval inclusivity and source supersession/conflict behavior unspecified. These are consequential validation rules, not cosmetic field names.
* Impact: An offered-only or stale/mismatched source can still unlock work; alternatively a legitimate future delivery interval may be rejected because evidence issue time and delivery time are conflated. Different surfaces/tests could implement different meanings of confirmed capacity.
* Smallest useful change: Define a small fictional commitment/acceptance record with a resolvable local fixture reference/version, named accepting actor/action/time and matching contract/call-off version. State that this is exercise evidence, not signature or legal verification. Pin source-issued/recorded/reviewed ordering, the chosen clock and exact review-due rule, inclusive delivery bounds, and when replaced/conflicting/unknown evidence fails closed. Apply the same contract at issue/reissue/booking/correction/advance. Keep one home-work-order per exact case/scope allocation and record known zero/loss independently of readiness. Do not import the manager lane's broader resource/financial evidence inventory into #90.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02 supplies the field/predicate table and example tiny fictional accepted source; P01-T01 names boundary subtests for offered-only, missing/unresolvable/superseded version, future issue/review, stale/due-day review, future-effective delivery, each interval endpoint, wrong case/unit/contract/scope and known-zero reduction. Tests assert both refusal and unchanged order/audit success state.
* Decision route: Direct planner correction. Explicitly label date/review choices as bounded exercise rules; do not claim new company policy or ask for unavailable live evidence.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Pin the positive advance contract and allocation-preserving lifecycle semantics

* Related IDs: #90 criterion 1; C2, C5; P01-T01, P01-T02.
* Evidence: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md:43,55 requires advance to recheck quota/evidence but supplies no positive transition contract. Details:19 tests the bypass without stating what makes advance valid. src/core/src/zava_forward/core/store.py:514-528 changes the case to Install booked without selecting an order or checking an appointment. src/core/src/zava_forward/core/procurement.py:_committed_used counts Issued/Appointed/Completed; reissue/booking/correction operate on an already-counted order. The manager lane:124-135 warns against silent quota recycling.
* Concern: Merely requiring some order or some capacity does not establish which current order/date authorizes a booked case. Reusing the new-issue quota check for an existing reservation would also reject valid booking/reissue at exactly full capacity. Withdrawal currently releases quota by state alone; the candidate neither preserves an explicit release rule nor specifies how release/history prevents unexplained reallocation.
* Impact: Advance can still confirm an unbooked/stale order, or a correct one-allocation flow can become unusable at its quota. Withdrawal/reopening behavior may unintentionally recycle capacity or change existing lifecycle semantics.
* Smallest useful change: Define how advance selects an unambiguous current case order and requires its current authorized booking and delivery date, while creating no order or second reservation itself; fail closed for missing/ambiguous/withdrawn/stale orders. Distinguish a new allocation from revalidating an existing counted reservation: at quota, a valid existing allocation can progress; in deficit, new progression is blocked without preventing loss recording or safe withdrawal. State the existing-order release/reissue/correction rules explicitly, retain completion consumption, and record any permitted release with actor/reason/version rather than silently changing consumption.
* Action owner: Planning parent.
* Exact resolving evidence: Revised details contain a short operation/state/allocation table. Named tests/subtests cover advance without order, with issued-but-unbooked order, a valid booked order at quota, expired or out-of-interval booking, ambiguous/stale/withdrawn order, reissue/correction without double counting, completion retaining quota, deficit refusal and the chosen auditable withdrawal/release rule. The valid at-quota path must pass, not just all negative bypass tests.
* Decision route: Direct planner correction within the existing home-order exercise model. No new scheduling service, resource model or user policy decision is required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Lock deterministic commit-time race and rollback acceptance tests

* Related IDs: C5-C7; P01-T01, P01-T02, P02-T02.
* Evidence: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md:49-50,55,73 and details:28 identify the right locks and rechecks but do not assign specific interleavings. src/core/src/zava_forward/core/sqlstore.py:_proc_write skips unchanged documents; therefore an advance that only reads procurement does not gain procurement CAS protection automatically. _finish can append pending audit after an unsuccessful operation, while generic save exceptions do not follow the ConflictError/GateError discard path. Existing src/core/tests/test_quality_procurement.py:SqlFlows.test_two_processes_see_procurement_changes is sequential visibility, not a contested write test.
* Concern: A general "concurrent writers" assertion or inherited sequential parity suite cannot prove the promised read-dependency and authority rechecks. The candidate also does not pin the failure oracle across cached procurement/cases, pending success audit, persisted state and subsequent reopen/retry.
* Impact: Advance can commit after another writer withdraws/rescopes/reduces its authorizing order/capacity; an authority revocation may race issuance; a refused write can leak a version, case mutation or success audit. These are central criterion-1 failures even when ordinary quota CAS tests pass.
* Smallest useful change: Assign deterministic two-store synchronization points after initial validation and before writer-transaction validation. Cover competing issuance for the last allocation; advance versus withdrawal/rescope/capacity loss; issue versus staff/delegation revocation; and injected persistence failure after local mutation. Assert one permitted allocation maximum, appropriate conflict/refusal, no losing transition/version/success audit, restored local cache and durable state on reopen, and a clean subsequent operation. Reuse current CAS, locks and opt-in SQL Server factory; add no production test framework.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 names the race methods, synchronization points and expected winner/loser outcomes; P01-T02 identifies the narrow read-dependency/authority validation hooks and cleanup path; P02-T02 names SQLite selectors and corresponding inherited local SQL Server selectors. SQL Server unavailable must be recorded as Not run, never counted as passed parity.
* Decision route: Direct planner correction. Required behavior is already selected; this does not require cloud access or an operational approval.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Make the claimed test and canonical-target lock executable within 35 methods

* Related IDs: All four #90 criteria; P01-T01 through P03-T01; preservation of #78/#97.
* Evidence: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md:101-103 supplies two basenames, generic migrated Python/JS targets and categories of validation, but no complete target/selector/command inventory. Details:41 likewise says focused suites and component lint/format/types. The actual SQL Server factory/wipe is src/api/tests/test_mssqlstore.py:26-36, not the two owned procurement test files. Existing lifecycle expectations in src/core/tests/test_quality_procurement.py assume only three versions, and its capacity test expects reductions below obligations to fail. Existing src/api/tests/test_role_matrix.py has coupled capacity fixtures and package 403 assertions.
* Concern: The document calls ownership, targets and validation locked while leaving the SQL inheritance location, coupled fixture edit boundary, test-method budget allocation and invocation details unresolved. Generic "all-change" coverage could omit non-Booked appointment outcomes, detached-read mutation or offline draft-review no-write checks. Broad regression or lint commands chosen during implementation could unexpectedly trigger unavailable environments or force unrelated repairs.
* Impact: The implementer cannot execute the claimed lock reproducibly, demonstrate all four semantic criteria separately from preservation, or establish that required coverage fits the fixed 35-method cap without removing/weaking existing assertions.
* Smallest useful change: Add one compact task-owned manifest to plan/details, not a new artifact: full canonical source/test/document paths; which existing fixture owners receive prerequisite-only changes; exact new method names/count by owner with subtest dimensions; inherited SQL class location; exact cwd, task-owned interpreter, import paths, unittest selectors, configured Ruff/format/mypy invocations, JS syntax command and local fictional browser action/assertions. Name the existing #78 provenance/bulk and #97 form suites explicitly. Preserve every existing test; change only obsolete prerequisite/expectation assertions necessary for new semantics, including the reduction test and sequential version count. Keep existing package HTTP denial. Record skips/Not run separately and do not remove exclusions or broaden mypy/lint scope merely to claim coverage.
* Action owner: Planning parent, retaining the parent-owned test allocation and the existing coupled-fixture ownership.
* Exact resolving evidence: A single manifest assigns no more than 35 new test method definitions, with inherited executions distinguished from new definitions and zero removals. It maps every #90 criterion to concrete positive/negative assertions, including every successful work-order mutation and rejected-write immutability, stable actor/delegation snapshots, detached nested return values, two contractors across direct/HTTP reads and writes, and offline template/AI-proposal/review with no procurement side effects. Commands identify exact migrated paths, standard opt-in SQL harness and task-owned local-only environment. Changed UI checks require current guideline retrieval and a local fictional browser; unavailable checks remain explicit limitations.
* Decision route: Direct planner correction. The user already fixed ownership, removal policy, maximum additions, local-only boundary and preservation requirements.

## Strengths and Residual Risk

* Existing procurement storage, JSON locking and SQL CAS/writer-lock architecture are retained. No per-row schema migration, replacement service, framework, mvp edits or generated-asset workaround is proposed.
* All work-order mutations, not only scope changes, are explicitly included in the requirement. Stable email/name, versioned authority/capacity snapshots and detached returned records are correct directions.
* Structured source/version/case/unit binding, fail-closed legacy reads, scope invalidation and recording real capacity losses rather than rejecting them are materially stronger than the existing passing suite.
* Direct package isolation and the two-contractor matrix close a concrete boundary without granting contractors new write or package access.
* Draft/review no-execution is separated from named human instruction authority. A literal not-an-instruction marker must remain on offline outputs without adding a send route or paid model call.
* Human permissions, company evidence, resource-productivity conversion, contractual/legal acceptance, hosted AI/Azure and full human/WCAG acceptance remain unknown and outside local engineering acceptance. None is a prerequisite for tiny fictional tests.
* The manager's recommendation to seek owner acceptance of fictional issuer fixtures is not treated as a new gate: the caller has already authorized local fictional data, not live permission. Broader manager recommendations do not silently expand #90.

## Questions or Blocking Evidence Gaps

* No user question or decision-critical missing live evidence blocks planning corrections.
* All five findings are direct planner corrections. No significant or divergent user decision is requested.
* Local SQL Server availability at implementation time is conditional. Its absence must produce a disclosed Not run result, not invented parity acceptance.

## Limitations

* This is a planning credibility assessment, not implementation Review, test execution, accessibility conformance, operational approval or legal review.
* The research's reported 21-test baseline and prior browser/guideline work were read as supplied evidence, not rerun or freshly certified.
* Source inspection was bounded to the supplied requirement/research pointers and the existing component contracts needed to assess executability. No open-ended research, new agents, service startup, private-dataset read or remote mutation occurred.
* Only this critique artifact was authored. Plan, details, research, manager lane and all application/test sources remain unchanged. Exactly one final-candidate critique was executed; no later findings are intentionally withheld for another pass.

## Recommended Next Action

* Highest-impact finding: PC-004, because an unchanged procurement document does not protect a case-only advance from commit-time dependency changes.
* Action owner: Planning parent.
* Smallest next action: Revise the existing P01 details with the deterministic race/rollback matrix, then disposition PC-001 through PC-005 together and lock their bounded contracts, targets and tests before implementation.
* User response required: No.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md | Final candidate assessed once; unchanged. |
| .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md | Task contracts and validation lock needing direct planner correction; unchanged. |
| .copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md | Supplied C1-C7 research evidence; unchanged. |
| .copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md | Supplied independent manager research instrument, not approval; unchanged. |
| .copilot-tracking/reviews/plans/2026-10-17/provider-capacity-controls-90-plan-critique.md | Complete single-pass critique and actionable disposition set. |

## Next Steps

Return Complete / Revise to the active planning parent. The parent directly dispositions PC-001 through PC-005, revises and finalizes without another critique, and proceeds only within the confirmed RPI gates and fixed scope. No user response is required. This critique stops after this report; no implementation or peer stage is invoked.
