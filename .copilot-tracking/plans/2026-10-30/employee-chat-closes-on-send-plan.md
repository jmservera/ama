<!-- markdownlint-disable-file -->
# RPI Plan: employee-chat-closes-on-send

## Task Metadata

* Task ID: employee-chat-closes-on-send-2026-10-30
* Task slug: employee-chat-closes-on-send
* Planning status: Planning completed; original critique Revise retained; implementation assessed Not accepted with routed follow-up
* Plan date: 2026-10-30
* Phase details: .copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-30/employee-chat-closes-on-send-plan-critique.md

## Executive Summary

Keep submitted employee chat visible through same-context workspace refresh and equivalent successful session re-check. Prevent background rendering from moving chat-owned focus, and preserve the employee session object only when its complete authenticated user/account snapshot matches. Keep real identity/role changes, access loss, navigation and resident consent boundaries.

Current outcome: the headline 12-case visibility/answer regression passes, but the one independent Review is Complete / Not accepted. RV-001 retains a delayed-dismissal focus defect; RV-002 retains blocked mandatory full-unit evidence. Local commit is delivery of this candidly incomplete candidate, not publication acceptance.

### What You May Not Know

Isolated Enter and Send already work locally. The reproduced failures require a concurrent refresh. A session re-check additionally strands the pending answer, independently of visibility. Existing refresh tests explicitly encode the old dismissal expectation and must be corrected, not bypassed. No live-site/model or human accessibility acceptance is claimed.

## User Decisions and Requirements

* Owner-visible Enter/Send bug is highest priority; reproduce using actual local app and Chromium, case/no-case, route refresh/session re-check.
* Check resident host and retain Escape, focus-return and ARIA behavior.
* Add a regression that fails before correction; run full API units with caller PYTHONPATH, ruff, mypy and browser.
* Dated Research, Plan/Details, Changes and Review; local commit only, Refs-only, no issue closure, push, Azure or deployment.

## Goals

* Eliminate refresh-induced dismissal and lost pending replies without weakening stale-result guards.
* Record executable red/green evidence and independent review.

## Scope and Non-Goals

* In scope: employee app rendering/session identity, shared widget focus behavior only if needed, bounded browser/unit checks, API README and RPI artifacts.
* Non-goals: redesign, server auth contract change, resident session reset removal, remote operations, unrelated cleanup.

## Functional Requirements

* FR1: Enter and mouse Send retain open dialog, ARIA expanded state and visible answer through same-context render/re-check.
* FR2: Rendering must not steal focus owned by the shared dialog; intentional external focus and Escape still dismiss, with correct return behavior.
* FR3: Exactly equal user/account re-check retains pending consumer identity. Different user, role, capability or account clears chat; failed/expired auth preserves existing explicit error/login path.
* FR4: Resident Enter/Send retain answer visibility and shared keyboard semantics; consent/session loss still invalidates.

## Non-Functional Requirements

* No timeouts, suppress-next-focus hacks, event-trust heuristics or automatic reopening.
* Native nonmodal dialog, labels, live updates and no asynchronous focus theft.
* Local constructed data only; preserve evidence and no secret output.

## Acceptance Criteria

* AC1: 12 employee browser combinations (2 contexts x 2 send methods x 3 refresh modes) assert open during/after pending request, visible returned answer, completed busy state, retained draft/skill and exact activeElement. Capture mouse-send focus after busy moves it into the input. Include history/Sources focus, Escape/external dismissal before delayed render, no reopening, and ordinary app focus when chat does not own it.
* AC2: Actual start() during delayed setup/thread/ask stays usable with equivalent user/account, including changed non-identity counts/navigation. Account-only, user and capability changes reset/abort; finish old setup/thread/ask and assert no stale request/text/focus/busy change to replacement. Hold /api/me, invalidate session, release old success and prove no restoration. Existing 401/403/404 and route change protections remain.
* AC3: Resident both methods with actual rules response, Escape/launcher focus and external focus behavior pass.
* AC4: Full API units, ruff check/format, mypy, JS syntax and actual browser checks are recorded, including honest unrelated failures/skips.
* AC5: One independent plan critique, one independent post-implementation Review, dated evidence and local commit; no push/deploy.

## Sources

* .copilot-tracking/research/2026-10-30/employee-chat-closes-on-send-research.md: C1-C8, W1, Ready.
* src/api/README.md: real loopback harness, source tool commands and explicit engineering boundaries.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Correct refresh lifecycle with failing regression

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Capture failing-before browser assertions

Add focused coverage to existing checks outside runtime package; prove baseline failure before source edits.

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Preserve chat-owned focus and equivalent session identity

Fix show()/start(), with explicit invalidation on auth change; update old browser refresh expectations and related README.

Headline correction implemented and browser-proven. Reopened completion marker after original Review RV-001: accepted delayed-dismissal outside/launcher focus requirement remains unmet; routed to later work, not corrected/reviewed again in this loop.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and review

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Run targeted then package and browser validation

Run all requested local selectors, retain results in Changes; record blocked prerequisites rather than claiming success.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Independent Review and local commit

One post-implementation review; route findings to later work, preserve outcome. Resolve GitHub identity privacy-safe local email before commit. No remote writes. Complete local publication gate is not bypassed: no publication requested or authorized here.

Original Review Complete / Not accepted is preserved at the canonical logs path below. Local delivery commit contains this record; discover its immutable ID through git log rather than embedding a self-referential hash.

## Test Ownership and Locked Boundary

* Canonical owners: src/api/checks/chat_widget_browser_check.py and tests/test_chat_widget_focus.py.
* Maximum additions: one focused browser check module and two JS-harness unit methods if existing owners cannot cover required behavior simply. No new dependency/tooling.
* Exact removals: none. Replace only old same-context refresh-hidden expectations with focus/visibility-aware requirements.
* Generated targets: external logs/screenshots/JSON only; no generated runtime assets.
* Semantic coverage: identity/access/consent boundary; regression coverage: original reproducible focus and lost-answer failures.
* Validation evidence: external original baseline matrix plus fail-before/pass-after browser log, focused units and full requested commands.

## Dependencies

Existing /tmp/mv Python/browser tools and Chromium; loopback synthetic API launcher. Pinned axe file needed only for existing comprehensive browser check. No real model dependency.

## Critique Disposition

Exactly one critique executed: Revise (original retained).

| Finding | Owner/disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Planner, applied directly | AC2 and phase details now explicitly require actual start(), account-only/capability changes, mutable non-identity refresh and held-auth invalidation race |
| PC-002 | Planner changes applied; implementation partially unmet | AC1/details require exact focus; original Review RV-001 identifies contrary delayed-dismissal test expectation |

No unresolved significant decision; no second critique.

## Follow-Up Items

* Owner/coordinator verifies deployed employee-site behavior after separately authorized redeployment; live environment unavailable locally.
* Rank 1: RV-001, later rpi-implement corrects delayed-dismissal focus and its test; bounded high-value accessibility completion.
* Rank 2: RV-002, bounded validation-evidence collection runs full API units when shared heavy lock admits; no bypass/queue.

## Handoff

* Changes: .copilot-tracking/changes/2026-10-30/employee-chat-closes-on-send-changes.md.
* Review: .copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md.
* Ordered loop executed once; local-only candidate committed. Next is routed follow-up, not another critique or Review of this task. No push/deploy or publication acceptance.
