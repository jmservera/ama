<!-- markdownlint-disable-file -->

# RPI Plan Critique: rai-release-218

## Metadata

* Task ID: #218; children #219, #222, #223, #221 and #220.
* Critique date: 2026-10-27.
* Plan: .copilot-tracking/plans/2026-10-27/rai-release-218-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/rai-release-218-phase-details.md
* Critique execution status: Complete.
* Assessment: exactly one independent final-candidate critique; no delegated review.

## Inputs and Criterion Boundary

* Caller requirements: complete the ordered RPI loop for the bounded engineering slice, not whole-epic acceptance. Do not invent named human authority, evaluations, manifest approval or participant evidence. #222 evaluator implementation remains blocked pending approval of the corrected manifest; PR #421 is open, unmerged and unapproved.
* Supplied evidence: .copilot-tracking/research/2026-10-27/rai-release-218-research.md, including C1-C10 and W1-W6; the supplied plan and phase details; targeted current core binding, capture, ranking, checklist and lifecycle source; existing API release and assistant test definitions; PRD AC-069 to AC-073; ADR 0002's responsible AI control-plane section.
* Project context: docs/case_study_48_original.md, the opening/current-scope material in docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory is context, not acceptance evidence.
* Decision boundary: local synthetic tests only; no Azure, private datasets, secrets, participants or paid inference. No full or heavy changed gate is planned, following the explicit caller direction. Existing workflow names stay unchanged. No gate, deployment or human acceptance is inferred.
* Assessment boundary: whether the intended small binding correction covers the actual ranking/checklist dependencies, preserves unrelated bindings and lifecycle controls, and accounts honestly for remaining child scope. This is a plan credibility assessment, not implementation validation, a semantic evaluator or a fresh legal/currentness assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #219; C1-C4; P01-T02 | Covered | Reuse ranking.policy_hash(ranking.CURRENT) for stock and retained priority; explicitly resolve CURRENT during stock capture. Current source confirms both binding omissions and describe's default-bound policy. |
| #219; C5; P01-T01/T02 | Partial | Binding the checklist definitions and dispatch mapping is required, but the specified failing-first mutations cover CHECKLISTS, not the independent ordered keyword mapping. PC-001. |
| #219; lifecycle acceptance; P01/P02 | Covered | Fresh/queued denial, in-flight quarantine, ready/verified reliance denial, renewed constructed release and unusable historical release are explicit acceptance requirements. Existing lifecycle paths recheck runtime bindings; evidence must distinguish release denial from incidental source staleness. |
| Unrelated bindings, permissions and ordinary work | Covered | Plan requires unaffected capability bindings and case state to remain unchanged; no global registry/ranking rule change, real renewal or role grant is planned. |
| #222; W2; P02-T03 | Covered at blocked boundary | No evaluator, labels or report is implemented before manifest approval. PR #421 and unknown appointments are not substituted for approval. |
| #223; AC-070; P02-T01/T03 | Covered at engineering boundary | Scripted defect rejection/correction, provenance and an automation-bias negative control are planned. Competent human effectiveness and paired workflow-only effort remain unmet. |
| #221; AC-072; P02-T02/T03 | Covered at regression boundary | Existing suspension/continuity tests run; no real restart, appointment or witnessed drill is claimed. |
| #220; AC-071; P02-T02/T03 | Covered at regression boundary | Existing retained-priority challenge tests run; wider assistant/form coverage is explicitly unimplemented. |
| Validation and change limits; P02-T02 | Covered | Failing-first, focused tests, affected suites, Ruff/mypy and recorded skips/unavailable checks; maximum twelve new methods, no new dependencies or evaluator. |
| Review/publication; P03 | Covered | One independent implementation Review, preserved outcome, privacy-safe identity and Refs-only PR; #224/#440 and remaining child acceptance prevent epic closure. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The production approach genuinely addresses the identified dependency omissions without requiring unapproved evaluator work or human decisions. One bounded test-plan correction is needed so an implementation that fingerprints checklist definitions but omits their dispatch mapping cannot satisfy the planned regression evidence. No scope expansion or additional critique pass is required.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Independently prove checklist dispatch-mapping invalidation

* Related IDs: C5; #219; P01-T01; P01-T02; policy-binding acceptance criteria.
* Evidence: .copilot-tracking/details/2026-10-27/rai-release-218-phase-details.md, P01-T01 specifies patches to ranking.CURRENT and quality.CHECKLISTS. P01-T02 separately requires a checklist definition/mapping fingerprint. In src/core/src/zava_forward/core/quality.py, CHECKLISTS holds definitions while _KEYWORDS is a separate ordered dispatch table; checklist_for selects the first matching keyword and otherwise General. src/core/src/zava_forward/core/assistants.py captures only the checklists selected for the case. Its current runtime_binding omits both policy dependencies.
* Concern: Mutating CHECKLISTS does not prove that the fingerprint includes _KEYWORDS or preserves its order. A definition-only fingerprint could pass the specified failing-first mutation while a mapping-only policy change still admits fresh quality work under old release evidence. For cases whose selected checklist changes, source staleness could also conceal the missing release dependency.
* Impact: The explicit requirement to bind the actual quality dispatch policy would remain unproved, allowing precisely the fresh-admission gap this slice intends to close. This is an engineering proof gap, not missing human acceptance.
* Smallest useful change: Extend P01-T01 with an independent mapping-only mutation, keeping CHECKLISTS and its version labels unchanged. Include an order-only mapping change using overlapping keywords, because first-match order is semantic. Assert quality's policy_version changes and actual admission denies under the previously matching constructed release, even for a case whose selected checklist is unchanged. Check that other assistant bindings and every unrelated retained-path binding remain identical. Keep these cases parameterized within the existing twelve-method ceiling; do not change production mapping rules. Retain the already planned definition/content and lifecycle scenarios, asserting release-specific denial rather than counting source-stale rejection as release evidence.
* Action owner: Planning parent, revising P01-T01 and its validation expectations; implementing agent executes the resulting tests.
* Exact resolving evidence: Revised phase details explicitly name the mapping-only and order-sensitive cases. Subsequent implementation evidence records a pre-fix failure showing unchanged release admission, then post-fix changed quality policy_version, release-specific denial and unaffected-binding equality. The existing renewal/lifecycle acceptance evidence remains required; no human/evaluation acceptance is inferred.
* Decision route: Direct planner correction. The caller already requires checklist dispatch mapping to be bound; no significant or divergent user decision is needed.

## Strengths and Residual Risk

* Canonical ranking content hashing avoids trusting only a version label or the stored content_hash field. Explicit CURRENT capture fixes the separate old-default explanation problem without changing ranking algorithms.
* Capability-local binding changes are the right mechanism. A global registry/version bump would unnecessarily invalidate unrelated tasks and is not required by this plan.
* Existing claim, completion and review paths already consume the runtime binding, supporting a small correction rather than duplicated lifecycle machinery. Planned tests must still establish their actual outcomes.
* New constructed release records demonstrate proposal-only mechanics, not approved evaluation, live authorization or permission to rely on historical proposals.
* The scripted false-attestation negative control accurately exposes that source IDs and explicit attestation do not establish truth or reviewer competence.
* #222 manifest approval, OQ-017/OQ-018 holders, real reviewer effectiveness, broader #220 challenge coverage, actual #221 restart/drill acceptance, #224 and #440 remain unresolved. Refs-only publication must retain those distinctions and must not imply any child or epic is complete.
* Local SQLite/unit success does not establish SQL Server, browser, deployment, full-gate or hosted approval evidence. These limitations are accepted in the supplied scope, not silently counted as passes.

## Questions or Blocking Evidence Gaps

* No new user question is required for this bounded implementation plan.
* Named approvers and manifest approval remain unknown/unmet. They block the relevant human/evaluator scope, not this independent binding correction.

## Limitations

* No tests, gate, model invocation or implementation review were performed during critique.
* GitHub decision status is taken from the caller and supplied dated research, not independently re-adjudicated or refreshed.
* No open-ended research, private-data inspection or source modification was performed.
* Only this critique artifact is authored. The existing untracked plan, details, research and workflow-state files are left untouched on feat/rai-release-218; read-only PR inspection found no existing topic PR.
* This is the complete actionable finding set for the supplied candidate boundary. Implementation findings and genuinely new evidence belong to the subsequent implementation Review, not a second candidate critique.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the independent mapping-only/order-sensitive regression expectations to P01-T01, record disposition of this original critique, and finalize the plan without another critique pass.
* User response required: No.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-27/rai-release-218-plan.md | Candidate plan assessed. |
| .copilot-tracking/details/2026-10-27/rai-release-218-phase-details.md | Phase details requiring the bounded PC-001 correction. |
| .copilot-tracking/research/2026-10-27/rai-release-218-research.md | Supplied dependency and acceptance evidence. |
| .copilot-tracking/plans/2026-10-27/rai-release-218-critique.md | Original independent critique and complete finding set. |

## Next Steps

The active planning parent should resolve PC-001 directly, preserve this original Revise verdict and proceed through the authorized implementation and independent Review stages. No user action or second plan critique is required. Human-dependent scope stays blocked until its actual evidence exists.
