<!-- markdownlint-disable-file -->
---
title: RPI Plan Critique - resident-survey-check-571-correction2
description: Single bounded credibility assessment of mandatory gate harness repairs
ms.date: 2026-10-31
---

## Metadata

* Task ID: 571-correction2; parent: 571-correction1.
* Slug: resident-survey-check-571-correction2.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction2-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/resident-survey-check-571-correction2-phase-details.md
* Critique execution status: Complete.
* Assessment count: Exactly one activation and one complete finding set for this distinct child. No re-critique is required or authorized.

## Inputs and Criterion Boundary

* Caller direction authorizes only minimal fixture stdout isolation, nine callback capture bindings, required whole-file formatting and a short src/README.md note. Complete validation and an eligible published main PR remain the owner's requested outcome. Existing resident source additions, earlier Review outcomes and the failed receipt must remain immutable.
* Read the complete current same-slug plan, details, research and state at their dated canonical paths. Read the exact chat-panel discovery skip fixture, complete employee journey browser harness, Runner.command, check_skips, static dispatch, isolated lint/format and browser dispatch contracts. Read relevant local-gate documentation and historical Review sections for provenance, not as another Review.
* Project context: docs/case_study_48_original.md, relevant resident proposal in docs/case_study_48_addendum.md, entry sections of docs/reference/README.md and docs/reference/memory.md. Memory supplies preferences, not evidence.
* Narrow callback-signature evidence: existing handlers in src/api/checks/chat_widget_browser_check.py:72 use keyword-only defaults; src/api/checks/workbench_browser_check.py:215 reserves the second positional argument for _request before a default-bound capture. These files are evidence only, not correction targets.
* Observed entry state: fix/resident-survey-check-571; only four new same-slug inputs were untracked. No tracked edit was shown. Candidate 10401c5a and main a75bbdff are supplied planning identities, not a freshly fetched publication assessment.
* Assessed boundary: G1-G2, FR1-FR3, NFR1-NFR3, AC1-AC4, C1-C6, both phases and all four tasks, coverage lock, dependencies, owner decisions, follow-ups and publication guards.
* This assessment determines plan credibility, not execution success, issue closure, source approval or permission to publish. No tests, source changes, git mutations, cloud/private-data access or nested delegation occurred.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| G1; C1-C2; FR1; AC1; P01-T01/P01-T02 | Partial | Fixture isolation targets the actual echo root; outer parser acceptance needs explicit pre-Review proof, PC-002. |
| C3-C5; FR2; AC2; P01-T01 | Partial | All nine captures are identified; callback signature safety needs an explicit binding rule, PC-001. |
| C6; AC2; P01-T02 | Covered | Runner.lint requires isolated E,F,I,B,UP, py312, line length 100 and whole-file format check; actual employee browser execution is retained. |
| FR3; AC3; P01-T02 | Covered | Fresh API discovery/Ruff/format and complete resident Chromium/axe execution remain required, with skips/incompletes disclosed. |
| NFR1; coverage lock | Covered | No real runner policy, allowlist/parser/matrix, workflow/hash, dependencies, runtime/UI, resident regression or assertion removal is authorized. |
| NFR2; P01-T02/P02-T02 | Covered | Task-owned pip environment, isolated synthetic execution, shared-lock admission, 1800-second wait and one admission retry are specified. Native full runner owns its lock; do not wrap it in an outer self-lock. |
| NFR3; state blocker; G2 | Covered | Actual failed correction1 execution and unrun dependent groups remain adverse historical evidence, not an admission-only failure or passing receipt. |
| AC4; P02-T01 | Covered | One new independent child Review follows validation; no material findings is an explicit publication prerequisite. Earlier Reviews remain unchanged. |
| AC4; P02-T02 | Covered | Evidence commit precedes a new full gate; current main/base/HEAD receipt verification and explicitly approving independent exact-head assessment precede non-force push and main PR. |
| Owner decisions; issue wording; follow-ups | Covered | Authorized historical main merge is not reopened; closing wording remains conditional on all actual criteria; direct resident/AT/live/model/WCAG and hosted/owner gates stay distinct. |

## Verdict

* Verdict: Revise.
* Rationale: The scope is appropriately narrow and both reported gate failures match the observed source roots. Two direct planning safeguards are needed to make the callback repair safe and demonstrate that fixture isolation resolves the enclosing-suite failure before the sole child Review. Neither requires a significant user decision or any change to runner policy.
* Execution is Complete; implementation, new Review, full-gate success and publication are not completed by this critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Default bindings must preserve Playwright callback argument slots

* Related IDs: C3-C5; FR2; AC2; P01-T01/P01-T02; coverage lock.
* Evidence: src/api/checks/case_journey_browser_check.py:84,98,166,170,255-265,370,374. The plan/details say default arguments without specifying their placement. Existing route bindings at src/api/checks/workbench_browser_check.py:215 reserve _request as the second positional parameter; src/api/checks/chat_widget_browser_check.py:72 uses keyword-only held.
* Concern: A naive lambda route, pending=pending or def threads(route, change=change, held=held) places a captured value in the optional positional request slot. Callback dispatch can then replace the list/change default with a Request. Clearing B023 alone would not prove that the nine bindings preserve route behavior.
* Impact: Mandatory browser validation can fail on append/fulfill or exercise the wrong thread branch, defeating a nominal lint-only repair.
* Smallest useful change: Specify keyword-only captured defaults after route, for example lambda route, *, pending=pending, and def threads(route: Route, *, change=change, held=held). Apply this rule to every affected callback without adding a factory/refactor: quality pending/loads; quality outcome pending/reads; chat threads change/held and hold held; mutation snapshot/pending. Preserve registration/unregistration callback identity.
* Action owner: Planning parent, then implementing parent.
* Exact resolving evidence: Reconciled P01-T01 details and FR2/coverage lock state the safe argument placement; reviewed diff shows all nine capture bindings and unchanged routes/scenarios/assertions; exact isolated Ruff check/format and the complete actual employee journey pass, including quality outcomes, both chat modes and all mutation families/outcomes.
* Decision route: Direct planner correction. Existing owner direction already authorizes these bounded bindings; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Prove outer static skip parsing succeeds before the child Review

* Related IDs: C1-C2; FR1; AC1; P01-T02; P02-T01.
* Evidence: tools/test_rpi_checks.py:89-115 exercises two real Runner.command calls; tools/rpi-checks.py:1240-1285 echoes subprocess output before skip checking; tools/rpi-checks.py:1025-1050 parses all enumerated skips against the enclosing group; tools/rpi-checks.py:1490-1495 invokes the tooling suite as suite=True in static. Research records that prior unit successes did not prevent enclosing static failure.
* Concern: Running the tooling suite successfully is insufficient proof of this specific root fix. P01-T02 does not explicitly feed its complete verbose combined transcript into the unchanged static-group parser before Review. A capture assertion can pass while leaked output still contaminates that enclosing transcript.
* Impact: The sole pre-publication Review can receive passing unit evidence yet leave the already-observed integration defect unproven until the expensive committed full gate.
* Smallest useful change: Add a pre-Review evidence step using the exact tooling discovery selector and verbose combined output. Evaluate that output with the unchanged check_skips in the static/non-integration context, record actual tests/executed/skips, and confirm no synthetic chat-panel skip entry leaked. Scope stdout capture to both fixture commands and use the permitted single added assertion to prove both transcript occurrences remain captured. Retain the admission/refusal and existing receipt assertions; do not mock Runner.command or alter the parser.
* Action owner: Planning parent, then validation/evidence-owning parent.
* Exact resolving evidence: Updated AC1/P01-T02 and changes evidence include the exact command, exit, log identity and successful outer static parser result with real suite counts. The diff retains existing assertions and at most one added capture assertion. The later fresh full gate also passes static with its normal parser.
* Decision route: Direct planner correction using existing contracts, without new test methods, runner changes or user input.

## Strengths and Residual Risk

* Root coverage is complete for the supplied failures: four loop-list lambda captures, three chat-function captures and two mutation lambda captures total nine B023 capture sites. Later non-loop handlers and the existing case_variant factory do not require broad capture refactoring.
* Fixture capture is correctly local: Runner.command still executes its subprocess, logs the real fixture transcript and records the accepted discovery skip; required-browser refusal still raises. Real suite output and strict policy must remain visible.
* Required whole-file formatting is explicitly scoped to the affected employee harness, not a justification for unrelated semantic edits. Independent Review must compare semantic preservation across the formatted file, not only the nine changed lines.
* Complete employee browser validation covers far more than a screenshot or selected route: mutation recovery, refusal/retry, draft retention, keyboard navigation, axe and existing browser-zoom checks remain mandatory.
* Full --all may reveal other baseline failures in currently unrun groups. The plan correctly blocks publication rather than assuming their success or weakening pins/contracts. Any genuinely necessary divergent repair needs its own authorized scope and evidence; this critique does not approve it.
* One child Review before commit and an independent exact-head publication assessment after the fresh full gate are separate obligations. A non-approving assessment, material Review finding, dirty input or stale receipt blocks publication.
* Fresh receipt verification must use freshly fetched main and the actual candidate HEAD/base. A later commit/rebase/correction invalidates the gate. Final authoritative receipt/status must remain outside tracked candidate inputs, without a post-gate evidence commit.

## Questions or Blocking Evidence Gaps

* No decision-critical owner question remains. Both findings are compatible planner-owned refinements.
* The old failed external receipt/log were not read: their supplied locations are under a filesystem path forbidden to this worker. Failure details are supplied observations corroborated by exact source mechanics, not independently rehashed execution evidence. Preserve originals unchanged; do not relocate or overwrite them under this critique's authority.

## Limitations

* No implementation or tests were executed; future success remains to be demonstrated. No fresh main fetch, full receipt verification, exact-head approval or issue/PR inspection occurred.
* Historical Review sections were read only to preserve provenance and acceptance boundaries. Their original/correction1 verdicts are not reclassified.
* External outputs must use an allowed, task-owned location outside candidate inputs. This critique grants no exception to active filesystem restrictions and does not authorize changes to the runner's shared-lock policy.
* Only this critique artifact was written. Plans/details/research/state, source, earlier evidence and Reviews remain parent-owned and unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001, safe callback argument placement.
* Action owner: Planning parent.
* Smallest next action: Incorporate PC-001 and PC-002 directly into current plan/details and record their dispositions; finalize without re-critique, then execute P01.
* User response required: No.
* Severity summary: Critical 0; High 1; Medium 1; Low 0.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction2-plan.md](.copilot-tracking/plans/2026-10-31/resident-survey-check-571-correction2-plan.md) | Current child plan assessed once. |
| [.copilot-tracking/details/2026-10-31/resident-survey-check-571-correction2-phase-details.md](.copilot-tracking/details/2026-10-31/resident-survey-check-571-correction2-phase-details.md) | Direct correction and validation targets. |
| [.copilot-tracking/research/2026-10-31/resident-survey-check-571-correction2-research.md](.copilot-tracking/research/2026-10-31/resident-survey-check-571-correction2-research.md) | Supplied failed-gate observations and roots. |
| [.copilot-tracking/rpi-sessions/2026-10-31/resident-survey-check-571-correction2-state.json](.copilot-tracking/rpi-sessions/2026-10-31/resident-survey-check-571-correction2-state.json) | Current parent-owned planning state. |
| [.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md](.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-review.md) | Immutable original Review provenance. |
| [.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-correction1-review.md](.copilot-tracking/reviews/logs/2026-10-31/resident-survey-check-571-correction1-review.md) | Immutable prior child Review provenance. |
| [.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-correction2-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/resident-survey-check-571-correction2-plan-critique.md) | Complete execution / Revise verdict and both findings. |

## Next Steps

The active planning parent applies and records both direct corrections, finalizes without another critique and proceeds through the existing implementation, one child Review and fresh full-gate publication sequence. No user action is required. This critique performs no peer-stage invocation and grants no publication approval.
