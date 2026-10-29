---
title: Chat widget fix cycle 3 plan
description: Delayed loading-row bottom-follow correction for issue 550 and PR 556
ms.date: 2026-10-29
---

<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: issue-550-pr-556-fix-cycle-3
* Task slug: chat-widget-550-fix-cycle-3
* Planning status: Ready after direct disposition of one independent critique
* Phase details: .copilot-tracking/details/2026-10-29/chat-widget-550-fix-cycle-3-phase-details.md

## Executive Summary

Keep bottom readers following a delayed reply by preserving their current scroll
intent immediately before the loading row changes layout. Reuse the same
bottom-distance and history-focus guard as message insertion. Apply the same
guard to controlled status/error layout changes through a shared widget helper.
Expand existing
regressions rather than add another browser harness.

### What You May Not Know

The prior positive browser test repositioned the log after loading appeared,
which hid this exact failure. Current geometry at the timer boundary avoids
stale send-time flags that would override upward scrolling during the delay.
This is local-only work; no full publication gate, Azure command or push.

## User Decisions and Requirements

* Run research, plan, implement and review with dated artifacts for #550 / #556 fix cycle 3.
* Run git pull --rebase first, completed already up to date.
* Preserve bottom following across the delayed loading/status row layout change
  without overriding genuine upward scrolling or history focus.
* Regression starts at bottom before sending and never repositions after loading.
* Run chat unittest discovery using /tmp/mv and the supplied PYTHONPATH, Ruff
  check/format check and node --check; commit locally with requested co-author.
* Source in src/ only; no push, az or manual latest.json changes.

## Goals

* The newest long reply remains visible for an eligible bottom reader after
  the 200 ms loading transition.
* Reader-controlled history position and focus remain unchanged.

## Scope and Non-Goals

Canonical source: shared chat-widget.js and its two adapters' widget status
assignments (not unrelated callback/regulatory status). Existing test owners:
src/api/tests/test_chat_widget_focus.py and
src/api/checks/chat_widget_browser_check.py. Update src/api/README.md.
No generated targets, generated JSON, API changes, model changes, visual
redesign, external resources or whole-issue closure.

## Functional Requirements

* Sample current bottom/focus eligibility before loading appears and disappears;
  pin immediately after mutation only if eligible.
* Preserve eligibility through empty/nonempty or wrapping status and inline
  error changes. Both adapters use the shared status setter.
* Share the eligibility predicate with message insertion, retaining <=1 CSS px
  tolerance and no focus movement.
* Keep 200 ms threshold, cancellation, disposal and existing control semantics.

## Non-Functional Requirements

* No sticky follow flags, observers, new listeners or smooth scrolling.
* Keep native semantics, live status, Fluent styling and reduced motion.
* No test removals. Maximum additions: two unit methods, two browser modes;
  adjust existing reply_scroll positive mode. No new test files.

## Acceptance Criteria

* Delayed two-site overflowing-thread positive case starts at bottom before send,
  does not alter log position afterward and ends <=2 CSS px from bottom.
* Older/history-focused cases retain position within 1 CSS px and exact focus.
* Negative control rejects original widget; requested checks pass.
* Dated critique and one independent post-implementation Review are preserved;
  source and original RPI evidence are committed locally with the trailer.

## Sources

Research: .copilot-tracking/research/2026-10-29/chat-widget-550-fix-cycle-3-research.md,
C1-C6 and W1. Base HEAD: 34f7f8fc.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve loading-transition scroll intent

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fix shared widget and strengthen owned regressions

Extract current eligibility helper, guard loading visibility mutations,
expose a preserving status setter and wire both adapters; preserve error layout
changes with the same helper.
add deterministic delayed lifecycle unit coverage, change browser follow mode
to position before sending and add pre-loading interaction checks. Update guide.
Dependencies: finalized critique.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate the correction

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted positive and negative checks

Run requested commands and existing two-site synthetic browser check. Keep logs
outside git under the current session files/fix-cycle-3 directory. Use a temporary
copy for original-widget negative control, never alter tracked source to test it.
Dependencies: P01-T01.

<!-- rpi:phase id=P03 -->
### [x] P03: Review and persist locally

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run one independent Review and commit locally

Reconcile all artifacts; independent reviewer reads bounded diff and evidence,
writes only its review. Resolve GitHub identity to privacy-safe local email,
then commit implementation and original evidence; no push.
Dependencies: P02-T01. Any review findings route to follow-up, not a second Review.

## Dependencies

Existing /tmp/mv Python/Ruff/Playwright and Node available. Browser needs pinned
axe-core 4.10.3 and installed Chromium; check actual execution before installing.

## Critique Disposition

Exactly one critique executed, original verdict Revise (one High).
PC-001 resolved directly by planner: resident empty-status insertion occurs
before the loading snapshot, so loading-only preservation is insufficient.
Explicitly include shared preserving status updates and scoped adapter wiring,
plus empty-status positive pre-send assertions and deterministic status geometry.
No divergent user decision or second critique. Resolving evidence: these
Functional Requirements and P01-T01, reconciled details and implementation tests.

## Follow-Up Items

* Publication requires the separate complete local gate, exact-head assessment,
  hosted checks and owner authorization. No publication is attempted here.

## Handoff

Changes record: .copilot-tracking/changes/2026-10-29/chat-widget-550-fix-cycle-3-changes.md.
Review: .copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-fix-cycle-3-review.md.
All P01-P03 complete. One independent Review: Complete / Conformant, zero
findings. Local persistence is fulfilled by the containing co-authored commit;
commit identity and clean-tree confirmation are external command evidence to
avoid self-referential commit IDs. No publication or child task begins here.
