---
title: Issue 1248 saved-call History browser readiness phase details
description: Step-level details for the prospective reproduction, cause gate, repair and validation of the saved-call History assertion
ms.date: 2026-11-07
ms.topic: reference
---

## Phase 1: Controlled delayed-refresh reproduction

* File: `src/api/checks/case_journey_browser_check.py`, around lines 739-753.
* Before clicking Save, register `page.route("**/api/cases/ZF-1", handler)` that appends each `Route` to a list. The POST `/api/cases/ZF-1/call` path does not match this glob.
* Click Save, then `page.wait_for_function` for empty `#outcome` (existing wait). Use `expect(...)` or `page.expect_request` to confirm exactly one held read was dispatched after Save, not a fixed sleep.
* Observe, before release, with `text_content()` of `#case-panel-history` (hidden panels are still readable): the saved outcome is absent. This is the old-condition observation; record it with a `check(...)` such as "delayed refresh hides the saved call from the old one-shot read".
* Release with `route.fulfill(response=route.fetch())` inside `page.expect_response("**/api/cases/ZF-1")`, then `page.unroute` in a `finally` path.
* Outcomes: History gains the call after release means H1 holds; no call after release means H2 (application) and the plan stops at Phase 2.
* Unchanged base run: record whether the original check reproduces R4. A pass is bounded "not reproduced", not a fix.

## Phase 2: Cause gate

* Record in the changes artifact the observed signal ordering, workspace identity before and after, and request correlation. State which of H1 to H4 holds and why.
* If H2: list application evidence (`app.js:886-888` conditions) and stop; this issue stays test-only.

## Phase 3: Repair

* Before Save: `workspace = page.locator("[data-case-workspace]").element_handle()` (existing idiom).
* After the existing `#outcome` empty wait and the unrelated-draft `check`: `page.wait_for_function("old => !old.isConnected", arg=workspace)`.
* Replace the one-shot check with `tab(page, "History")` followed by `expect(page.locator("#case-panel-history")).to_contain_text("Unsaved synthetic call")` and keep a `check("saved call reaches actual history", ...)` name so receipts stay comparable.
* Do not add `wait_for_timeout`, loops, retries, longer global timeouts or substring weakening. Preserve the "successful call clears itself, not unrelated draft" check and everything after.
* Under the held read, the old condition must fail and the repaired wait must pass; keep that pair in the focused regression, not as a skip or conditional.

## Phase 4: Validation (at admission only, under the heavy lock)

* `python3 -m checks.case_journey_browser_check` as built by the `browser` group of `tools/rpi-checks.py` (lines ~1077 and ~1105), from `src/api`, scratch outside the checkout.
* `python3 tools/rpi-checks.py --changed` for the focused tier; relevant unit tests such as `src/api/tests/test_case_journey.py` and `test_browser_harness_scratch.py` and static checks (ruff or the repository's configured linters) as the gate selects.
* Record actual exit codes and module/source identities. A focused pass is not a FULL gate pass.

## Phase 5: Evidence and review

* Create dated changes and review artifacts under `.copilot-tracking/changes/2026-11-07/` and `.copilot-tracking/reviews/2026-11-07/` only after implementation.
* Update the creation record and issue comment only through separately authorised steps; leave acceptance criteria unticked until proven by reviewed evidence.

## Risks

* Hidden-panel text reading and tab persistence across the workspace swap are unverified; Phase 1 resolves them.
* A held route can stall later steps if not unrouted; require unroute on every path.
* Another in-flight case read could be consumed by the hold; count reads after Save only.
