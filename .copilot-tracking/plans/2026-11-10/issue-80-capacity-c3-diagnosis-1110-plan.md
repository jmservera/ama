---
title: Issue 80 capacity line-754 diagnosis, plan
description: Plan for the proposed checker-only correction of the delayed sibling 401 stage; not admitted for implementation in C3
ms.date: 2026-11-10
---

Task `issue-80-capacity-c3-diagnosis-1110`. Status: planned only. C3 admits diagnosis, plan, details and critique; no implement or review. Any execution needs a separate Root admission (no automatic C4).

## Objective

Make the stage `delayed sibling {endpoint} 401 ...` in `capacity_browser_check.py` answer the application's designed startup retries of its non-JSON 503 so the checker's own assertion "We could not load {label}" can pass, without weakening the delayed-401 race.

## Phases

1. [ ] Re-confirm, in a Root-admitted chain, base `6d4cd624`, HEAD and that `app.js` retry code is unchanged (`git diff`).
2. [ ] In the stage only: add a local flag consulted by `hold_capacity_read`. While set, a request for the failing endpoint is answered `fulfill(status=503, body="Unavailable")` (same as the first answer); the sibling's request is still held. Set the flag immediately before the first `failed.fulfill(...)`; clear it after the failure assertion succeeds so the later retry click re-holds both reads as today.
3. [ ] Keep unchanged: the paged patterns, `held`, the two-held wait, every later assertion (retry disabled and busy, sibling `401` after the retry click, Sign in, alert, focus, zero capacity heading, zero Try again, POST count, configuration count), `expected_failures` handling and failure lists.
4. [ ] Focused validation on the exact head: Ruff check and format of the checker; unchanged `ops.js` Node syntax; list-export API tests (11) and related static tests (60); ONE whole `capacity_browser_check --axe` under the nonblocking heavy lock. It must reach, in order, both downloads, corrected time status, aftercare 403 assertion, all stages including both delayed-401 iterations, and the empty-capacity zero-anchor assertion. Any failure, busy lock or missing prerequisite is reported as it is; no retry or auto-repair.
5. [ ] Native review once, then independent exact-head assessment by Root after a genuine pass.

## Explicitly out of plan

Removing or skipping the race assertion, ignoring 401, widening accepted errors, dropping the packages failure assertion, pre-releasing the held 401, JSON 503 body, application retry or role/auth/session change, any source edit in C3, a pinned-main baseline run (not needed: the code under observation is identical to main).

## Open items

* The workorders iteration is symmetric by source reading, not observed.
* Later parts of the stage in the checker's own ordering and everything after it are unobserved; the next full run may expose further failures.
* C2, C4, #73 and owner thresholds stay open.
