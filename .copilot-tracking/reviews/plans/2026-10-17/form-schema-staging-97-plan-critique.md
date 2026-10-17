---
title: Final-candidate plan critique for issue 97
description: One bounded assessment of form schema registration and candidate staging
ms.date: 2026-10-17
---

## Metadata

* Task ID: 97
* Task slug: form-schema-staging-97
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/form-schema-staging-97-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/form-schema-staging-97-phase-details.md
* Research: .copilot-tracking/research/2026-10-17/form-schema-staging-97-research.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate critique; no implementation or second critique.

## Inputs and Criterion Boundary

* Caller direction permits one ordered delivery loop for exact FR-038/039, using the existing core/API/JSON/SQL architecture. Parent #96 is hierarchy; #105 already supplies the AI registry. No private data, live AI/Azure/SQL, new services/UI or #98 review/pack workflow is authorized.
* The supplied final candidate intentionally implements only unapproved registry and candidate collection. Actual approved-template preparation remains unmet. A Refs #97 PR must preserve that distinction and must not close the issue or imply full acceptance.
* Read the complete supplied research, plan and phase details. Consulted their specific evidence pointers in docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/case_study_48_addendum.md, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/projection.py, src/core/src/zava_forward/core/ai_registry.py and src/api/src/zava_forward/api/server.py. Also read the required original case study, reference-index routing, memory and customer-primer context.
* Assessed requirements, alternatives, dependencies, phases P01-P03, tasks P01-T01/P02-T01/P02-T02/P03-T01, acceptance limits, permissions, provenance, persistence and validation together.
* The branch is feat/form-schema-staging-97. Existing untracked planning/session artifacts were present and left untouched. This critique writes only its specified output.
* This is a plan credibility assessment, not implementation verification, security certification, source-authority approval or full PRD acceptance. Issue facts W1-W4 are supplied research evidence, not independently refreshed remote findings.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller scope and one-loop control | Covered | Exactly one critique, bounded backend slice, Refs-only handoff and no merge/rebase/force-push. |
| FR-038 / AC-046 | Partial by explicit decision | Unapproved registry is a useful foundation, not approved form binding; schema association/policy representation needs PC-002. |
| FR-039 / AC-047 | Partial by explicit decision | Candidate imports, alternatives, source hashes and manual recovery are planned; precise processing/locator provenance needs PC-003. No extraction-engine positive path is claimed. |
| FR-039 / relevant AC-053 permissions | Partial | Staff/document/Finance checks are named, but field-level and retained-output disclosure rules need PC-001. #98 selection/review checks remain deferred. |
| C2 / accepted exercise baseline versus form authority | Partial | No approved form evidence exists, but the supplied addendum explicitly records PRD exercise-baseline acceptance; PC-005 separates these facts. |
| W2/W4 / FR-036 dependency | Covered | Existing registry reused; no new AI capability or provider invocation. Neither parent hierarchy nor a future selector blocks this collection slice. |
| P01-T01 / test ownership | Partial | Two exact external test files and fail-before evidence are appropriate. Add targeted permissions, payload/provenance and failed-save cases under PC-001 through PC-004 without adding files. |
| P02-T01 / immutable registry and candidates | Partial | One forms.py module, checked shared documents, case-body versions and defensive copies are credible. Input-policy ambiguity and recovery proof remain. |
| P02-T02 / HTTP, projection and documentation | Partial | Endpoint paths, authentication, status families, component docs and generic-detail exclusion are explicit. Current field permissions must cover the dedicated output too. |
| P03-T01 / persistence and regression evidence | Partial | Reopen, second-process sync/conflict, real loopback HTTP and existing suites/checks are planned. Non-conflict failure recovery needs PC-004. |
| FR-040 onward / #98 | Covered as excluded | No acceptance, deterministic form validation, reviewed pack, export or stale-propagation workflow should be added to resolve this critique. |
| Live-platform and full acceptance claims | Covered as unavailable | SQLite and loopback evidence cannot establish actual SQL Server/Azure/model execution, human approval or full AC-046/047/053. |

## Verdict

* Verdict: Revise
* Severity summary: 1 High, 4 Medium, 0 Low, 0 Critical.
* Rationale: The bounded delivery is adequate in principle and does not require a new user decision. Its explicit acceptance exclusions are honest. Before implementation, tighten the source/field disclosure contract, schema/provenance representation and fault-test commitments. Correct the PRD authority distinction so an already accepted planning baseline cannot become an invented prerequisite.
* This verdict does not require actual template approval before unapproved collection, a synthetic approval fixture, a new approval workflow or a second critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Staff/document access alone does not define candidate field disclosure

* Related IDs: FR-039, relevant AC-053, C7, P01-T01, P02-T01, P02-T02.
* Evidence: .copilot-tracking/plans/2026-10-17/form-schema-staging-97-plan.md:45-50 names source-kind policy and Finance restrictions. .copilot-tracking/details/2026-10-17/form-schema-staging-97-phase-details.md:45 names staff/document/Finance checks and excludes generic-detail leakage. src/core/src/zava_forward/core/store.py:575-577 makes document access a broad staff-role check. src/core/src/zava_forward/core/projection.py:130-165 separately protects resident records, adjustment reasons/free text and financial fields.
* Concern: The dedicated candidate response contains arbitrary source-derived raw values, but the plan does not specify its relationship to the existing field-level resident/reason permissions. Hiding form_staging from generic detail is necessary but not sufficient. It also does not explicitly require current authorization on retained candidate reads, independently of the importing actor's historical permission. This is a missing contract, not a demonstrated implementation vulnerability.
* Impact: A new raw-value endpoint could bypass existing field projection while passing a staff-role and non-Finance-source check. Merely labeling schema policy Unapproved does not grant disclosure rights.
* Smallest useful change: Specify a server-enforced source/field read-and-stage policy using existing rights. Caller-defined schema policy may narrow, never widen, those rights. Deny fields whose safe permitted disclosure cannot be established; do not claim free-text redaction. Apply the policy to POST, GET and returned source/locator metadata and recheck the current requesting role. Preserve historical candidates without implementing #98 stale propagation. Add explicit non-Finance, resident/reason-restricted, contractor, unknown-role and permission-change read tests, plus generic-detail/error/audit non-disclosure checks.
* Action owner: Planning parent, for P01/P02 contract and test revisions; implementer executes the existing permission hooks.
* Exact resolving evidence: Plan/details name the field/source policy and read-time enforcement point; the two owned test files specify allowed and denied raw-value/metadata expectations, including an initially permitted retained batch requested by a subsequently disallowed role. Test outcomes must later show no disclosed prohibited value and no unauthorized write.
* Decision route: Direct planner correction. Existing least-privilege direction resolves the decision; no new human permission ratification is a prerequisite to deny-by-default collection.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The schema policy input contract leaves important FR-038 distinctions implicit

* Related IDs: FR-038, AC-046 foundation only, P01-T01, P02-T01, P02-T02.
* Evidence: .copilot-tracking/plans/2026-10-17/form-schema-staging-97-plan.md:45 lists schema metadata but omits explicit funding-association representation; line 46 prohibits caller-set source authority while phase details line 36 permits schema source-authority policy. Line 50 requires human-only prefill denial without specifying how the immutable field contract identifies those fields. docs/prds/zava-forward-retrofit-programme-demonstrator.md:873 and AC-046 distinguish evidenced funding scheme/route from non-funding not-applicable association.
* Concern: A versioned schema needs an unambiguous declarative contract before independent fail-before assertions can be written. It is currently unclear which source-policy fields a registrant may supply versus which authority assertions are forbidden, how mandatory human-only categories are represented/enforced, and how funding/unknown/not-applicable association is retained without claiming approval.
* Impact: Implementations could reject necessary policy metadata, accept authority-bearing overrides, or lose the funding/non-funding distinction required for later exact-version binding. A caller-supplied generic prefill flag must not authorize declarations, signatures or controlled approvals.
* Smallest useful change: Pin the accepted schema keys and minimal invariants in P02 details: explicit funding applicability with scheme/route/evidence references or Unknown, explicit not-applicable for non-funding forms, declarative source-kind/precedence/evidence policy, and server-enforced human-only field categories. Separate supplied policy/reference metadata from server-assigned approval, actor and trust state. Conditions and rule references remain data, not executable rules. Missing authority remains Unknown/Unapproved, not a registration approval gate. Define exact-version duplicate/conflict behavior without adding draft preparation.
* Action owner: Planning parent.
* Exact resolving evidence: A compact schema payload contract and rejection/unknown-state matrix in the existing details, mirrored by independent fixtures in src/core/tests/test_form_staging.py and endpoint tests in src/api/tests/test_form_staging_api.py. Include funding Unknown, non-funding not-applicable, protected-field denial and attempted approval/identity override.
* Decision route: Direct planner correction within the agreed FR-038 foundation. Actual authority acquisition and approved-template binding remain deferred; no user response is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Verified location and asserted processing lineage need separate defined contracts

* Related IDs: FR-039, AC-047 foundation, P01-T01, P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/form-schema-staging-97-plan.md:47-49 requires copied parser/model metadata, exact text offsets/CSV cells and unverified OCR imports. Phase details:38 preserves imported route/version/model/error metadata. C4's actual document record in src/core/src/zava_forward/core/store.py:605-606 contains upload hash/version/scan, not an attested parser/model execution record.
* Concern: The plan correctly labels OCR lineage unverified, but does not distinguish importer-supplied processing assertions from server-observed location verification for other routes. Text offset coordinates/encoding and CSV cell conventions are unspecified. An exact raw-value assertion is not reproducible across Unicode, quoting or newline differences until these conventions are fixed.
* Impact: Candidates can retain apparently precise but irreproducible locators or appear to attest a parser/model that this implementation never invoked. Synthetic happy-path text tests could pass despite incorrect source binding on real uploaded byte structures.
* Smallest useful change: Define the bounded locator convention, decoding policy, CSV row/column/header behavior and raw-value meaning. Record server-generated verifier identity/version and verification result separately from supplied importer/parser/OCR/model assertions; never copy a client's assertion into a server-attested execution field. Keep unsupported/decode failures as owned recovery without invented values. Clarify that deterministic text/CSV verification parses bytes locally while parser/OCR extraction-engine invocation remains out of scope.
* Action owner: Planning parent.
* Exact resolving evidence: Existing phase details state the locator and lineage contract; owned core tests use independent literal Unicode text offsets and quoted/multiline CSV expectations, invalid/out-of-range locators, duplicate alternatives, forged processing metadata and unverified OCR import cases. Later HTTP evidence returns the distinct supplied-versus-verified labels.
* Decision route: Direct planner correction; the planner can choose and document a simple deterministic convention without expanding services or asking the user.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Non-conflict save failures are not explicitly covered by the recovery tests

* Related IDs: P01-T01, P02-T01, P03-T01, persistence acceptance, C5.
* Evidence: Phase details:40 requires restoration after failed saves but names reopen, sync and controlled concurrent failure as the SQL test cases. Plan:60-61 names invalid-input atomicity and writer conflicts. src/core/src/zava_forward/core/sqlstore.py:579-586 discards local state for ConflictError/GateError but rolls back and rethrows other exceptions without that discard.
* Concern: The intended restoration contract is stronger than the explicit planned tests. Malformed-input refusal and optimistic conflicts do not exercise a database/audit write exception after in-memory registry/candidate mutation. An exception path could leave a value locally readable or eligible for a later unrelated save even though its original request failed.
* Impact: Audit/body inconsistency or a later accidental commit of a refused registration/batch would violate append-only provenance and atomicity despite passing the stated conflict tests.
* Smallest useful change: Add bounded fault-injection cases for a non-conflict save failure after mutation and a failure during the audit/write transaction. Cover registry and candidate paths, including existing JSON save restoration as applicable. Assert no success-shaped API result, no failed value in same-process reads, no durable failed body/audit entry after reopen, and no replay on the next unrelated successful save. Preserve the existing database exception rather than translating it to success/manual recovery.
* Action owner: Planning parent for explicit P01/P03 commitments; implementer for operation-local restoration through existing hooks.
* Exact resolving evidence: Test matrix entries in the existing details and tests confined to the two owned files. Later evidence must include injected non-ConflictError outcomes and independent before/after persistent-state checks, not only an exception assertion.
* Decision route: Direct planner correction. No store redesign, new test file or live SQL service is necessary.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: PRD planning acceptance must not be conflated with unavailable form approval

* Related IDs: C1/C2, research Wider synthesis, plan authority narrative and dependencies.
* Evidence: .copilot-tracking/research/2026-10-17/form-schema-staging-97-research.md says the caller's approved-PRD wording does not supersede frontmatter status and characterizes the addendum as assumptions rather than particular-form approval. Plan:21 repeats the in-review frontmatter caveat. docs/case_study_48_addendum.md, Owner-Approved Exercise Baseline, explicitly records owner acceptance of PRD v0.12.0 for exercise implementation planning on 2026-10-10, after review and corrections. That is separate from particular-form authority.
* Concern: The absence of a concrete approved template is supported, but treating the supplied baseline as only approved assumptions omits explicit recorded PRD planning acceptance. The frontmatter value alone does not invalidate that dated acceptance. Conversely, that historical baseline acceptance does not attest approval of every later revision or any actual form version.
* Impact: An inaccurate authority narrative can cause a later stage to invent a renewed PRD/human prerequisite or falsely treat general PRD acceptance as template approval.
* Smallest useful change: Correct the existing planning/research disposition to record the dated v0.12.0 exercise-planning acceptance, the current in-review frontmatter as a separate status fact, and the absence of particular approved-form evidence. Do not rewrite the PRD/addendum, seek a new signature or block this unapproved-only slice.
* Action owner: Planning parent.
* Exact resolving evidence: Consistent sentences in the existing research and plan distinguish baseline planning acceptance, particular template approval and operational release; dependencies still state collection may proceed and actual approved-template acceptance is unmet.
* Decision route: Direct planner correction from supplied evidence. No significant/divergent decision and no user response.

## Strengths and Residual Risk

* Reusing checked shared documents and row-versioned case bodies is credible within the one-new-core-module budget. Neither a new store nor a parallel AI registry is warranted.
* Server-assigned Unapproved state, immutable versions, alternative retention, metadata-only audit and defensive copies are appropriate collection controls. They do not establish that any candidate is correct or authoritative.
* The exact two-test-file ownership, no removals, independent expected keys/spans, fail-before evidence and component-suite regression checks are strong foundations. The findings extend those same files; they do not authorize more test modules or production modules.
* Keeping actual template binding, field decisions, reviewed packs, calculations and stale propagation unavailable preserves the caller's #97/#98 boundary. Current access enforcement is still needed and is not stale-propagation scope.
* Explicit manual recovery and source-store 502 distinguish unreadable input from infrastructure failure. Recovery ownership must be generated from the authenticated exercise context or an existing permitted role, not from invented external authority.
* The caller explicitly accepts this bounded engineering slice with actual approved-template acceptance unmet. A pushed Refs #97 PR is persistent delivery of that slice only. It must report which mechanical portions were exercised and leave full FR-038/039 and AC-046/047/053 acceptance open where unsupported.
* Existing SQL Server harness skips are valid disclosed limitations. SQLite evidence is not a live SQL Server/Azure guarantee.

## Questions or Blocking Evidence Gaps

* No user question or decision-critical blocker prevents the bounded slice.
* Real approved template/version, evidenced funding route and delegated authority remain unavailable, as already disclosed. Do not manufacture them or treat their acquisition as a prerequisite to registering Unapproved schemas and collecting permitted candidates.
* No new legal or regulatory currentness conclusion is made.

## Limitations

* No runtime code was changed or executed. No tests, HTTP service, private data, provider, Azure resource or live SQL connection were used.
* Reviewed only the supplied planning boundary and its specific local evidence pointers. Findings describe planning gaps, not confirmed exploitable implementation bugs.
* Local JSON/SQLite behavior, rollback handling, MssqlStore parity and endpoint failure semantics still require the planned implementation evidence.
* Source plan, phase details, research, existing reviews and session records remain unchanged by this critique.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define the deny-by-default field/source disclosure contract and retained-read checks, then disposition all five findings directly in the existing plan/details and add their cases to the two owned tests.
* Significant or divergent user decision: None. Current user direction resolves the scope and authority choices.
* User response required: No.
* After dispositions: Finalize the plan and continue P01 in the active ordered loop. Do not invoke another critique. Preserve the Refs-only, explicitly incomplete-acceptance PR boundary.

## Artifact References

| Artifact | Description |
| --- | --- |
| .copilot-tracking/research/2026-10-17/form-schema-staging-97-research.md | Supplied research and evidence disposition. |
| .copilot-tracking/plans/2026-10-17/form-schema-staging-97-plan.md | Final-candidate plan assessed once. |
| .copilot-tracking/details/2026-10-17/form-schema-staging-97-phase-details.md | Task contracts and validation expectations. |
| .copilot-tracking/reviews/plans/2026-10-17/form-schema-staging-97-plan-critique.md | Complete actionable finding set and handoff. |

## Next Steps

The active planning parent resolves PC-001 through PC-005 directly, records dispositions and finalizes without another critique. No user action is required. This critique stops after writing and verifying this artifact; it does not implement, mutate issues, commit or launch delivery agents.
