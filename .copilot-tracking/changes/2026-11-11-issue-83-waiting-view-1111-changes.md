---
title: Issue 83 waiting-time screen changes
ms.date: 2026-11-11
task_id: issue-83-waiting-view-1111
---

## Scope

Full plan (P01 to P03) implemented; P04 Review follows. Base `7880b95b19525ff465cab27870ba9d55b57110a3`, branch `feat/demo-handoff-waiting-view-83-1111`. Local only, no push.

## Changes

* P01 `src/api/src/zava_forward/api/web/app.js`: `WAITING_READ_ERROR`, `WAITING_DENIED`, `waitingRows` validator, `waitingTime`, `waitingHours`, `handoffWaitingView`; route `#/handoff-waiting` before the `#/assistants` dispatch (after contractor and no-case-service guards); route status label; "Handoff waiting times" link in the list header row of both list views.
* P02 `src/api/tests/test_handoff_waiting_view.py`: 6 Node cases and 4 Chromium cases (10 total; plan maximum about 12 Node scenarios and 6 browser methods).
* P03 `src/api/README.md`: short section with scope and limits.

## Divergences and discoveries

* Real-backend finding (kept as original evidence): the first validator rejected negative `age_hours`; the real route returned `-0.01` for just-offered handoffs because the server truncates timestamps to the minute, so the first browser run showed the failure alert for valid data and two Chromium cases failed. Corrected inside the initial increment before freeze: finite numbers are accepted and display clamps at 0 hours; a Node case (`ZF-4`, -0.01) covers it. This is an initial-candidate fix, not a post-review correction.
* Environment finding: editable installs of `zava-forward-*` point at the coordinator's primary checkout, so Chromium first served the primary checkout's app.js (link not found, 4 errors). Tests were rerun with `PYTHONPATH` set to this worktree's `src` directories (no install, primary checkout untouched).
* "Personal list empty but queue present" cannot occur with real data (same scope, research C5); covered by a labelled constructed response and by a constructed card-load failure.
* Escalated and merely-old rows are constructed (the fixture has no such state without direct store mutation); due-reason and no-reason rows come from the real backend.
* Fresh web-rules fetch for final review was truncated at 3000 characters by the tool limit after the full rule text had been retrieved earlier in the session; disclosed, same source.

## Validation (focused tier; cwd `src/api`; head 7880b95b plus uncommitted candidate; PYTHONPATH set to worktree sources)

| Command | Result |
| --- | --- |
| `node --check src/zava_forward/api/web/app.js` | exit 0 |
| `python3 -m unittest test_handoff_waiting_view` (no browser flag) | OK, 4 skipped opt-in browser cases (before final run) |
| `ZF_BROWSER_TESTS=1 python3 -m unittest test_handoff_waiting_view -q` (final, after lint fixes) | 10 tests OK, 0 skipped |
| `ZF_BROWSER_TESTS=1 python3 -m unittest test_unaccepted_handoff_download_ui test_handoff_read_guidance test_handoff_api test_role_endpoint_inventory test_workbench test_role_screens -q` | 59 tests OK |
| `ruff check` and `ruff format --check` on the new test | clean after one import-order fix and line wrapping |
| `mypy tests/test_handoff_waiting_view.py` | no issues |

Not run (out of focused tier): full gate, SQL service, image build, deployment, other Chromium suites, hosted CI. No new issues, pushes, PR, or acceptance edits.

## Follow-up items

* OD-09 times, routes and operational acceptance (human). Whole #83 remains unaccepted; C3 not ticked.
