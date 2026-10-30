<!-- markdownlint-disable-file -->
# RPI Phase Details: employee-chat-closes-on-send

## Metadata

* Task ID: employee-chat-closes-on-send-2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md
* Research: .copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md
* Initial readiness: research Ready; implementation candidate ready for critique.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Partial after Review RV-001; headline red/green passes | P01-T01 complete; P01-T02 routed |
| P02 | Partial: full units lock-blocked; Review/local commit delivered | P02-T01 blocked; P02-T02 complete |

<!-- rpi:phase id=P01 -->
## P01: Correct refresh lifecycle

Context: research C1-C8 demonstrates unintended app.focus and stale me reference. Scope excludes redesign and remote behavior.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Failing-before assertions

Extend existing browser infrastructure using actual synthetic loopback API. Hold answer, use real keyboard/mouse, await actual route()/start() rendering, assert dialog stays visible and reply appends. Exercise no-case and ZF-1 case, each activation, and no refresh/route/session refresh. Record initial failure before source edits. Check real resident rules replies for Enter and Send, preserving explicit consent.

Completion: original failure and post-fix 12/12 matrix plus resident evidence. Tests outside distributable runtime package; no credentials printed.

PC-001: use actual start() with held setup/thread/ask plus /api/me account-only/user/capability changes and changed counts/navigation with identical auth. After changed snapshot, complete obsolete work and prove replacement text/focus/busy unchanged. Hold successful /api/me across session invalidation; release and prove no restoration.

PC-002: capture exact activeElement after send busy transition and retain through refresh and answer; representative log/Sources focus must stay. Delayed render after Escape/external focus must not reopen chat or redirect deliberately chosen focus. Ordinary workspace focus remains when chat does not own it.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Root-cause correction

In app.js show(), leave focus unchanged when an existing visible shared chat owns document.activeElement; otherwise preserve ordinary app focus behavior. Never reopen a deliberately hidden popup or refocus on answer. Keep focusin/Escape handlers unless evidence demands change.

In start(), fetch the auth snapshot and preserve object identity only when complete user and account payloads match. Reset employee chat before accepting changed identity/capabilities; preserve source/current guards and explicit access loss. Add guard against resurrection if me changes during re-check. Equivalent counts/navigation data still update. Verify pending setup/thread/ask after real equivalent re-check, and changed user/capability while pending.

Update same-context refresh browser expectation based on whether chat owned focus at render time: automatic background focus must not dismiss, explicit outside focus still does. Update API README only for this contract.

Completion: bounded code diff and semantic boundary tests. No runtime resident change unless its focused browser evidence reproduces a host-specific issue.

<!-- rpi:phase id=P02 -->
## P02: Validation and review

Dependency: P01 complete.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validation

From src/api use PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests and existing /tmp/mv tools. Focused test_chat_widget_focus/test_chat_panel/test_resident_chat_api; full unittest discover; ruff check ., ruff format --check ., mypy; node --check changed JS. Browser runs use fresh external directories and actual Chromium. Preserve baseline evidence and distinguish actual rules answers from intercepted timing tests. Shared heavy lock follows README; do not mutate a shared environment.

Completion: accurate pass/fail/skip summary with logs; no WCAG or live-site acceptance claim.

Current evidence: focused 68-unit run passes (one opt-in SQL skip), final Ruff/format/mypy/JS/compile/whitespace passes; standalone focused and final integrated Chromium/axe pass. Full API discovery not started on two nonblocking lock attempts. P02-T01 remains unchecked for that missing required result.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and local delivery

Activate rpi-review once after implementation, independently inspect full changed boundary and refreshed Web Interface Guidelines. Preserve original outcome and route review findings; no review loop. Commit original dated evidence plus implementation locally using gh-resolved privacy-safe author/committer email and required Copilot trailer. All issue references Refs-only. No push, no PR creation, no deploy. Publication requires separately authorized complete exact-head gate and hosted/human approval, not claimed by local tests.

Completion: durable review and local commit ID, clean candidate state, honest remaining gates.

Original one-pass Review: Complete / Not accepted, canonical .copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md. RV-001 routes delayed-dismissal focus correction to later implementation; RV-002 routes missing full-unit evidence. Commit includes this dated record; immutable ID is obtained from git log. No source correction after Review, no repeated assessment or remote publication.
