---
title: Issue 80 capacity browser check time-status expectation, research
description: Source contract research for aligning one stale expectation in capacity_browser_check.py (issue 80 criterion 2 correction C1)
ms.date: 2026-11-10
---

## Scope and disposition

* Task `issue-80-capacity-c1-1110`, parent `issue-80-capacity-exports-1110`. Research disposition: `executed` (source reading only; the original failing run is reused as evidence, not re-run).
* Root admits one correction: the `#/time` status expectation in `src/api/checks/capacity_browser_check.py`. Not admitted: `ops.js` or any application, core, API, policy, data, route, export or permission change; fixture or role expansion; progress-report work.
* Immutable and preserved: original source `4a0af32f` (tree `0a64fd15`), its adverse Review (R1 Medium, R2-R5), `browser-run1.log` and `browser-run1.exit`, and both earlier partial diagnostic chains.
* Source base: `origin/main` fetched on 2026-11-10 is still `6d4cd624`; HEAD `4a0af32f` already contains it. No merge is needed or done.

## Original failure (historical, reused)

* `ROOT/phase80-capacity-exports-evidence-1110/browser-run1.log`: `#/time` stage failed at the status assertion. Expected the bare API reason `Time capture is switched off.`; the rendered `<p role="status">` read `Time capture is switched off, so nothing can be recorded. Owner: application support. Next action: ask application support to switch it on when the programme agrees to start staff time capture.`
* Consequence: the empty-capacity scenario and its zero-anchor assertion were never reached. The old `seven-phase verify 0` is a chain-integrity result, not a passing validation verdict.

## Current source contract (HEAD `4a0af32f`, unchanged from `6d4cd624` for these files)

* `timecapture.js` `timeView`: fetches `/api/time/status`, then renders first `h("p", { role: "status" }, st.enabled ? "Time capture is on." : timeBlockedText(st, isManager()))`, then an empty second `role=status` paragraph used for action failures. The check's `#app [role=status]` `.first` is therefore the status line.
* The comment at `timecapture.js:52` states the server `reason` is never shown because it can carry internal detail. Text is composed from the status flags by `timeGuidance(reason, owner, next)` as `${reason} Owner: ${owner}. Next action: ${next}`.
* `timeBlockedText(st, manager)` branches on the API flags: `flag_on` false gives the exact "switched off" sentence with owner "application support"; DPIA, consultation and notice-approval gaps give "Time capture cannot start until ... is recorded." with the same owner; not requested and not activated name a manager owner and differ by `manager`; the default branch says the reason is not shown.
* API shape (`timecapture.py` status): `enabled, flag_on, dpia_recorded, consultation_recorded, notice_approved, requested, activated, requested_role, reason`. The existing maintained test `api/tests/test_timecapture_copy.py` already pins the copy per state and the `\. Owner: .+\. Next action: .+` shape (lines 107-127), so the browser check need only agree with it for the scenario it renders.
* Disabled and manual path: when not enabled the page shows the checklist (`ul`) and no entry form; the check's route table at line 56 still verifies heading and `#app ul`. Nothing changes there.

## Findings for the plan

* F1: the old expectation compares to `status["reason"]`, which the UI deliberately never shows. The correct alignment is to the flag-driven copy, not to the API reason.
* F2: the maintained fixture status is `flag_on` false (observed text above). The smallest faithful assertion for that state is the exact full sentence; for any other blocked state the check must assert the shape (reason, `Owner:` and `Next action:` both present) rather than "some text".
* F3: asserting `reason` is absent from the page is not needed; the maintained unit test owns that copy contract.
* Limits: this is source reading plus the original observation; the corrected check has not run yet. No baseline re-run of the pre-#1343 check is claimed (R5 stays source-only attribution).

## Planning Readiness

Ready: one edit location (`capacity_browser_check.py` `elif href == "#/time"` branch), one focused validation set, one browser run.
