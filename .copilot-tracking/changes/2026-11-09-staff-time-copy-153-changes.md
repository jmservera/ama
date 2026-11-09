---
title: Issue 153 staff-time refusal and error guidance changes
ms.date: 2026-11-09
task_id: 153-staff-time-copy-1109
---

## Changes (implemented 2026-11-09T22:51Z to 22:56Z, after plan and critique)

* `src/api/src/zava_forward/api/web/timecapture.js`: added `timeGuidance`, `timeManagers`, `timeBlockedText`, `timeActionKind`, `timeRefusal`, `timeActionFailureText`, `timeLoadFailureText` (function declarations only, so a script reload cannot redeclare constants). `timeView` now shows blocked guidance derived from status flags instead of `st.reason`, action failures through `timeActionFailureText` (401 stays silent), and load failures through `timeLoadFailureText`. No server text is rendered; rendering is unchanged text nodes.
* `src/api/tests/test_timecapture_copy.py` (new): seven Node VM cases on the real JS and five opt-in served-browser cases (`ZF_BROWSER_TESTS=1`).
* Untouched: `timecapture.py`, `server.py`, `app.js`, `role-screens.js`, store, schema, endpoint inventory, knowledge base.

## Amendments and divergences

* Critique C1-C7 applied before implementation (see critique record). No divergence from the plan except: knowledge-base documentation was not edited (ownership boundary), recorded here and in the handoff.
* Process note: an early local commit accidentally included the unfinished JS edit; before any publication it was undone with `git reset --mixed` to the research/plan/critique commit (local, unpublished) and recommitted as separate commits.
* A first browser run failed on a test defect (strict locator matched two checklist lines in the disabled case); fixed in the test, no source change. A mypy strict run failed on three annotation points; fixed. Correction cycles used: 0 of 5 (no reviewer-driven correction).

## Validation (focused tier, raw logs in `/tmp/zf-153-1109/logs/`)

| Check | Result |
| --- | --- |
| Reproduction before change (served app, Chromium, one nonqueued `flock -n /tmp/ama-rpi-heavy.lock`, lock free) | `repro-before.log`, exit 0: missing owner/action, `Failed to fetch`, raw detail echoed |
| New tests against base JS (red) | `new-tests-red-base-js.log`: 5 run, 7 failures, 1 error |
| New tests, final (browser enabled) | `new-tests-final.log`: 12 run, OK, 0 skipped; without `ZF_BROWSER_TESTS` 12 run, 5 skipped |
| Reproduction after change | `repro-after.log`, exit 0: every state shows reason, owner, next action; unsafe detail not rendered |
| Existing `test_timecapture` 26, `test_content_standard` 18, `test_workspace_scripts` 5, `test_role_screens` 8, `test_static_assets` 5 | all OK (`after-unit.log`) |
| Ruff check (whole api project), Ruff format and mypy strict on the new test | pass |
| `node --check`, `git diff --check` | pass |

Not run: blanket full gate, SQL, cloud, axe, assistive technology, human or DPO review.
