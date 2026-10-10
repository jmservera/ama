---
title: RPI Plan Critique - Proper Warm Exercise PoC Rebuild
description: Single final-candidate credibility assessment against the accepted exercise baseline
ms.date: 2026-10-10
---

## Metadata

* Task ID: exercise-poc-rebuild-2026-10-10
* Critique date: 2026-10-10
* Plan: .copilot-tracking/plans/2026-10-10/exercise-poc-rebuild-plan.md
* Phase details: .copilot-tracking/details/2026-10-10/exercise-poc-rebuild-phase-details.md
* Critique execution status: Complete
* Candidate: final candidate, assessed once; no nested critique or repeat requested.

## Inputs and Criterion Boundary

* Caller direction: merge the accepted PRD and rebuild end to end. The caller records PR 57 merged at 5a6ec60f885a3e207b6984a725870a48e0d4cf99 and a passing baseline unit suite. Those are supplied observations, not newly executed checks.
* Requirements: docs/prds/proper-warm-retrofit-programme-demonstrator.md, accepted v0.12.0, including FR-001 through FR-046, AC-001 through AC-056, NFR-001 through NFR-013, goals, constraints and the exact Exercise Acceptance Contract.
* Assumptions: docs/case_study_48_addendum.md, EXA-001 through EXA-016, numerical oracles and four-week evidence plan; docs/case_study_48_original.md supplies preserved framing.
* Research: .copilot-tracking/research/2026-10-10/system-one-decision-models-research.md, particularly W2/W3, provider-contract conflicts, authority limits and serving uncertainty. Historical research recommendations do not override the subsequently accepted PRD.
* Baseline evidence: mvp/README.md, .github/workflows/mvp-ci.yml and bounded inspection of mvp/properwarm_mvp/ai.py, ai_tasks.py, factory.py, documents.py, store.py and workflows.py. Knowledge-base index, memory and housing-association primer supplied context, not company validation.
* Decisions: manual mode remains in force; the owner's direct rebuild instruction authorizes implementation after the planning gate. No resource creation, live calls, billable inference, external submission/payment or real-data processing is authorized.
* Boundary: correctness, implementation readiness, exact acceptance rather than proxy tests, practical domain/provider/fixture isolation, and truthful approval/results. This is not an implementation review, independent reproduction of the baseline suite, legal-currentness assessment or deployment verification.
* Frozen constraints: retain existing tests and CI gates, remove no tests, preserve named ownership and the plan's runtime/test/fixture addition ceilings. Findings below can be corrected by assigning work in existing integration targets and existing allocated tests/manifests, without increasing those ceilings.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner authority; merge prerequisite; EXA-001/012; P01/P06 | Covered | Supplied merge and baseline evidence; implementation authority is distinct from live-call authority. No new company ratification is needed for fictional exercise design. |
| FR-001/002/012/029/035; NFR-005/008; EXA-002/003/013; P01/P04/P05 | Partial | Fictional lead/sibling, cohorts and scale populations are separated in intent, but startup can still resolve the legacy private-data seed. PC-005. |
| FR-003 through FR-011/025/026/030/032 through FR-034; NFR-003/004/010/013; P01/P05/P06 | Covered | Service rights, distinct identities, no-self-approval, versioned chronology, exact denials and regression retention are explicit. Implementation still must prove every applicable action. |
| FR-014/015/031/033/045/046; EXA-004/005/008/014; AC-018/038/055/056; P05 | Partial | Resident choice and isolated withdrawal are explicit. Reuse overlooks a baseline workbench-owned hazard release operation that conflicts with the accepted read-only external authority. PC-002. |
| FR-013/016 through FR-019/041/042; EXA-007/010/015; P02/P05 | Covered | Separate technical/QA/provider/Finance evidence, version-bound application and claim records, deterministic arithmetic and no export-to-cash implication are specified. The P01 map must bind the referenced fixture values to implementation tests. |
| FR-036/037/044; AC-044/045/052/054; EXA-016; research W2/W3; P03/P05 | Partial | Dedicated scoring, allowed candidates, abstention and no rationale are sound. Existing generative entry points need a shared authorization/registry gate, and generation has no explicit evidence-contract work owner. PC-001/003. |
| FR-038 through FR-043; AC-046 through AC-053; P02/P05 | Partial | Schema, candidate, review, protected-field and stale-set contracts are explicit; actual readable-source parsing and its independent raw-source oracle are not assigned. PC-004. |
| FR-020 through FR-024; NFR-007/012; EXA-009/013; P04/P05/P06 | Covered | Four exact arrays, six scenarios, independent outcomes, separate stage pools, unknown-input abstention, as-of/denominators and complementary suppression are retained. |
| NFR-001/002/006/009/011; EXA-011/012; P06 | Covered | Exact core/scale shapes, samples, durations, restore/restart/RPO, accessibility and AI/effort gates are retained, with honest Not run/Blocked disposition. Existing timing/browser tests are explicitly not substitutes. |
| GOAL-001 through GOAL-004; AC-043; four-week delivery; P01 through P06 | Covered with findings | Connected same-home delivery, regression CI, report and PR are planned. Deferred representations and unavailable inference must remain unmet full-MVP evidence, not completed acceptance. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 3; Medium 2; Low 0.
* Rationale: The reuse strategy and acceptance boundaries are credible, but safe launch and several required contracts remain implicit despite concrete conflicting legacy behavior. Correct the five gaps before implementation handoff. No significant or divergent user decision is needed to resolve them.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Existing inference paths lack a planned shared fail-closed authorization gate

* Related IDs: FR-036/044, AC-044/052/054, EXA-012/016, P01-T01/P03-T01/P05-T01.
* Evidence: Phase details P03 restricts inference to approved registry tasks, but owns decision.py and registry/provider tests only; P05 does not assign enforcement at existing generative dispatch. mvp/properwarm_mvp/ai.py enables inference when AI_ENDPOINT exists; ai_tasks.py calls existing text/document transports, with workflow-only handling dependent on mode or PW_AI. The caller explicitly authorizes no live calls.
* Concern: A disabled Decision adapter does not prevent an existing generative action from making a live call under inherited configuration. Registration alone also does not ensure unapproved legacy tasks cannot call a provider. This is an implementation-readiness gap, not evidence that a call occurred.
* Impact: Local integration/browser validation could use an unauthorized endpoint, or exercise an unregistered task, while appearing to respect the new adapter's disabled state.
* Smallest useful change: Assign the primary P05 implementer a common pre-transport guard for all inference entry points. Require explicit exercise enablement and the registry's task/capability/source permissions; default to disabled/manual under this task's authority. Document separate future live prerequisites, including authorization, access/processing/cost evidence, quota and cost-pause conditions. Do not enable live calls during this rebuild.
* Action owner: Planning parent for the task amendment; primary integrator for the common guard; P03 owner supplies registry contracts.
* Exact resolving evidence: Amended P01/P05 details assign the guard and a denied-call matrix. Allocated provider/integration tests use injected transports and assert zero calls for inherited endpoint configuration without authorization, unregistered/unapproved tasks, wrong capability and disabled/throttled assistance; manual completion remains possible. No real endpoint is used.
* Decision route: Direct planner correction. Future live authorization is a separately unresolved prerequisite, not a user decision required to finish this plan revision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Legacy hazard release conflicts with the accepted external-authority boundary

* Related IDs: FR-015, AC-018/038/054, EXA-005/008, P01-T01/P05-T01/P06-T01.
* Evidence: The accepted PRD makes external hazard classification/clock/closure and authoritative release evidence read-only to the workbench. mvp/properwarm_mvp/workflows.py, raise_hazard/record_repair/release_hazard, instead stores classification/repair state and permits a Safety role or manager to set released=True after its own repaired/no-self-approval checks. mvp/README.md describes that workflow as reusable; phase details P05 has no explicit adaptation for it.
* Concern: Independent humans inside a workbench release action do not make that action an external authoritative release reference. Generic regression retention could preserve the conflicting operation in the exercise.
* Impact: The same-home journey could demonstrate apparent safety clearance that the accepted workbench is specifically prohibited from authorizing.
* Smallest useful change: Assign P05 an exercise-specific distinction between editable referral/follow-up records and read-only, evidence-linked external hold/release decisions. Deny workbench classification, closure and release authority in the exercise. Record supplied fictional external decision evidence through an authorized reference-recording action, not a sufficiency decision. If legacy behavior is preserved for compatibility, isolate it from the accepted exercise entry points and do not count its tests as AC-038 evidence.
* Action owner: Planning parent and primary integration implementer.
* Exact resolving evidence: P01 capability map and P05 details explicitly identify the baseline mismatch and adaptation. Integrated API/browser tests deny workbench-owned release/classification/closure without changing the prior state; separate fictional external source/authority/version references remain inspectable, referral receipt and acceptance stay distinct, and human intake continues independently of AI. Existing tests are retained; tightly coupled expectations may change only as already permitted by the frozen plan.
* Decision route: Direct planner correction; the accepted PRD already resolves the authority choice. No legal or company approval is fabricated.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Required generative inference evidence has no explicit implementation owner

* Related IDs: FR-027/028/036, NFR-009, EXA-016, GOAL-004, P03-T01/P05-T01/P06-T01.
* Evidence: Plan goals retain real scoring and generation, but P03 covers only the Decision transport. Phase details P05 wires forms/forecast/finance without assigning generative evidence changes. Baseline ai.py returns text plus a deployment name, and _chat discards the rest of the provider response; ai_tasks.py supplies a generic prompt version and comparison record. The PRD requires source-bound narrative plus actual request/model identity, versions, usage, latency, errors and protected cost evidence.
* Concern: Reusing the existing text generator cannot by itself meet the new provenance/evaluation contract. Merely listing live inference as Blocked in P06 leaves the local implementation of that contract unowned.
* Impact: Later authorized generative evaluation could not reconstruct provider identity/usage or compare complete task costs, despite successful text production. Conversely, a template fallback could be mistaken for evidence of model execution.
* Smallest useful change: Assign primary P05 ownership of changes to existing ai.py/ai_tasks.py and result persistence for the registered source-bound narrative task. Preserve provider response metadata, permitted citation binding, per-task versions, explicit failure/fallback and provenance; keep provider-success status distinct from template availability. Reuse allocated tests and existing modules rather than adding a second provider module.
* Action owner: Planning parent; primary integration implementer, consuming the P03 registry.
* Exact resolving evidence: P05 has a named generative contract target and P06 separates scoring, screening and narrative results. Injected response tests prove metadata retention, rejected unsupported citations, unavailable/manual distinction and restart/export fidelity. Actual-platform success remains Blocked until a separately authorized real run supplies its required records.
* Decision route: Direct planner correction; no provider purchase, resource creation or live test is requested.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Candidate storage is planned, but readable-source extraction is not assigned

* Related IDs: FR-039, AC-047/053, NFR-008/009, P01-T01/P02-T01/P05-T01.
* Evidence: P02 defines candidate lineage and owns forms.py/test_forms.py; its completion list does not name raw-source parsing. P05 wiring does not assign it either. Baseline documents.py stores bytes; ai.py look_at summarizes text/images and explicitly stores other file types without reading them. Neither is the source-span/table candidate extraction required by the PRD.
* Concern: Tests can construct lineage-bearing candidates directly and pass all candidate selection checks without extracting any value from readable text/table evidence. A provenance-shaped record is not proof that its raw value/hash/locator matches the supplied source.
* Impact: The assisted subsidy-form journey could remain a hand-authored candidate demonstration, not the required extraction/selection/filling path; parser error propagation and unreadable/manual handling would remain untested.
* Smallest useful change: Assign bounded deterministic text/table extraction to forms.py under P02, with authorized source retrieval integrated by P05. Freeze supported formats and a manual path for unsupported/unreadable inputs in P01; no OCR/vision purchase is needed. Test extraction from independent source bytes, not only prebuilt candidates.
* Action owner: Planning parent; P02 forms implementer for extraction semantics; primary integrator for retrieval permissions.
* Exact resolving evidence: Amended details name supported text/table inputs and the extractor contract. Allocated form tests independently assert raw value, source hash/version, locator and parser version from source bytes, retained conflicting EPC alternatives, explicit unreadable-scan/manual state, and rejection of cross-home/restricted evidence and embedded instructions. Integration demonstrates those extracted candidates entering the same-home draft.
* Decision route: Direct planner correction within the existing domain/test budget.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: A fictional fixture does not yet guarantee an isolated exercise startup

* Related IDs: FR-001/035, NFR-005, EXA-002/003/012/013, P01-T01/P04-T01/P05-T01.
* Evidence: Phase details P01 correctly notes that factory defaults to JSON and excludes private geography; P04 supplies a fictional seed and says fresh SQLite state is generated separately. mvp/properwarm_mvp/factory.py still resolves PW_DATA to mvp/data/properwarm.json unless explicitly overridden, including when PW_STORE selects SQLite. Thus choosing SQLite alone does not choose the fictional seed.
* Concern: No phase explicitly owns the exercise launcher/factory contract that rejects the legacy seed, an existing incompatible database, or an external document backend. Fixture creation and store selection can succeed individually while the actual workbench opens unrelated persisted data.
* Impact: The browser may display or import private-geography records, invalidate same-home acceptance evidence, or route fictional evidence into an inherited external backend contrary to local-only scope.
* Smallest useful change: Assign P05 an explicit exercise startup/configuration contract using the versioned fictional manifest, fresh named SQLite state and local evidence storage. Validate fixture identity/version before opening or reseeding state; reject incompatible existing state rather than silently mixing or overwriting it. Use caller-compliant scratch/session paths, not forbidden temporary directories. Preserve the legacy launcher separately where compatibility requires it.
* Action owner: Planning parent; primary integration implementer, with P04 supplying the manifest and fictional seed contract.
* Exact resolving evidence: Amended P01/P05 details name the startup configuration and refusal rules. Allocated integration tests start with inherited PW_DATA/backend settings and incompatible existing state and prove rejection or safe explicit override without accessing the private fixture or external backend. Fresh startup, restart and export identify only the accepted fixture version and wholly fictional lead/sibling/cohort populations.
* Decision route: Direct planner correction. No permission to inspect private geography or migrate existing working data is needed.

## Strengths and Residual Risk

* Reusing existing domain controls and SQL persistence is more credible than discarding tested behavior. Disjoint forms/scoring/forecast ownership and primary-owned integration provide a workable parallel boundary.
* Exact field/stale-set, forecast-array and lifecycle oracles are required; the forecast deliberately separates install and QA resource pools and analytical versus scale populations.
* The candidate explicitly preserves test removal count zero, existing unit/API/SQL/image gates and honest workload reporting. Browser smoke, mocked inference and generated scale data are not accepted substitutes for prescribed checks.
* Funding application, award, claim, cash and provider payment remain independent; protected human fields and per-field review cannot be replaced by a probability.
* Remaining unavailable Decision 1 access, pricing/processing verification, adjudicated labels and paired human effort evaluation are already disclosed. They block corresponding acceptance/activation, not fictional implementation. Recording Blocked is truthful reporting, not satisfaction of GOAL-004.
* Engineering scripts may reach expected safe blocks, but deferred labels never satisfy the full MVP's missing workflow capabilities. P06 must keep per-check status and full-baseline completion distinct.

## Questions or Blocking Evidence Gaps

* No additional user answer is required for these five corrections. Approved EXA assumptions resolve fictional company facts, role fixtures, finance rules and thresholds.
* Live scoring/generation and real human evaluation remain prerequisite-blocked as supplied. Do not manufacture labels, approval, successful inference, benefit or full completion to close them.

## Limitations

* No implementation, test, browser session, model call, resource operation or external research was executed during this critique.
* Baseline code inspection was bounded to the plan's reusable-control, source/provider and launch interfaces. It is not a complete repository or vulnerability audit.
* This report is the complete actionable finding set for the supplied boundary. Other requirements have planned coverage, not independently verified implementation.
* Plan, phase details, accepted PRD, addendum, research and all other sources remain unchanged. Only this caller-specified report was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Amend P01/P05 to own the common fail-closed inference gate; fold PC-002 through PC-005 into the same direct revision, retaining frozen ownership ceilings and zero test removals.
* User response required: No.
* Handoff: Return Revise to the planning parent. Resolve and record dispositions for all five findings, finalize without another critique, then use the owner's existing rebuild instruction for implementation after the gate. Remain manual and leave live/resource authorization unchanged.

## Next Steps

The active planning parent should make the five direct corrections and finalize the candidate without a repeat critique. No user action is required. This critique stops after the report; it does not implement or advance a peer stage.
