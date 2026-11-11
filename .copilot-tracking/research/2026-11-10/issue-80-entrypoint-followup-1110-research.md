# Research: issue 80 entrypoint follow-up run (one bounded observation)

* Date: 2026-11-10
* Task: `issue-80-entrypoint-followup-1110` (parent `issue-80-entrypoint-runtime-1110`, commit `bfcaf604`)
* Pin: source at `583d4fbd58662e7ac9be71f5f2a8ae3021cd8078` (worktree HEAD `bfcaf6045cf45b100bbd712c7257ee95f0fc6100` adds tracking files only). Latest main `6d4cd624` was reported by Root as differing in IoT documentation only; it was not checked out or executed. This is not a fresh current-main execution.
* Research disposition: executed. Planning Readiness: Ready for a proposal-only plan.
* Scope: one authorised run, three targets, role Retrofit Programme Manager (`pam@example.test`), synthetic fixture, local only. Not deployed, user or assistive-technology acceptance. No source allowance. Every-list criterion stays UNPROVEN; criterion 2, criterion 4 and #73 stay open.

## Run

* Driver v3 (disposable, external): `ROOT/phase80-entrypoint-followup-evidence-1110/driver/entrypoint_driver_v3.py`, sha256 `186addd2...ec76`. Earlier v1, v2 and their logs are untouched in `phase80-entrypoint-runtime-evidence-1110/`.
* Corrections applied before the run: the Popen guard applies only to the owned `zava_forward.api.server` command; the My cases href is awaited with `a[download='cases.csv'][href]` and the click-captured URL is used; `pageerror` and request listeners are registered before navigation; evidence is saved after every stage and on error; each stage is isolated; route readiness (heading, populated text `SYN north wave` and `WO-0001`) precedes every observation. Syntax checked and stages reviewed once before the run.
* Command: `timeout 300 flock -n /tmp/ama-rpi-heavy.lock /tmp/ama-80-audit-venv-1110/bin/python driver/entrypoint_driver_v3.py` from `src/api`, `ZF_BROWSER_SCRATCH=/tmp/ama-80-ef-scratch-1110`. The lock was free (not busy). Exit 1 because three driver stages failed (see below); the driver itself completed ("DRIVER DONE failures=3").
* Owned `ZF_DATA` was asserted inside the scratch and not under `~/.zava-forward` before server start; JSON store, loopback ephemeral port, password auth, no dependency install, no credentials or network model. Scratch removed (0 left), no server or Chromium helper left. Chromium 156.0.8078.4.
* Evidence: `run/driver.log` (`64182460...f248`) and `run/observations.json` (`2afd7785...6095`).

## Observations (role pam, this fixture only)

| Target | Observation | Reading |
| --- | --- | --- |
| 3 `cases.csv?report=progress` | `/api/me` `work_queues.default` has no `report` key. My cases and All cases each render one `a[download="cases.csv"]` ("Download for Excel"); hrefs `/api/cases.csv?view=mine&sort=urgent` and `/api/cases.csv?view=all&sort=urgent`; the click on My cases downloaded `cases.csv` from the first URL. The progress dashboard (plain and with start and end filters) and the overview rendered with no CSV or Excel anchor, no matching control and no matching text. Only `.csv` request after sign-in was the My cases download. The URL probes `#/progress?report=progress` and `#/all?report=progress` failed in the driver (see below) so they are not observed. | In the observed states no rendered control produced the `report=progress` variant and the default cannot. Not covered: the two URL probes, other roles. |
| 1 `packages.csv` | `#/capacity` rendered populated (one package card `SYN north wave`, one work order `WO-0001`; readiness waited on that text). No anchor with `.csv`, no `download` attribute, no button, summary or option matching csv, excel, download or export, and no matching page text. The read-only Package queue screen for `ZF-1` (populated, `WO-0001` present) also had none. | Not located at run time in the observed populated scenario for this role. This does not show a defect. |
| 2 `workorders.csv` | Same pages and result as target 1. The `ZF-1` case page stage failed in the driver, so the case page is not observed. | Same qualification. |
| Interpretation only | Direct GET as pam: `/api/packages.csv` 200 `text/csv`, `filename="packages.csv"`, 2 lines; `/api/workorders.csv` 200, `filename="workorders.csv"`, 2 lines; JSON `/api/packages` and `/api/workorders` 200 with the same seeded records; `/api/cases.csv?report=progress` 400 `As-of must include a date, time and timezone.` | Server routes exist and respond; this proves neither UI reachability, correct rows, nor the variant's contract (the bare GET needs `as_of`). |

Non-GET requests after sign-in: only `POST /api/login`. Page errors: none recorded.

## Driver failures (preserved, not application claims)

* `T3-progress-probe`: waiting for heading "Progress summary" after `goto(#/progress?report=progress)` timed out (15 s).
* `T3-all-probe`: waiting for heading "All open cases" after `goto(#/all?report=progress)` timed out.
* `T2-case-page`: waiting for a heading matching `ZF-1` after `goto(#/case/ZF-1)` timed out.

Full traces are in `observations.json` `failures`. Likely drivers include a same-document hash change that did not re-route or a heading text assumption, but the cause was not determined and no repair or rerun was made (one run only). No application defect is asserted.

## Static note retained

Per the earlier trace (`server.py:528-552`, `taskqueues.py:11-13`, `app.js:461-467, 807, 845`) the default state cannot carry `report`; the run agrees for the observed states.

## Skips

Other roles and registers, axe and design review, SQL, Docker, full gate, other browsers, the two URL probes and the case page (driver failures), progress variant with `as_of` (needs a requirement reading, not run).
