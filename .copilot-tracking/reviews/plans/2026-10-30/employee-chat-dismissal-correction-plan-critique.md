<!-- markdownlint-disable-file -->
# RPI Plan Critique: employee-chat-dismissal-correction

## Metadata

* Task ID: employee-chat-dismissal-correction-2026-10-30
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-dismissal-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-chat-dismissal-correction-phase-details.md
* Critique execution status: Complete
* Candidate baseline: fix/employee-chat-closes-on-send, HEAD 366ca4a2
* Execution count: exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: correct original RV-001 and obtain RV-002 full API evidence through the authorized correction RPI cycle; preserve all 12 Enter/Send combinations; local Refs-only commit, no push, live warming, Azure or credential output.
* Candidate inputs: the plan and phase details named above; .copilot-tracking/research/2026-10-30/employee-chat-dismissal-correction-research.md, including C1-C8/W1; .copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md.
* Source inputs: src/api/src/zava_forward/api/web/app.js, particularly show(), login(), start(), route() and caseView(); src/api/checks/chat_submit_browser_check.py; relevant unchanged hide/external-focus behavior in src/api/src/zava_forward/api/web/chat-widget.js; focused-check integration in src/api/checks/chat_widget_browser_check.py; src/api/README.md and src/api/pyproject.toml validation configuration.
* Repository context: original case study, addendum, reference index and owner memory. No company, legal or live-system acceptance claim is inferred from these contextual documents.
* Decisions and dependencies: existing topic branch; one critique and one later independent Review; maximum runtime changes limited to show() and one last-rendered-context variable; existing focused check extended with at most one helper; no removals, new check module, dependency or shared-widget/auth/resident changes.
* Assessment boundary: credibility of the complete supplied plan, its functional and non-functional requirements, phases, tasks, dependencies, acceptance criteria, risk handling and delivery boundary. This is not implementation Review or execution of the planned browser/full-unit gates.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner direction; AC5; P02-T02 | Covered | Baseline matches 366ca4a2 on the requested topic. Plan requires local privacy-safe Refs #550 commit, preserved adverse evidence and one independent Review; no remote publication. |
| RV-001; C1-C3; FR1; AC1; P01-T01 | Covered | Baseline show() redirects any non-chat focus to #app; render_focus() captures renderFocus but asserts #app instead. Plan requires the opposite exact equality assertion before runtime edits and includes delayed Escape, Close and external dismissal with hidden/expanded state and retained draft. |
| C5-C6; FR1/FR3; AC3 | Covered | route() advances displayedHash before awaited reads. The candidate instead retains the previously rendered authenticated session/path and checks connected outside-app focus after replacement. This distinguishes refresh from actual destination/session transition. |
| FR2; AC2; C3/C8; P01-T01 | Covered | Existing send_matrix() covers 2 activations x 2 case contexts x 3 refresh modes. Plan preserves all 12 and retains composer/log/Sources assertions and existing auth/resident boundaries. |
| FR3; AC3; P01-T01 | Covered | Actual browser counterexamples explicitly cover cross-path navigation, changed session, replaced app input, disconnected external control, body/no-chat rendering and normal #app fallback. |
| NFR1; scope; P01-T01 | Covered | One show-local decision plus one context variable fits the traced lifecycle without timers, dismissal flags or widget callbacks. Existing render_focus() owns dismissal changes; at most one helper owns navigation counterexamples. |
| RV-002; C4/C7; NFR2/NFR3; AC4; P02-T01 | Covered | Full API discovery retains the specified PYTHONPATH/python3 command under flock -w 600. Ruff check, format check, mypy and focused/shared/employee/resident browser checks are explicit. Sanitized synthetic loopback evidence and failure/timeout blocking are required. |
| C8; P02-T01 | Covered | The shared browser check already imports the focused employee runner; the standalone focused runner additionally exercises actual constructed resident rules replies. Existing integration is retained rather than duplicated in a new module. |
| W1; documentation; limitations | Covered within supplied evidence | Research records the retrieved guideline and focus rationale; the plan promises only scoped engineering evidence, not fresh whole-app accessibility, human or live acceptance. No independent external-source refresh was needed for this read-only planning assessment. |
| P01/P02 dependencies and handoff | Covered | Critique disposition precedes regression/correction; finalized runtime precedes full validation; reconciled validation precedes independent Review and local commit. Failures are not silently converted into acceptance. |

## Verdict

* Verdict: Pass
* Rationale: The candidate directly corrects the coupled source/assertion defect without losing ordinary navigation focus or the original submitted-chat behavior. It makes the missing full discovery a blocking measured requirement, retains bounded ownership and additions, and separates local delivery from publication and live acceptance.
* Severity counts: 0 Critical, 0 High, 0 Medium, 0 Low.

## Findings

No actionable PC-xxx findings were identified in the supplied candidate boundary. There are no withheld findings, direct planner corrections or significant/divergent user decisions.

## Strengths and Residual Risk

* Last-rendered context, rather than the eagerly updated displayedHash alone, addresses the actual lifecycle. Equal successful start() rechecks retain me identity; changed identity/account/capability replaces it and resets chat. Requiring an authenticated matching rendered context avoids treating login/auth transition as a same-session refresh.
* Preserving existing visible-chat ownership separately protects the original composer/log/Sources and pending-send behavior. Genuine path changes already reset chat; the plan does not broaden visible-chat preservation into a navigation exemption.
* Capturing current activeElement at render time and requiring connectivity after replacement avoids restoring a stale earlier choice. Replaced app descendants and removed external controls must fall back, while a connected deliberate launcher/nav target can remain focused.
* The baseline render_focus() includes only Escape/external dismissal and positively expects the defective target. Adding Close and replacing that expectation with exact retained-focus equality is explicitly required, not left to a passing aggregate browser status.
* All 12 sends and existing session/stale-result/resident checks remain required. No test removal or new dependency is authorized.
* Full-suite success, browser success and lock admission are unmeasured. The plan expressly treats timeout, missing prerequisites or failing checks as acceptance blockers. Expected skip counts/reasons must be supported by actual retained run evidence, not inferred from prior results.
* Local synthetic browser checks cannot establish live-site, real-model, human assistive-technology or whole-app WCAG acceptance. This limitation is retained rather than waived.

## Questions or Blocking Evidence Gaps

* None for planning readiness. The still-unexecuted implementation and validation gates are planned work, not missing evidence necessary to assess this candidate plan.

## Limitations

* No source edits, browser runs, full-suite attempts, lock acquisition, dependency changes, remote writes or credential access were performed.
* The existing untracked correction plan/details/research/state were left untouched. Only this critique artifact was written.
* Research C1-C8 was assessed against the supplied review and relevant source. W1 was considered as supplied research evidence, not independently re-retrieved or represented as a fresh web-interface conformance review.
* This Pass approves planning credibility only. It does not resolve RV-001/RV-002, approve implementation, establish publication eligibility or supersede the original adverse Review.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: active planning parent.
* Smallest next action: record this single Pass disposition, finalize the candidate and proceed to P01-T01, first obtaining the unchanged-runtime failing browser assertion.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/employee-chat-dismissal-correction-plan.md](.copilot-tracking/plans/2026-10-30/employee-chat-dismissal-correction-plan.md) | Assessed correction candidate |
| [.copilot-tracking/details/2026-10-30/employee-chat-dismissal-correction-phase-details.md](.copilot-tracking/details/2026-10-30/employee-chat-dismissal-correction-phase-details.md) | Assessed task boundaries and validation |
| [.copilot-tracking/research/2026-10-30/employee-chat-dismissal-correction-research.md](.copilot-tracking/research/2026-10-30/employee-chat-dismissal-correction-research.md) | Supplied C1-C8/W1 evidence |
| [.copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md](.copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md) | Preserved original RV-001/RV-002 |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-chat-dismissal-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-chat-dismissal-correction-plan-critique.md) | Complete single critique |

## Next Steps

The active parent may finalize planning and continue P01-T01 under the existing owner authorization. No user action or repeated critique is required. Retain the single independent post-implementation Review and all validation/local-only delivery boundaries.
