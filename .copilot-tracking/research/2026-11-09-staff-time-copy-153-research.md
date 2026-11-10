---
title: Issue 153 staff-time refusal and error guidance research
ms.date: 2026-11-09
task_id: 153-staff-time-copy-1109
task_slug: staff-time-copy-153
---

## Disposition and readiness

* Research executed 2026-11-09T22:45Z to 22:49Z UTC (new, prospective). Planning Readiness: Ready.
* Branch `fix/demo-staff-time-copy-153-1109`, base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`, declared PR target `feat/demo-content-workflows-149-1109`. Refs #153 only (parent #149).
* Scope: staff-time refusal and error guidance in `src/api/src/zava_forward/api/web/timecapture.js` plus one new dedicated regression file. No activation, new data collection, DPIA approval, new staff names, or live user acceptance.

## Evidence read

* Reading set: external `demo-capacity-rpi-common.md`, repository instructions, both case studies, `docs/reference/README.md` and `memory.md`, `docs/reference/research/ux/content-standard.md` (three-part blocked pattern: reason, owner, next action), `src/api/README.md`, skills `redesign-existing-projects` and `web-design-guidelines` (fresh guidelines fetched 2026-11-09 from the skill source URL, `command.md`).
* Content standard: every blocked or refused action states reason, owner and next action; owner is a role or support route, never "unassigned"; internal terms (gate, hold, provenance, trace) are banned. Time capture is already in the lexical guard (`tests/test_content_standard.py::test_time_capture_copy_is_guarded`).
* `timecapture.js`: `timeView` renders `st.reason` (line 9) verbatim, and `save()` catch (line 13) and view catch (line 48) render `error.message` verbatim.
* `app.js` `api()` (lines 56-86): throws `Error(data.error || GENERIC_*)` with `status`, `generic`, `outcome`; a network rejection has no `status` and the browser message (for example "Failed to fetch"); a pending duplicate throws a 409 without `outcome`; 401 signs the person out.
* Backend contract (`timecapture.py`, `server.py`): status flags `flag_on`, `dpia_recorded`, `consultation_recorded`, `notice_approved`, `requested`, `activated`, `enabled`, `reason`. Refusals: `TimeCaptureOff`, `NoticeNotAcknowledged`, `SeparationOfDuties` and the manager-only `PermissionError` map to HTTP 403; validation `ValueError` to 400 (`Minutes must be a whole number.`, `Minutes must be between 1 and 600.`, `Choose an activity from the list.`); unknown case `KeyError` to 404 `Case not found.`; other exceptions to 500 with a server message. `GET /api/time/mine` and `/report` return 403 with `enabled`.
* The save path `POST /api/time` inserts one row per call, so a repeat after an unknown outcome can add a duplicate; `GET /api/time/mine` lists up to 200 own entries.

## Reproduction of the current gap (before any change)

Served isolated app (loopback, synthetic data `test_mvp.DATA`, `ThreadingHTTPServer` with `make_handler`) driven by Chromium through the one nonqueued shared-heavy-resource admission (`flock -n /tmp/ama-rpi-heavy.lock`, lock free, no holder; `logs/admission-pre-repro.txt`). Constructed actors Pam (manager) and Sam (staff); constructed responses by route. Raw output: `/tmp/zf-153-1109/logs/repro-before.log`, exit 0.

| State | Text shown today | Gap |
| --- | --- | --- |
| Disabled | "Time capture is switched off." then a Done/Missing list | No owner or next action |
| Missing DPIA | "...until a DPIA reference is recorded (DPIA_APPROVED), not a boolean flag such as yes, true, on or 1." | Internal variable name; no owner or action |
| Invalid minutes | "Minutes must be between 1 and 600." | Reason only; does not say nothing was saved |
| Unknown case | "Case not found." | No fix or action |
| Network drop on save | "Failed to fetch" | Browser text; no check-before-retry advice |
| 500 with internal detail | Raw `Traceback: sqlite3.OperationalError at /srv/x.py` rendered | Unsafe echo |
| Status read dropped | "Failed to fetch" under the heading | Browser text; no owner or action |

## Design constraints derived

* Map to guidance from stable signals (path, HTTP status, status flags, `outcome`) and recognised server refusals; never echo unrecognised server detail. Render with `textContent` (the helper `h` already creates text nodes).
* Owner: use existing roles or routes only: "a manager (Retrofit Programme Manager or Programme Support Officer)" for enabling steps and "application support" for setup items and unknown faults. Do not name a person or approver, and do not claim a DPIA or consultation was approved.
* Unknown save outcome (no status, 5xx, 409 pending, `outcome` uncertain/committed): say it is not known whether the entry was saved, check My entries before saving again, never claim success, failure, replay or safe duplication.
* Keep load failure distinct from a blocked state; keep defaults, buttons, `role` live regions, keyboard behaviour, text-based status and no animation.
* Out of scope and not edited: `timecapture.py`, `server.py`, `app.js`, `role-screens.js`, store, shared helpers.

## Follow-ups

* C2, C3 (universal error coverage), C5 (named human wording review) stay open. No evidence of resident wording review exists; this change creates none.
