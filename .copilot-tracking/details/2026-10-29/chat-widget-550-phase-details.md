<!-- markdownlint-disable-file -->
# RPI Phase Details: Shared chat widget

Task ID: 550; slug: chat-widget-550; date: 2026-10-29.
Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-plan.md.
Research: .copilot-tracking/research/2026-10-29/chat-widget-550-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Implemented and locally validated | P01-T01 |
| P02 | Implemented and locally validated | P02-T01 |
| P03 | Local checks/documentation complete; Review/commit pending | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Shared widget and adapters

<!-- rpi:task id=P01-T01 -->
### P01-T01: Shared layout and audience adapters

Factory owns named icon launcher, nonmodal dialog, title/close, scrolling log/articles,
native details intro, consent slot, textarea, input-area select, disabled attach/
voice with visible reasons, send and polite status/error. Return explicit refs
and lifecycle methods; no API coupling. Preserve current IDs where useful.
Shared CSS consumes both sites' existing semantic tokens, safe areas and
dynamic viewport height; no global restyling. Async loading indicator starts at
200ms, timer cleared on finish/disposal. Enter handling ignores IME composition.
Adapters append turns, retain drafts on failure, preserve newly typed text,
prevent duplicate sends and invalidate obsolete results.
Employee shares /api/chat skills/thread/ask and aborts on context/session/access
changes. Resident consent stays above composition; withdrawing clears transcript,
draft and pending results. No network request from opening or consent alone.
Callback results add an explicit button to open the existing manual form.
Completion: both actual apps use identical shared asset bytes; browser checks
prove lifecycle, UI and safety behavior. No dependencies or source tests added.
The case panel's duplicate generic composer is replaced by Open chat, using the
same popup and preserving proposal/regulatory controls. The employee popup
requires the existing /api/chat/status privacy warning before enabling typing.
Pending and edited drafts retain existing data-case-dirty/unsaved warning
semantics across same-case tab/save reconstruction. Migrate the directly affected
test_chat_panel opt-in browser and case_journey_browser_check lifecycle selectors;
retain their success/failure, typed-ahead, dirty/unload and privacy-failure checks.

Lifecycle contract (PC-001): hide retains draft/skill/thread/history and pending
skills/thread/ask; reopen reuses the same instance and pending setup. Hiding
never aborts, destroys or restarts initialization. Success/error while hidden
may update that same session's thread/status, never focus. Disposal on employee
route/session/access loss aborts controller, removes instance and guards every
success/catch/finally. A replacement has its own identity and timer. Resident
consent/session generation fences success/error/finally; withdrawal clears busy
timer and permits re-consent/new send, whose timer/status cannot be touched by
old continuations.

PC-002: the chat adapter owns shared-factory readiness through the existing
bounded workspace script recovery helper, without adding a shell-wide dependency.
Adapter evaluates without eagerly invoking factory; install only when ready.
Missing factory disables only chat with visible
manual-workflow feedback, bounded recovery/exhaustion, no lexical re-evaluation.

<!-- rpi:phase id=P02 -->
## P02: Resident intent regression

<!-- rpi:task id=P02-T01 -->
### P02-T01: Restrict home summary routing

chat.route currently lets a single "home" token capture unrelated reports.
Use explicit supported record/address/planned-improvement requests; safety
remains first and unknown is the safe default. Add rat, other home concerns
and unsupported policy questions to route and real HTTP tests. Keep explicit
home topic behavior and cross-case denial. Correct old expectations that
accidentally encode the home-summary bug. No raw text-to-model forwarding.
Completion: rat response contains honest inability/housing contact, no address,
no summary content, no model invocation; hazard suite remains passing.

<!-- rpi:phase id=P03 -->
## P03: Validation and documentation

<!-- rpi:task id=P03-T01 -->
### P03-T01: Local validation

Use existing real server fixtures, not a standalone mock UI. New browser harness
serves both local apps, checks consent/request count, sends multiple turns,
controls delayed/errors via bounded route interception, verifies dimensions,
source collapse, focus/Enter/Shift+Enter, six/one selector choices and reset
boundaries. Store outputs outside source. Existing regressions check API roles,
audits and session binding. Run component ruff and full configured mypy; report
pre-existing failures accurately. No az or cloud fallback.

PC-003 exact browser oracles:

| Area | Assertion |
| --- | --- |
| Thread/layout | Multiple turns overflow log; scroll log while composer bounding box stays fixed; newest answer at scroll bottom; popup stays visible. Repeat 320/390/1280. |
| Timing | Controlled browser clock: held request has no indicator at 199ms; indicator at 200ms; fast success/error clears timer; disposal clears timer; reduced motion has no animation. |
| Keyboard | Shift+Enter adds newline and zero requests; Enter exactly one request; composition Enter zero; Escape hides and focuses launcher; Tab can leave nonmodal popup. |
| Sources/controls | Details initially closed, truthful compact label; disabled attach/voice with readable reasons; six employee/one resident choices. |
| Isolation | Obsolete successes/rejections after route/session/consent invalidation leave replacement log/status/draft/focus/busy unchanged, no downstream ask. Hidden current request may finish without focus. |
| Failure | Shared asset transient recovery/exhaustion uses bounded existing loader; ordinary authorized workflow remains available with visible feedback. |

Replace old modal-containment/close-destroys assertions with nonmodal traversal/
hide-retains assertions; preserve route/session/denial and late-success coverage.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Documentation, Review and commit

README states session-only persistence, disabled capabilities and evidence limits.
Record commands/results in changes. Invoke rpi-review once and use independent
reviewer for meaningful source boundary, not just a self-review. Keep original
critique and Review evidence even if blocked. Resolve GitHub identity with gh
api user and configure local noreply email before commit. No push or PR.
No source correction after Review inside this task; route findings as follow-up.
Human acceptance stays unchecked. No full publication-gate claim.
