---
title: Chat widget fix cycle 3 phase details
description: Bounded implementation and evidence contracts
ms.date: 2026-10-29
---

## Metadata

Task ID: issue-550-pr-556-fix-cycle-3.
Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan.md.
Research: .copilot-tracking/research/2026-10-29/chat-widget-550-fix-cycle-3-research.md.
Current state: P01-P03 complete with evidence in the changes and Review records;
the containing commit supplies local persistence. Actual additions:
one seven-mode unit method and two browser modes; no test removals. Browser clock
is paused during reply_scroll, advanced exactly 200 ms after pre-loading actions
and resumed afterward. Later existing threshold checks reuse that same clock.

<!-- rpi:phase id=P01 -->
## P01: Preserve loading-transition scroll intent

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fix shared widget and strengthen owned regressions

Use the existing <=1 pixel distance/history containment guard in a shared helper.
Before each busy loading-hide and delayed loading-show, capture eligibility;
after the visibility mutation, synchronously bottom only when eligible. Do not
retain a send-time flag: a reader can move upward or focus Sources in 200 ms.
Keep active/disposal guard, timer cancellation and focus behavior unchanged.
PC-001 direct disposition: use the same synchronous preserving helper for
setStatus and error changes; replace only shared-widget status writes in both
adapters, keeping unrelated callback/regulatory status untouched. This handles
resident empty-status insertion before message and employee wrapping status
after a reply without retaining stale intent.

Model shrinking clientHeight when the delayed row appears in the existing Node
harness with controlled timers and status/error geometry. Cover no loading before
200 ms, pin on reveal,
long answer following, removal, upward readers and history focus before/after
the delay, and moving back to bottom. Maximum two new test methods.

Browser reply_scroll: before sending, position follow mode at bottom with input
focused; after loading appears only read/assert geometry, never reposition that
mode. Resident follow must start after a completed reply with empty status and
assert bottom eligibility after synchronous send, before loading.
Add at most two modes for upward movement and focused history during the
delay; preserve all existing after-loading cases and focus identity assertions.
Six modified src files: widget, two existing tests, README and both scoped
adapters. Adapter wiring is justified by source-backed PC-001.

Completion: eligible delayed reply <=2 px from bottom, nonfollowers <=1 px
position change, exact focused element retained on both synthetic sites.

<!-- rpi:phase id=P02 -->
## P02: Validate the correction

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run targeted positive and negative checks

From src/api set
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Use /tmp/mv/bin/python -m unittest discover -s tests -p 'test_*chat*' -q,
/tmp/mv/bin/ruff check ., /tmp/mv/bin/ruff format --check .,
and node --check src/zava_forward/api/web/chat-widget.js.
Run checks.chat_widget_browser_check with pinned axe and an external output
directory. Preserve adverse results and explain any correction, not just passes.
Execute regression against an external copy of original chat-widget.js to prove
sensitivity. No original evidence replacement or latest.json edits.

<!-- rpi:phase id=P03 -->
## P03: Review and persist locally

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run one independent Review and commit locally

After code and checks finish, independent Review compares bounded source diff,
plan, details, critique, changes and supplied logs against caller acceptance.
Refresh Web Interface Guidelines and assess all applicable changed-web rules,
preserving baseline/changed-scope distinction. Write only the review artifact.
Human/live/assistive technology and complete publication gate remain unperformed.
Parent reconciles markers/state and commits locally with privacy-safe identity
and Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>.
