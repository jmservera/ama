---
title: Loading and HAX briefing plan critique
description: One independent final-candidate critique for issue 531
ms.date: 2026-10-28
---

## Metadata

* Task ID: #531, loading-briefing-hax-531.
* Critique date: 2026-10-28.
* Plan: .copilot-tracking/plans/2026-10-28/loading-briefing-hax-531-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/loading-briefing-hax-531-phase-details.md
* Critique execution status: Complete.
* Assessment: Exactly one independent final-candidate critique; this is the complete actionable finding set for the supplied boundary.

## Inputs and Criterion Boundary

* Primary research: .copilot-tracking/research/2026-10-28/loading-briefing-hax-531-research.md, including C1-C4, W1-W7 and the bounded design note.
* Caller requirements: Full RPI; retain native Fluent patterns without a framework swap; immediate/slow/retry shell feedback; immediate action text, spinner after 200ms, disabled duplicates, polite status and errors for all employee async actions; actual briefing sources and clear generation time; outcome-labelled conditional draft review; immutable review evidence and manual paths.
* Dependencies: Stacked on feat/case-journey-ux-526, PR #529. Existing branch is feat/loading-briefing-hax-531. The supplied plan, details and research were already untracked inputs and were not altered.
* Acceptance boundary: P01-T01, P02-T01, P03-T01; plan functional/non-functional requirements, acceptance criteria, test ownership and addition/removal budget, and publication safeguards.
* Source inspection: Relevant native employee scripts and shell, shared AI-task completion/review, briefing generation/cache, existing briefing and case-journey checks, and the local gate contract. No open-ended external research, Azure, az, secrets, .env, private dataset, implementation or live-site execution.
* Repository context: Case-study original/addendum and knowledge-base index/memory; these do not establish validated employee usability.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1; P01-T01; immediate/slow/retry shell | Covered | Static fallback, independent watchdog, 4s/15s thresholds, startup failure and existing bounded script recovery are explicit. |
| C2; P01-T01; all employee async actions | Partial | Returned-promise observation is credible, but the named integration points omit separate event factories and non-returning mutation callbacks. PC-001. |
| P01-T01; timing, status and state ownership | Covered with integration gap | Immediate text, 200ms spinner, scoped polite status, duplicate prevention, owned disabled-state restoration, cancellation and no automatic write retries are explicit. PC-001 addresses completeness. |
| C3; P02-T01; statement sources/time | Partial | No fabricated attribution and scoped case links are explicit; metadata alignment with filtered, fallback and quarantined output needs a lifecycle invariant and tests. PC-002. |
| C3; P02-T01; draft-only review/manual paths | Covered | Required reasons, conditional fields, local dismissal, source checks and one-time immutable reviews remain explicit. |
| C4; P03-T01; regression migration | Partial | Existing briefing selectors are budgeted for updates, but case-journey review flows also require changes to remain executable and meaningful. PC-003. |
| W2-W7; native Fluent/HAX constraints | Covered | Native semantics and existing tokens remain; explanations are not treated as correctness or confidence evidence. |
| P03-T01; test ownership/budget | Covered | Server versus browser ownership, zero removals, bounded additions and real-helper/server behavioral checks are stated. Findings can be resolved within that budget. |
| Full RPI; parent dependency; restricted publication | Covered | Independent Review, original evidence, commit-before-gate, parent-targeted PR wording and local-only fallback are explicit. Full-gate restriction is a known blocker, not permission to weaken the gate. |
| Unknown user research | Covered as limitation | Stakeholder feedback is not validated usability. Staff usability expectations remain hypotheses; manual assistive-technology and deployed checks remain separate. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: The direction and safeguards are credible, but the implementation contracts do not yet close demonstrated integration and regression gaps. All findings permit direct planner disposition under existing user direction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The integration contract does not cover every employee async action

* Related IDs: C2; P01-T01; P03-T01; caller's all-employee-actions requirement.
* Evidence: Phase details lines 16-20 rely on returned promises and name direct account/import/filter listeners plus fire-and-forget redraws. src/api/src/zava_forward/api/web/ops.js:318-321 invokes asynchronous appointment submission without returning its promise. This is a mutation, not just a redraw. src/api/src/zava_forward/api/web/law.js:22,42,62,69-71 creates separate direct listeners and launches requests without returning them; its standalone shell, src/api/src/zava_forward/api/web/law.html:25, loads law.js without app.js or its h factory. app.js:1365-1380 also starts async map work through Leaflet events, outside h.
* Concern: Instrumenting h and the three named direct-listener families cannot establish the universal requirement. Fixing redraw promises alone leaves at least an appointment mutation and the employee law-viewer actions outside the proposed observable lifecycle. Background map refreshes also need an explicit regional feedback classification rather than an accidental exclusion.
* Impact: Some real actions can retain silent waits and enabled duplicate submission even when a synthetic delayed helper test passes.
* Smallest useful change: Add a bounded integration inventory in P01 details covering h-based callbacks, direct listeners, standalone employee scripts and library-triggered refreshes. Explicitly require return/await or direct helper adaptation for mutation callbacks as well as redraws. Include the law viewer under the all-employee requirement; classify non-control/background work for regional busy/status feedback without indiscriminately disabling navigation.
* Action owner: Planning parent; implementation owner executes the inventory.
* Exact resolving evidence: Revised P01 details identify these source entry points and adapters. P03 maps controlled-delay, error and duplicate-request assertions to an actual appointment submit and an actual law-viewer action, alongside h/account/import/filter coverage; map refresh has a named regional-feedback check. Extend existing checks or the single permitted new browser check without removing tests.
* Decision route: Direct planner correction. Direct disposition is possible: Yes. No new framework, authority change or user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Statement metadata is not explicitly bound to the output that survives publication

* Related IDs: C3; P02-T01; P03-T01; actual-source and clear-time acceptance criteria.
* Evidence: Phase details lines 30-33 require retaining raw statement associations before analyse strips markers and adding a generation timestamp. src/core/src/zava_forward/core/ai_tasks.py:111-133 also drops invalid/uncited bullets and cleans the shown text. Its finish function, lines 198-234, can replace AI text with workflow_text and empty citations during continuity quarantine. src/core/src/zava_forward/core/store.py:737-742 returns cached briefing results unchanged. Existing _now at ai_tasks.py:156-157 returns an offset-free local timestamp.
* Concern: Capturing raw associations is necessary but does not specify which statements survive validation or the late-publication fence. Metadata assembled before those decisions could display removed statements or AI references beside a rules fallback. The shared finish path makes this relevant beyond briefing. A timestamp without an explicit timezone also does not unambiguously identify generation time in the browser.
* Impact: The new source presentation can misattribute the visible output or imply freshness that the published result does not have, despite preserving the old flattened-citation checks.
* Smallest useful change: State that the returned statement collection must describe only the final shown output, with unchanged validation/drop behavior. On fallback or quarantine, derive statements from the actual displayed template or explicitly report unavailable attribution, never retain abandoned AI associations. Specify a timezone-bearing generation timestamp, stable across cache reads. Add this lifecycle matrix to server-test ownership; no new model call or authority change is required.
* Action owner: Planning parent; core/API implementation and unit-test owner.
* Exact resolving evidence: Revised P02/P03 contracts require deterministic server tests using constructed AI results, not live AI: valid and unresolved references, filtered bullets, rules fallback including fewer than three/zero cases, late-result quarantine, cache-hit timestamp stability and a timezone-bearing timestamp. Assertions compare statement text/references to final text and prohibit stale AI metadata on template output. These fit the existing unit suite and one permitted new module.
* Decision route: Direct planner correction. Direct disposition is possible: Yes. This preserves current validation and continuity safeguards rather than expanding them.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Existing journey tests assume the review fields that the plan intentionally hides

* Related IDs: C4; P02-T01; P03-T01; draft retention and immutable-review acceptance.
* Evidence: Plan lines 105-108 explicitly budget existing briefing-label updates and require the existing journey check. src/api/checks/case_journey_browser_check.py:590-595 fills Edited draft and Reason before choosing Edit. Lines 616-638 again fill the fields and use the Edit button as submission, then lines 651-669 assert preservation of later, unsubmitted edits after the immutable review. P02 instead makes Edit a reveal choice and hides fields until that choice is made.
* Concern: The current executable review scenario will stop at the hidden field or click only the new reveal action instead of submitting. Updating briefing selectors alone does not migrate the existing draft-retention/audit regression to the new interaction.
* Impact: A required check becomes predictably incompatible; a superficial selector rewrite could also drop the exact parent safeguards the caller requires.
* Smallest useful change: Explicitly include case-journey review-flow migration in P03, within the zero-removal budget. Separate reveal and submit steps, retaining the existing delayed-response and later-edit assertions. Cover cancel/reopen field retention and the getText-backed resident draft as well as the internally edited document draft, so conditional fields do not introduce a second divergent draft value.
* Action owner: Planning parent; browser-check owner.
* Exact resolving evidence: Revised P03 names case_journey_browser_check.py and the affected scenarios. Updated scenarios choose the outcome before filling, explicitly submit it, and still prove immutable dispatched text/reason, one-time review, copyable later edits and retained record handlers after refresh. Cancel/reopen preserves local values, and the resident review payload equals the visible draft. Existing briefing/script/journey checks remain required and no tests are removed.
* Decision route: Direct planner correction. Direct disposition is possible: Yes. The user already selected conditional outcome-led fields.

## Strengths and Residual Risk

* The plan preserves native Fluent patterns, existing manual routes, optional AI, role scope and draft-only human review. It rejects fabricated provenance and mutation retries.
* The test budget and ownership are explicit and allow all three corrections through existing-file updates plus the already permitted additions.
* The static shell cannot report an HTML document that never arrives. This is correctly separated from delayed scripts and APIs.
* tools/rpi-checks.py:62,601,670-671 demonstrates that the full gate requires/invokes az. Under the caller's prohibition, local-only handoff is an expected publication block. Do not execute that prohibited path, substitute a partial receipt, or publish without the required gate.
* Synthetic checks cannot establish employee usability, assistive-technology acceptance or deployed cold-start behavior. These remain labelled hypotheses or outstanding owner verification, not completed findings.

## Questions or Blocking Evidence Gaps

* No user question is required. The supplied direction resolves the choices relevant to these findings.
* No decision-critical evidence gap blocks this critique. External W-series retrievals are supplied research evidence, not fresh verification performed in this critique.

## Limitations

* This is a plan credibility assessment, not an implementation review, runtime test, security assessment or accessibility-conformance claim.
* Source inspection was bounded to resolving supplied requirements. No implementation or test execution was performed.
* PR lifecycle and remote head were taken from supplied context rather than freshly queried. No branch, source, plan, phase-detail or research changes were made.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the async integration inventory and representative real-handler acceptance checks, then directly disposition PC-002 and PC-003 in the same plan revision.
* User response required: No.
* Do not request another critique pass; preserve this original finding set and record exact resolving evidence during the parent's direct disposition.

## Next Steps

The active planning parent revises and dispositions PC-001 through PC-003, then continues the confirmed full RPI sequence subject to the existing gates. No user action is required.
