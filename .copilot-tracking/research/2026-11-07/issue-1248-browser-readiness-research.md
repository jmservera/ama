---
title: Issue 1248 saved-call History browser readiness research
description: Prospective research on the R4 saved-call History assertion failure, with hypotheses, evidence and planning readiness
ms.date: 2026-11-07
ms.topic: reference
---

## Scope and Status

* Task slug: `issue-1248-browser-readiness`. Issue #1248, base main 0f420dc9514db22081cb48fa733267d9d33a0d24.
* Prospective, read-only research. No browser, test, SQL, scanner or source action was run in this turn.
* Research disposition: `executed` (source and log reading only).
* Planning Readiness: `Ready` for a controlled-reproduction-first plan. Root cause is NOT proven; the plan treats it as a hypothesis to be confirmed by a synthetic delayed-refresh observation before any repair.

## Evidence Read

| Source | Finding |
| --- | --- |
| `/mnt/ama-gates/g86-r4-1107/0102-browser.log` (immutable) | The check passed "unrelated refresh preserves call and complete dynamic draft" and "successful call clears itself, not unrelated draft", then failed at line 750 with `AssertionError: saved call reaches actual history`. No application error or page error preceded it in the log. |
| `/mnt/ama-gates/g86-r4-1107/receipt.json` | SHA-256 7c96fb63ead9ab52c197fb5a468709fe761e2b778598ff8680dc97d07fb46091, matching the issue. |
| `/tmp/rpi-86-browser-diagnosis-1107.log` | Prior read-only diagnosis: checker, app call path and `log_call` unchanged since the passing R3; one unchanged rerun later passed 407 checks. It left ownership "unresolved". |

## Code Path (main 0f420dc)

* Check, `src/api/checks/case_journey_browser_check.py:739-753`: click Save, `page.wait_for_function` until `#outcome` is empty, assert the draft message survived, `tab(page, "History")`, then one `inner_text()` of `#case-panel-history` tested for "Unsaved synthetic call".
* App, `src/api/src/zava_forward/api/web/app.js:902-922` (`refresh`): `await fn()` (POST `/call`), then `reconcileCaseSubmission(sent)` clears the submitted `#outcome` and `#note` fields, and only then `await caseView(id)`, which issues `GET /api/cases/{id}` (`app.js:885`) and rebuilds the workspace (`app.js:1058-1103`).
* History panel, `app.js:1016-1020`: renders `c.contacts.slice(0, 15)`. The API returns `list(reversed(contacts))[:40]` (`src/core/src/zava_forward/core/store.py:440`), so a new call is first and cannot be capped out.
* `log_call` (`store.py:565-577`, in `src/core`, not `src/api`) appends the contact under `self.lock` before the POST returns, so the data is committed before the refresh begins.

## Hypotheses

| ID | Hypothesis | Status | Discriminating observation |
| --- | --- | --- | --- |
| H1 | Checker readiness race: `#outcome` empties in `reconcileCaseSubmission` before the `GET` completes and the workspace is replaced. The check selects History on the still-attached old workspace and reads it once, so the new contact is absent. | Plausible, unproven. The wait signal precedes the data by the in-flight `caseView` GET and re-render. | With the case read held by a Playwright route, `#outcome` is empty yet History lacks the call; releasing the read makes it appear in the replaced workspace. |
| H2 | The application drops the refresh (`caseSession !== session` or `historyGeneration` changed, `app.js:886-888`), so History never updates. | Not supported by the R4 log, not excluded. | After the held read is released, History still never shows the call. This is an application finding for separate scope. |
| H3 | Data not committed, ordering or cap. | Contradicted by code: committed before response, newest-first, within 15. | Needed only if H1 and H2 fail. |
| H4 | Environment or scratch changes from #81 (`design_system_browser_check.py`) alter timing. | No link found; could affect load timing only. | Not pursued unless H1 is refuted. |

## Existing Conventions to Reuse

* Workspace replacement wait: `workspace = page.locator("[data-case-workspace]").element_handle()` then `page.wait_for_function("old => !old.isConnected", arg=workspace)`, used by `refresh_proposals` (lines 46-49) and after Save in the checklist section (added by #1184 for the same class of race).
* Controlled held reads: `page.route("**/api/cases/ZF-1", handler)` storing the `Route`, later `route.fulfill(response=route.fetch())`, with `page.expect_request`/`expect_response` (lines 176-232), followed by `page.unroute`.
* Web-first assertions `expect(...).to_contain_text(...)` already used (for example line 203).
* `check(name, condition)` from `design_system_browser_check.py` records and raises on failure.

## Candidate Repair (only if H1 is confirmed)

* Test-only, in `case_journey_browser_check.py`: capture the workspace handle before Save, wait for it to detach (the refresh completion signal), then `tab(page, "History")` and `expect(page.locator("#case-panel-history")).to_contain_text("Unsaved synthetic call")` in place of the one-shot `inner_text()`. It waits on the exact saved outcome in the actual panel, adds no retry, sleep or blanket timeout, and keeps the same substring and panel.
* Focused regression: hold the case read and prove (a) the old condition (empty `#outcome` then one read) sees no saved call while the refresh is held and (b) the repaired wait returns the exact content after release.

## Risks and Unknowns

* Whether the tab selection survives the workspace swap is unverified; selecting History after detach makes the repair independent of it.
* A held `GET` must hold only reads started after Save and be unrouted on every path.
* The heavy lock is shared with FULL runs; #86 FULL r5 is reported as holding it. The browser proof is admitted separately and serialised.
* The R4 failure may not reproduce; "not reproduced" satisfies criterion 1 only with the controlled delayed-refresh proof recorded.

## Boundaries

* No weakening of strict history, unrelated-draft, persistence, keyboard or axe checks; no retry, fixed sleep, blanket timeout or skip.
* If H2 is confirmed, record application attribution and scope its repair separately.
* No SQL, Azure, model, private-data, approval, consent or policy action.

## Follow-ups

* Issues #86 and #81 acceptance should cite the R4 negative evidence and the final outcome of this issue.
