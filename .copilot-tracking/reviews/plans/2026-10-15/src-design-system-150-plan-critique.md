---
title: Issue 150 final-candidate RPI plan critique
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: #150, jmservera/ama.
* Critique date: 2026-10-15.
* Plan: .copilot-tracking/plans/2026-10-15/src-design-system-150-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/src-design-system-150-phase-details.md.
* Critique execution status: Complete.
* Execution boundary: exactly one final-candidate assessment; no nested agents, implementation, second critique, plan edits or research edits.
* Workspace: /home/azureuser/source/ama-wt/issue-150; branch feat/src-design-system-150.

## Inputs and Criterion Boundary

The assessment covers the supplied plan, details and research in full, the
caller's requirements, and minimal supporting source evidence:

* .copilot-tracking/research/2026-10-15/src-design-system-150-research.md, C1-C7 and W1-W3.
* Issue #150 body and all four comments, read using gh issue view on 2026-10-15. The owner explicitly chose adoption, then named Fluent UI (Fluent 2); the migration comment preserves the issue's five acceptance criteria.
* docs/reference/research/ux/design-system.md; docs/reference/README.md and docs/reference/memory.md.
* docs/case_study_48_original.md and relevant context in docs/case_study_48_addendum.md.
* docs/adrs/0006-src-layout-and-cutover.md, accepted layout and dependency rules; src/README.md.
* docs/architecture/mvp-to-src-parity-matrix.md, #150 carry-forward row.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md, SA-001 through SA-008.
* src/api/src/zava_forward/api/web/app.js, aiNotes(), mapPanel() and overviewView(); existing stylesheet tokens.
* src/api/tests/test_design_system.py; src/api/tests/test_accessibility_baseline.py; src/api/pyproject.toml.
* src/api/README.md and src/api/checks/browser_check.py, existing browser-test boundaries.

Binding constraints are the complete RPI loop and committed research/plan/change/
review evidence, src-only new code/tests, ADR 0006, no mvp changes, no excluded
.env/.vscode/.copilot-tracking/github-issues changes, pip only, preserved AI and
human/resident controls, local suites/ruff/mypy/synthetic application evidence,
and a PR using Refs #150. Test ownership is locked: no removals, existing test
updates, at most one new browser-check module.

This is a planning credibility assessment, not implementation acceptance. No
external Fluent guidance was independently researched beyond the supplied
research's evidence descriptions. No application, suite, browser, lint, type,
Docker or cloud check was executed. Existing live-service evidence is not
evidence for this proposed change.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner Fluent 2 adoption; W1; research Q1 | Partial | Owner choice is correctly recorded, but the candidate substitutes a native-foundation slice for adoption completion without an explicit remaining adoption gate; PC-001. |
| Issue criterion 1; C2/C3; P01-T01 | Partial | All token groups and consumption are named, but Fluent provenance and concrete adopted values/recipes are not specified; PC-002. |
| Issue criteria 2 and 4; SA-003/SA-004; P02-T02 | Covered with verification pending | Seven-state inventory, blocked owner/next action and truthful AI review documentation are required. Existing documentation's review-button wording must be reconciled with actual aiNotes() actions. |
| Issue criterion 3; C1; P01-T02 | Covered with verification pending | Shapes, visible status words, cluster safety totals including zero, selected words, list alternative, DOM construction and keyboard behavior have explicit owners. |
| Issue criterion 5; C4/W1; P02-T02 | Covered as a decision record, not delivery proof | Replace the rejected proposal with the dated owner adoption decision. Recording the decision is not evidence of packaged adoption. |
| Contrast, focus, reduced motion, forced colours, responsive widths; P02-T01 | Covered with verification pending | Planned browser/static checks are suitable bounded engineering evidence, not full WCAG or human acceptance. |
| ADR 0006; C5/C6; path and dependency constraints | Covered | Assets belong in the API package, tests/checks outside its importable package; no move or copy from mvp is needed for this slice. |
| Locked test ownership and unchanged tooling exemptions; P02-T01 | Partial | Existing API configuration silently exempts the proposed new check from many lint rules and formatting; PC-003. |
| Five suites, ruff/mypy and synthetic app evidence; P02-T01 | Covered subject to PC-003 | Fixture reuse, real loopback app and disclosed mock map responses are planned; commands/results must distinguish execution, skips and unavailable services. |
| Full RPI loop, committed artifacts, push and Refs #150 PR | Partial | Requirements and handoff mention delivery, but executable closeout tasks and gates are absent; PC-004. |
| AI availability, approvals, resident consent; C7 | Covered as invariants | No provider, workflow authority or consent changes are proposed; existing integration suites remain required. Label-only browser checks do not establish real inference or controlled approval. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 3 Medium, 0 Low.
* Rationale: The non-colour and regression slice is credible, but the plan is not yet a credible completion plan for the owner-selected adoption workstream. Honest disclaimers are necessary, not a substitute for respecting that direction. Concrete Fluent mapping, effective new-check quality gates and delivery closeout also need correction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The foundation slice is not an evidenced completion of the owner's adoption direction

* Related IDs: owner adoption requirement; W1; research Q1, Alternatives and Decision State; P01-T01; acceptance criteria; Follow-Up Items.
* Evidence: The issue comments select adoption instead of extending the MVP, then explicitly select Fluent UI (Fluent 2). The plan excludes runtime adoption, forbids new production modules/dependencies and defers the packaged migration. Research labels the native slice accepted, but provides no owner acceptance of that narrowed delivery scope. The supplied source already has native controls, Segoe/system typography, tokens and state classes.
* Concern: Adding Fluent-style aliases to the existing hand-written system may be preparatory work, but does not by itself demonstrate the chosen system has been adopted. The candidate correctly disclaims a library rollout yet does not make adoption completion an operationally open gate or define what additional implementation would satisfy it. A research synthesis cannot approve a scope reduction on the owner's behalf.
* Impact: A successful small CSS/non-colour PR could be mistaken for completion of the superseding owner instruction, while preserving the rejected extension strategy in substance.
* Smallest useful change: Explicitly designate this PR as a partial foundation/non-colour slice under the Fluent adoption workstream, retain an unresolved adoption-delivery gate with an owner and required evidence, and prohibit issue closure or adoption-complete claims from this slice. Alternatively, amend the plan to include an evidenced Fluent implementation path compatible with ADR 0006. Do not assume a React rewrite is necessary, or that a package installation alone proves adoption.
* Action owner: Planning parent.
* Exact resolving evidence: Revised plan/details and the eventual changes/review/PR consistently identify the delivered slice, the remaining adoption implementation and acceptance evidence, and whether #150 remains open. An adoption-complete path must identify the actual Fluent integration and rendered component evidence; a native-only final substitute requires explicit owner acceptance, not a planner assertion.
* Decision route: Direct planner correction for truthful partial scope and an open gate. The owner has already chosen Fluent, so do not ask them to choose extend versus adopt again. Only a proposal to treat native-only CSS as the final substitute, or to change binding scope/dependency constraints, requires a significant user decision. No user response is needed to make the direct correction.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Fluent-style aliases have no reviewable adoption contract

* Related IDs: issue criterion 1; research W2; plan Sources; P01-T01; P02-T02.
* Evidence: P01-T01 says "Fluent-style" colours, font ramp, spacing/radii and motion aliases, preserves the existing teal and legacy names, and completes when rendered tokens resolve and contrast holds. Research W2 supports the global/semantic alias model, while the plan adds a typography retrieval claim without a precise source mapping or selected dimensions. Existing CSS already contains these token groups.
* Concern: Generic alias names, resolved CSS and contrast are insufficient to distinguish a sourced Fluent foundation from a rename of existing CSS. No concrete token/value or native-component recipe mapping makes the central adoption claim falsifiable.
* Impact: Implementation and review could pass without any meaningful Fluent-specific change, even after PC-001 correctly limits the PR to a foundation slice.
* Smallest useful change: Add a compact mapping contract to the existing details: chosen global values and semantic aliases, source/version or retrieval reference, consuming buttons/fields/cards/type/spacing/focus/motion rules, and explicit retained-brand or accessibility deviations. Where supplied evidence lacks a specific recipe/value, mark it unresolved and obtain focused evidence before implementing that claim; do not invent Fluent dimensions.
* Action owner: Planning parent; implementer records the actual mapping in the existing design synthesis.
* Exact resolving evidence: Plan/details name the mapped values/recipes and deviations; existing design tests assert meaningful mapped values and use, not just token presence; the sole browser check demonstrates representative resolved native-component styles. Review can trace each claimed Fluent foundation to supplied or subsequently recorded official evidence.
* Decision route: Direct planner correction and, where necessary, bounded evidence gathering. Neither keeping a documented custom brand nor preserving accessibility controls requires reopening the already settled system choice.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The new browser module inherits migration exemptions

* Related IDs: P02-T01; Locked Test and Change Ownership; no new tooling exclusions.
* Evidence: src/api/pyproject.toml exempts checks/*.py from numerous lint rules and excludes checks/*.py from ruff formatting. The proposed src/api/checks/design_system_browser_check.py matches both wildcards. The new module is not among the explicitly grandfathered mypy modules, so strict typing still applies.
* Concern: Running the ordinary project ruff commands will not provide full lint/format evidence for the only new test module, even without editing any exclusion configuration. The candidate's "no existing exemptions added" language does not prevent inherited exemption coverage.
* Impact: A green project lint/format result can overstate validation of new code and conceal a formatting check that never ran.
* Smallest useful change: Keep the ownership cap and existing migration configuration unchanged, but add an explicit non-exempt lint and format check for the single new module, with the intended rules stated, alongside normal project commands. For example, use a suitable explicit ruff --isolated invocation so both inherited per-file ignores and format exclusions are bypassed; preserve the project's line length and Python target explicitly. Keep the new module in strict mypy coverage.
* Action owner: Planning parent specifies the checks; implementer executes them.
* Exact resolving evidence: Recorded commands show the new module was actually checked and formatted without inherited migration exemptions, and strictly type-checked; normal five-project results remain separately recorded. No extra browser module, deletion, blanket exemption removal or unrelated legacy cleanup is needed.
* Decision route: Direct planner correction; no significant user decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Required RPI and PR delivery are not scheduled acceptance gates

* Related IDs: full-loop/commit/PR user requirements; P02-T02; Handoff.
* Evidence: The only phases are implementation and validation/documentation. P02-T02 ends "ready for one post-implementation Review" and mentions committing requested artifacts; Handoff names a changes file. There is no owned task specifying the review artifact/outcome, finding disposition, final artifact completeness, privacy-safe commit, branch push or Refs #150 main-based PR.
* Concern: The candidate stops at readiness for review rather than planning the requested completed loop and persistent delivery. Requirements in a preamble do not establish a completion gate.
* Impact: An implementer can finish every scheduled task while leaving review, durable evidence or the requested PR undelivered.
* Smallest useful change: Add an owned closeout task or phase after validation: create the implementation changes record and one implementation-review record; reconcile criteria and findings; commit the research, plan, details, critique, changes and review artifacts together with the bounded changes; resolve the authenticated GitHub identity and repository-local noreply commit email; push only the topic branch and open a main PR containing Refs #150, actual evidence and open gates. No merge is authorized. A subsequent implementation review is not a second plan critique.
* Action owner: Planning parent defines the gate; delivery implementer executes it.
* Exact resolving evidence: An explicit ordered closeout task with artifact paths and review acceptance conditions, followed at execution by committed artifact paths, commit SHA, push result and PR URL/base/body. Excluded paths, .venv, private/generated working data and mvp changes remain outside the commit. Unavailable checks remain unmet instead of being checked by proxy.
* Decision route: Direct planner correction implementing the existing user request; no user response required.

## Acceptance Disposition: What Must Remain Unticked

* Every plan implementation/validation checkbox is currently pending. This critique supplies no execution evidence and checks none.
* The issue's token criterion can be supported by native CSS work if definitions, consumption and mapping are verified. Its component-inventory and AI-pattern criteria can be supported by accurate reviewed documentation and regressions. Prior delivery is not automatic verification of this candidate.
* The issue's non-colour criterion remains open until actual point markers, both cluster safety-count states, selected/unselected tiles, keys, labels and the retained list alternative have verified non-colour semantics. Checking only a map list or a mocked response is insufficient; disclose which mode/response was constructed.
* The issue's decision-record criterion can be satisfied by accurately recording the dated owner choice and superseding the rejected proposal. It does not require falsely claiming an installed Fluent package, and it does not prove adoption delivery.
* Full Fluent UI runtime migration/adoption-complete status remains unverified for this native-only candidate. Do not tick it because semantic alias names, fonts or contrast tests pass. Do not close the adoption workstream without the gate in PC-001 being resolved.
* Human accessibility acceptance, full WCAG conformance, live AI inference/quality, live SQL/Azure operation and deployment remain unmet for this change. These are evidence limitations, not newly invented issue #150 criteria. Unchanged controls and local synthetic results do not satisfy them by proxy.
* Full-loop delivery remains pending until implementation review and committed/pushed PR evidence exist. Use Refs #150, not an automatic closing phrase, while adoption delivery remains unresolved.

## Strengths and Residual Risk

* Correct src/API ownership and move-not-copy discipline; no mvp implementation, new workload dependencies or uncontrolled authority changes are planned.
* Shape plus visible text, explicit zero safety counts and selected words address the observed colour-only failures directly. DOM-built markers avoid introducing record-string HTML interpolation.
* One browser module plus existing test changes is sufficient for the bounded coverage. Keep the locked ownership, zero removals and explicit fixture disclosure.
* Existing design documentation describes "Use as draft"/"Dismiss" and a reviewed CSS pattern; actual aiNotes() exposes "Accept as is", "I changed it" and "Reject", with reviewed-draft disclaimers. P02-T02's promised accuracy must reflect actual controls, without changing their authority or resident-consent semantics.
* Existing integration suites, not label presence alone, are the regression evidence for optional AI/manual flow, authorization and approval/consent boundaries. No live inference claim follows.
* Forced colours, reduced motion and three widths are useful reproducible engineering checks. Screen-reader/user acceptance, external tile-service behavior and real-service validation remain separate evidence.

## Questions or Blocking Evidence Gaps

No new owner decision is needed for the direct corrections. The owner choice
is known. What is missing is an evidenced completion path or a truthful staged
delivery gate, not permission to reinstate the rejected extension proposal.
If the parent insists this native-only slice completes adoption, explicit
owner acceptance of that significant substitution is required before that
claim can be made.

## Limitations

This single critique assesses the supplied final candidate and bounded source
evidence, not undiscovered product scope. It does not establish that a particular
Fluent runtime or integration approach is compatible, select a framework, or
authorize new dependencies. Official guidance assertions are limited to the
supplied research; PC-002 identifies where more precise evidence is required.
All source inputs and existing uncommitted work were left unchanged. Only this
critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Mark this candidate as a partial foundation slice with an explicit open Fluent adoption-delivery gate, then resolve PC-002 through PC-004 directly in the plan/details.
* User response required: No for these direct revisions. Yes only if proposing native-only final adoption or another significant departure from current direction.
* Critique lifecycle: Complete; verdict Revise. Finalize the corrected plan without another plan critique, then proceed through implementation and implementation review under the existing parent loop.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/src-design-system-150-plan.md](.copilot-tracking/plans/2026-10-15/src-design-system-150-plan.md) | Assessed final-candidate plan; unchanged |
| [.copilot-tracking/details/2026-10-15/src-design-system-150-phase-details.md](.copilot-tracking/details/2026-10-15/src-design-system-150-phase-details.md) | Assessed phase details; unchanged |
| [.copilot-tracking/research/2026-10-15/src-design-system-150-research.md](.copilot-tracking/research/2026-10-15/src-design-system-150-research.md) | Supplied evidence synthesis; unchanged |
| [.copilot-tracking/reviews/plans/2026-10-15/src-design-system-150-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-15/src-design-system-150-plan-critique.md) | This one completed critique |

## Next Steps

The active planning parent should dispose PC-001 through PC-004, finalize
without a second critique, and continue the requested RPI loop. No user action
is required unless the parent proposes the significant scope substitution
identified in PC-001.
