<!-- markdownlint-disable-file -->
# Task Research: employee-acceptance-attempt-3

## Research Brief

* Date: 2026-10-30, owner update 11:45Z.
* Status: Complete. Output mode: audit. Posture: focused, from bounded caller scope.
* Purpose: employee-site authenticated acceptance evidence for Refs #550, Refs #551 and Refs #552.
* Audience: owner and independent evidence reviewer.
* Scope: extend authenticated-live-acceptance and employee-password-acceptance; read both original Reviews first, preserve them unchanged.
* Non-goals: resident sign-in, product repairs, Azure/resource/role/policy changes, publication or issue closure.
* Criteria: actual authenticated chat/map/case observations; complete original 19-row criterion inventory with compound limitations; /api/me binding booleans only.
* Output: dated Research/Plan/Implement/Review artifacts and local Refs-only commit.

## Research Parameters and Direction Controls

* Root: .copilot-tracking/. Existing clean topic chore/auth-acceptance-1030; no remote PR found.
* At most TWO sign-in attempts in this task, with no silent retries.
* First trimmed file line is password; second line, when nonempty, is a Temporary Access Pass (TAP). Read only inside automation. Never emit either.
* Owner reports passkey requirement removed; MFA exclusion and ProgrammeManager are supplied context, not independently validated policy.
* Use supported Other ways / Sign-in options / password / Cancel routes; use TAP option if line 2 exists. Stop if no supported route exists and retain exact sanitized offered text.
* No screenshots, video, HAR, trace, console/request logs or raw exceptions. Zero screenshots is stricter than masked secret-field screenshots.
* Secrets are never passed as tool arguments or printed. Capture-free employee-only runner, not prior fail-open resident runner.
* User explicitly selected the next full finite loop; existing automatic session supplies mode consent. No routine clarification required.

## Extension Registry and Participation

* Selected: repository instructions (all paths), rpi-research and subsequent canonical RPI phase skills; caller's strict attempt/capture constraints take precedence.
* Skipped: redesign/design skills, no web implementation; research specialists, tightly coupled bounded trace handled inline.
* Independent plan critique and final Review will use bounded read-only delegates, never credential access or live authentication.

## Prior Knowledge Gate

* Read authenticated-live-acceptance original Review and employee-password-acceptance original Review before this task.
* Original eighteen unmet criteria and source-only 551-04 remain historical, not current live acceptance.
* Earlier password runner has callback/deadline/uncertain-submit defects. Do not execute it unchanged.
* Known gate limitation: prior current-main ancestry failure. Local commit requested; no lineage rewriting or push authorized.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What prior findings and exact issue criteria must constrain attempt 3? | Answered by original Reviews and current issue bodies |
| Q2 | What authoritative employee authentication contract and selectors can be used without retaining claims? | Answered C3/C4 |
| Q3 | How can two supported attempts use password/TAP without secret or retry ambiguity? | Answered C2 and explicit caller constraints |

## Research Cycle Log

### Cycle 1: Wider

Read original Reviews, current issue bodies and existing runners. Reflection: earlier no-route observations do not prove current policy; a fresh bounded attempt is justified by owner direction, but old runner defects must not be inherited.

### Cycle 1: Deeper

Inline source inspection: protected /api/me returns 401 without provider authentication. Its supported response is user/account, including trusted-proxy provider, display-email/account-email, mapped role, view_only and optional bound object. Derive only booleans in-browser, compare expected account email and employee role, require explicit schema/provider/identity match before UI interaction. Binding is independent and can legitimately be false. Reflection: do not infer authenticated from a name or email alone. Inspect shared chat, map browser assertions and case workspace selectors; no product edits are needed.

### Cycle 1: Contrarian

Challenge: a username-page hidden password decoy is not a credential route; require a visible supported password/TAP heading plus visible input. A timed-out submit can have delivered credentials; persist submission intent before keypress, never retry uncertain delivery. Count each fresh browser sign-in as an attempt, including no-route attempts. At most one credential submission per attempt. Prefer the actual supported TAP route when the second line exists, rather than filling TAP into a password box. No route means terminal stop, not two mandatory launches. An existing source test proves coverage, not live marker agreement; current thin geometry is not comparative improvement; employee-only evidence cannot prove resident/shared-use obligations. Reflection: reject broad acceptance and preserve exact sanitized stop text with no captures.

### Parent Synthesis and Disposition

* Accepted C1/C2: historical adverse outcomes and runner defects remain unchanged; new runner must avoid these defects before live reuse.
* Accepted C3/C4: strict in-browser response classification and scoped UI observations.
* Accepted caller control: fresh bounded execution is authorized after tenant change; policy state is not independently diagnosed.
* Rejected: unbounded retries, passkey bypass, policy/role repair, secret-bearing tool calls, raw provider exceptions or authenticated page dumps.
* Deferred: resident obligations, human acceptance, native AT and trusted prior geometry.
* Re-entry: no further research cycle needed; current questions are answered sufficiently to plan. Actual access is implementation evidence, not assumed.

## Evidence Log

* C1: .copilot-tracking/reviews/logs/2026-10-30/authenticated-live-acceptance-review.md:1, original adverse evidence and 19-row boundary.
* C2: .copilot-tracking/reviews/logs/2026-10-30/employee-password-acceptance-review.md:142, callback/deadline/uncertain-submit findings.
* W1: https://github.com/jmservera/ama/issues/550, retrieved 2026-10-30 with gh; nine compound criteria.
* W2: https://github.com/jmservera/ama/issues/551, retrieved 2026-10-30 with gh; four map criteria.
* W3: https://github.com/jmservera/ama/issues/552, retrieved 2026-10-30 with gh; six case criteria.
* C3: src/api/src/zava_forward/api/server.py:262 and :396; authenticated /api/me contract. src/api/src/zava_forward/api/auth.py:159; trusted-proxy account identity. src/core/src/zava_forward/core/identity.py:52 and :169; role/view-only/binding distinction.
* C4: src/api/src/zava_forward/api/web/chat-widget.js:28; shared chat semantics and 200ms timer. src/api/src/zava_forward/api/web/chat.js:84; ask behavior and AI/rules distinction. src/api/checks/map_fullscreen_browser_check.py:98; compact filters and genuine marker checks. src/api/src/zava_forward/api/web/case-workspace.js:61; blocker disclosure, icons and tabs.

## Alternatives, Decisions and Residual Uncertainty

* Selected: new capture-free employee-only runner; reuse concepts, not defective original executable.
* Password alone versus TAP: select the offered method consistent with available file lines; no credential guessing, account recovery or repeated submission.
* Unresolved live access/roster/deployed parity remain unknown until observed. No full Fluent/WCAG or whole-issue approval can be inferred from scoped automation.
* Self-check: all three waves completed inline, references and constraints explicit, no credential read or live attempt during Research.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready. No live sign-in has occurred in this task.
