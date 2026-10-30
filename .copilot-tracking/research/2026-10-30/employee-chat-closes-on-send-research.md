<!-- markdownlint-disable-file -->
# Task Research: employee-chat-closes-on-send

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md |

## Research Brief

* Target: reproduce employee chat dismissal on Enter and Send; trace shared focus, submission, route and session lifecycle; check resident chat.
* Purpose/audience: owner-visible bug correction and independent local assessment.
* Scope: shared widget, employee host/router, resident host, existing checks/tests.
* Non-goals: Azure, deployment, push, issue closure, unrelated visual changes.
* Criteria: actual loopback applications and real Chromium; Enter and mouse Send retain visible answer across no-case/case and refresh/session re-check; retain Escape, focus-return, ARIA and access-loss boundaries.
* Outputs: dated full RPI evidence and local commit only.
* Output mode: convergence.

## Research Parameters

* Posture: focused (default for caller-specified code and failure).
* Evidence root: .copilot-tracking/research/2026-10-30/.
* Initial internal areas: src/api/README.md, web/chat-widget.js, chat.js, app.js, resident_demo/web/assistant.js, checks and tests.
* External area: current Web Interface Guidelines, fetched 2026-10-30.
* Limits: constructed data, loopback only; no secrets, Azure, deployment or remote writes.
* Research edits: evidence/state only.

## Extension Registry and Provenance

* Repository instructions selected: source guides, branch/privacy and full publication gate boundaries.
* rpi-research selected: ordered Wider, Deeper, Contrarian evidence.
* web-design-guidelines selected: fetched source before web edits/review.
* Design overhaul skills skipped: functional app bug, no redesign.
* Specialists skipped: tightly coupled continuous trace; inline investigation.

## User Participation and Research Decisions

Explicit full-loop request authorizes ordered phase progression without routine prompts. Noninteractive execution; no extra automatic follow-up session inferred. Existing clean topic branch fix/employee-chat-closes-on-send matches the task, has no PR, and is reused. Commit locally only.

## Direction Controls

Owner bug is top priority. Refs-only issue references. No push/deploy/Azure. Preserve accessibility and access/consent invalidation.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What event actually dismisses the employee dialog? | depth | Answered |
| Q2 | Do routes, session refresh, errors or resident submission share the bug? | depth | Answered |
| Q3 | What regression fails before correction and proves required behavior? | depth | Answered |

## Prior Knowledge Gate

Read original case, addendum, reference index and owner memory. README claims same-context refresh preserves chat; verify rather than trust. Supplied suspects are hypotheses, not established causes.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inventory confirmed the real constructed-data app launcher and existing shared-widget browser harness. Both hosts use the same widget. Employee submit does not call hide/reset; ordinary api() calls do not call route(). Existing checks intentionally expect same-context refresh to hide the widget.

Reflection: prioritize programmatic workspace focus and session object identity, not speculative request-triggered navigation.

#### Wave 2: Deeper

Ran the actual local API with isolated synthetic JSON, password auth and privacy fixtures using checks.design_system_browser_check.main, healthz readiness, installed Playwright and real Chromium. Network restricted to loopback. Instrumented focusin and held only the answer response while calling actual route() or start().

All 12 combinations: no-case/case x Enter/mouse Send x none/route/session. Without refresh all four remain open and show an answer. Same-route refresh hides all four with focus target app, although answer appends. Successful same-user session re-check hides all four AND discards the pending answer because start() replaces me and current() requires reference identity. Busy then remains true. Original JSON and screenshot retained externally in session files; summarized exact results below.

Reflection: the observed local failure is refresh-associated; ordinary Enter/Send alone did not reproduce. Do not claim proof of every live-site trigger.

#### Wave 3: Contrarian

Challenged disabled-Send hypothesis: focus trace shows Send -> textarea before disabling, with no external focus on isolated successful sends. Escape, explicit external focus and genuine access loss must still dismiss/reset. Examined deny(): only 401/403/404 deliberately clear chat. No such response occurred in successful reproductions. Resident submit uses the same busy() focus path and does not rerender its workspace on answers; its session setter deliberately clears on sign-in/out and must retain that boundary.

Reflection: deleting focus dismissal wholesale would break deliberate keyboard dismissal. Preserve it; stop same-context background rendering from stealing focus. Preserve employee session identity only for an exactly matching authenticated user/account payload; changed identity/capability must dispose.

#### Parent Synthesis and Disposition

* Accepted C1/C2: same-context show() focus causes unintended dismissal.
* Accepted C3: successful same-user start() creates an obsolete-consumer false positive.
* Rejected: ordinary successful submit unconditionally hides, disabled Send is the reproduced cause, API requests themselves trigger routing, or deny() caused these successful-response failures.
* Selected: preserve focus currently owned by the shared dialog during show(); reconcile equivalent employee auth snapshots without replacing me; reset on changed snapshots.
* Re-entry: not needed; bounded source trace and 12 real-browser cases settle the material hypotheses. Resident regression still required in Implement.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Workspace rendering unconditionally focuses app | src/api/src/zava_forward/api/web/app.js:92 | High |
| C2 | Any external focusin hides shared dialog; busy moves Send focus inside before disabling | src/api/src/zava_forward/api/web/chat-widget.js:86,123 | High |
| C3 | start replaces me; current() compares reference identity | src/api/src/zava_forward/api/web/app.js:136; src/api/src/zava_forward/api/web/chat.js:59 | High |
| C4 | route resets only changed context; install preserves existing widget | src/api/src/zava_forward/api/web/app.js:293; src/api/src/zava_forward/api/web/chat.js:23 | High |
| C5 | Existing browser refresh contract expects hidden dialog, missing owner-required open behavior | src/api/checks/chat_widget_browser_check.py:360 | High |
| C6 | Resident submit uses shared busy and generation guards; session/consent deliberately clear | src/api/src/zava_forward/api/resident_demo/web/assistant.js:249,297,309 | High |
| C7 | Auth projection exposes complete staff user; contractor chat forbidden | src/core/src/zava_forward/core/projection.py:197 | High |
| C8 | Real Chromium baseline: 4/4 ordinary sends pass; 4/4 route-refresh sends hidden; 4/4 session re-check sends hidden/missing answer | external session files/baseline-reproduction.json, reproduce_chat.py | High |
| W1 | Native controls, focus visibility and polite async feedback guide correction | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-30) | High |

## Alternatives and Decision State

Selected C1/C3 correction above. Reject timeout/suppression flags, synthetic event trust checks and unconditional reopening: they mask legitimate focus changes or steal focus. Reject removing all session/current guards: stale results after real identity/access loss must remain impossible.

## Open Questions, Risks, and Residual Uncertainty

Actual owner browser environment is unavailable; local constructed data cannot prove live deployment behavior.

## Planning Readiness

Ready. Research disposition: executed. Q1-Q3 answered. Plan must add a real-browser failing-before/passing-after assertion for both send methods, both contexts and both refresh types, plus resident submit/Escape/external focus, auth change and stale-result coverage.

## Artifact Self-check

Ordered Wider/Deeper/Contrarian completed inline; no delegated lane claimed. Evidence separates observed local failure from live-site uncertainty. Caller constraints retained. Parent authorized to continue Plan.
