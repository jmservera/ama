---
title: Issue 96 impact correction C3 changes
description: Changes, validation and divergences for the tests-only role-screen contract correction
ms.date: 2026-11-13
---

## Changes

* `src/api/tests/test_role_screens.py`: `test_host_reads_existing_scoped_endpoints_without_post` replaced by `test_host_posts_only_the_read_only_saved_copy_check` using `request_findings` (exact `path` assignment, exact raw-text `fetch(path, { method: "POST", ... "X-ZF-CSRF": "1" ... body: text, signal })` inside `fundingSavedCopyCheck`, a single `fetch` and `method` token, no other transport, every `api(` call passes `undefined` options). New `test_request_guard_rejects_broadened_requests` proves eight broadened forms fail.
* `src/api/tests/test_role_screens_conformance.py`: the single-timer equality replaced by `timer_findings` (balanced-parenthesis extraction; exactly the revoke timer and the exact guarded focus restoration under `if (hadFocus) `; alias rejection). Existing bans on `setInterval`, `requestAnimationFrame`, `.animate(` and `animation` or `transition` in `.screen-*` CSS stay. New `test_timer_guard_rejects_motion_and_unguarded_focus_timers` proves seven forms fail.
* No product source, CSS, HTML, README, helper or 233 file changed. Product behavior (raw JSON and numeric fidelity, session, CSRF, view-only, roles, default OFF, duplicate, abort, 503 and error handling) is unchanged.

## Divergences from plan

* None in scope. The critique (CR-1 to CR-3) was applied before implementation. One self-caught test slip (prefix window 13 rather than 14 characters) was fixed within the same C3 batch before any commit; ruff format was applied to the two files.

## Validation (actual)

* Failing first on exact base: 19 ran, 2 FAIL (`unit-failing-first.log`).
* After patch: RoleScreens + RoleScreenConformance 21 ran, OK (19 existing plus 2 regression tests), run once as the impacted classes. FinanceGrantsScreens 20 OK.
* Ruff 0.17.1 `check` and `format` clean and mypy 2.4.0 configured strict on the two changed test files clean (not the whole configured tree).
* Under the non-blocking heavy lock with pinned axe 4.10.3 (sha 880970c0...8bb): held_copy browser 88 PASS, shared role browser 47 PASS, 0 FAIL or SKIP. Browser checks ran from the same-head archive because no product source changed.
* Not run: the complete local gate and the rest of the full tier, by instruction. Hosted CI for the final head is unobserved. Web guideline file:line review is not applicable (no web file changed).
