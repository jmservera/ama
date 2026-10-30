---
title: "RPI Plan Critique: Authenticated live acceptance"
description: "One independent final-candidate assessment of the supplied acceptance plan."
ms.date: 2026-10-30
---

## Metadata

* Task ID: authenticated-live-acceptance-2026-10-30
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/authenticated-live-acceptance-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/authenticated-live-acceptance-phase-details.md
* Critique execution status: Complete
* Original verdict: Revise
* Severity counts: Critical 0; High 2; Medium 2; Low 0.
* This is the one final-candidate critique, not an execution or a subsequent assessment.

## Inputs and Criterion Boundary

* Read the supplied research, plan and phase details only, plus the critique skill/template and the exact bodies of issues #550, #551 and #552 retrieved with gh on 2026-10-30.
* Inspected Git status and branch without modifying existing work. Branch is chore/auth-acceptance-1030; the supplied tracking inputs are untracked parent work.
* Assessment covers all nine chat, four map and six case criteria, including compound obligations, secret hygiene, live-versus-source evidence, authorization refusal, change budget, independent Review and local persistence.
* Caller authorizes actual authenticated acceptance on the two exact supplied sites, not access repair, product edits, private-data changes, Azure deletion, push or issue closure.
* The supplied identity is context only. The password file was not read. No live automation, source-code inspection, private-dataset access or delegation occurred.
* Research citations C1-C8/W4 are supplied evidence pointers, not independently revalidated source contents. Issues W1-W3 were directly checked.

## Coverage Assessment

The criterion identifiers below follow the plan's proposed original issue order. Covered means adequately planned, not proven on the deployment.

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| 550-01: shared component and bottom-right popup on both sites | Partial | Launchers covered; component-use provenance needs PC-004. |
| 550-02: persistent scrolling conversation, newest bottom, pinned input, stays open | Covered | P01-T02 specifies live two-turn results and geometry; persistence is not assumed to require cross-session storage. |
| 550-03: Enter, Shift+Enter and send button | Covered | Explicit plan functional requirement and keyboard exercise. |
| 550-04: compact employee selector in input area, changes skill, active indication | Covered | Functional requirement and live selected-skill observation; preserve every subpart in the matrix. |
| 550-05: attachment/voice controls or disabled controls with reasons | Covered | Explicit controls-and-reasons observation. |
| 550-06: actual AI label and collapsed sources | Covered | Actual AI output required; rules-only output is explicitly insufficient. |
| 550-07: consent before any resident data use | Partial | Consent distinguished from works approval, but pre-consent timing evidence needs PC-003. |
| 550-08: relevant rat response or honest contact fallback, not home summary | Covered | Exact query and honest response classification specified. |
| 550-09: 200 ms loading, errors, keyboard/screen-reader semantics, reduced motion | Partial | Timing and native screen-reader limitation are honest; error/reduced-motion probe rules need PC-002. |
| 551-01: compact header filters at top of expanded map | Covered | Actual expanded controls and geometry planned. |
| 551-02: markers and header state change consistently | Covered | Selections, counts/markers and restored state planned without record identities. |
| 551-03: keyboard, non-colour state and narrow readability | Partial | Keyboard/text and narrow geometry covered; non-colour selected-state proof needs PC-002. |
| 551-04: browser or unit coverage | Covered with limitation | Existing coverage may establish this source-level criterion only when concrete assertions are cited; it cannot establish live behavior or deployed revision parity. |
| 552-01: presentation icons with labels | Covered with limitation | Labels and byte provenance where accessible planned; unavailable provenance remains unmet. |
| 552-02: visibly thinner, less vertical space per step | Covered with limitation | Heights planned; absent trusted before baseline correctly prevents a comparative pass. |
| 552-03: one-line blocker and full reason by keyboard and touch | Covered | Actual blocker, keyboard and genuine touch context required; unsafe session reuse must remain blocked. |
| 552-04: visually joined tabs/panel outside inner scroll box, panel scrolls below | Covered | Ancestry, bounds and scrolling planned; geometry alone must not replace the actual scrolling observation. |
| 552-05: preserved Fluent 2 and WCAG baselines | Partial | Viewports and general semantics are not the baseline's whole scope; PC-002. |
| 552-06: desktop and narrow browser evidence | Covered | 1280/390/320 CSS px observations planned, conditional on authorized case access. |
| AC-01, P02-T01: 19 complete compound decisions | Partial | Overall proven/unmet rule is sound; explicit subpart-to-proof mapping needs PC-002 through PC-004. |
| AC-02/03, P01-T01: actual login and roster refusal | Covered | Distinct per-site auth, binding and authorization categories; no initializer, role edits or private-dataset access. |
| Secret hygiene and runtime dependency | Partial | Strong logging/capture restrictions; forbidden temporary-path dependency and browser artifact containment need PC-001. |
| AC-04, P02-T02: original Review, local Refs-only commit and gate | Covered | Original outcome retained; no remediation/review loop, push or closure; blocked local gate distinguished from live criteria. |
| Change budget | Covered | One tracking script, sanitized generated evidence and required RPI artifacts; no product edits or test removals. |

## Verdict

* Verdict: Revise.
* The bounded acceptance objective is credible and does not require all product criteria to pass. Four direct planner corrections are needed to prevent unsafe runtime artifacts or unsupported criterion decisions.
* No significant or divergent user decision is necessary. Current authorization already resolves access-repair, product-remediation and publication questions negatively.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The runtime dependency conflicts with the execution-path restriction and leaves browser artifacts unspecified

* Related IDs: P01-T01; plan Dependencies and Non-Functional Requirements; research Wave 2.
* Evidence: The plan requires an existing /tmp/mv Python environment. The caller environment prohibits any file operations in temporary directories, requires new files relative to the project, and the plan prohibits stored credential artifacts. Neither document specifies where browser profiles, downloads, crash files or runtime scratch will be created.
* Concern: The proposed dependency is not usable as written under the active path restriction. Disabling traces and storage-state exports does not stop a browser from creating a credential-bearing profile or crash artifacts in its default locations.
* Impact: Execution can violate the path boundary or retain authentication material outside the intended sanitized evidence workflow.
* Smallest useful change: Select or locate an allowed interpreter/runtime before execution; if unavailable, record a tooling blocker rather than use the forbidden dependency. Specify project-relative, task-owned non-evidence browser scratch/profile paths and temporary-directory environment settings; disable unnecessary downloads/crash capture, exclude runtime artifacts from staging and remove only task-owned scratch on success and failure. Do not copy the password into scratch.
* Action owner: Planning parent; acceptance executor implements containment in the single allowed script.
* Exact resolving evidence: Revised dependency and execution instructions name allowed runtime/scratch paths and failure cleanup. Execution records only sanitized preflight/cleanup booleans; staged-file inspection shows no profile, secret, token, crash or authentication artifacts.
* Decision route: Direct planner correction. Missing permitted tooling may block execution; it does not authorize an exception.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Several compound obligations have no executable probe or explicit untested disposition

* Related IDs: 550-09; 551-03; 552-05; AC-01/03; P01-T02; P02-T01.
* Evidence: P01-T02 says to record reduced-motion styles but does not require reduced-motion preference emulation/comparison; map checks do not explicitly verify a non-colour selected-state signal. The plan mentions actual errors and optional fault injection without a required bounded error probe or not-observed result. No task maps the preserved Fluent 2/WCAG baseline criterion beyond viewport and general semantics observations.
* Concern: Copying all criteria into a matrix after execution does not ensure these reachable subparts receive an observation. Default-motion CSS, readable map geometry or successful chat responses do not prove reduced-motion behavior, non-colour selection or error handling. A blanket baseline pass cannot be inferred from those checks.
* Impact: Reachable requested behavior may be skipped, or compound criteria may be marked proven from incomplete observations.
* Smallest useful change: Before execution, add a subpart/probe/evidence-or-blocker mapping for these obligations. Require actual non-colour map selection evidence, a reduced-motion preference comparison, and a safely bounded error observation or explicit not-observed result. Scope applicable baseline checks from the supplied baseline pointers within existing authority; if they cannot be assessed, mark 552-05 unmet with the exact untested scope. Do not add a native screen-reader requirement or manufacture a full conformance claim.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02/P02-T01 instructions enumerate each missing subpart and its observation or unmet rule. Final evidence distinguishes natural failures, any narrowly scoped browser fault injection, unmeasured timing and unavailable assistive-technology testing. Every compound criterion remains unmet if any required subpart lacks proof.
* Decision route: Direct planner correction; no new tooling, product edits or expanded acceptance authority required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Consent visibility is not proof that resident data was unused beforehand

* Related IDs: 550-07; P01-T01; P01-T02.
* Evidence: The functional requirements say consent precedes requests; details distinguish record-use consent from works consent. The execution task does not define an observation starting before resident navigation/assistant opening or identify which record-use boundary is being tested.
* Concern: Observing a consent control and then sending a question can miss an earlier assistant context fetch or record-backed response. Conversely, ordinary authentication requests must not be misclassified as resident-record use.
* Impact: A visible consent step could produce an unsupported proven decision for the stronger "before any data is used" criterion.
* Smallest useful change: Define the relevant resident record-use boundary and begin a sanitized observer before the first relevant page/assistant action in a fresh session. Retain only approved endpoint classes, ordering and booleans, not payloads, headers or query strings. Observe the pre-consent state without sending a record-use request; then exercise the normal permitted consent path. If backend-only use cannot be observed, state that limit and withhold the overall pass unless supplied applicable evidence resolves it.
* Action owner: Planning parent; acceptance executor owns the bounded observation.
* Exact resolving evidence: Plan/details specify pre-consent and post-consent observation points and the pass/unmet rule. Sanitized evidence records consent ordering, observed data-use request classes and the residual server-side visibility limitation.
* Decision route: Direct planner correction; not permission to inspect private records or bypass consent.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Shared asset provenance needs a separate rule from shared rendered-component proof

* Related IDs: 550-01; P01-T02; P02-T01.
* Evidence: The plan offers same-origin asset hashes as support for shared provenance and warns that they do not prove backend or full source revision parity. It does not state what establishes that both observed popup chats actually use one shared component.
* Concern: Matching served assets can include unused code, and different bundles can legitimately contain the same shared component. Similar-looking popups or the presence of a shared asset alone do not prove the compound criterion's implementation obligation.
* Impact: Live launcher success plus a weak source/asset proxy could be incorrectly promoted into a proven 550-01 result.
* Smallest useful change: Split 550-01 into live launcher/popup observations on each site and the shared-component obligation. Specify the trusted applicable implementation/provenance evidence needed for the latter, tied to the served frontend when possible; if unavailable within scope, retain the successful live subparts but mark the whole criterion unmet. Do not require backend revision parity for this frontend obligation.
* Action owner: Planning parent.
* Exact resolving evidence: Revised evidence rules explicitly reject appearance or asset presence alone as shared-component proof. The final row cites sufficient applicable provenance or names shared-component use as missing proof.
* Decision route: Direct planner correction; reporting unmet is authorized and does not require new source changes or user input.

## Strengths and Residual Risk

* Authentication success is correctly separate from binding and authorization. A generic 403 is not evidence of a missing roster entry.
* The SQL initializer, role changes, guessed case IDs, private-dataset inspection and record mutations are explicitly excluded. Missing authorization is a stopping boundary, not a remediation invitation.
* Both sites receive their own sign-in attempt; the resident site's separate enrollment is not assumed from employee Entra access.
* Secret reading is confined to automation; traces, HAR, raw console/network dumps, authentication query strings and storage-state exports are prohibited. Safe failure categories are preferable to exception strings.
* Missing before baselines, actual AI output, native screen-reader testing and deployed parity are correctly acknowledged rather than replaced with synthetic tests.
* All 19 outcomes may honestly remain unmet when access or proof is missing. A denied journey is not evidence of a product defect, and a local gate failure is not a failed live UI criterion.
* One script and sanitized evidence are sufficient; none of these findings authorizes product edits, test removals, repeated Review, publication or issue closure.

## Questions or Blocking Evidence Gaps

* No unresolved user decision blocks plan correction.
* Authorized runtime availability, employee binding, resident enrollment and reachable feature data remain execution uncertainties. Report them as blockers if encountered; do not repair access.

## Limitations

* This assessment establishes plan credibility, not deployed behavior, current credential validity, browser availability or full accessibility conformance.
* The cited code, infra guides, baseline documents and local gate implementation were not independently opened under the caller's bounded read scope.
* No secret was inspected, no screenshot taken and no live site visited.
* All actionable findings available from this supplied boundary are returned together. No second critique is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Replace the forbidden runtime dependency and define credential-bearing browser artifact containment; resolve PC-002 through PC-004 directly in the plan/details and record this original verdict without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/authenticated-live-acceptance-research.md](.copilot-tracking/research/2026-10-30/authenticated-live-acceptance-research.md) | Supplied research boundary |
| [.copilot-tracking/plans/2026-10-30/authenticated-live-acceptance-plan.md](.copilot-tracking/plans/2026-10-30/authenticated-live-acceptance-plan.md) | Unmodified final-candidate plan |
| [.copilot-tracking/details/2026-10-30/authenticated-live-acceptance-phase-details.md](.copilot-tracking/details/2026-10-30/authenticated-live-acceptance-phase-details.md) | Unmodified phase details |
| [.copilot-tracking/reviews/plans/2026-10-30/authenticated-live-acceptance-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/authenticated-live-acceptance-plan-critique.md) | Complete original critique |

## Next Steps

The active planning parent should resolve PC-001 through PC-004 directly, preserve the original Revise verdict and finalize without another critique. No user action is required. This bounded critique stops here.
