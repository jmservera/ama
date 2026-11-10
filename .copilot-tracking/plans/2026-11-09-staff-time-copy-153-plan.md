---
title: Issue 153 staff-time refusal and error guidance plan
ms.date: 2026-11-09
task_id: 153-staff-time-copy-1109
task_slug: staff-time-copy-153
---

## Task metadata

* Research `.copilot-tracking/research/2026-11-09-staff-time-copy-153-research.md` (executed, Ready). Details `.copilot-tracking/details/2026-11-09-staff-time-copy-153-details.md`. Critique `.copilot-tracking/plans/2026-11-09-staff-time-copy-153-critique.md`.
* Branch `fix/demo-staff-time-copy-153-1109`, base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`, declared PR target `feat/demo-content-workflows-149-1109`. Refs #153 only. Plan authored 2026-11-09T22:50Z before any source edit.

## Requirements

* R1 Every supported blocked state (disabled, each missing prerequisite, awaiting request, awaiting a different-role manager) states reason, owner (existing role or support route, no named person) and next action. Derived from status flags, not echoed server text.
* R2 Validation refusals (minutes not a whole number, minutes out of range, no activity, unknown case) name the correctable input and say nothing was saved.
* R3 Unknown save outcomes (no HTTP status, 5xx, 409 pending, `outcome` uncertain or committed) say it is not known whether it was saved and tell the person to check My entries (or the checklist for enabling steps) BEFORE repeating; no claim of success, failure, replay or safe duplication.
* R4 Load failure is distinct from a blocked state and an unsaved write; 403 on a read maps to the same refusal wording.
* R5 Unrecognised server detail is never displayed; all text via `textContent`/text nodes.
* R6 Preserve default-disabled behaviour, privacy, financial and approval controls, button availability, `role` live regions, keyboard behaviour, non-colour cues, no animation, Fluent 2 and WCAG baseline, plain-language standard (reason, owner, next action; no gate, hold, provenance, trace).

## Scope

* Edit only `src/api/src/zava_forward/api/web/timecapture.js`; add `src/api/tests/test_timecapture_copy.py`; dated tracking records. No edit to `timecapture.py`, `server.py`, `app.js`, `role-screens.js`, shared error helpers, store, schema, AI, resident, importer or endpoint inventory. No knowledge-base edit (ownership boundary); the handoff names that deferral.

## Phases and criteria

* P1 Pure helpers `timeBlockedText(st, manager)`, `timeActionFailureText(error, kind)`, `timeLoadFailureText(error)` in `timecapture.js`, uniquely prefixed to avoid shared global collisions.
* P2 Wire helpers into `timeView` (status paragraph, `save` catch, view catch); 401 stays silent as before.
* P3 Regression `test_timecapture_copy.py`: Node VM unit cases for every supported state plus no echo of unsafe detail and the three-part pattern; opt-in (`ZF_BROWSER_TESTS=1`) served-app Chromium cases for disabled, missing prerequisite, invalid minutes, read failure, ambiguous save, 403 refusal.
* P4 Validation (targeted tier, documented basis): reproduction repeated after the change; new test file; existing `test_timecapture`, `test_content_standard`, `test_workspace_scripts`; Ruff check and format on the new test file; node syntax check of the JS; a fresh web-design-guidelines review of the changed files; one nonqueued admission for the browser run with actual-holder inspection; diff checks.
* Classification: web copy plus test only, no workflow, dependency, permission, SQL, deployment, infrastructure or security-control change. Focused tier; the complete local gate is not claimed and no blanket FULL run.
* Order: commit research, plan, details, critique and state; implement; review; record changes and review; commit. Local only, no push.
