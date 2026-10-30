<!-- markdownlint-disable-file -->
# RPI Plan Critique: employee-chat-closes-on-send

## Metadata

* Task ID: employee-chat-closes-on-send-2026-10-30
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md
* Critique execution status: Complete
* Execution: exactly one independent final-candidate critique; no implementation, nested delegation or repeat critique.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan/Details, Implement/Changes and independent Review; actual local Chromium Enter and mouse Send, case/no-case, no refresh/same-route refresh/same-user re-check; executable failure before correction; resident rules-response check; preserved accessibility and identity/access/consent boundaries; API units, Ruff, mypy and browser validation; local commit only, Refs-only, no push, deployment or Azure.
* Research considered: .copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md, particularly C1-C8 and its selected/rejected alternatives.
* Source considered: src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/web/chat.js, src/api/src/zava_forward/api/web/chat-widget.js, src/api/src/zava_forward/api/resident_demo/web/assistant.js, src/core/src/zava_forward/core/projection.py, and the account/navigation assembly references in src/api/src/zava_forward/api/server.py.
* Test and command evidence considered: src/api/checks/chat_widget_browser_check.py, src/api/tests/test_chat_widget_focus.py and src/api/README.md. Required project context was read from the original case study, addendum, reference index and owner memory.
* Decisions and dependencies: preserve chat-owned focus in show(); preserve me reference only for equal complete user/account snapshots; keep current()/abort guards and explicit invalidation; P02 depends on P01; no redesign or resident runtime changes without evidence.
* Locked test boundary: existing browser check and focus unit owner; at most one focused browser module and two JS-harness unit methods if necessary; no test removals or new tooling. The corrections below fit that boundary.
* Assessment covers all supplied FR1-FR4, non-functional requirements, AC1-AC5 and P01/P02 tasks once. It assesses plan credibility, not implementation correctness, live-site reproduction or human accessibility acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, AC1, C1-C5, P01-T01 | Covered | Actual local app, real send interactions, 12-case matrix and failing-before order are explicit. Both reproduced failure modes must be retained in red/green evidence. |
| FR2, accessibility requirements, P01-T02 | Partial | Focus-preservation approach is sound, but acceptance does not explicitly assert the exact focused control through rendering; PC-002. |
| FR3, AC2, C3/C7, P01-T02 | Partial | Complete user/account equality and a resurrection guard are specified; account-only changes and the re-check race are not explicit executable cases; PC-001. |
| FR4, AC3, C6 | Covered | Actual resident rules answers for both methods, consent/session invalidation, Escape and external focus are retained. Existing browser coverage supplies useful consent/stale-result checks. |
| Non-functional requirements | Covered | No timers, suppression heuristics, automatic reopening or asynchronous answer focus. Native nonmodal controls and live updates remain. |
| AC4, P02-T01, dependencies | Covered | Targeted then full API tests, Ruff check/format, mypy, JS syntax and actual browser checks are explicit; prerequisite failures/skips must remain honest. |
| AC5, P02-T02, delivery restrictions | Covered | One critique, one independent Review and local commit with dated evidence; no remote writes or claimed publication approval. |
| Locked test ownership and scope | Covered | Existing owners can accommodate bounded parametrized cases; no wider test framework or unrelated app changes are needed. |

## Verdict

* Verdict: Revise
* Rationale: The proposed correction addresses both source-backed causes without removing deliberate dismissal or stale-consumer protections. Two executable acceptance gaps remain around the newly introduced session reconciliation and the precise focus contract. These require small planner corrections, not a different design or another critique.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Prove complete account comparison and the auth re-check race through start()

* Related IDs: FR3, AC2, C3/C7, P01-T01, P01-T02.
* Evidence: Phase details P01-T02 requires complete user/account matching and a guard against resurrection, but its executable cases name equivalent re-check and changed user/capability only. src/api/src/zava_forward/api/web/app.js:133-149 currently assigns the fetched snapshot directly. src/api/src/zava_forward/api/web/chat.js:59 makes reference identity a consumer boundary. src/api/checks/chat_widget_browser_check.py:648-737 tests stale chat promises, but its session transition assigns me = null and calls reset directly; it does not exercise start() or delayed /api/me reconciliation. The /api/me response separately assembles user, account and navigation in src/api/src/zava_forward/api/server.py:399-402.
* Concern: The current planned tests could pass with a user-only comparator, an incomplete capability comparator, or a guard that never gets exercised against an obsolete successful auth response. Existing manual session/reset coverage cannot verify the new reconciliation path.
* Impact: A changed account could retain the previous conversation/consumer, or a delayed successful re-check could restore an invalidated session. Conversely, comparing unrelated mutable data could keep dropping valid pending replies. This is a risk in the proposed implementation boundary, not a claim that the unimplemented fix already has those bugs.
* Smallest useful change: Add explicit acceptance cases through actual start() with controlled /api/me timing: equal complete user/account with changed counts/navigation updates those non-identity fields while preserving the pending consumer; account-only change and user capability change each reset/abort; a held successful re-check released after logout/session invalidation does not restore me, navigation or chat. Complete a held old setup/thread/ask result after a changed snapshot and assert no stale request continuation, answer, focus or busy cleanup affects a replacement widget. Retain the already required real equivalent re-check during setup/thread/ask; do not replace it with direct me assignment.
* Action owner: Planning parent.
* Exact resolving evidence: Revised AC2 and P01 task details name these cases and their assertions within the locked owners. Implementation evidence must identify the executed cases, real start() invocation, controlled payload differences and late-response ordering, with passing results; equivalent re-check red evidence must demonstrate the original lost-answer/busy failure independently of visibility.
* Decision route: Direct planner correction. The owner already requires full user/account comparison and stale/access protection; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make exact focus preservation an executable refresh assertion

* Related IDs: FR1, FR2, AC1, AC3, C1/C2/C5, P01-T01, P01-T02.
* Evidence: AC1 enumerates visibility, answer, busy, draft and skill assertions, but not exact document.activeElement retention. P01-T02 correctly says to leave chat-owned focus unchanged. src/api/src/zava_forward/api/web/chat-widget.js:86 moves mouse Send focus to the input before disabling; its externalFocus handler at lines 122-125 deliberately hides on outside focus. Existing employee_refresh in src/api/checks/chat_widget_browser_check.py:327-379 expects app focus and hidden chat. The unit harness loads chat-widget.js/chat.js, not app.js, so existing focus unit tests do not exercise show().
* Concern: A replacement refresh test that checks only open/expanded state could accept a fix that moves focus to another control inside the popup. It could also miss reopening a deliberately closed popup after a delayed render. Both contradict the plan's stated focus contract even if the answer is visible.
* Impact: Keyboard users and history/Sources readers could lose their interaction position while the headline browser matrix remains green; deliberate dismissal could regress.
* Smallest useful change: Require the browser matrix to capture and compare the actual focused element after send activation, during pending refresh and after completion. For mouse Send, capture after the existing busy transition into the input, not before disabling Send. Add bounded representative refresh checks with history/Sources focus, and with deliberate external focus or Escape occurring before a delayed render completes: preserve internal focus; keep dismissed chat hidden/aria-expanded=false; do not redirect outside focus or reopen on completion. Retain ordinary workspace focus when chat does not own it. These can be cases in the existing browser owner, not additional modules.
* Action owner: Planning parent.
* Exact resolving evidence: Revised AC1/FR2 task assertions explicitly require activeElement identity, the mouse-send capture point, history/Sources focus and hidden-before-completion behavior. Browser red/green logs then demonstrate the original render focus theft and the passing internal/external/closed cases, alongside retained Escape-to-launcher behavior.
* Decision route: Direct planner correction. The owner has already required preserved accessibility and intentional dismissal; no significant or divergent user decision is needed.

## Strengths and Residual Risk

* The selected fix is narrowly aligned with the two demonstrated causes: unconditional app.focus() and replacement of the me reference during a successful equivalent re-check.
* Retaining external-focus dismissal, object/current guards, aborts and explicit access-loss handling avoids masking the bug with reopening or weakening stale-result protection.
* The 12-case actual-app matrix, resident actual-rules requirement and explicit separation from intercepted timing tests are credible engineering evidence boundaries.
* Baseline reproduction is reported in the supplied research; its external JSON, script and screenshots were not supplied at workspace-relative locations and were not independently rerun in this critique. Implement must preserve and reference the original evidence and its new executable failing-before results.
* Actual owner-site triggers, live model behavior and human screen-reader/voice-control acceptance remain unestablished, as the plan already acknowledges. No extra deployment or accessibility acceptance scope is requested here.

## Questions or Blocking Evidence Gaps

* No unresolved owner decision or decision-critical research gap. Both findings can be resolved by direct planning edits without broadening the bug.

## Limitations

* Source and existing checks were inspected read-only. No tests, local browser, dependency setup, authentication request, commit or remote operation was performed.
* The source inspection supports the proposed mechanism; it does not verify a future implementation or reproduce every live-site trigger.
* Only this critique artifact was written. Supplied untracked planning/research/state artifacts were left untouched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Amend AC2 and the P01 details with the bounded real-start identity/race assertions, add PC-002 focus assertions, record both dispositions, then finalize planning without another critique.
* User response required: No.

| [.copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md](.copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md](.copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md) | Phase details needing bounded assertion corrections |
| [.copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md](.copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md) | Supplied reproduction and source evidence |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-chat-closes-on-send-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-chat-closes-on-send-plan-critique.md) | Complete independent finding set |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly within the locked test boundary, record dispositions and finalize the plan. No user action or repeat critique is required. Implementation remains the next ordered stage after those corrections; no push, deployment or Azure operation is authorized.
