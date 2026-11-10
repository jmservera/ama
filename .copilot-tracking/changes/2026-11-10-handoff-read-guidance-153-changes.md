---
title: Issue 153 pending-handoff read-failure guidance changes
ms.date: 2026-11-10
task_id: 153-handoff-read-guidance-1110
---

## Changes (implemented 2026-11-10 after plan and critique; the stub preceded implement-start)

* `src/api/src/zava_forward/api/web/app.js`: added `HANDOFF_READ_ERROR` (line 751) and changed the `pendingHandoffs` catch (lines 763-767). An `AbortError` returns without painting; an error with an HTTP `status` keeps `Could not load handoffs: ${e.message}`; any other failure (transport rejection) renders the constant with reason, owner (application support) and next action. Same `p[role=alert]`, card visible, no style, layout, request, retry or mutation change. The frozen #130 nomination hunk (~line 1062) is untouched.
* `src/api/tests/test_handoff_read_guidance.py` (new): five Node VM cases on the real function source (rejection, one read-only call per scenario, abort, HTTP and 401 text kept, rows and empty, source shape) and four opt-in served-browser cases (actual success and empty projection, constructed rejection with canary, 401 sign-in path, navigation during a pending read).
* Untouched: `role_screens_browser_check.py` and its fixture, paging and atlas checkers, `ops.js`, `panels.js`, Core, schema, auth, infra, provider code, knowledge-base audit tables (the content-standard inventory row is deferred to an owner-admitted documentation change).

## Amendments and divergences

* No divergence from the plan. Critique C1-C7 applied; C2 (a 200 non-JSON body reads as an empty queue) is recorded as out of scope and routed as a follow-up, not changed.
* First red run failed on a test-marker defect (constant did not exist on base), fixed by slicing from the function (log `first-red-marker-failure.log`). First browser run failed on a test defect (`page.on` with a builtin method); fixed in the test, no source change (`first-browser-run-test-defect.log`). A first Ruff/mypy pass found line length and two unused `type: ignore` comments; fixed in the test. Correction cycles: none claimed; no allowance assumed.

## Validation (focused tier; raw logs in `/tmp/zf-153-handoff-1110/logs/`, copied to the coordinator evidence folder)

| Check | Result |
| --- | --- |
| Reproduction before (served, Chromium, nonqueued `flock -n /tmp/ama-rpi-heavy.lock`, lock free) | `repro-before.log`: success and empty baseline; rejected GET showed `Could not load handoffs: Failed to fetch CANARY...` with no owner or action |
| New tests on base `app.js` (red) | 9 run, 2 failures, 1 error (Node cases); browser-enabled: 3 failures, 1 error, including the constructed rejection |
| New tests final | 9 run, OK, browser included (`new-tests-final.log`); without `ZF_BROWSER_TESTS` 9 run, 4 skipped |
| Reproduction after | `repro-after.log`: guidance shown, canary absent, card visible, one GET, success and empty unchanged |
| Related existing tests: handoff API, content standard, UI support, case journey, static assets, workspace scripts, accessibility baseline | 99 run, OK, 4 skipped (the opt-in cases) |
| Static | `node --check`, Ruff check and format, mypy strict on the new test, `git diff --check`: pass |
| Module origins | server and store resolved in this worktree (`origins.log`), not another checkout |

Not run: full or `--changed` gate, SQL, cloud, axe, assistive technology, human or resident-wording review. Manifest recipe SHA: N/A, no registered recipe changed (no workflow, gate tool or dependency edit).

## Web guidelines review (rules fetched 2026-11-10), changed hunk `app.js:751,763-767`

* `app.js:766` - "Error messages include fix/next step": pass, owner and next action present.
* `app.js:766` - async status: existing `role="alert"` retained; semantic `p`, no ARIA added; pass.
* `app.js:751` - typography rules (curly quotes, ellipsis, Title Case): not applied; repository ASCII and plain-language rules override. Existing loading text `Loading handoffs...` unchanged.
* `app.js:764` - cancellation: abort paints nothing; pass.
* No focus, form, animation, layout, performance, locale or image rule is touched.
