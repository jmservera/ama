---
title: Chat widget loading scroll intent research, fix cycle 3
description: Focused evidence for issue 550 and PR 556
ms.date: 2026-10-29
---

<!-- markdownlint-disable-file -->

## Research Brief

Fix the delayed loading-row layout change that loses bottom-follow intent in
an overflowing conversation. Audience: implementer and PR reviewer. Output mode:
convergence. Posture: focused, selected from the named source and supplied failure.
Source changes stay in src/. No push, Azure operations, latest.json edits or
unrelated design changes. Produce dated Research, Plan, Implement and Review
evidence and a local co-authored commit.

## Research Parameters and Direction Controls

Investigate chat-widget.js, its callers, CSS, browser check and focus tests.
Questions: where does geometry change; how can current reader intent be sampled
without retaining stale intent; what test reproduces the delayed failure without
repositioning after loading? User supplied adequate scope; no intake question is
needed. Initial hypothesis: the loading row reduces clientHeight after the last
bottom pin, so the reply's geometry-only check incorrectly disables following.

## Extension Registry and Provenance

Repository instructions and RPI research selected. Web Interface Guidelines
selected and fetched from their current upstream source on 2026-10-29.
Fluent/WCAG/content baselines remain authoritative. Public-page design and visual
redesign skills skipped: this is a bounded app behavior correction, not redesign.
Research specialists skipped: one tightly coupled code trace is handled inline.

## Prior Knowledge and Participation

Read original specification, addendum, reference index and owner memory.
Memory is context, not evidence. Prior session search returned no matching
sessions. git pull --rebase completed first, already up to date. Clean worktree,
feat/chat-widget-550, active PR 556 targeting main: continue the same workstream.

## Research Cycle Log

Cycle 1 Wider: widget exposes busy/message/status independently; inspect callers,
layout and existing browser coverage before selecting a correction.
Reflection: supplied bug agrees with current widget code, but status timing and
reader interaction need deeper inspection.

Cycle 1 Deeper: both adapters set status and append the user message synchronously
after busy(true); reply_scroll waits for loading, then positions even its positive
follow case at the bottom. This masks the actual 200 ms layout transition.
The loading row is a flex sibling that reduces the log clientHeight (C2-C4).
Reflection: sample eligibility immediately before changing loading visibility,
then restore bottom synchronously, avoiding any cached send-time intention.

Cycle 1 Contrarian: an unconditional bottom call or cached send-time flag would
override upward scrolling during the 200 ms delay. History focus must suppress
following even when geometrically at bottom. Existing five-mode browser test
already covers upward/history interaction after loading, but not during delay.
The unit harness can model the loading row height and timer deterministically.
Reflection: share one current-geometry/history-focus predicate between message
and loading transitions; no observers, sticky flags or new event listeners.
Re-entry is unnecessary: focused questions are covered and remaining behavior
can be settled by targeted positive/negative controls during implementation.

## Evidence Log

* C1: src/api/src/zava_forward/api/web/chat-widget.js:75-103.
  busy reveals loading after 200 ms; message calculates follow from current
  geometry and refuses to follow while focus is in history.
* W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-29. Preserve accessible async feedback, focus and native
  semantics; avoid unrelated visual changes.
* C2: src/api/checks/chat_widget_browser_check.py:157-220. Existing follow case
  repositions after loading, masking the defect.
* C3: src/api/src/zava_forward/api/web/chat-widget.css:12,24-29.
  Log flexes while status and loading consume nonshrinking sibling space.
* C4: src/api/src/zava_forward/api/web/chat.js:86-119 and
  src/api/src/zava_forward/api/resident_demo/web/assistant.js:246-295.
  Both adapters share the same widget and busy/message lifecycle.
* C5: src/api/tests/test_chat_widget_focus.py:1-145. Node harness already checks
  bottom tolerance, older readers and history focus without a browser.
* C6: .copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-copilot-fixes-review.md:61-65.
  Prior cycle deliberately moved test positioning after loading; preserve that
  original evidence rather than relabel it as proof of this newly requested case.

## Findings, Alternatives and Decision State

Accepted: snapshot current follow eligibility immediately before loading
visibility changes, then restore bottom only if allowed (C1-C5). This preserves
intent across this status-row size change without overriding newer user actions.
Rejected: unconditional pinning, stale send-time flags and layout observers.
Planning critique PC-001 establishes that resident empty-status insertion
precedes message/loading sampling. Amend the recommendation to a shared
synchronous preserving status setter, wired only to both widget adapters,
and apply the same guard to error sibling changes. This supersedes the initial
rejection of a status API; it is needed to preserve bottom-before-send intent.
No copy, consent, model or semantic changes.

Unit coverage will model 200 ms loading shrink, long reply growth, loading removal,
upward scrolling and focused log/Sources both before and after the delay.
The two-site browser positive case must position only before sending and then
leave the log untouched through loading and the long reply.

## Readiness and Continuation

Research disposition: executed. Planning Readiness: Ready. All questions answered;
no unresolved design decision. Self-check: source IDs and retrieved external
source recorded; wider/deeper/contrarian waves complete; no source writes.
Parent owns automatic continuation for the explicitly requested full RPI loop.
