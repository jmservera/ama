---
title: Issue 96 impact correction C3 research (role-screen contract tests)
description: Research for one behavior-preserving test-contract correction of two existing role-screen tests that the 96 saved-copy checker UI legitimately breaks
ms.date: 2026-11-13
---

## Identities and scope

* Worktree `issue-96-impact-c3-0052`, branch `fix/demo-96-impact-c3-0052`, head `9085e85c626745a7133caf59373fe558e94f0a70`, src tree `1f4ac07f3985a99e7c71af8d24fd84c20dea7028`, clean at start. Task id and slug `issue-96-impact-c3-0052`. Refs #96 only.
* Parent integration scope 149 stays prospective, partial and Refs-only. The actual failed 9085 head and the original d790 candidate and Review are immutable and not relabelled. Entire 233 is excluded (no 233 source, tests, helper, navigation or grant touched).
* Research disposition: executed. Planning Readiness: Ready.

## Budget authority (finite history)

* Actual original 96 UI state `.copilot-tracking/rpi-sessions/2026-11-12/issue-96-ui-implementation-2333-state.json` records "correction 1 and M1 correction 2 spent, no new pool". Backend state `issue-96-saved-export-check-2236-state.json` independently records 2 spent corrections. Standing default five total leaves three; the root admits exactly one (C3) now, ending 3 of 5 spent with 2 remaining. Older whole-96 unknown and finite extension history is preserved, not zeroed. No contradictory spending or grant evidence was found, so no write is blocked.

## Confirmed failures (reproduced on exact base 9085e85)

* Root evidence `rpi-149-roles-0045-result.json` and `unit.log` recorded 2 of 19 failing. Re-run in a fresh owned archive (`rpi-96-impact-c3-0052`, same head, pip-installed core, agents and api, pinned Playwright 1.64.0, ruff 0.17.1, mypy 2.4.0): 19 ran, 2 FAIL, log `unit-failing-first.log`.
* `tests/test_role_screens.py::RoleScreens::test_host_reads_existing_scoped_endpoints_without_post` line 283: `assertNotIn('"POST"', role-screens.js)`.
* `tests/test_role_screens_conformance.py::RoleScreenConformance::test_screen_styles_add_no_motion`: asserts the only `setTimeout` is the `URL.revokeObjectURL` release.
* Both tests are unchanged from main; the causes are source additions from the 96 UI (`fundingSavedCopyCheck`, role-screens.js lines 1372 to 1425).

## Actual role host boundaries (evidence)

* Requests: every call in role-screens.js goes through the shared `api(path, undefined, signal)` GET helper (20 call sites, all with `undefined` options) except exactly one `fetch(path, { method: "POST", ... })` at line 1411 inside `fundingSavedCopyCheck`. No PUT, PATCH or DELETE literal exists.
* That POST targets only `/api/cases/{case}/form-review/{draft}/held-export/freshness`. The served route is read-only (README saved freshness section: nothing is recorded, approved or submitted; core `export_freshness` does not mutate the store). It sends the raw saved JSON text (decision G4, preserves `12.0` and integers above 2^53), `X-ZF-CSRF: 1`, session `me`, route `signal`, and a pending-duplicate guard.
* Timers: line 946 `setTimeout(() => URL.revokeObjectURL(started), 1000);` and line 1423 `setTimeout(() => { if (button.isConnected && !button.disabled && document.activeElement === document.body) button.focus(); }, 0);`. The second runs only when the person had focus on the button (`hadFocus`), after the shared wrapper re-enables it, and only if focus fell to `body`. It has no style, class, animation or transition effect: accessible focus restoration, not motion. The test already separately forbids `setInterval`, `requestAnimationFrame`, `.animate(` and any `animation` or `transition` in `.screen-*` CSS rules.

## Findings

* Source is correct and unchanged by design; the old assertions encode a stale blanket ("no POST at all", "exactly one timer"). Deleting them or exempting the control would lose the guard; the precise contract is "exactly one mutating-looking request and it is the read-only freshness check; exactly two known timers and neither drives motion".
* No web source, CSS or HTML edit is needed. Web guidance (web-design-guidelines fetch, Fluent 2, WCAG baseline, content standard) governs web source edits; none are made, so the pre-edit skill load and file:line review of changed web files do not apply. This is disclosed, not claimed as a review.

## Out of scope and preserved

* Early PARTIAL source Review Low items (403 copy, file input, gate wording) are not fixed. No finance, resident, human or legal approval, Current authenticity, submission, eligibility or whole-96 criterion claim is made.
