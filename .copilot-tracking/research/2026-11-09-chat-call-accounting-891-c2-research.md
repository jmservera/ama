---
title: Issue 891 chat call accounting C2 research (test isolation)
ms.date: 2026-11-09
---

## Scope

* Task `issue-891-chat-call-accounting-1109-c2`, parent C1 `issue-891-chat-call-accounting-1109-c1`. Cycle 2 of 5 (3 remain). Clean head `613a1919665631a9559c5a3dc87c1c9e84496148`, base main `1b7a1719`. C1 and original records are preserved unchanged.
* Input: independent 341ffe3a review (coordinator `independent-891-c1-transport-1109/functional-findings.json`): production marker approved for the synchronous core `Ai.evidence` composition; one Medium test-isolation defect.

## Findings (read from source, 2026-11-09)

* `src/core/tests/test_ai_dispatch_marker.py:86-88`: the "guard denial" case calls `mock.patch(...).start()` and never stops it. The case loop also calls `self.setUp()` repeatedly; each registers only its own allowing-patch cleanups. After the test the process-global `data_protection.dispatch_hold` stays a Mock returning "denied", so later modules in the same interpreter take guard-denial paths.
* Wording defect: C1 README (`src/agents/README.md` line 31), C1 plan, critique and changes call the unwitnessed assumed 1 an "upper bound". An arbitrary provider may make more than one call, so it is neither an upper bound nor exact nor a billing estimate. It is an unverified legacy assumption (the pre-C1 `calls=1` default). The chat.py log text already says "assuming one call" and is accurate.
* Small related coverage gaps (review R2/R3): fence withdrawal raised from the opener's `.open`, `TimeoutError` and `HTTPError` after hand-off are untested. Attempt definition: one count per request handed to the transport, not wire or billing exactness.

## Planning Readiness

Ready. Disposition `executed`.

## Correction after critique

The suite alone restores the original guard. The leaked started patch stays registered; `mock.patch.stopall()` (used by other modules' `tearDown`, e.g. agents `test_chat_model`) stops it after the allowing patch and restores a stale mock returning "denied". That is the order-dependence mechanism.
