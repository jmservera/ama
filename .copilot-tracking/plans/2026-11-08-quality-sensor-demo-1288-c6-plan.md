---
title: Quality sensor demo 1288 C6 plan
ms.date: 2026-11-08
---

Written 2026-11-08T22:26Z (corrected from a later stated minute) after the C6 research and before any product or test edit. Refs #1288, #107. No closing claim.

## Phases

* [ ] P1 Red tests (SQLite) in `src/api/tests/test_quality_sensors.py` and `src/api/tests/test_assistants_dispatch.py` if suitable; logs `/tmp/c6-red-*.txt`.
* [ ] P2 C6-1 dispatch hold table, atomic check-and-hold, hold release, `configure` ordering.
* [ ] P3 C6-2/3/5 immutable identity (supersede plus enqueue, replaced counter), lazy backfill with `ix_assistant_case`, manual requests do not occupy the slot.
* [ ] P4 C6-6 backend-specific test helpers.
* [ ] P5 C6-4/7/8 web: refresh guidelines, list endpoint review_flag, case review path and waiting, as-of block, panel wording.
* [ ] P6 Green runs, ruff, changes, one review, commit.

## Red/green scenarios

* S1 barrier after the former final check (hold written) and before provider transport: a second connection calls `configure` with a withdrawal; it must not commit while the provider runs (assert control still granted in the DB at provider time); after the provider returns it commits (red: withdrawal commits first and the provider already holds the request). Also: withdrawal committed before the hold means no provider call; provider exception and timeout release the hold; an expired hold does not block; hold write failure means no send.
* S2 A enqueue, B arrives before claim, claim: A is stale (`superseded`), exactly one new task for B; manual invoke of B during the lease reuses that task and creates no third; exact A return reuses A's row; dispatches and allowance calls are bounded; restart keeps one.
* S3 pre-upgrade database (tasks inserted without schedule rows): assessment and funding changes after a legacy result are eligible; same-bucket Quality arrival does not re-dispatch; release or epoch change is not adopted; second pass idempotent; restart.
* S4 browser-free UI test: a static test that `assistants.js` and `case-workspace.js` keep a stale `review-suggested` flag in the main path and count it as waiting, and the API list carries `review_flag` for arrivals during and after inference. Rendered browser check is PENDING (no browser authorised).
* S5 manual before scan, manual before claim, manual failure, then same-bucket arrivals: an autonomous flag is produced once, manual output is never labelled autonomous, calls stay within the allowance.
* S6 tests helpers are backend-specific; SQLite runs pass; SQL Server variants remain skipped and explicit.
* S7 delayed claim: queued fresh, claimed stale: API flag and rendered text show captured as-of, stale, age; absent readings show unknown.
* S8 panel text no longer says same readings; flag exposes `changed_since_capture`; matching and changed cases tested.

## Critique (one, final candidate)

* Executed once 2026-11-08T22:26Z (corrected from a later stated minute). Verdict: proceed with amendments.
* Amendment 1: the hold must be released in a second transaction even on provider error; expiry is the crash backstop.
* Amendment 2: `configure` must read the hold using the database clock, not the process clock.
* Amendment 3: a replaced-counter exhaustion must be tested with a stable recovery and restart.
* Rejected: holding an open transaction across the call (global writer block on SQLite).
* Significant divergence needing an owner decision: none; the withdrawal delay is bounded and explicit, inside current authority.

## Validation tier

FULL (SQL consent/control schema, security-sensitive projection). Light SQLite and ruff now; actual SQL Server, query plans, browser/axe/keyboard/reflow, #184 and #1292 integration, FULL receipt, release and live walkthrough are pending separate admission.
